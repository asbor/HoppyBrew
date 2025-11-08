# services/backend/Database/Schemas/fermentation_readings.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


FERMENTATION_READING_BASE_EXAMPLE = {
    "timestamp": "2024-03-21T14:30:00Z",
    "gravity": 1.048,
    "temperature": 18.5,
    "ph": 5.4,
    "notes": "Active fermentation observed, krausen forming nicely",
    "device_id": None,
    "source": "manual",
}

FERMENTATION_READING_FULL_EXAMPLE = {
    **FERMENTATION_READING_BASE_EXAMPLE,
    "id": 1,
    "batch_id": 11,
    "created_at": "2024-03-21T14:30:00Z",
}

CHART_DATA_EXAMPLE = {
    "timestamps": [
        "2024-03-21T14:30:00Z",
        "2024-03-22T14:30:00Z",
        "2024-03-23T14:30:00Z",
    ],
    "gravity": [1.048, 1.032, 1.020],
    "temperature": [18.5, 19.0, 18.8],
    "ph": [5.4, 5.2, 5.1],
    "abv": [0.0, 2.1, 3.7],
    "attenuation": [0.0, 33.3, 58.3],
}


class FermentationReadingBase(BaseModel):
    timestamp: datetime = Field(..., description="Time when the reading was taken")
    gravity: Optional[float] = Field(
        None, description="Specific gravity reading (e.g., 1.048)"
    )
    temperature: Optional[float] = Field(
        None, description="Temperature in degrees Celsius"
    )
    ph: Optional[float] = Field(None, description="pH level of the fermenting beer")
    notes: Optional[str] = Field(None, description="Additional notes about the reading")
    device_id: Optional[int] = Field(None, description="ID of device that created this reading")
    source: Optional[str] = Field("manual", description="Source of reading: manual, tilt, ispindel, etc.")

    model_config = ConfigDict(
        json_schema_extra={"example": FERMENTATION_READING_BASE_EXAMPLE}
    )


class FermentationReadingCreate(FermentationReadingBase):
    pass


class FermentationReadingUpdate(BaseModel):
    timestamp: Optional[datetime] = None
    gravity: Optional[float] = None
    temperature: Optional[float] = None
    ph: Optional[float] = None
    notes: Optional[str] = None
    device_id: Optional[int] = None
    source: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "gravity": 1.020,
                "temperature": 19.0,
                "notes": "Updated gravity reading after 3 days",
            }
        }
    )


class FermentationReading(FermentationReadingBase):
    id: int
    batch_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": FERMENTATION_READING_FULL_EXAMPLE},
    )


class FermentationChartData(BaseModel):
    timestamps: list[str] = Field(
        ..., description="List of reading timestamps in ISO format"
    )
    gravity: list[Optional[float]] = Field(..., description="List of gravity readings")
    temperature: list[Optional[float]] = Field(
        ..., description="List of temperature readings"
    )
    ph: list[Optional[float]] = Field(..., description="List of pH readings")
    abv: list[float] = Field(..., description="Calculated ABV at each reading")
    attenuation: list[float] = Field(
        ..., description="Calculated attenuation percentage at each reading"
    )

    model_config = ConfigDict(json_schema_extra={"example": CHART_DATA_EXAMPLE})
