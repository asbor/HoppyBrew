from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

DEVICE_BASE_EXAMPLE = {
    "name": "My iSpindel",
    "device_type": "ispindel",
    "description": "iSpindel for monitoring IPA fermentation",
    "api_endpoint": "/api/devices/ispindel/data",
    "api_token": "secret-token-123",
    "calibration_data": {
        "polynomial": [0.0, 0.0, 0.0, 1.0],  # Calibration polynomial coefficients
        "temp_correction": True,
    },
    "configuration": {
        "update_interval": 900,  # 15 minutes in seconds
        "battery_warning_threshold": 3.5,
    },
    "is_active": True,
}


class DeviceBase(BaseModel):
    name: str
    device_type: str
    description: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_token: Optional[str] = None
    calibration_data: Optional[Dict[str, Any]] = None
    configuration: Optional[Dict[str, Any]] = None
    is_active: bool = True

    model_config = ConfigDict(json_schema_extra={"example": DEVICE_BASE_EXAMPLE})


class DeviceCreate(DeviceBase):
    model_config = ConfigDict(json_schema_extra={"example": DEVICE_BASE_EXAMPLE})


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    device_type: Optional[str] = None
    description: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_token: Optional[str] = None
    calibration_data: Optional[Dict[str, Any]] = None
    configuration: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": "Updated iSpindel Name", "is_active": False}
        }
    )


class DeviceInDBBase(DeviceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **DEVICE_BASE_EXAMPLE,
                "id": 1,
                "created_at": "2024-03-01T10:00:00Z",
                "updated_at": "2024-03-15T09:30:00Z",
            }
        },
    )


class Device(DeviceInDBBase):
    pass
