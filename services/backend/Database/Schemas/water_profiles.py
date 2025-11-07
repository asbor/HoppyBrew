from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

WATER_PROFILE_EXAMPLE = {
    "name": "Burton-on-Trent IPA",
    "description": "Classic British brewing water profile ideal for hoppy, bitter beers",
    "profile_type": "target",
    "style_category": "IPA",
    "calcium": 275,
    "magnesium": 45,
    "sodium": 25,
    "chloride": 35,
    "sulfate": 650,
    "bicarbonate": 260,
    "ph": 8.0,
    "notes": "Idealized profile for hoppy ales with high sulfate to chloride ratio.",
}

SOURCE_PROFILE_EXAMPLE = {
    "name": "Reverse Osmosis Water",
    "description": "Starting water with minimal mineral content",
    "profile_type": "source",
    "calcium": 1,
    "magnesium": 0,
    "sodium": 8,
    "chloride": 4,
    "sulfate": 1,
    "bicarbonate": 16,
}


class WaterProfileBase(BaseModel):
    """
    Base schema for water profiles.

    Supports two types of profiles:
    - source: Starting water (e.g., RO water, tap water, distilled water)
    - target: Desired brewing water profile for specific beer styles
    """

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    profile_type: str = Field(default='source', pattern='^(source|target)$')
    style_category: Optional[str] = Field(None, max_length=100)

    # Ion concentrations (ppm)
    calcium: Decimal = Field(default=0, ge=0, le=10000)
    magnesium: Decimal = Field(default=0, ge=0, le=10000)
    sodium: Decimal = Field(default=0, ge=0, le=10000)
    chloride: Decimal = Field(default=0, ge=0, le=10000)
    sulfate: Decimal = Field(default=0, ge=0, le=10000)
    bicarbonate: Decimal = Field(default=0, ge=0, le=10000)

    # Additional properties
    ph: Optional[Decimal] = Field(None, ge=0, le=14)
    total_alkalinity: Optional[Decimal] = Field(None, ge=0)
    residual_alkalinity: Optional[Decimal] = None

    # Legacy fields (for backward compatibility)
    version: Optional[int] = None
    amount: Optional[int] = None
    notes: Optional[str] = None
    display_amount: Optional[str] = None
    inventory: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={"example": WATER_PROFILE_EXAMPLE}
    )


class WaterProfileCreate(WaterProfileBase):
    """Schema for creating a new water profile."""

    is_custom: bool = Field(default=True)

    model_config = ConfigDict(
        json_schema_extra={"example": WATER_PROFILE_EXAMPLE}
    )


class WaterProfileUpdate(BaseModel):
    """Schema for updating an existing water profile."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    profile_type: Optional[str] = Field(None, pattern='^(source|target)$')
    style_category: Optional[str] = Field(None, max_length=100)

    # Ion concentrations (ppm)
    calcium: Optional[Decimal] = Field(None, ge=0, le=10000)
    magnesium: Optional[Decimal] = Field(None, ge=0, le=10000)
    sodium: Optional[Decimal] = Field(None, ge=0, le=10000)
    chloride: Optional[Decimal] = Field(None, ge=0, le=10000)
    sulfate: Optional[Decimal] = Field(None, ge=0, le=10000)
    bicarbonate: Optional[Decimal] = Field(None, ge=0, le=10000)

    # Additional properties
    ph: Optional[Decimal] = Field(None, ge=0, le=14)
    total_alkalinity: Optional[Decimal] = Field(None, ge=0)
    residual_alkalinity: Optional[Decimal] = None

    # Legacy fields
    version: Optional[int] = None
    amount: Optional[int] = None
    notes: Optional[str] = None
    display_amount: Optional[str] = None
    inventory: Optional[int] = None


class WaterProfile(WaterProfileBase):
    """Schema for water profile with database fields."""

    id: int
    is_default: bool
    is_custom: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {
            "id": 1,
            "name": "Amber Balanced",
            "description": "Balanced water profile for amber ales",
            "profile_type": "target",
            "style_category": "Amber Ales",
            "calcium": 50,
            "magnesium": 10,
            "sodium": 15,
            "chloride": 63,
            "sulfate": 75,
            "bicarbonate": 40,
            "ph": 7.0,
            "is_default": True,
            "is_custom": False,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }}
    )
