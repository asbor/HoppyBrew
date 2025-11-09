# Database/Schemas/recipe_comments.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class RecipeCommentBase(BaseModel):
    """Base schema for recipe comment"""
    comment_text: str = Field(..., min_length=1, max_length=2000)
    parent_comment_id: Optional[int] = Field(None, description="Parent comment ID for threaded replies")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "comment_text": "Has anyone tried this with Cascade hops instead?",
                "parent_comment_id": None
            }
        }
    )


class RecipeCommentCreate(RecipeCommentBase):
    """Schema for creating a new comment"""
    pass


class RecipeCommentUpdate(BaseModel):
    """Schema for updating an existing comment"""
    comment_text: str = Field(..., min_length=1, max_length=2000)


class RecipeComment(RecipeCommentBase):
    """Full comment schema with database fields"""
    id: int
    user_id: int
    recipe_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecipeCommentWithUser(RecipeComment):
    """Comment with user information and replies"""
    username: Optional[str] = None
    user_full_name: Optional[str] = None
    replies: List["RecipeCommentWithUser"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# Enable forward references for recursive model
RecipeCommentWithUser.model_rebuild()
