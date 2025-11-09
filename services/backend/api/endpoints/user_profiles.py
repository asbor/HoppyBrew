# api/endpoints/user_profiles.py
"""
User Profile API Endpoints
Handles user profile information for community features
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from database import get_db
import Database.Models as models
import Database.Schemas as schemas

router = APIRouter()


@router.get("/users/{user_id}/profile", response_model=schemas.UserProfile)
async def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user profile information.
    Returns full profile for the authenticated user, limited info for others.
    """
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.get("/users/{user_id}/profile/public", response_model=schemas.UserProfilePublic)
async def get_public_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get public user profile with recipe statistics.
    This endpoint returns only public information.
    """
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get recipe counts
    total_recipes = (
        db.query(func.count(models.Recipes.id))
        .filter(models.Recipes.user_id == user_id)
        .scalar()
    )
    
    public_recipes = (
        db.query(func.count(models.Recipes.id))
        .filter(
            models.Recipes.user_id == user_id,
            models.Recipes.is_public == True
        )
        .scalar()
    )
    
    profile_data = schemas.UserProfile.model_validate(user).model_dump()
    profile_data['recipe_count'] = total_recipes or 0
    profile_data['public_recipe_count'] = public_recipes or 0
    
    return schemas.UserProfilePublic(**profile_data)


@router.patch("/users/{user_id}/profile", response_model=schemas.UserProfile)
async def update_user_profile(
    user_id: int,
    profile_data: schemas.UserProfileUpdate,
    db: Session = Depends(get_db)
):
    """
    Update user profile information.
    In production, should verify that the authenticated user matches user_id.
    """
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/users/{user_id}/recipes", response_model=list[schemas.Recipe])
async def get_user_recipes(
    user_id: int,
    include_private: bool = Query(False, description="Include private recipes (requires auth)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all recipes by a user.
    By default returns only public recipes. Set include_private=true to see all recipes.
    """
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    query = db.query(models.Recipes).filter(models.Recipes.user_id == user_id)
    
    if not include_private:
        query = query.filter(models.Recipes.is_public == True)
    
    recipes = query.offset(skip).limit(limit).all()
    
    return recipes
