"""
Pydantic schemas for authentication and user management
"""

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration"""

    admin = "admin"
    brewer = "brewer"
    viewer = "viewer"


class UserBase(BaseModel):
    """Base user schema"""

    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole = UserRole.viewer
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for user creation"""

    password: str


class UserUpdate(BaseModel):
    """Schema for user updates"""

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response (no password)"""

    id: int
    is_verified: bool
    created_at: str
    full_name: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """JWT token response schema"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema"""

    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema"""

    username: str
    password: str
