# api/endpoints/homeassistant.py

"""
HomeAssistant Integration Endpoints

This module provides REST API endpoints for HomeAssistant integration,
enabling monitoring of brewing batches through HomeAssistant's REST sensor platform.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
import Database.Models as models
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()


class HomeAssistantBatchSensor(BaseModel):
    """Batch sensor data formatted for HomeAssistant"""
    entity_id: str
    name: str
    state: str
    attributes: Dict[str, Any]
    unit_of_measurement: Optional[str] = None
    device_class: Optional[str] = None
    icon: str = "mdi:beer"


class HomeAssistantDiscoveryConfig(BaseModel):
    """HomeAssistant MQTT Discovery configuration"""
    name: str
    state_topic: str
    value_template: str
    unique_id: str
    device: Dict[str, Any]
    icon: str = "mdi:beer"


@router.get(
    "/homeassistant/batches",
    response_model=List[HomeAssistantBatchSensor],
    summary="Get all batches as HomeAssistant sensors",
    response_description="List of batches formatted for HomeAssistant REST sensors",
    tags=["homeassistant"],
)
async def get_batches_for_homeassistant(db: Session = Depends(get_db)):
    """
    Returns all active batches in a format optimized for HomeAssistant REST sensors.
    
    This endpoint can be used with HomeAssistant's RESTful sensor platform:
    
    ```yaml
    sensor:
      - platform: rest
        resource: http://your-hoppybrew-instance:8000/api/homeassistant/batches
        name: "HoppyBrew Batches"
        value_template: "{{ value_json | length }}"
        json_attributes_path: "$[0]"
        json_attributes:
          - name
          - state
          - attributes
    ```
    """
    batches = (
        db.query(models.Batches)
        .options(
            joinedload(models.Batches.recipe),
            joinedload(models.Batches.batch_log),
        )
        .all()
    )
    
    sensors = []
    for batch in batches:
        # Calculate batch age in days
        batch_age_days = (datetime.now() - batch.created_at).days
        
        # Determine batch state based on age and logs
        if batch_age_days < 1:
            state = "brewing"
        elif batch_age_days < 14:
            state = "fermenting"
        elif batch_age_days < 28:
            state = "conditioning"
        else:
            state = "ready"
        
        # Build attributes
        attributes = {
            "batch_id": batch.id,
            "batch_number": batch.batch_number,
            "batch_size": batch.batch_size,
            "batch_size_unit": "L",
            "brewer": batch.brewer,
            "brew_date": batch.brew_date.isoformat(),
            "created_at": batch.created_at.isoformat(),
            "updated_at": batch.updated_at.isoformat(),
            "age_days": batch_age_days,
            "recipe_id": batch.recipe_id,
            "recipe_name": batch.recipe.name if batch.recipe else "Unknown",
        }
        
        # Add latest log activity if available
        if batch.batch_log:
            attributes["last_activity"] = batch.batch_log.activity
            attributes["last_activity_time"] = batch.batch_log.timestamp.isoformat()
            attributes["notes"] = batch.batch_log.notes
        
        sensor = HomeAssistantBatchSensor(
            entity_id=f"sensor.hoppybrew_batch_{batch.id}",
            name=f"HoppyBrew - {batch.batch_name}",
            state=state,
            attributes=attributes,
            icon="mdi:beer" if state == "ready" else "mdi:flask",
        )
        sensors.append(sensor)
    
    return sensors


@router.get(
    "/homeassistant/batches/{batch_id}",
    response_model=HomeAssistantBatchSensor,
    summary="Get specific batch as HomeAssistant sensor",
    response_description="Single batch formatted for HomeAssistant",
    tags=["homeassistant"],
)
async def get_batch_for_homeassistant(
    batch_id: int, 
    db: Session = Depends(get_db)
):
    """
    Returns a specific batch in HomeAssistant sensor format.
    
    Useful for creating individual sensors per batch:
    
    ```yaml
    sensor:
      - platform: rest
        resource: http://your-hoppybrew-instance:8000/api/homeassistant/batches/1
        name: "Current Batch"
        value_template: "{{ value_json.state }}"
        json_attributes_path: "$.attributes"
        json_attributes:
          - batch_name
          - age_days
          - batch_size
    ```
    """
    batch = (
        db.query(models.Batches)
        .options(
            joinedload(models.Batches.recipe),
            joinedload(models.Batches.batch_log),
        )
        .filter(models.Batches.id == batch_id)
        .first()
    )
    
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    batch_age_days = (datetime.now() - batch.created_at).days
    
    if batch_age_days < 1:
        state = "brewing"
    elif batch_age_days < 14:
        state = "fermenting"
    elif batch_age_days < 28:
        state = "conditioning"
    else:
        state = "ready"
    
    attributes = {
        "batch_id": batch.id,
        "batch_number": batch.batch_number,
        "batch_name": batch.batch_name,
        "batch_size": batch.batch_size,
        "batch_size_unit": "L",
        "brewer": batch.brewer,
        "brew_date": batch.brew_date.isoformat(),
        "created_at": batch.created_at.isoformat(),
        "updated_at": batch.updated_at.isoformat(),
        "age_days": batch_age_days,
        "recipe_id": batch.recipe_id,
        "recipe_name": batch.recipe.name if batch.recipe else "Unknown",
    }
    
    if batch.batch_log:
        attributes["last_activity"] = batch.batch_log.activity
        attributes["last_activity_time"] = batch.batch_log.timestamp.isoformat()
        attributes["notes"] = batch.batch_log.notes
    
    return HomeAssistantBatchSensor(
        entity_id=f"sensor.hoppybrew_batch_{batch.id}",
        name=f"HoppyBrew - {batch.batch_name}",
        state=state,
        attributes=attributes,
        icon="mdi:beer" if state == "ready" else "mdi:flask",
    )


@router.get(
    "/homeassistant/summary",
    summary="Get brewery summary for HomeAssistant",
    response_description="Overall brewery status",
    tags=["homeassistant"],
)
async def get_brewery_summary(db: Session = Depends(get_db)):
    """
    Returns a summary of the brewery status for HomeAssistant dashboard.
    
    Example configuration:
    ```yaml
    sensor:
      - platform: rest
        resource: http://your-hoppybrew-instance:8000/api/homeassistant/summary
        name: "Brewery Status"
        value_template: "{{ value_json.active_batches }}"
        json_attributes:
          - total_batches
          - fermenting_batches
          - conditioning_batches
          - ready_batches
    ```
    """
    batches = db.query(models.Batches).all()
    
    total_batches = len(batches)
    brewing_count = 0
    fermenting_count = 0
    conditioning_count = 0
    ready_count = 0
    
    for batch in batches:
        batch_age_days = (datetime.now() - batch.created_at).days
        
        if batch_age_days < 1:
            brewing_count += 1
        elif batch_age_days < 14:
            fermenting_count += 1
        elif batch_age_days < 28:
            conditioning_count += 1
        else:
            ready_count += 1
    
    return {
        "active_batches": total_batches,
        "total_batches": total_batches,
        "brewing_batches": brewing_count,
        "fermenting_batches": fermenting_count,
        "conditioning_batches": conditioning_count,
        "ready_batches": ready_count,
        "state": "active" if total_batches > 0 else "idle",
        "icon": "mdi:brewery" if total_batches > 0 else "mdi:beer-outline",
    }


@router.get(
    "/homeassistant/discovery/batch/{batch_id}",
    summary="Get MQTT discovery configuration for a batch",
    response_description="MQTT discovery JSON for HomeAssistant",
    tags=["homeassistant"],
)
async def get_batch_mqtt_discovery(
    batch_id: int,
    db: Session = Depends(get_db)
):
    """
    Returns MQTT discovery configuration for automatic sensor setup.
    
    This endpoint generates the configuration that would be published to:
    `homeassistant/sensor/hoppybrew_batch_{batch_id}/config`
    
    For manual MQTT setup, publish this JSON to the topic above.
    """
    batch = (
        db.query(models.Batches)
        .filter(models.Batches.id == batch_id)
        .first()
    )
    
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    discovery_config = {
        "name": f"HoppyBrew Batch {batch.batch_name}",
        "state_topic": f"hoppybrew/batch/{batch_id}/state",
        "json_attributes_topic": f"hoppybrew/batch/{batch_id}/attributes",
        "unique_id": f"hoppybrew_batch_{batch_id}",
        "device": {
            "identifiers": [f"hoppybrew_batch_{batch_id}"],
            "name": f"HoppyBrew Batch {batch.batch_number}",
            "model": "HoppyBrew Batch",
            "manufacturer": "HoppyBrew",
            "sw_version": "1.0.0",
        },
        "icon": "mdi:beer",
        "device_class": None,
    }
    
    return discovery_config
