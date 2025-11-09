# services/backend/Database/Schemas/packaging_details.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


PACKAGING_DETAILS_BASE_EXAMPLE = {
    "packaging_date": "2024-04-15T10:00:00Z",
    "method": "bottling",
    "carbonation_method": "priming_sugar",
    "volumes_co2": 2.4,
    "container_count": 48,
    "container_size": 0.5,
    "priming_sugar_amount": 120.5,
    "priming_sugar_type": "table",
    "temperature": 68.0,
    "notes": "Bottled into 500ml amber bottles, stored in basement",
}

PACKAGING_DETAILS_KEGGING_EXAMPLE = {
    "packaging_date": "2024-04-15T10:00:00Z",
    "method": "kegging",
    "carbonation_method": "forced",
    "volumes_co2": 2.5,
    "container_count": 1,
    "container_size": 19.0,
    "pressure_psi": 12.5,
    "temperature": 38.0,
    "notes": "Kegged into 5 gallon corny keg, carbonating at 38F",
}

PACKAGING_DETAILS_FULL_EXAMPLE = {
    **PACKAGING_DETAILS_BASE_EXAMPLE,
    "id": 1,
    "batch_id": 11,
    "created_at": "2024-04-15T10:00:00Z",
    "updated_at": "2024-04-15T10:00:00Z",
}


class PackagingDetailsBase(BaseModel):
    packaging_date: datetime = Field(..., description="Date when packaging was completed")
    method: str = Field(..., description="Packaging method: 'bottling' or 'kegging'")
    carbonation_method: str = Field(
        ..., 
        description="Carbonation method: 'priming_sugar', 'forced', or 'natural'"
    )
    volumes_co2: Optional[float] = Field(
        None, 
        description="Target CO2 volumes (typically 2.0-3.0)"
    )
    container_count: Optional[int] = Field(
        None, 
        description="Number of bottles or kegs"
    )
    container_size: Optional[float] = Field(
        None, 
        description="Size of each container in liters or gallons"
    )
    priming_sugar_amount: Optional[float] = Field(
        None, 
        description="Amount of priming sugar in grams (for bottling)"
    )
    priming_sugar_type: Optional[str] = Field(
        None, 
        description="Type of priming sugar: 'table', 'corn', 'dme', or 'honey'"
    )
    pressure_psi: Optional[float] = Field(
        None, 
        description="Carbonation pressure in PSI (for kegging)"
    )
    temperature: Optional[float] = Field(
        None, 
        description="Temperature at packaging in Fahrenheit"
    )
    notes: Optional[str] = Field(
        None, 
        description="Additional notes about packaging"
    )

    model_config = ConfigDict(
        json_schema_extra={"example": PACKAGING_DETAILS_BASE_EXAMPLE}
    )


class PackagingDetailsCreate(PackagingDetailsBase):
    pass


class PackagingDetailsUpdate(BaseModel):
    packaging_date: Optional[datetime] = None
    method: Optional[str] = None
    carbonation_method: Optional[str] = None
    volumes_co2: Optional[float] = None
    container_count: Optional[int] = None
    container_size: Optional[float] = None
    priming_sugar_amount: Optional[float] = None
    priming_sugar_type: Optional[str] = None
    pressure_psi: Optional[float] = None
    temperature: Optional[float] = None
    notes: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "container_count": 50,
                "notes": "Updated bottle count after breakage",
            }
        }
    )


class PackagingDetails(PackagingDetailsBase):
    id: int
    batch_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": PACKAGING_DETAILS_FULL_EXAMPLE},
    )
