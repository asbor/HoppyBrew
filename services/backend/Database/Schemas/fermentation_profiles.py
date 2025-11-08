from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# Fermentation Step Schemas
class FermentationStepBase(BaseModel):
    """Base schema for fermentation step"""

    step_order: int = Field(
        ..., description="Order of the step in the fermentation process"
    )
    name: Optional[str] = Field(None, description="Name of the fermentation step")
    step_type: str = Field(
        default="primary",
        description="Type of fermentation step (primary, secondary, conditioning, cold_crash, diacetyl_rest, lagering)",
    )
    temperature: Optional[Decimal] = Field(None, description="Temperature in Celsius")
    duration_days: Optional[int] = Field(None, description="Duration in days")
    ramp_days: int = Field(
        default=0, description="Ramp time in days for gradual temperature changes"
    )
    pressure_psi: Optional[Decimal] = Field(
        None, description="Pressure in PSI for pressurized fermentation"
    )
    notes: Optional[str] = Field(None, description="Additional notes for the step")

    model_config = ConfigDict(from_attributes=True)


class FermentationStepCreate(FermentationStepBase):
    """Schema for creating a fermentation step"""

    pass


class FermentationStepUpdate(BaseModel):
    """Schema for updating a fermentation step"""

    step_order: Optional[int] = None
    name: Optional[str] = None
    step_type: Optional[str] = None
    temperature: Optional[Decimal] = None
    duration_days: Optional[int] = None
    ramp_days: Optional[int] = None
    pressure_psi: Optional[Decimal] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class FermentationStep(FermentationStepBase):
    """Schema for fermentation step response"""

    id: int
    fermentation_profile_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FermentationProfileBase(BaseModel):
    """Base schema for fermentation profile"""

    name: str = Field(..., description="Name of the fermentation profile")
    description: Optional[str] = Field(None, description="Description of the profile")
    is_pressurized: bool = Field(
        default=False, description="Whether the profile uses pressurized fermentation"
    )
    is_template: bool = Field(
        default=False, description="Whether this is a template profile"
    )

    model_config = ConfigDict(from_attributes=True)


class FermentationProfileCreate(FermentationProfileBase):
    """Schema for creating a fermentation profile"""

    steps: Optional[List[FermentationStepCreate]] = Field(
        default_factory=list, description="List of fermentation steps"
    )


class FermentationProfileUpdate(BaseModel):
    """Schema for updating a fermentation profile"""

    name: Optional[str] = None
    description: Optional[str] = None
    is_pressurized: Optional[bool] = None
    is_template: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class FermentationProfile(FermentationProfileBase):
    """Schema for fermentation profile response"""

    id: int
    created_at: datetime
    updated_at: datetime
    steps: List[FermentationStep] = []

    model_config = ConfigDict(from_attributes=True)


FERMENTATION_PROFILE_EXAMPLE = {
    "name": "Standard Ale",
    "description": "Basic ale fermentation profile with primary and conditioning phases",
    "is_pressurized": False,
    "is_template": True,
    "steps": [
        {
            "step_order": 1,
            "name": "Primary Fermentation",
            "step_type": "primary",
            "temperature": 20,
            "duration_days": 7,
            "ramp_days": 0,
            "notes": "Primary fermentation at 20°C",
        },
        {
            "step_order": 2,
            "name": "Conditioning",
            "step_type": "conditioning",
            "temperature": 18,
            "duration_days": 7,
            "ramp_days": 1,
            "notes": "Conditioning phase with gradual temperature ramp",
        },
    ],
}

LAGER_PROFILE_EXAMPLE = {
    "name": "Lager",
    "description": "Traditional lager fermentation profile with lagering phase",
    "is_pressurized": False,
    "is_template": True,
    "steps": [
        {
            "step_order": 1,
            "name": "Primary Fermentation",
            "step_type": "primary",
            "temperature": 10,
            "duration_days": 14,
            "ramp_days": 0,
        },
        {
            "step_order": 2,
            "name": "Diacetyl Rest",
            "step_type": "diacetyl_rest",
            "temperature": 18,
            "duration_days": 2,
            "ramp_days": 1,
        },
        {
            "step_order": 3,
            "name": "Lagering",
            "step_type": "lagering",
            "temperature": 2,
            "duration_days": 28,
            "ramp_days": 2,
        },
    ],
}

NEIPA_PROFILE_EXAMPLE = {
    "name": "NEIPA",
    "description": "New England IPA fermentation profile with cold crash",
    "is_pressurized": False,
    "is_template": True,
    "steps": [
        {
            "step_order": 1,
            "name": "Primary Fermentation",
            "step_type": "primary",
            "temperature": 19,
            "duration_days": 4,
            "ramp_days": 0,
        },
        {
            "step_order": 2,
            "name": "Dry Hop Conditioning",
            "step_type": "conditioning",
            "temperature": 21,
            "duration_days": 3,
            "ramp_days": 0,
        },
        {
            "step_order": 3,
            "name": "Cold Crash",
            "step_type": "cold_crash",
            "temperature": 4,
            "duration_days": 2,
            "ramp_days": 1,
        },
    ],
}
