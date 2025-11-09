# api/endpoints/recipes.py

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
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
                grain_bill.append((float(amount) * KILOGRAM_TO_POUND, float(color)))
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
async def create_recipe(recipe: schemas.RecipeBase, db: Session = Depends(get_db)):
    """
    This endpoint creates a new recipe in the database.

    """
    # Check if the recipe already exists

    existing_recipe = (
        db.query(models.Recipes).filter(models.Recipes.name == recipe.name).first()
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
        db_yeast = models.RecipeYeast(**yeast_data.model_dump(), recipe_id=db_recipe.id)
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
    db_recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    # Update the recipe

    for key, value in recipe.model_dump(
        exclude={"hops", "fermentables", "yeasts", "miscs"}
    ).items():
        setattr(db_recipe, key, value)
    # Update hops

    db.query(models.RecipeHop).filter(models.RecipeHop.recipe_id == recipe_id).delete()
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
    db_recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.query(models.RecipeHop).filter(models.RecipeHop.recipe_id == recipe_id).delete()
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


@router.post("/recipes/{recipe_id}/scale", response_model=schemas.RecipeScaleResponse)
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


@router.post(
    "/recipes/{recipe_id}/scale-to-equipment/{equipment_id}",
    response_model=schemas.RecipeScaleToEquipmentResponse,
)
async def scale_recipe_to_equipment(
    recipe_id: int,
    equipment_id: int,
    db: Session = Depends(get_db),
):
    """
    Scale a recipe to match an equipment profile's batch size and boil size.
    
    This endpoint automatically scales recipes based on equipment profiles,
    allowing brewers to adapt recipes to their specific brewing equipment.
    """
    # Fetch the recipe
    recipe = _fetch_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Fetch the equipment profile
    equipment = (
        db.query(models.EquipmentProfiles)
        .filter(models.EquipmentProfiles.id == equipment_id)
        .first()
    )
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment profile not found")

    # Validate equipment has required fields
    if equipment.batch_size is None:
        raise HTTPException(
            status_code=400,
            detail="Equipment profile is missing batch_size value for scaling.",
        )

    recipe_model = schemas.Recipe.model_validate(recipe)
    if recipe_model.batch_size is None:
        raise HTTPException(
            status_code=400,
            detail="Recipe is missing a batch_size value for scaling.",
        )

    try:
        original_batch_size = float(recipe_model.batch_size)
        target_batch_size = float(equipment.batch_size)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Recipe and equipment batch_size must be valid numeric values.",
        )

    if target_batch_size <= 0:
        raise HTTPException(
            status_code=400,
            detail="Equipment batch size must be greater than zero.",
        )

    scale_factor = target_batch_size / original_batch_size

    # Build scaled recipe data
    scaled_recipe_data = recipe_model.model_dump()
    scaled_recipe_data["batch_size"] = target_batch_size
    
    # Use equipment's boil_size if available, otherwise scale proportionally
    if equipment.boil_size is not None:
        scaled_recipe_data["boil_size"] = float(equipment.boil_size)
    else:
        scaled_recipe_data["boil_size"] = _scale_value(
            recipe_model.boil_size, scale_factor
        )

    # Scale all ingredients
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
    boil_volume = scaled_recipe.boil_size
    
    # Calculate metrics for the scaled recipe
    metrics = _calculate_recipe_metrics(
        scaled_recipe,
        target_batch_size=target_batch_size,
        boil_volume=boil_volume,
    )
    
    # Update scaled recipe with calculated metrics
    if metrics.abv is not None:
        scaled_recipe.abv = metrics.abv
        scaled_recipe.est_abv = metrics.abv
    if metrics.ibu is not None:
        scaled_recipe.ibu = metrics.ibu
    if metrics.srm is not None:
        scaled_recipe.est_color = metrics.srm

    return schemas.RecipeScaleToEquipmentResponse(
        original_batch_size=original_batch_size,
        target_batch_size=target_batch_size,
        scale_factor=scale_factor,
        scaled_recipe=scaled_recipe,
        metrics=metrics,
        equipment_profile_id=equipment.id,
        equipment_profile_name=equipment.name or "Unnamed Equipment",
    )


# Individual ingredient CRUD endpoints


@router.post("/recipes/{recipe_id}/ingredients/hops")
async def add_hop_to_recipe(
    recipe_id: int,
    hop: schemas.RecipeHopBase,
    db: Session = Depends(get_db),
):
    """Add a hop ingredient to a recipe"""
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_hop = models.RecipeHop(**hop.model_dump(), recipe_id=recipe_id)
    db.add(db_hop)
    db.commit()
    db.refresh(db_hop)
    return db_hop


@router.put("/recipes/{recipe_id}/ingredients/hops/{ingredient_id}")
async def update_hop_in_recipe(
    recipe_id: int,
    ingredient_id: int,
    hop: schemas.RecipeHopBase,
    db: Session = Depends(get_db),
):
    """Update a hop ingredient in a recipe"""
    db_hop = (
        db.query(models.RecipeHop)
        .filter(
            models.RecipeHop.id == ingredient_id,
            models.RecipeHop.recipe_id == recipe_id,
        )
        .first()
    )
    if not db_hop:
        raise HTTPException(status_code=404, detail="Hop ingredient not found")

    for key, value in hop.model_dump().items():
        setattr(db_hop, key, value)

    db.commit()
    db.refresh(db_hop)
    return db_hop


@router.delete("/recipes/{recipe_id}/ingredients/hops/{ingredient_id}")
async def delete_hop_from_recipe(
    recipe_id: int,
    ingredient_id: int,
    db: Session = Depends(get_db),
):
    """Delete a hop ingredient from a recipe"""
    db_hop = (
        db.query(models.RecipeHop)
        .filter(
            models.RecipeHop.id == ingredient_id,
            models.RecipeHop.recipe_id == recipe_id,
        )
        .first()
    )
    if not db_hop:
        raise HTTPException(status_code=404, detail="Hop ingredient not found")

    db.delete(db_hop)
    db.commit()
    return {"message": "Hop ingredient deleted successfully"}


@router.post("/recipes/{recipe_id}/ingredients/fermentables")
async def add_fermentable_to_recipe(
    recipe_id: int,
    fermentable: schemas.RecipeFermentableBase,
    db: Session = Depends(get_db),
):
    """Add a fermentable ingredient to a recipe"""
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_fermentable = models.RecipeFermentable(
        **fermentable.model_dump(), recipe_id=recipe_id
    )
    db.add(db_fermentable)
    db.commit()
    db.refresh(db_fermentable)
    return db_fermentable


@router.put("/recipes/{recipe_id}/ingredients/fermentables/{ingredient_id}")
async def update_fermentable_in_recipe(
    recipe_id: int,
    ingredient_id: int,
    fermentable: schemas.RecipeFermentableBase,
    db: Session = Depends(get_db),
):
    """Update a fermentable ingredient in a recipe"""
    db_fermentable = (
        db.query(models.RecipeFermentable)
        .filter(
            models.RecipeFermentable.id == ingredient_id,
            models.RecipeFermentable.recipe_id == recipe_id,
        )
        .first()
    )
    if not db_fermentable:
        raise HTTPException(status_code=404, detail="Fermentable ingredient not found")

    for key, value in fermentable.model_dump().items():
        setattr(db_fermentable, key, value)

    db.commit()
    db.refresh(db_fermentable)
    return db_fermentable


@router.delete("/recipes/{recipe_id}/ingredients/fermentables/{ingredient_id}")
async def delete_fermentable_from_recipe(
    recipe_id: int,
    ingredient_id: int,
    db: Session = Depends(get_db),
):
    """Delete a fermentable ingredient from a recipe"""
    db_fermentable = (
        db.query(models.RecipeFermentable)
        .filter(
            models.RecipeFermentable.id == ingredient_id,
            models.RecipeFermentable.recipe_id == recipe_id,
        )
        .first()
    )
    if not db_fermentable:
        raise HTTPException(status_code=404, detail="Fermentable ingredient not found")

    db.delete(db_fermentable)
    db.commit()
    return {"message": "Fermentable ingredient deleted successfully"}


@router.post("/recipes/{recipe_id}/ingredients/yeasts")
async def add_yeast_to_recipe(
    recipe_id: int,
    yeast: schemas.RecipeYeastBase,
    db: Session = Depends(get_db),
):
    """Add a yeast ingredient to a recipe"""
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_yeast = models.RecipeYeast(**yeast.model_dump(), recipe_id=recipe_id)
    db.add(db_yeast)
    db.commit()
    db.refresh(db_yeast)
    return db_yeast


@router.put("/recipes/{recipe_id}/ingredients/yeasts/{ingredient_id}")
async def update_yeast_in_recipe(
    recipe_id: int,
    ingredient_id: int,
    yeast: schemas.RecipeYeastBase,
    db: Session = Depends(get_db),
):
    """Update a yeast ingredient in a recipe"""
    db_yeast = (
        db.query(models.RecipeYeast)
        .filter(
            models.RecipeYeast.id == ingredient_id,
            models.RecipeYeast.recipe_id == recipe_id,
        )
        .first()
    )
    if not db_yeast:
        raise HTTPException(status_code=404, detail="Yeast ingredient not found")

    for key, value in yeast.model_dump().items():
        setattr(db_yeast, key, value)

    db.commit()
    db.refresh(db_yeast)
    return db_yeast


@router.delete("/recipes/{recipe_id}/ingredients/yeasts/{ingredient_id}")
async def delete_yeast_from_recipe(
    recipe_id: int,
    ingredient_id: int,
    db: Session = Depends(get_db),
):
    """Delete a yeast ingredient from a recipe"""
    db_yeast = (
        db.query(models.RecipeYeast)
        .filter(
            models.RecipeYeast.id == ingredient_id,
            models.RecipeYeast.recipe_id == recipe_id,
        )
        .first()
    )
    if not db_yeast:
        raise HTTPException(status_code=404, detail="Yeast ingredient not found")

    db.delete(db_yeast)
    db.commit()
    return {"message": "Yeast ingredient deleted successfully"}


@router.post("/recipes/{recipe_id}/ingredients/miscs")
async def add_misc_to_recipe(
    recipe_id: int,
    misc: schemas.RecipeMiscBase,
    db: Session = Depends(get_db),
):
    """Add a misc ingredient to a recipe"""
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_misc = models.RecipeMisc(**misc.model_dump(), recipe_id=recipe_id)
    db.add(db_misc)
    db.commit()
    db.refresh(db_misc)
    return db_misc


@router.put("/recipes/{recipe_id}/ingredients/miscs/{ingredient_id}")
async def update_misc_in_recipe(
    recipe_id: int,
    ingredient_id: int,
    misc: schemas.RecipeMiscBase,
    db: Session = Depends(get_db),
):
    """Update a misc ingredient in a recipe"""
    db_misc = (
        db.query(models.RecipeMisc)
        .filter(
            models.RecipeMisc.id == ingredient_id,
            models.RecipeMisc.recipe_id == recipe_id,
        )
        .first()
    )
    if not db_misc:
        raise HTTPException(status_code=404, detail="Misc ingredient not found")

    for key, value in misc.model_dump().items():
        setattr(db_misc, key, value)

    db.commit()
    db.refresh(db_misc)
    return db_misc


@router.delete("/recipes/{recipe_id}/ingredients/miscs/{ingredient_id}")
async def delete_misc_from_recipe(
    recipe_id: int,
    ingredient_id: int,
    db: Session = Depends(get_db),
):
    """Delete a misc ingredient from a recipe"""
    db_misc = (
        db.query(models.RecipeMisc)
        .filter(
            models.RecipeMisc.id == ingredient_id,
            models.RecipeMisc.recipe_id == recipe_id,
        )
        .first()
    )
    if not db_misc:
        raise HTTPException(status_code=404, detail="Misc ingredient not found")

    db.delete(db_misc)
    db.commit()
    return {"message": "Misc ingredient deleted successfully"}


# Recipe versioning endpoints


@router.post("/recipes/{recipe_id}/version", response_model=schemas.RecipeVersion)
async def create_recipe_version(
    recipe_id: int,
    version_data: schemas.RecipeVersionCreate,
    db: Session = Depends(get_db),
):
    """Create a new version snapshot of a recipe"""
    import json

    recipe = _fetch_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Get the current highest version number for this recipe
    max_version = (
        db.query(models.RecipeVersion.version_number)
        .filter(models.RecipeVersion.recipe_id == recipe_id)
        .order_by(models.RecipeVersion.version_number.desc())
        .first()
    )
    next_version = (max_version[0] + 1) if max_version else 1

    # Create a snapshot of the current recipe state
    recipe_dict = schemas.Recipe.model_validate(recipe).model_dump(mode="json")
    recipe_snapshot = json.dumps(recipe_dict)

    # Create the version record
    db_version = models.RecipeVersion(
        recipe_id=recipe_id,
        version_number=next_version,
        version_name=version_data.version_name,
        notes=version_data.notes,
        recipe_snapshot=recipe_snapshot,
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)

    return db_version


@router.get("/recipes/{recipe_id}/versions", response_model=List[schemas.RecipeVersion])
async def get_recipe_versions(
    recipe_id: int,
    db: Session = Depends(get_db),
):
    """Get all version history for a recipe"""
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    versions = (
        db.query(models.RecipeVersion)
        .filter(models.RecipeVersion.recipe_id == recipe_id)
        .order_by(models.RecipeVersion.version_number.desc())
        .all()
    )

    return versions


# BeerXML Import/Export Endpoints


@router.post("/recipes/import/beerxml")
async def import_beerxml_recipes(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Import recipes from BeerXML format.
    
    This endpoint accepts a BeerXML file and imports all recipes found within it.
    The import process validates the XML structure and creates new recipe records
    with all associated ingredients.
    
    Returns a summary of the import operation including success count and any errors.
    """
    from modules.beerxml_parser import parse_beerxml, BeerXMLParseError, validate_beerxml
    from pydantic import BaseModel
    
    class BeerXMLImportResponse(BaseModel):
        message: str
        imported_count: int
        skipped_count: int
        errors: List[str]
        recipe_ids: List[int]
    
    # Read file content
    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read uploaded file: {str(e)}"
        )
    
    # Validate XML first
    validation = validate_beerxml(content)
    if not validation["valid"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid BeerXML: {', '.join(validation['errors'])}"
        )
    
    # Parse recipes
    try:
        beerxml_recipes = parse_beerxml(content)
    except BeerXMLParseError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse BeerXML: {str(e)}"
        )
    
    imported_count = 0
    skipped_count = 0
    errors = []
    recipe_ids = []
    
    for beerxml_recipe in beerxml_recipes:
        try:
            # Create recipe record
            db_recipe = models.Recipes(
                name=beerxml_recipe.name,
                version=beerxml_recipe.version or 1,
                type=beerxml_recipe.type,
                brewer=beerxml_recipe.brewer,
                asst_brewer=beerxml_recipe.asst_brewer,
                batch_size=beerxml_recipe.batch_size,
                boil_size=beerxml_recipe.boil_size,
                boil_time=beerxml_recipe.boil_time,
                efficiency=beerxml_recipe.efficiency,
                notes=beerxml_recipe.notes,
                taste_notes=beerxml_recipe.taste_notes,
                taste_rating=beerxml_recipe.taste_rating,
                og=beerxml_recipe.og,
                fg=beerxml_recipe.fg,
                fermentation_stages=beerxml_recipe.fermentation_stages,
                primary_age=beerxml_recipe.primary_age,
                primary_temp=beerxml_recipe.primary_temp,
                secondary_age=beerxml_recipe.secondary_age,
                secondary_temp=beerxml_recipe.secondary_temp,
                tertiary_age=beerxml_recipe.tertiary_age,
                age=beerxml_recipe.age,
                age_temp=beerxml_recipe.age_temp,
                carbonation_used=beerxml_recipe.carbonation_used,
                est_og=beerxml_recipe.est_og,
                est_fg=beerxml_recipe.est_fg,
                est_color=beerxml_recipe.est_color,
                ibu=beerxml_recipe.ibu,
                ibu_method=beerxml_recipe.ibu_method,
                est_abv=beerxml_recipe.est_abv,
                abv=beerxml_recipe.abv,
                actual_efficiency=beerxml_recipe.actual_efficiency,
                calories=beerxml_recipe.calories,
                display_batch_size=beerxml_recipe.display_batch_size,
                display_boil_size=beerxml_recipe.display_boil_size,
                display_og=beerxml_recipe.display_og,
                display_fg=beerxml_recipe.display_fg,
                display_primary_temp=beerxml_recipe.display_primary_temp,
                display_secondary_temp=beerxml_recipe.display_secondary_temp,
                display_tertiary_temp=beerxml_recipe.display_tertiary_temp,
                display_age_temp=beerxml_recipe.display_age_temp,
            )
            
            db.add(db_recipe)
            db.flush()  # Get the recipe ID
            
            # Add hops
            for hop in beerxml_recipe.hops:
                db_hop = models.RecipeHop(
                    recipe_id=db_recipe.id,
                    name=hop.name,
                    version=hop.version,
                    alpha=hop.alpha,
                    amount=hop.amount,
                    use=hop.use,
                    time=hop.time,
                    notes=hop.notes,
                    type=hop.type,
                    form=hop.form,
                    beta=hop.beta,
                    hsi=hop.hsi,
                    origin=hop.origin,
                    substitutes=hop.substitutes,
                    humulene=hop.humulene,
                    caryophyllene=hop.caryophyllene,
                    cohumulone=hop.cohumulone,
                    myrcene=hop.myrcene,
                    display_amount=hop.display_amount,
                    inventory=hop.inventory,
                    display_time=hop.display_time,
                )
                db.add(db_hop)
            
            # Add fermentables
            for ferm in beerxml_recipe.fermentables:
                db_ferm = models.RecipeFermentable(
                    recipe_id=db_recipe.id,
                    name=ferm.name,
                    version=ferm.version,
                    type=ferm.type,
                    amount=ferm.amount,
                    yield_=ferm.yield_,
                    color=ferm.color,
                    add_after_boil=ferm.add_after_boil,
                    origin=ferm.origin,
                    supplier=ferm.supplier,
                    notes=ferm.notes,
                    coarse_fine_diff=ferm.coarse_fine_diff,
                    moisture=ferm.moisture,
                    diastatic_power=ferm.diastatic_power,
                    protein=ferm.protein,
                    max_in_batch=ferm.max_in_batch,
                    recommend_mash=ferm.recommend_mash,
                    ibu_gal_per_lb=ferm.ibu_gal_per_lb,
                    display_amount=ferm.display_amount,
                    potential=ferm.potential,
                    inventory=ferm.inventory,
                    display_color=ferm.display_color,
                )
                db.add(db_ferm)
            
            # Add yeasts
            for yeast in beerxml_recipe.yeasts:
                db_yeast = models.RecipeYeast(
                    recipe_id=db_recipe.id,
                    name=yeast.name,
                    version=yeast.version,
                    type=yeast.type,
                    form=yeast.form,
                    amount=yeast.amount,
                    amount_is_weight=yeast.amount_is_weight,
                    laboratory=yeast.laboratory,
                    product_id=yeast.product_id,
                    min_temperature=yeast.min_temperature,
                    max_temperature=yeast.max_temperature,
                    flocculation=yeast.flocculation,
                    attenuation=yeast.attenuation,
                    notes=yeast.notes,
                    best_for=yeast.best_for,
                    max_reuse=yeast.max_reuse,
                    times_cultured=yeast.times_cultured,
                    add_to_secondary=yeast.add_to_secondary,
                    display_amount=yeast.display_amount,
                    disp_min_temp=yeast.disp_min_temp,
                    disp_max_temp=yeast.disp_max_temp,
                    inventory=yeast.inventory,
                    culture_date=yeast.culture_date,
                )
                db.add(db_yeast)
            
            # Add miscs
            for misc in beerxml_recipe.miscs:
                db_misc = models.RecipeMisc(
                    recipe_id=db_recipe.id,
                    name=misc.name,
                    version=misc.version,
                    type=misc.type,
                    use=misc.use,
                    amount=misc.amount,
                    time=misc.time,
                    amount_is_weight=misc.amount_is_weight,
                    use_for=misc.use_for,
                    notes=misc.notes,
                    display_amount=misc.display_amount,
                    inventory=misc.inventory,
                    display_time=misc.display_time,
                    batch_size=misc.batch_size,
                )
                db.add(db_misc)
            
            db.commit()
            recipe_ids.append(db_recipe.id)
            imported_count += 1
            
        except Exception as e:
            db.rollback()
            skipped_count += 1
            errors.append(f"Failed to import recipe '{beerxml_recipe.name}': {str(e)}")
    
    return BeerXMLImportResponse(
        message=f"Import completed: {imported_count} recipes imported, {skipped_count} skipped",
        imported_count=imported_count,
        skipped_count=skipped_count,
        errors=errors,
        recipe_ids=recipe_ids,
    )


@router.get("/recipes/{recipe_id}/export/beerxml")
async def export_recipe_beerxml(
    recipe_id: int,
    db: Session = Depends(get_db),
):
    """
    Export a single recipe to BeerXML format.
    
    Returns the recipe in BeerXML format as a downloadable file.
    """
    from modules.beerxml_exporter import export_recipe_to_beerxml, BeerXMLExportError
    from fastapi.responses import Response
    
    # Fetch recipe with all relationships
    recipe = _fetch_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    try:
        xml_content = export_recipe_to_beerxml(recipe, pretty_print=True)
    except BeerXMLExportError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export recipe: {str(e)}"
        )
    
    # Generate filename
    safe_name = "".join(c for c in recipe.name if c.isalnum() or c in (' ', '-', '_')).strip()
    filename = f"{safe_name or 'recipe'}_{recipe_id}.xml"
    
    return Response(
        content=xml_content.encode('utf-8'),
        media_type="application/xml",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.post("/recipes/export/beerxml")
async def export_multiple_recipes_beerxml(
    recipe_ids: List[int],
    db: Session = Depends(get_db),
):
    """
    Export multiple recipes to a single BeerXML file.
    
    Accepts a list of recipe IDs and returns them in a single BeerXML file.
    """
    from modules.beerxml_exporter import export_to_beerxml, BeerXMLExportError
    from fastapi.responses import Response
    
    if not recipe_ids:
        raise HTTPException(
            status_code=400,
            detail="No recipe IDs provided"
        )
    
    # Fetch all recipes
    recipes = []
    for recipe_id in recipe_ids:
        recipe = _fetch_recipe(db, recipe_id)
        if recipe:
            recipes.append(recipe)
    
    if not recipes:
        raise HTTPException(
            status_code=404,
            detail="No recipes found with the provided IDs"
        )
    
    try:
        xml_content = export_to_beerxml(recipes, pretty_print=True)
    except BeerXMLExportError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to export recipes: {str(e)}"
        )
    
    return Response(
        content=xml_content.encode('utf-8'),
        media_type="application/xml",
        headers={
            "Content-Disposition": "attachment; filename=recipes_export.xml"
        }
    )
