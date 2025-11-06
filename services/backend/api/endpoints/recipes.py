# api/endpoints/recipes.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from modules.brewing_calculations import (
    calculate_abv,
    calculate_ibu_tinseth,
    calculate_srm_morey,
)

router = APIRouter()

OUNCE_TO_GRAM = 28.3495
KILOGRAM_TO_POUND = 2.20462
LITER_TO_GALLON = 0.264172
BOIL_UTILIZATION_USES = {"boil", "first wort", "aroma", "whirlpool"}


def _with_relationships(query):
    """
    Apply the common joinedload options needed to return full recipe payloads.
    """
    return query.options(
        joinedload(models.Recipes.hops),
        joinedload(models.Recipes.fermentables),
        joinedload(models.Recipes.yeasts),
        joinedload(models.Recipes.miscs),
    )


def _fetch_recipe(db: Session, recipe_id: int):
    return (
        _with_relationships(db.query(models.Recipes))
        .filter(models.Recipes.id == recipe_id)
        .first()
    )


def _scale_value(value: Optional[float], scale_factor: float) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value) * scale_factor
    except (TypeError, ValueError):
        return None


def _calculate_recipe_metrics(
    recipe: schemas.Recipe,
    target_batch_size: float,
    boil_volume: Optional[float],
) -> schemas.RecipeMetrics:
    metrics = schemas.RecipeMetrics()

    if recipe.og is not None and recipe.fg is not None:
        try:
            metrics.abv = calculate_abv(recipe.og, recipe.fg)
        except ValueError:
            pass

    ibu_total = 0.0
    ibu_contributions = 0
    if recipe.og is not None and boil_volume:
        try:
            boil_volume_l = float(boil_volume)
        except (TypeError, ValueError):
            boil_volume_l = None
        if boil_volume_l and boil_volume_l > 0:
            for hop in recipe.hops:
                alpha = getattr(hop, "alpha", None)
                amount = getattr(hop, "amount", None)
                boil_time = getattr(hop, "time", None) or 0
                use = (getattr(hop, "use", "") or "").lower()
                if (
                    alpha is None
                    or amount is None
                    or boil_time <= 0
                    or use not in BOIL_UTILIZATION_USES
                ):
                    continue
                try:
                    ibu = calculate_ibu_tinseth(
                        original_gravity=recipe.og,
                        boil_volume_liters=boil_volume_l,
                        hop_alpha_acid=float(alpha),
                        hop_mass_grams=float(amount) * OUNCE_TO_GRAM,
                        boil_time_minutes=float(boil_time),
                    )
                except (TypeError, ValueError):
                    continue
                ibu_total += ibu
                ibu_contributions += 1
            if ibu_contributions:
                metrics.ibu = ibu_total

    try:
        batch_volume_l = float(target_batch_size)
    except (TypeError, ValueError):
        batch_volume_l = None
    if batch_volume_l and batch_volume_l > 0:
        grain_bill = []
        for fermentable in recipe.fermentables:
            amount = getattr(fermentable, "amount", None)
            color = getattr(fermentable, "color", None)
            if amount is None or color is None:
                continue
            try:
                grain_bill.append(
                    (float(amount) * KILOGRAM_TO_POUND, float(color))
                )
            except (TypeError, ValueError):
                continue
        if grain_bill:
            volume_gal = batch_volume_l * LITER_TO_GALLON
            try:
                metrics.srm = calculate_srm_morey(grain_bill, volume_gal)
            except ValueError:
                pass

    return metrics

# Get all recipes


@router.get("/recipes", response_model=List[schemas.Recipe])
async def get_all_recipes(db: Session = Depends(get_db)):
    """
    This endpoint returns all the recipes stored in the database.

    """
    recipes = _with_relationships(db.query(models.Recipes)).all()
    return recipes

# Get a recipe by ID


@router.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
async def get_recipe_by_id(recipe_id: int, db: Session = Depends(get_db)):
    """
    This endpoint returns a recipe by its ID.

    """
    recipe = _fetch_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

# Create a new recipe


@router.post("/recipes", response_model=schemas.Recipe)
async def create_recipe(
    recipe: schemas.RecipeBase, db: Session = Depends(get_db)
):
    """
    This endpoint creates a new recipe in the database.

    """
    # Check if the recipe already exists

    existing_recipe = (
        db.query(models.Recipes)
        .filter(models.Recipes.name == recipe.name)
        .first()
    )
    if existing_recipe:
        raise HTTPException(
            status_code=400, detail="Recipe with this name already exists"
        )
    # Exclude the related fields when creating the Recipes instance
    db_recipe = models.Recipes(
        **recipe.model_dump(exclude={"hops", "fermentables", "yeasts", "miscs"})
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    # Add hops to the recipe

    for hop_data in recipe.hops:
        db_hop = models.RecipeHop(**hop_data.model_dump(), recipe_id=db_recipe.id)
        db.add(db_hop)
    # Add fermentables to the recipe

    for fermentable_data in recipe.fermentables:
        db_fermentable = models.RecipeFermentable(
            **fermentable_data.model_dump(), recipe_id=db_recipe.id
        )
        db.add(db_fermentable)
    # Add miscs to the recipe

    for misc_data in recipe.miscs:
        db_misc = models.RecipeMisc(**misc_data.model_dump(), recipe_id=db_recipe.id)
        db.add(db_misc)
    # Add yeasts to the recipe

    for yeast_data in recipe.yeasts:
        db_yeast = models.RecipeYeast(
            **yeast_data.model_dump(), recipe_id=db_recipe.id
        )
        db.add(db_yeast)
    db.commit()
    return _fetch_recipe(db, db_recipe.id)

# Update a recipe by ID


@router.put("/recipes/{recipe_id}", response_model=schemas.Recipe)
async def update_recipe(
    recipe_id: int, recipe: schemas.RecipeBase, db: Session = Depends(get_db)
):
    """
    This endpoint updates a recipe by its ID.

    """
    db_recipe = (
        db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    )
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    # Update the recipe

    for key, value in recipe.model_dump(
        exclude={"hops", "fermentables", "yeasts", "miscs"}
    ).items():
        setattr(db_recipe, key, value)
    # Update hops

    db.query(models.RecipeHop).filter(
        models.RecipeHop.recipe_id == recipe_id
    ).delete()
    for hop_data in recipe.hops:
        db_hop = models.RecipeHop(**hop_data.model_dump(), recipe_id=recipe_id)
        db.add(db_hop)
    # Update fermentables

    db.query(models.RecipeFermentable).filter(
        models.RecipeFermentable.recipe_id == recipe_id
    ).delete()
    for fermentable_data in recipe.fermentables:
        db_fermentable = models.RecipeFermentable(
            **fermentable_data.model_dump(), recipe_id=recipe_id
        )
        db.add(db_fermentable)
    # Update miscs

    db.query(models.RecipeMisc).filter(
        models.RecipeMisc.recipe_id == recipe_id
    ).delete()
    for misc_data in recipe.miscs:
        db_misc = models.RecipeMisc(**misc_data.model_dump(), recipe_id=recipe_id)
        db.add(db_misc)
    # Update yeasts

    db.query(models.RecipeYeast).filter(
        models.RecipeYeast.recipe_id == recipe_id
    ).delete()
    for yeast_data in recipe.yeasts:
        db_yeast = models.RecipeYeast(**yeast_data.model_dump(), recipe_id=recipe_id)
        db.add(db_yeast)
    db.commit()
    return _fetch_recipe(db, recipe_id)

# Delete a recipe by ID


@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    This endpoint deletes a recipe by its ID.

    """
    db_recipe = (
        db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    )
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.query(models.RecipeHop).filter(
        models.RecipeHop.recipe_id == recipe_id
    ).delete()
    db.query(models.RecipeFermentable).filter(
        models.RecipeFermentable.recipe_id == recipe_id
    ).delete()
    db.query(models.RecipeMisc).filter(
        models.RecipeMisc.recipe_id == recipe_id
    ).delete()
    db.query(models.RecipeYeast).filter(
        models.RecipeYeast.recipe_id == recipe_id
    ).delete()
    db.delete(db_recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}


@router.post(
    "/recipes/{recipe_id}/scale", response_model=schemas.RecipeScaleResponse
)
async def scale_recipe(
    recipe_id: int,
    payload: schemas.RecipeScaleRequest,
    db: Session = Depends(get_db),
):
    recipe = _fetch_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe_model = schemas.Recipe.model_validate(recipe)
    if recipe_model.batch_size is None:
        raise HTTPException(
            status_code=400,
            detail="Recipe is missing a batch_size value for scaling.",
        )

    try:
        original_batch_size = float(recipe_model.batch_size)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Recipe batch_size must be a valid numeric value.",
        )

    target_batch_size = payload.target_batch_size
    if target_batch_size <= 0:
        raise HTTPException(
            status_code=400,
            detail="Target batch size must be greater than zero.",
        )

    scale_factor = target_batch_size / original_batch_size

    scaled_recipe_data = recipe_model.model_dump()
    scaled_recipe_data["batch_size"] = target_batch_size
    scaled_recipe_data["boil_size"] = (
        payload.target_boil_size
        if payload.target_boil_size is not None
        else _scale_value(recipe_model.boil_size, scale_factor)
    )

    scaled_recipe_data["hops"] = [
        {**hop.model_dump(), "amount": _scale_value(hop.amount, scale_factor)}
        for hop in recipe_model.hops
    ]
    scaled_recipe_data["fermentables"] = [
        {
            **fermentable.model_dump(),
            "amount": _scale_value(fermentable.amount, scale_factor),
        }
        for fermentable in recipe_model.fermentables
    ]
    scaled_recipe_data["yeasts"] = [
        {**yeast.model_dump(), "amount": _scale_value(yeast.amount, scale_factor)}
        for yeast in recipe_model.yeasts
    ]

    scaled_miscs = []
    for misc in recipe_model.miscs:
        misc_data = misc.model_dump()
        misc_data["amount"] = _scale_value(misc_data.get("amount"), scale_factor)
        if misc_data.get("batch_size") is not None:
            misc_data["batch_size"] = _scale_value(
                misc_data.get("batch_size"), scale_factor
            )
        scaled_miscs.append(misc_data)
    scaled_recipe_data["miscs"] = scaled_miscs

    scaled_recipe = schemas.Recipe(**scaled_recipe_data)
    boil_volume = (
        payload.target_boil_size
        if payload.target_boil_size is not None
        else scaled_recipe.boil_size
    )
    metrics = _calculate_recipe_metrics(
        scaled_recipe,
        target_batch_size=target_batch_size,
        boil_volume=boil_volume,
    )
    if metrics.abv is not None:
        scaled_recipe.abv = metrics.abv
        scaled_recipe.est_abv = metrics.abv
    if metrics.ibu is not None:
        scaled_recipe.ibu = metrics.ibu
    if metrics.srm is not None:
        scaled_recipe.est_color = metrics.srm

    return schemas.RecipeScaleResponse(
        original_batch_size=original_batch_size,
        target_batch_size=target_batch_size,
        scale_factor=scale_factor,
        scaled_recipe=scaled_recipe,
        metrics=metrics,
    )
