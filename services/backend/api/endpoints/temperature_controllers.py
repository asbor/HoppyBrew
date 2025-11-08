# api/endpoints/temperature_controllers.py

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


# Pydantic models for webhook data
class TiltData(BaseModel):
    """Data structure for Tilt Hydrometer webhook"""
    color: str = Field(..., description="Tilt color identifier (Red, Green, Black, Purple, Orange, Blue, Yellow, Pink)")
    temp_fahrenheit: Optional[float] = Field(None, description="Temperature in Fahrenheit")
    temp_celsius: Optional[float] = Field(None, description="Temperature in Celsius")
    gravity: float = Field(..., description="Specific gravity reading")
    timestamp: Optional[datetime] = Field(None, description="Reading timestamp")
    rssi: Optional[int] = Field(None, description="Signal strength")
    beer: Optional[str] = Field(None, description="Beer name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "color": "Red",
                "temp_fahrenheit": 68.5,
                "temp_celsius": 20.3,
                "gravity": 1.048,
                "timestamp": "2024-03-21T14:30:00Z",
                "rssi": -45,
                "beer": "IPA Batch 42"
            }
        }


class ISpindelData(BaseModel):
    """Data structure for iSpindel webhook"""
    name: str = Field(..., description="iSpindel device name")
    ID: Optional[int] = Field(None, description="Device chip ID")
    angle: float = Field(..., description="Tilt angle in degrees")
    temperature: float = Field(..., description="Temperature in Celsius")
    temp_units: Optional[str] = Field("C", description="Temperature units")
    battery: float = Field(..., description="Battery voltage")
    gravity: float = Field(..., description="Specific gravity reading")
    interval: Optional[int] = Field(None, description="Update interval in seconds")
    RSSI: Optional[int] = Field(None, description="WiFi signal strength")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "iSpindel001",
                "ID": 12345678,
                "angle": 45.23,
                "temperature": 20.5,
                "temp_units": "C",
                "battery": 3.87,
                "gravity": 1.048,
                "interval": 900,
                "RSSI": -62
            }
        }


def apply_calibration(gravity: float, angle: float, calibration_data: Optional[Dict[str, Any]]) -> float:
    """
    Apply calibration polynomial to convert angle to gravity.
    For iSpindel, calibration is typically: gravity = a0 + a1*angle + a2*angle^2 + a3*angle^3
    """
    if not calibration_data or "polynomial" not in calibration_data:
        return gravity
    
    poly = calibration_data["polynomial"]
    if not poly or len(poly) == 0:
        return gravity
    
    # Apply polynomial: sum(coef[i] * angle^i)
    calibrated = sum(coef * (angle ** i) for i, coef in enumerate(poly))
    return round(calibrated, 4)


def check_alerts(device: models.Device, temperature: Optional[float], gravity: Optional[float]) -> List[str]:
    """
    Check if readings trigger any configured alerts.
    Returns list of alert messages.
    """
    alerts = []
    
    if not device.alert_config:
        return alerts
    
    config = device.alert_config
    
    # Temperature alerts
    if temperature is not None:
        if "temp_min" in config and temperature < config["temp_min"]:
            alerts.append(f"Temperature too low: {temperature}°C < {config['temp_min']}°C")
        if "temp_max" in config and temperature > config["temp_max"]:
            alerts.append(f"Temperature too high: {temperature}°C > {config['temp_max']}°C")
    
    # Gravity alerts (e.g., fermentation stuck)
    if gravity is not None and config.get("gravity_alert_enabled"):
        # This is a placeholder - in real implementation, you'd check if gravity hasn't changed
        # over multiple readings to detect stuck fermentation
        pass
    
    return alerts


@router.post("/temperature-controllers/tilt/webhook/{device_id}", tags=["temperature_controllers"])
async def receive_tilt_data(
    device_id: int,
    data: TiltData,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Webhook endpoint to receive data from Tilt Hydrometer.
    
    This endpoint receives telemetry data from Tilt devices via cloud services
    or local bridges. The data is validated, stored as a fermentation reading,
    and checked against alert thresholds.
    """
    # Verify device exists and is a Tilt
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if device.device_type.lower() != "tilt":
        raise HTTPException(status_code=400, detail="Device is not a Tilt hydrometer")
    
    if not device.is_active:
        raise HTTPException(status_code=400, detail="Device is not active")
    
    if device.manual_override:
        logger.info(f"Tilt device {device_id} has manual override enabled, skipping import")
        return {"status": "skipped", "reason": "manual_override"}
    
    if not device.batch_id:
        raise HTTPException(status_code=400, detail="Device is not associated with a batch")
    
    # Use Celsius for consistency, convert if needed
    temperature = data.temp_celsius if data.temp_celsius is not None else (
        (data.temp_fahrenheit - 32) * 5/9 if data.temp_fahrenheit is not None else None
    )
    
    # Create fermentation reading
    reading = models.FermentationReadings(
        batch_id=device.batch_id,
        device_id=device_id,
        timestamp=data.timestamp or datetime.now(timezone.utc),
        gravity=data.gravity,
        temperature=temperature,
        source="tilt",
        notes=f"Tilt {data.color}" + (f" (RSSI: {data.rssi})" if data.rssi else "")
    )
    
    db.add(reading)
    
    # Update device last import time
    device.last_import_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(reading)
    
    # Check alerts
    alerts = check_alerts(device, temperature, data.gravity)
    
    logger.info(f"Received Tilt data from device {device_id}, created reading {reading.id}")
    if alerts:
        logger.warning(f"Alerts triggered for device {device_id}: {alerts}")
    
    return {
        "status": "success",
        "reading_id": reading.id,
        "alerts": alerts
    }


@router.post("/temperature-controllers/ispindel/webhook/{device_id}", tags=["temperature_controllers"])
async def receive_ispindel_data(
    device_id: int,
    data: ISpindelData,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Webhook endpoint to receive data from iSpindel.
    
    This endpoint receives telemetry data from iSpindel devices.
    The gravity value is calibrated using the device's calibration polynomial,
    then stored as a fermentation reading and checked against alert thresholds.
    """
    # Verify device exists and is an iSpindel
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if device.device_type.lower() != "ispindel":
        raise HTTPException(status_code=400, detail="Device is not an iSpindel")
    
    if not device.is_active:
        raise HTTPException(status_code=400, detail="Device is not active")
    
    if device.manual_override:
        logger.info(f"iSpindel device {device_id} has manual override enabled, skipping import")
        return {"status": "skipped", "reason": "manual_override"}
    
    if not device.batch_id:
        raise HTTPException(status_code=400, detail="Device is not associated with a batch")
    
    # Apply calibration to gravity reading
    calibrated_gravity = apply_calibration(data.gravity, data.angle, device.calibration_data)
    
    # Create fermentation reading
    reading = models.FermentationReadings(
        batch_id=device.batch_id,
        device_id=device_id,
        timestamp=datetime.now(timezone.utc),
        gravity=calibrated_gravity,
        temperature=data.temperature,
        source="ispindel",
        notes=f"iSpindel {data.name} (battery: {data.battery}V, angle: {data.angle}°)"
    )
    
    db.add(reading)
    
    # Update device last import time
    device.last_import_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(reading)
    
    # Check alerts
    alerts = check_alerts(device, data.temperature, calibrated_gravity)
    
    logger.info(f"Received iSpindel data from device {device_id}, created reading {reading.id}")
    if alerts:
        logger.warning(f"Alerts triggered for device {device_id}: {alerts}")
    
    return {
        "status": "success",
        "reading_id": reading.id,
        "calibrated_gravity": calibrated_gravity,
        "alerts": alerts
    }


@router.get("/temperature-controllers/alerts/{device_id}", tags=["temperature_controllers"])
async def get_device_alerts(device_id: int, db: Session = Depends(get_db)):
    """
    Get current alert status for a device.
    
    Returns the latest fermentation reading and checks if any alerts are triggered.
    """
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if not device.batch_id:
        return {"alerts": [], "message": "Device not associated with a batch"}
    
    # Get latest reading for the device
    latest_reading = (
        db.query(models.FermentationReadings)
        .filter(
            models.FermentationReadings.device_id == device_id,
            models.FermentationReadings.batch_id == device.batch_id
        )
        .order_by(models.FermentationReadings.timestamp.desc())
        .first()
    )
    
    if not latest_reading:
        return {"alerts": [], "message": "No readings found"}
    
    alerts = check_alerts(device, latest_reading.temperature, latest_reading.gravity)
    
    return {
        "device_id": device_id,
        "batch_id": device.batch_id,
        "latest_reading": {
            "timestamp": latest_reading.timestamp.isoformat(),
            "temperature": latest_reading.temperature,
            "gravity": latest_reading.gravity,
        },
        "alerts": alerts,
        "alert_config": device.alert_config
    }


@router.post("/temperature-controllers/manual-reading/{device_id}", tags=["temperature_controllers"])
async def create_manual_reading(
    device_id: int,
    reading: schemas.FermentationReadingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a manual fermentation reading for a device.
    
    This allows users to manually override automatic readings or add
    readings when a device is in manual override mode.
    """
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if not device.batch_id:
        raise HTTPException(status_code=400, detail="Device is not associated with a batch")
    
    # Create manual reading
    db_reading = models.FermentationReadings(
        batch_id=device.batch_id,
        device_id=device_id,
        timestamp=reading.timestamp,
        gravity=reading.gravity,
        temperature=reading.temperature,
        ph=reading.ph,
        notes=reading.notes or "Manual override reading",
        source="manual_override"
    )
    
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    
    logger.info(f"Manual reading created for device {device_id}, reading {db_reading.id}")
    
    return db_reading
