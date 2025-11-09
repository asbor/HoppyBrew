# api/endpoints/equipment_profiles.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List

router = APIRouter()


def profile_to_dict(profile: models.EquipmentProfiles) -> dict:
    """Convert equipment profile model to dictionary."""
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
        "brewhouse_efficiency": profile.brewhouse_efficiency,
        "mash_efficiency": profile.mash_efficiency,
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


@router.get("/equipment", response_model=List[dict])
async def get_equipment_profiles(db: Session = Depends(get_db)):
    """
    List all equipment profiles.
    """
    profiles = (
        db.query(models.EquipmentProfiles).order_by(
            models.EquipmentProfiles.name).all()
    )

    # Convert to dict to match frontend expectations
    result = [profile_to_dict(profile) for profile in profiles]

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

    return profile_to_dict(db_profile)


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
        raise HTTPException(
            status_code=404, detail="Equipment profile not found")

    return profile_to_dict(profile)


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
        raise HTTPException(
            status_code=404, detail="Equipment profile not found")

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

    return profile_to_dict(profile)


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
        raise HTTPException(
            status_code=404, detail="Equipment profile not found")

    db.delete(profile)
    db.commit()

    return {
        "id": str(profile.id),
        "name": profile.name,
        "message": "Equipment profile deleted successfully",
    }
