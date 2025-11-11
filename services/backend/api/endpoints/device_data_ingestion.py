# api/endpoints/device_data_ingestion.py

from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import Optional, Dict, Any
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/devices/ispindel/data")
async def receive_ispindel_data(
    data: Dict[str, Any],
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """
    Receive data from iSpindel device.
    
    iSpindel sends data in the following format:
    {
        "name": "iSpindel000",
        "ID": 1234567,
        "angle": 45.2,
        "temperature": 20.5,
        "temp_units": "C",
        "battery": 3.8,
        "gravity": 1.048,
        "interval": 900,
        "RSSI": -75
    }
    """
    try:
        # Find device by name or API key
        device_name = data.get("name")
        device = None
        
        if x_api_key:
            device = db.query(models.Device).filter(
                models.Device.api_token == x_api_key,
                models.Device.device_type == "ispindel"
            ).first()
        
        if not device and device_name:
            device = db.query(models.Device).filter(
                models.Device.name == device_name,
                models.Device.device_type == "ispindel"
            ).first()
        
        if not device:
            raise HTTPException(
                status_code=404,
                detail="Device not found. Please configure device in HoppyBrew first."
            )
        
        if not device.is_active:
            raise HTTPException(
                status_code=403,
                detail="Device is not active"
            )
        
        if not device.batch_id:
            logger.warning(f"Device {device.name} received data but no batch is assigned")
            return {"status": "received", "message": "No batch assigned to device"}
        
        # Extract data
        temperature = data.get("temperature")
        gravity = data.get("gravity")
        
        # Create fermentation reading
        reading = models.FermentationReadings(
            batch_id=device.batch_id,
            device_id=device.id,
            timestamp=datetime.now(),
            gravity=gravity,
            temperature=temperature,
            source="ispindel",
            notes=f"iSpindel auto-import. Battery: {data.get('battery', 'N/A')}V, Angle: {data.get('angle', 'N/A')}°"
        )
        
        db.add(reading)
        
        # Update device last reading timestamp
        device.last_reading_at = datetime.now()
        
        db.commit()
        db.refresh(reading)
        
        # Check alerts
        alerts = check_temperature_alerts(device, temperature)
        
        return {
            "status": "success",
            "reading_id": reading.id,
            "batch_id": device.batch_id,
            "alerts": alerts
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing iSpindel data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")


@router.post("/devices/tilt/data")
async def receive_tilt_data(
    data: Dict[str, Any],
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """
    Receive data from Tilt Hydrometer (via Tilt Pi or cloud).
    
    Tilt data format:
    {
        "Color": "Red",
        "Temp": 68,
        "SG": 1.048,
        "Timepoint": "2024-03-21T14:30:00Z",
        "Comment": "",
        "Beer": "My IPA"
    }
    """
    try:
        # Find device by color/name or API key
        device_color = data.get("Color", "").lower()
        device = None
        
        if x_api_key:
            device = db.query(models.Device).filter(
                models.Device.api_token == x_api_key,
                models.Device.device_type == "tilt"
            ).first()
        
        if not device and device_color:
            # Try to find by name containing color
            device = db.query(models.Device).filter(
                models.Device.name.ilike(f"%{device_color}%"),
                models.Device.device_type == "tilt"
            ).first()
        
        if not device:
            raise HTTPException(
                status_code=404,
                detail="Tilt device not found. Please configure device in HoppyBrew first."
            )
        
        if not device.is_active:
            raise HTTPException(
                status_code=403,
                detail="Device is not active"
            )
        
        if not device.batch_id:
            logger.warning(f"Tilt device {device.name} received data but no batch is assigned")
            return {"status": "received", "message": "No batch assigned to device"}
        
        # Extract data
        # Tilt reports in Fahrenheit by default
        temperature_f = data.get("Temp")
        temperature_c = (temperature_f - 32) * 5/9 if temperature_f else None
        gravity = data.get("SG")
        
        # Parse timestamp if provided
        timestamp_str = data.get("Timepoint")
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")) if timestamp_str else datetime.now()
        
        # Create fermentation reading
        reading = models.FermentationReadings(
            batch_id=device.batch_id,
            device_id=device.id,
            timestamp=timestamp,
            gravity=gravity,
            temperature=temperature_c,
            source="tilt",
            notes=f"Tilt {data.get('Color', 'Unknown')} auto-import. {data.get('Comment', '')}"
        )
        
        db.add(reading)
        
        # Update device last reading timestamp
        device.last_reading_at = datetime.now()
        
        db.commit()
        db.refresh(reading)
        
        # Check alerts
        alerts = check_temperature_alerts(device, temperature_c)
        
        return {
            "status": "success",
            "reading_id": reading.id,
            "batch_id": device.batch_id,
            "alerts": alerts
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing Tilt data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")


@router.post("/devices/{device_id}/batch/{batch_id}/associate")
async def associate_device_with_batch(
    device_id: int,
    batch_id: int,
    db: Session = Depends(get_db),
):
    """
    Associate a device with a batch for automatic data collection.
    """
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    device.batch_id = batch_id
    db.commit()
    db.refresh(device)
    
    return {
        "status": "success",
        "message": f"Device {device.name} associated with batch {batch.batch_name}"
    }


@router.delete("/devices/{device_id}/batch")
async def dissociate_device_from_batch(
    device_id: int,
    db: Session = Depends(get_db),
):
    """
    Remove batch association from device (manual override).
    """
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device.batch_id = None
    db.commit()
    db.refresh(device)
    
    return {
        "status": "success",
        "message": f"Device {device.name} dissociated from batch"
    }


def check_temperature_alerts(device: models.Device, temperature: Optional[float]) -> list:
    """
    Check if temperature is outside configured alert thresholds.
    
    Returns list of alert messages.
    """
    alerts = []
    
    if not device.alert_config or not temperature:
        return alerts
    
    config = device.alert_config
    if not config.get("enable_alerts", False):
        return alerts
    
    temp_min = config.get("temperature_min")
    temp_max = config.get("temperature_max")
    
    if temp_min and temperature < temp_min:
        alerts.append({
            "type": "temperature_low",
            "message": f"Temperature {temperature:.1f}°C is below minimum {temp_min}°C",
            "severity": "warning"
        })
    
    if temp_max and temperature > temp_max:
        alerts.append({
            "type": "temperature_high",
            "message": f"Temperature {temperature:.1f}°C is above maximum {temp_max}°C",
            "severity": "warning"
        })
    
    return alerts
