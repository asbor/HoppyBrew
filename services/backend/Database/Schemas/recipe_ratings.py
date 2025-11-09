# Database/Schemas/recipe_ratings.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class RecipeRatingBase(BaseModel):
    """Base schema for recipe rating"""
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating from 1 to 5 stars")
    review_text: Optional[str] = Field(None, max_length=2000, description="Optional review text")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rating": 4.5,
                "review_text": "Great recipe! The hop profile is well balanced."
            }
        }
    )


class RecipeRatingCreate(RecipeRatingBase):
    """Schema for creating a new rating"""
    pass


class RecipeRatingUpdate(BaseModel):
    """Schema for updating an existing rating"""
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    review_text: Optional[str] = Field(None, max_length=2000)


class RecipeRating(RecipeRatingBase):
    """Full rating schema with database fields"""
    id: int
    user_id: int
    recipe_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecipeRatingWithUser(RecipeRating):
    """Rating with user information"""
    username: Optional[str] = None
    user_full_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RecipeRatingSummary(BaseModel):
    """Aggregated rating statistics for a recipe"""
    recipe_id: int
    average_rating: float
    total_ratings: int
    rating_distribution: dict  # {1: count, 2: count, ...}

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "recipe_id": 1,
                "average_rating": 4.2,
                "total_ratings": 15,
                "rating_distribution": {"1": 0, "2": 1, "3": 2, "4": 5, "5": 7}
            }
        }
    )
