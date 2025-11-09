# Database/Schemas/community.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# Recipe Rating Schemas
class RecipeRatingBase(BaseModel):
    """Base schema for recipe ratings"""
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating from 1 to 5 stars")
    review_text: Optional[str] = Field(None, description="Optional review text")


class RecipeRatingCreate(RecipeRatingBase):
    """Schema for creating a recipe rating"""
    pass


class RecipeRatingUpdate(BaseModel):
    """Schema for updating a recipe rating"""
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    review_text: Optional[str] = None


class RecipeRating(RecipeRatingBase):
    """Schema for recipe rating with metadata"""
    id: int
    recipe_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class RecipeRatingWithUser(RecipeRating):
    """Schema for recipe rating including user information"""
    username: str
    user_avatar: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# Recipe Comment Schemas
class RecipeCommentBase(BaseModel):
    """Base schema for recipe comments"""
    comment_text: str = Field(..., min_length=1, max_length=5000)
    parent_id: Optional[int] = Field(None, description="Parent comment ID for threading")


class RecipeCommentCreate(RecipeCommentBase):
    """Schema for creating a recipe comment"""
    pass


class RecipeCommentUpdate(BaseModel):
    """Schema for updating a recipe comment"""
    comment_text: str = Field(..., min_length=1, max_length=5000)


class RecipeComment(RecipeCommentBase):
    """Schema for recipe comment with metadata"""
    id: int
    recipe_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class RecipeCommentWithUser(RecipeComment):
    """Schema for recipe comment including user information"""
    username: str
    user_avatar: Optional[str] = None
    replies: List["RecipeCommentWithUser"] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)


# Recipe Star Schemas
class RecipeStarCreate(BaseModel):
    """Schema for starring a recipe"""
    pass


class RecipeStar(BaseModel):
    """Schema for recipe star with metadata"""
    id: int
    recipe_id: int
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Recipe Statistics Schemas
class RecipeStats(BaseModel):
    """Schema for recipe statistics"""
    rating_average: Optional[float] = None
    rating_count: int = 0
    comment_count: int = 0
    star_count: int = 0
    fork_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)


# User Profile Schemas
class UserProfileBase(BaseModel):
    """Base schema for user profile"""
    bio: Optional[str] = Field(None, max_length=1000)
    avatar_url: Optional[str] = Field(None, max_length=500)
    website: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=200)


class UserProfileUpdate(UserProfileBase):
    """Schema for updating user profile"""
    pass


class UserProfile(UserProfileBase):
    """Schema for user profile with public information"""
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    recipe_count: int = 0
    rating_count: int = 0
    comment_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)


# Recipe Fork Schemas
class RecipeForkCreate(BaseModel):
    """Schema for forking a recipe"""
    name: Optional[str] = Field(None, description="New name for the forked recipe")
    notes: Optional[str] = Field(None, description="Notes about changes in the fork")


class RecipeForkResponse(BaseModel):
    """Schema for recipe fork response"""
    forked_recipe_id: int
    original_recipe_id: int
    message: str
    
    model_config = ConfigDict(from_attributes=True)
