# Database/Schemas/user_profile.py

from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


class UserProfileBase(BaseModel):
    """Base schema for user profile"""
    bio: Optional[str] = Field(None, max_length=500, description="User biography")
    location: Optional[str] = Field(None, max_length=100, description="User location")
    avatar_url: Optional[str] = Field(None, max_length=255, description="Avatar image URL")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "bio": "Home brewer for 5 years, specializing in IPAs and Belgian styles",
                "location": "Portland, OR",
                "avatar_url": "https://example.com/avatars/user123.jpg"
            }
        }
    )


class UserProfileUpdate(UserProfileBase):
    """Schema for updating user profile"""
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


class UserProfile(BaseModel):
    """Full user profile schema"""
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserProfilePublic(BaseModel):
    """Public user profile (limited information)"""
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    recipe_count: Optional[int] = 0
    public_recipe_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)
