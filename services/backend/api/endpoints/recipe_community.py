# api/endpoints/recipe_community.py
"""
Recipe Community Features API Endpoints
Handles public recipes, ratings, comments, and forking
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from datetime import datetime

router = APIRouter()


# ============================================================================
# Public Recipes
# ============================================================================

@router.get("/recipes/public", response_model=List[schemas.Recipe])
async def get_public_recipes(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all public recipes.
    Returns recipes that have been marked as public by their authors.
    """
    recipes = (
        db.query(models.Recipes)
        .options(
            joinedload(models.Recipes.hops),
            joinedload(models.Recipes.fermentables),
            joinedload(models.Recipes.yeasts),
            joinedload(models.Recipes.miscs),
        )
        .filter(models.Recipes.is_public == True)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return recipes


@router.patch("/recipes/{recipe_id}/visibility")
async def toggle_recipe_visibility(
    recipe_id: int,
    is_public: bool,
    db: Session = Depends(get_db)
):
    """
    Toggle recipe visibility between public and private.
    Only the recipe owner should be able to do this (authentication required in production).
    """
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    recipe.is_public = is_public
    db.commit()
    db.refresh(recipe)
    
    return {
        "recipe_id": recipe_id,
        "is_public": is_public,
        "message": f"Recipe visibility set to {'public' if is_public else 'private'}"
    }


# ============================================================================
# Recipe Forking
# ============================================================================

@router.post("/recipes/{recipe_id}/fork", response_model=schemas.Recipe)
async def fork_recipe(
    recipe_id: int,
    new_name: Optional[str] = None,
    user_id: int = Query(..., description="ID of the user forking the recipe"),
    db: Session = Depends(get_db)
):
    """
    Fork a recipe, creating a new copy with attribution to the original.
    The forked recipe will reference the original via forked_from_id.
    """
    # Get the original recipe with all ingredients
    original_recipe = (
        db.query(models.Recipes)
        .options(
            joinedload(models.Recipes.hops),
            joinedload(models.Recipes.fermentables),
            joinedload(models.Recipes.yeasts),
            joinedload(models.Recipes.miscs),
        )
        .filter(models.Recipes.id == recipe_id)
        .first()
    )
    
    if not original_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Create new recipe with forked data
    fork_name = new_name or f"{original_recipe.name} (Forked)"
    
    # Create the forked recipe
    forked_recipe = models.Recipes(
        name=fork_name,
        version=1,  # Start at version 1 for forked recipe
        type=original_recipe.type,
        brewer=original_recipe.brewer,
        asst_brewer=original_recipe.asst_brewer,
        batch_size=original_recipe.batch_size,
        boil_size=original_recipe.boil_size,
        boil_time=original_recipe.boil_time,
        efficiency=original_recipe.efficiency,
        notes=f"Forked from: {original_recipe.name}\n\n{original_recipe.notes or ''}",
        taste_notes=original_recipe.taste_notes,
        og=original_recipe.og,
        fg=original_recipe.fg,
        fermentation_stages=original_recipe.fermentation_stages,
        primary_age=original_recipe.primary_age,
        primary_temp=original_recipe.primary_temp,
        secondary_age=original_recipe.secondary_age,
        secondary_temp=original_recipe.secondary_temp,
        tertiary_age=original_recipe.tertiary_age,
        age=original_recipe.age,
        age_temp=original_recipe.age_temp,
        carbonation_used=original_recipe.carbonation_used,
        est_og=original_recipe.est_og,
        est_fg=original_recipe.est_fg,
        est_color=original_recipe.est_color,
        ibu=original_recipe.ibu,
        ibu_method=original_recipe.ibu_method,
        est_abv=original_recipe.est_abv,
        abv=original_recipe.abv,
        actual_efficiency=original_recipe.actual_efficiency,
        calories=original_recipe.calories,
        display_batch_size=original_recipe.display_batch_size,
        display_boil_size=original_recipe.display_boil_size,
        display_og=original_recipe.display_og,
        display_fg=original_recipe.display_fg,
        display_primary_temp=original_recipe.display_primary_temp,
        display_secondary_temp=original_recipe.display_secondary_temp,
        display_tertiary_temp=original_recipe.display_tertiary_temp,
        display_age_temp=original_recipe.display_age_temp,
        # Set community fields
        user_id=user_id,
        forked_from_id=recipe_id,
        is_public=False,  # Forked recipes are private by default
    )
    
    db.add(forked_recipe)
    db.commit()
    db.refresh(forked_recipe)
    
    # Copy all ingredients
    for hop in original_recipe.hops:
        forked_hop = models.RecipeHop(
            recipe_id=forked_recipe.id,
            name=hop.name,
            origin=hop.origin,
            alpha=hop.alpha,
            amount=hop.amount,
            use=hop.use,
            time=hop.time,
            form=hop.form,
            notes=hop.notes,
            stage=hop.stage,
            duration=hop.duration,
            display_amount=hop.display_amount,
            display_time=hop.display_time,
        )
        db.add(forked_hop)
    
    for fermentable in original_recipe.fermentables:
        forked_fermentable = models.RecipeFermentable(
            recipe_id=forked_recipe.id,
            name=fermentable.name,
            type=fermentable.type,
            amount=fermentable.amount,
            yield_=fermentable.yield_,
            color=fermentable.color,
            origin=fermentable.origin,
            supplier=fermentable.supplier,
            notes=fermentable.notes,
            coarse_fine_diff=fermentable.coarse_fine_diff,
            moisture=fermentable.moisture,
            diastatic_power=fermentable.diastatic_power,
            protein=fermentable.protein,
            max_in_batch=fermentable.max_in_batch,
            recommend_mash=fermentable.recommend_mash,
            ibu_gal_per_lb=fermentable.ibu_gal_per_lb,
            add_after_boil=fermentable.add_after_boil,
            stage=fermentable.stage,
            duration=fermentable.duration,
            display_amount=fermentable.display_amount,
            display_color=fermentable.display_color,
        )
        db.add(forked_fermentable)
    
    for yeast in original_recipe.yeasts:
        forked_yeast = models.RecipeYeast(
            recipe_id=forked_recipe.id,
            name=yeast.name,
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
            times_cultured=yeast.times_cultured,
            max_reuse=yeast.max_reuse,
            add_to_secondary=yeast.add_to_secondary,
            stage=yeast.stage,
            duration=yeast.duration,
            display_amount=yeast.display_amount,
            display_min_temp=yeast.display_min_temp,
            display_max_temp=yeast.display_max_temp,
        )
        db.add(forked_yeast)
    
    for misc in original_recipe.miscs:
        forked_misc = models.RecipeMisc(
            recipe_id=forked_recipe.id,
            name=misc.name,
            type=misc.type,
            use=misc.use,
            amount=misc.amount,
            amount_is_weight=misc.amount_is_weight,
            use_for=misc.use_for,
            notes=misc.notes,
            time=misc.time,
            stage=misc.stage,
            duration=misc.duration,
            display_amount=misc.display_amount,
            display_time=misc.display_time,
        )
        db.add(forked_misc)
    
    db.commit()
    
    # Return the complete forked recipe with all ingredients
    return (
        db.query(models.Recipes)
        .options(
            joinedload(models.Recipes.hops),
            joinedload(models.Recipes.fermentables),
            joinedload(models.Recipes.yeasts),
            joinedload(models.Recipes.miscs),
        )
        .filter(models.Recipes.id == forked_recipe.id)
        .first()
    )


# ============================================================================
# Recipe Ratings
# ============================================================================

@router.post("/recipes/{recipe_id}/ratings", response_model=schemas.RecipeRating)
async def create_or_update_rating(
    recipe_id: int,
    rating_data: schemas.RecipeRatingCreate,
    user_id: int = Query(..., description="ID of the user rating the recipe"),
    db: Session = Depends(get_db)
):
    """
    Create or update a recipe rating.
    Users can only have one rating per recipe (enforced by unique constraint).
    """
    # Check if recipe exists
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Check if user already rated this recipe
    existing_rating = (
        db.query(models.RecipeRating)
        .filter(
            models.RecipeRating.recipe_id == recipe_id,
            models.RecipeRating.user_id == user_id
        )
        .first()
    )
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating_data.rating
        existing_rating.review_text = rating_data.review_text
        existing_rating.updated_at = datetime.now()
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        # Create new rating
        new_rating = models.RecipeRating(
            user_id=user_id,
            recipe_id=recipe_id,
            rating=rating_data.rating,
            review_text=rating_data.review_text,
        )
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return new_rating


@router.get("/recipes/{recipe_id}/ratings", response_model=List[schemas.RecipeRatingWithUser])
async def get_recipe_ratings(
    recipe_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all ratings for a recipe, ordered by most recent first.
    """
    ratings = (
        db.query(models.RecipeRating)
        .filter(models.RecipeRating.recipe_id == recipe_id)
        .order_by(desc(models.RecipeRating.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # Enrich with user information
    result = []
    for rating in ratings:
        user = db.query(models.Users).filter(models.Users.id == rating.user_id).first()
        rating_dict = schemas.RecipeRating.model_validate(rating).model_dump()
        rating_dict['username'] = user.username if user else None
        rating_dict['user_full_name'] = user.full_name if user else None
        result.append(schemas.RecipeRatingWithUser(**rating_dict))
    
    return result


@router.get("/recipes/{recipe_id}/ratings/summary", response_model=schemas.RecipeRatingSummary)
async def get_recipe_rating_summary(
    recipe_id: int,
    db: Session = Depends(get_db)
):
    """
    Get aggregated rating statistics for a recipe.
    """
    # Check if recipe exists
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Calculate statistics
    ratings = db.query(models.RecipeRating).filter(models.RecipeRating.recipe_id == recipe_id).all()
    
    if not ratings:
        return schemas.RecipeRatingSummary(
            recipe_id=recipe_id,
            average_rating=0.0,
            total_ratings=0,
            rating_distribution={str(i): 0 for i in range(1, 6)}
        )
    
    total_ratings = len(ratings)
    average_rating = sum(r.rating for r in ratings) / total_ratings
    
    # Calculate distribution
    distribution = {str(i): 0 for i in range(1, 6)}
    for rating in ratings:
        rounded_rating = str(round(rating.rating))
        distribution[rounded_rating] = distribution.get(rounded_rating, 0) + 1
    
    return schemas.RecipeRatingSummary(
        recipe_id=recipe_id,
        average_rating=round(average_rating, 2),
        total_ratings=total_ratings,
        rating_distribution=distribution
    )


# ============================================================================
# Recipe Comments
# ============================================================================

@router.post("/recipes/{recipe_id}/comments", response_model=schemas.RecipeComment)
async def create_comment(
    recipe_id: int,
    comment_data: schemas.RecipeCommentCreate,
    user_id: int = Query(..., description="ID of the user creating the comment"),
    db: Session = Depends(get_db)
):
    """
    Create a new comment on a recipe.
    Can be a top-level comment or a reply to another comment.
    """
    # Check if recipe exists
    recipe = db.query(models.Recipes).filter(models.Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # If this is a reply, check if parent comment exists
    if comment_data.parent_comment_id:
        parent = (
            db.query(models.RecipeComment)
            .filter(models.RecipeComment.id == comment_data.parent_comment_id)
            .first()
        )
        if not parent:
            raise HTTPException(status_code=404, detail="Parent comment not found")
        if parent.recipe_id != recipe_id:
            raise HTTPException(status_code=400, detail="Parent comment is not from this recipe")
    
    # Create the comment
    new_comment = models.RecipeComment(
        user_id=user_id,
        recipe_id=recipe_id,
        comment_text=comment_data.comment_text,
        parent_comment_id=comment_data.parent_comment_id,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment


@router.get("/recipes/{recipe_id}/comments", response_model=List[schemas.RecipeCommentWithUser])
async def get_recipe_comments(
    recipe_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Get all comments for a recipe with threading support.
    Returns top-level comments with nested replies.
    """
    # Get all top-level comments (no parent)
    top_level_comments = (
        db.query(models.RecipeComment)
        .filter(
            models.RecipeComment.recipe_id == recipe_id,
            models.RecipeComment.parent_comment_id == None
        )
        .order_by(desc(models.RecipeComment.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    def build_comment_tree(comment):
        """Recursively build comment tree with user info"""
        user = db.query(models.Users).filter(models.Users.id == comment.user_id).first()
        comment_dict = schemas.RecipeComment.model_validate(comment).model_dump()
        comment_dict['username'] = user.username if user else None
        comment_dict['user_full_name'] = user.full_name if user else None
        
        # Get replies
        replies = (
            db.query(models.RecipeComment)
            .filter(models.RecipeComment.parent_comment_id == comment.id)
            .order_by(models.RecipeComment.created_at)
            .all()
        )
        comment_dict['replies'] = [build_comment_tree(reply) for reply in replies]
        
        return schemas.RecipeCommentWithUser(**comment_dict)
    
    return [build_comment_tree(comment) for comment in top_level_comments]


@router.put("/comments/{comment_id}", response_model=schemas.RecipeComment)
async def update_comment(
    comment_id: int,
    comment_data: schemas.RecipeCommentUpdate,
    user_id: int = Query(..., description="ID of the user updating the comment"),
    db: Session = Depends(get_db)
):
    """
    Update a comment. Only the comment author can update their comment.
    """
    comment = db.query(models.RecipeComment).filter(models.RecipeComment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check ownership (in production, this should use proper authentication)
    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    
    comment.comment_text = comment_data.comment_text
    comment.updated_at = datetime.now()
    db.commit()
    db.refresh(comment)
    
    return comment


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    user_id: int = Query(..., description="ID of the user deleting the comment"),
    db: Session = Depends(get_db)
):
    """
    Delete a comment. Only the comment author can delete their comment.
    Deleting a parent comment also deletes all replies (cascade).
    """
    comment = db.query(models.RecipeComment).filter(models.RecipeComment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check ownership (in production, this should use proper authentication)
    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(comment)
    db.commit()
    
    return {"message": "Comment deleted successfully"}
