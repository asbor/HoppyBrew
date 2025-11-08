# api/endpoints/equipment_profiles.py

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List, Optional
from datetime import datetime

router = APIRouter()


@router.get("/equipment", response_model=List[dict])
async def get_equipment_profiles(db: Session = Depends(get_db)):
    """
    List all equipment profiles.
    """
    profiles = (
        db.query(models.EquipmentProfiles).order_by(models.EquipmentProfiles.name).all()
    )

    # Convert to dict to match frontend expectations
    result = []
    for profile in profiles:
        profile_dict = {
            "id": str(profile.id),
            "name": profile.name,
            "version": profile.version,
            "boil_size": profile.boil_size,
            "batch_size": profile.batch_size,
            "tun_volume": profile.tun_volume,
            "tun_weight": profile.tun_weight,
            "tun_specific_heat": profile.tun_specific_heat,
            "top_up_water": profile.top_up_water,
            "trub_chiller_loss": profile.trub_chiller_loss,
            "evap_rate": profile.evap_rate,
            "boil_time": profile.boil_time,
            "calc_boil_volume": profile.calc_boil_volume,
            "lauter_deadspace": profile.lauter_deadspace,
            "top_up_kettle": profile.top_up_kettle,
            "hop_utilization": profile.hop_utilization,
            "notes": profile.notes,
            "display_boil_size": profile.display_boil_size,
            "display_batch_size": profile.display_batch_size,
            "display_tun_volume": profile.display_tun_volume,
            "display_tun_weight": profile.display_tun_weight,
            "display_top_up_water": profile.display_top_up_water,
            "display_trub_chiller_loss": profile.display_trub_chiller_loss,
            "display_lauter_deadspace": profile.display_lauter_deadspace,
            "display_top_up_kettle": profile.display_top_up_kettle,
        }
        result.append(profile_dict)

    return result


@router.post("/equipment", response_model=dict, status_code=201)
async def create_equipment_profile(
    profile: schemas.EquipmentProfileBase, db: Session = Depends(get_db)
):
    """
    Create a new equipment profile.
    """
    # Check if profile with same name already exists
    existing = (
        db.query(models.EquipmentProfiles)
        .filter(models.EquipmentProfiles.name == profile.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Equipment profile with name '{profile.name}' already exists",
        )

    db_profile = models.EquipmentProfiles(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return {
        "id": str(db_profile.id),
        "name": db_profile.name,
        "version": db_profile.version,
        "boil_size": db_profile.boil_size,
        "batch_size": db_profile.batch_size,
        "tun_volume": db_profile.tun_volume,
        "tun_weight": db_profile.tun_weight,
        "tun_specific_heat": db_profile.tun_specific_heat,
        "top_up_water": db_profile.top_up_water,
        "trub_chiller_loss": db_profile.trub_chiller_loss,
        "evap_rate": db_profile.evap_rate,
        "boil_time": db_profile.boil_time,
        "calc_boil_volume": db_profile.calc_boil_volume,
        "lauter_deadspace": db_profile.lauter_deadspace,
        "top_up_kettle": db_profile.top_up_kettle,
        "hop_utilization": db_profile.hop_utilization,
        "notes": db_profile.notes,
        "display_boil_size": db_profile.display_boil_size,
        "display_batch_size": db_profile.display_batch_size,
        "display_tun_volume": db_profile.display_tun_volume,
        "display_tun_weight": db_profile.display_tun_weight,
        "display_top_up_water": db_profile.display_top_up_water,
        "display_trub_chiller_loss": db_profile.display_trub_chiller_loss,
        "display_lauter_deadspace": db_profile.display_lauter_deadspace,
        "display_top_up_kettle": db_profile.display_top_up_kettle,
    }


@router.get("/equipment/{profile_id}", response_model=dict)
async def get_equipment_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get a specific equipment profile by ID.
    """
    profile = (
        db.query(models.EquipmentProfiles)
        .filter(models.EquipmentProfiles.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Equipment profile not found")

    return {
        "id": str(profile.id),
        "name": profile.name,
        "version": profile.version,
        "boil_size": profile.boil_size,
        "batch_size": profile.batch_size,
        "tun_volume": profile.tun_volume,
        "tun_weight": profile.tun_weight,
        "tun_specific_heat": profile.tun_specific_heat,
        "top_up_water": profile.top_up_water,
        "trub_chiller_loss": profile.trub_chiller_loss,
        "evap_rate": profile.evap_rate,
        "boil_time": profile.boil_time,
        "calc_boil_volume": profile.calc_boil_volume,
        "lauter_deadspace": profile.lauter_deadspace,
        "top_up_kettle": profile.top_up_kettle,
        "hop_utilization": profile.hop_utilization,
        "notes": profile.notes,
        "display_boil_size": profile.display_boil_size,
        "display_batch_size": profile.display_batch_size,
        "display_tun_volume": profile.display_tun_volume,
        "display_tun_weight": profile.display_tun_weight,
        "display_top_up_water": profile.display_top_up_water,
        "display_trub_chiller_loss": profile.display_trub_chiller_loss,
        "display_lauter_deadspace": profile.display_lauter_deadspace,
        "display_top_up_kettle": profile.display_top_up_kettle,
    }


@router.put("/equipment/{profile_id}", response_model=dict)
async def update_equipment_profile(
    profile_id: int,
    profile_update: schemas.EquipmentProfileBase,
    db: Session = Depends(get_db),
):
    """
    Update an existing equipment profile.
    """
    profile = (
        db.query(models.EquipmentProfiles)
        .filter(models.EquipmentProfiles.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Equipment profile not found")

    # Check for name conflicts if name is being updated
    if profile_update.name and profile_update.name != profile.name:
        existing = (
            db.query(models.EquipmentProfiles)
            .filter(
                models.EquipmentProfiles.name == profile_update.name,
                models.EquipmentProfiles.id != profile_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Equipment profile with name '{profile_update.name}' already exists",
            )

    # Update only provided fields
    update_data = profile_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(profile, key):
            setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return {
        "id": str(profile.id),
        "name": profile.name,
        "version": profile.version,
        "boil_size": profile.boil_size,
        "batch_size": profile.batch_size,
        "tun_volume": profile.tun_volume,
        "tun_weight": profile.tun_weight,
        "tun_specific_heat": profile.tun_specific_heat,
        "top_up_water": profile.top_up_water,
        "trub_chiller_loss": profile.trub_chiller_loss,
        "evap_rate": profile.evap_rate,
        "boil_time": profile.boil_time,
        "calc_boil_volume": profile.calc_boil_volume,
        "lauter_deadspace": profile.lauter_deadspace,
        "top_up_kettle": profile.top_up_kettle,
        "hop_utilization": profile.hop_utilization,
        "notes": profile.notes,
        "display_boil_size": profile.display_boil_size,
        "display_batch_size": profile.display_batch_size,
        "display_tun_volume": profile.display_tun_volume,
        "display_tun_weight": profile.display_tun_weight,
        "display_top_up_water": profile.display_top_up_water,
        "display_trub_chiller_loss": profile.display_trub_chiller_loss,
        "display_lauter_deadspace": profile.display_lauter_deadspace,
        "display_top_up_kettle": profile.display_top_up_kettle,
    }


@router.delete("/equipment/{profile_id}", response_model=dict)
async def delete_equipment_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Delete an equipment profile.
    """
    profile = (
        db.query(models.EquipmentProfiles)
        .filter(models.EquipmentProfiles.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Equipment profile not found")

    db.delete(profile)
    db.commit()

    return {
        "id": str(profile.id),
        "name": profile.name,
        "message": "Equipment profile deleted successfully",
    }
