# services/backend/Database/Schemas/packaging_details.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class PackagingDetailsBase(BaseModel):
    """Base schema for packaging details"""

    method: str = Field(
        ..., description="Packaging method: 'bottle' or 'keg'"
    )
    date: datetime = Field(
        default_factory=datetime.now, description="Packaging date"
    )
    carbonation_method: Optional[str] = Field(
        None, description="Carbonation method: 'priming', 'forced', 'natural'"
    )
    volumes: Optional[float] = Field(
        None, ge=0, le=5, description="Target CO2 volumes (e.g., 2.5)"
    )
    container_count: Optional[int] = Field(
        None, ge=0, description="Number of bottles or kegs"
    )
    container_size: Optional[float] = Field(
        None, ge=0, description="Container size in liters or gallons"
    )
    priming_sugar_type: Optional[str] = Field(
        None, description="Type of priming sugar: 'table', 'corn', 'dme', 'honey'"
    )
    priming_sugar_amount: Optional[float] = Field(
        None, ge=0, description="Amount of priming sugar in grams"
    )
    carbonation_temp: Optional[float] = Field(
        None, description="Temperature for carbonation in Fahrenheit"
    )
    carbonation_psi: Optional[float] = Field(
        None, ge=0, description="PSI for forced carbonation"
    )
    notes: Optional[str] = Field(None, description="Additional notes")


class PackagingDetailsCreate(PackagingDetailsBase):
    """Schema for creating packaging details"""

    batch_id: int = Field(..., description="ID of the batch being packaged")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "batch_id": 1,
                "method": "bottle",
                "date": "2024-11-09T12:00:00",
                "carbonation_method": "priming",
                "volumes": 2.5,
                "container_count": 48,
                "container_size": 0.5,
                "priming_sugar_type": "corn",
                "priming_sugar_amount": 150.0,
                "notes": "Bottled using 500ml bottles",
            }
        }
    )


class PackagingDetailsUpdate(BaseModel):
    """Schema for updating packaging details"""

    method: Optional[str] = None
    date: Optional[datetime] = None
    carbonation_method: Optional[str] = None
    volumes: Optional[float] = Field(None, ge=0, le=5)
    container_count: Optional[int] = Field(None, ge=0)
    container_size: Optional[float] = Field(None, ge=0)
    priming_sugar_type: Optional[str] = None
    priming_sugar_amount: Optional[float] = Field(None, ge=0)
    carbonation_temp: Optional[float] = None
    carbonation_psi: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class PackagingDetails(PackagingDetailsBase):
    """Schema for reading packaging details"""

    id: int
    batch_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
