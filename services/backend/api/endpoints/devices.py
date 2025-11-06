# api/endpoints/devices.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List

router = APIRouter()


@router.get("/devices", response_model=List[schemas.Device])
async def get_all_devices(db: Session = Depends(get_db)):
    """
    Get all configured devices.
    
    Returns a list of all external devices configured in the system,
    including iSpindel, Tilt, and other brewing monitoring devices.
    """
    devices = db.query(models.Device).all()
    return devices


@router.get("/devices/{device_id}", response_model=schemas.Device)
async def get_device(device_id: int, db: Session = Depends(get_db)):
    """
    Get a specific device by ID.
    
    Returns detailed information about a specific device including
    its configuration and calibration data.
    """
    device = (
        db.query(models.Device)
        .filter(models.Device.id == device_id)
        .first()
    )
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("/devices", response_model=schemas.Device)
async def create_device(
    device: schemas.DeviceCreate, db: Session = Depends(get_db)
):
    """
    Create a new device configuration.
    
    Creates a new external device configuration in the system.
    Supports various device types including iSpindel and Tilt hydrometers.
    """
    # Create device
    db_device = models.Device(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


@router.put("/devices/{device_id}", response_model=schemas.Device)
async def update_device(
    device_id: int,
    device: schemas.DeviceUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing device configuration.
    
    Updates the configuration, calibration data, or other settings
    for an existing device. Only provided fields will be updated.
    """
    db_device = (
        db.query(models.Device)
        .filter(models.Device.id == device_id)
        .first()
    )
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Only update fields that were provided
    update_data = device.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_device, key, value)
    
    db.commit()
    db.refresh(db_device)
    return db_device


@router.delete("/devices/{device_id}", response_model=schemas.Device)
async def delete_device(device_id: int, db: Session = Depends(get_db)):
    """
    Delete a device configuration.
    
    Removes a device configuration from the system. This cannot be undone.
    """
    device = (
        db.query(models.Device)
        .filter(models.Device.id == device_id)
        .first()
    )
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db.delete(device)
    db.commit()
    return device
