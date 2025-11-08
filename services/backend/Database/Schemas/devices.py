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
    "batch_id": None,
    "auto_import_enabled": True,
    "import_interval_seconds": 900,
    "alert_config": {
        "temp_min": 18.0,
        "temp_max": 22.0,
        "gravity_alert_enabled": True,
        "notification_enabled": True,
    },
    "manual_override": False,
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
    batch_id: Optional[int] = None
    auto_import_enabled: bool = True
    import_interval_seconds: int = 900
    alert_config: Optional[Dict[str, Any]] = None
    manual_override: bool = False
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
    batch_id: Optional[int] = None
    auto_import_enabled: Optional[bool] = None
    import_interval_seconds: Optional[int] = None
    alert_config: Optional[Dict[str, Any]] = None
    manual_override: Optional[bool] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated iSpindel Name",
                "batch_id": 1,
                "manual_override": True,
                "is_active": False,
            }
        }
    )


class DeviceInDBBase(DeviceBase):
    id: int
    last_import_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **DEVICE_BASE_EXAMPLE,
                "id": 1,
                "last_import_at": "2024-03-15T09:30:00Z",
                "created_at": "2024-03-01T10:00:00Z",
                "updated_at": "2024-03-15T09:30:00Z",
            }
        },
    )


class Device(DeviceInDBBase):
    pass
