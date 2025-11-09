"""
Pydantic schemas for yeast management features.
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


# YeastStrain Schemas
class YeastStrainBase(BaseModel):
    """Base schema for yeast strain"""
    name: str = Field(..., description="Name of the yeast strain")
    laboratory: Optional[str] = Field(None, description="Laboratory/manufacturer")
    product_id: Optional[str] = Field(None, description="Product ID or catalog number")
    type: Optional[str] = Field(None, description="Type of yeast (Ale, Lager, Wine, etc.)")
    form: Optional[str] = Field(None, description="Form (Liquid, Dry, Slant, Culture)")
    min_temperature: Optional[float] = Field(None, description="Minimum fermentation temperature (°C)")
    max_temperature: Optional[float] = Field(None, description="Maximum fermentation temperature (°C)")
    flocculation: Optional[str] = Field(None, description="Flocculation level (Low, Medium, High, Very High)")
    attenuation_min: Optional[float] = Field(None, description="Minimum attenuation percentage")
    attenuation_max: Optional[float] = Field(None, description="Maximum attenuation percentage")
    alcohol_tolerance: Optional[float] = Field(None, description="Alcohol tolerance (ABV %)")
    best_for: Optional[str] = Field(None, description="Best uses for this strain")
    notes: Optional[str] = Field(None, description="Additional notes")
    max_reuse: Optional[int] = Field(5, description="Maximum recommended reuse generations")
    viability_days_dry: Optional[int] = Field(1095, description="Viability days for dry yeast")
    viability_days_liquid: Optional[int] = Field(180, description="Viability days for liquid yeast")
    viability_days_slant: Optional[int] = Field(730, description="Viability days for slant")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "SafAle US-05",
                "laboratory": "Fermentis",
                "product_id": "US-05",
                "type": "Ale",
                "form": "Dry",
                "min_temperature": 15.0,
                "max_temperature": 24.0,
                "flocculation": "Medium",
                "attenuation_min": 78.0,
                "attenuation_max": 82.0,
                "alcohol_tolerance": 12.0,
                "best_for": "American Pale Ales, IPAs, and other American styles",
                "max_reuse": 5
            }
        }
    )


class YeastStrainCreate(YeastStrainBase):
    """Schema for creating a new yeast strain"""
    pass


class YeastStrainUpdate(BaseModel):
    """Schema for updating a yeast strain"""
    name: Optional[str] = None
    laboratory: Optional[str] = None
    product_id: Optional[str] = None
    type: Optional[str] = None
    form: Optional[str] = None
    min_temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    flocculation: Optional[str] = None
    attenuation_min: Optional[float] = None
    attenuation_max: Optional[float] = None
    alcohol_tolerance: Optional[float] = None
    best_for: Optional[str] = None
    notes: Optional[str] = None
    max_reuse: Optional[int] = None
    viability_days_dry: Optional[int] = None
    viability_days_liquid: Optional[int] = None
    viability_days_slant: Optional[int] = None


class YeastStrain(YeastStrainBase):
    """Schema for returning yeast strain data"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# YeastHarvest Schemas
class YeastHarvestBase(BaseModel):
    """Base schema for yeast harvest"""
    source_batch_id: Optional[int] = Field(None, description="ID of the batch this yeast was harvested from")
    source_inventory_id: Optional[int] = Field(None, description="ID of the source inventory yeast")
    yeast_strain_id: int = Field(..., description="ID of the yeast strain")
    generation: int = Field(1, description="Generation number (1 for first generation)")
    parent_harvest_id: Optional[int] = Field(None, description="ID of the parent harvest")
    quantity_harvested: float = Field(..., description="Quantity harvested")
    unit: str = Field("ml", description="Unit of measurement (ml, g, cells)")
    viability_at_harvest: Optional[float] = Field(None, description="Viability at harvest (0-100%)")
    cell_count: Optional[float] = Field(None, description="Cell count in billions")
    storage_method: Optional[str] = Field(None, description="Storage method (refrigerated, frozen, slant)")
    storage_temperature: Optional[float] = Field(None, description="Storage temperature (°C)")
    status: str = Field("active", description="Status (active, used, discarded)")
    notes: Optional[str] = Field(None, description="Additional notes")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "source_batch_id": 1,
                "yeast_strain_id": 1,
                "generation": 1,
                "quantity_harvested": 200.0,
                "unit": "ml",
                "viability_at_harvest": 95.0,
                "cell_count": 250.0,
                "storage_method": "refrigerated",
                "storage_temperature": 4.0,
                "status": "active",
                "notes": "Harvested from top cropping"
            }
        }
    )


class YeastHarvestCreate(YeastHarvestBase):
    """Schema for creating a new yeast harvest"""
    harvest_date: Optional[datetime] = None


class YeastHarvestUpdate(BaseModel):
    """Schema for updating a yeast harvest"""
    quantity_harvested: Optional[float] = None
    viability_at_harvest: Optional[float] = None
    cell_count: Optional[float] = None
    storage_method: Optional[str] = None
    storage_temperature: Optional[float] = None
    status: Optional[str] = None
    used_date: Optional[datetime] = None
    notes: Optional[str] = None


class YeastHarvest(YeastHarvestBase):
    """Schema for returning yeast harvest data"""
    id: int
    harvest_date: datetime
    used_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Viability Calculation Schemas
class ViabilityCalculationRequest(BaseModel):
    """Schema for viability calculation request"""
    yeast_form: str = Field(..., description="Form of yeast (Dry, Liquid, Slant)")
    manufacture_date: Optional[datetime] = Field(None, description="Manufacture/packaging date")
    expiry_date: Optional[datetime] = Field(None, description="Expiry date")
    current_date: Optional[datetime] = Field(None, description="Date to calculate viability for (default: today)")
    initial_viability: float = Field(100.0, description="Initial viability percentage")
    storage_temperature: Optional[float] = Field(None, description="Storage temperature (°C)")
    generation: int = Field(0, description="Generation number (0 for commercial)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "yeast_form": "Liquid",
                "manufacture_date": "2024-01-01T00:00:00",
                "initial_viability": 100.0,
                "storage_temperature": 4.0,
                "generation": 0
            }
        }
    )


class ViabilityCalculationResponse(BaseModel):
    """Schema for viability calculation response"""
    current_viability: float = Field(..., description="Current estimated viability (0-100%)")
    days_since_manufacture: Optional[int] = Field(None, description="Days since manufacture")
    days_until_expiry: Optional[int] = Field(None, description="Days until expiry")
    viability_status: str = Field(..., description="Status (excellent, good, fair, poor, expired)")
    recommendation: str = Field(..., description="Recommendation for use")
    estimated_cell_loss_percent: float = Field(..., description="Percentage of cells lost")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "current_viability": 85.2,
                "days_since_manufacture": 90,
                "days_until_expiry": 90,
                "viability_status": "good",
                "recommendation": "Suitable for use with a starter",
                "estimated_cell_loss_percent": 14.8
            }
        }
    )
