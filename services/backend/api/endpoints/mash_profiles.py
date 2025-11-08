# api/endpoints/mash_profiles.py

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List, Optional
from datetime import datetime

router = APIRouter()


@router.get("/mash", response_model=List[dict])
async def get_mash_profiles(db: Session = Depends(get_db)):
    """
    List all mash profiles.
    """
    profiles = db.query(models.MashProfiles).order_by(models.MashProfiles.name).all()

    # Convert to dict to match frontend expectations
    result = []
    for profile in profiles:
        profile_dict = {
            "id": str(profile.id),
            "name": profile.name,
            "version": profile.version,
            "grain_temp": profile.grain_temp,
            "tun_temp": profile.tun_temp,
            "sparge_temp": profile.sparge_temp,
            "ph": profile.ph,
            "tun_weight": profile.tun_weight,
            "tun_specific_heat": profile.tun_specific_heat,
            "notes": profile.notes,
            "display_grain_temp": profile.display_grain_temp,
            "display_tun_temp": profile.display_tun_temp,
            "display_sparge_temp": profile.display_sparge_temp,
            "display_tun_weight": profile.display_tun_weight,
        }
        result.append(profile_dict)

    return result


@router.post("/mash", response_model=dict, status_code=201)
async def create_mash_profile(
    profile: schemas.MashProfileBase, db: Session = Depends(get_db)
):
    """
    Create a new mash profile.
    """
    # Check if profile with same name already exists
    existing = (
        db.query(models.MashProfiles)
        .filter(models.MashProfiles.name == profile.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Mash profile with name '{profile.name}' already exists",
        )

    db_profile = models.MashProfiles(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return {
        "id": str(db_profile.id),
        "name": db_profile.name,
        "version": db_profile.version,
        "grain_temp": db_profile.grain_temp,
        "tun_temp": db_profile.tun_temp,
        "sparge_temp": db_profile.sparge_temp,
        "ph": db_profile.ph,
        "tun_weight": db_profile.tun_weight,
        "tun_specific_heat": db_profile.tun_specific_heat,
        "notes": db_profile.notes,
        "display_grain_temp": db_profile.display_grain_temp,
        "display_tun_temp": db_profile.display_tun_temp,
        "display_sparge_temp": db_profile.display_sparge_temp,
        "display_tun_weight": db_profile.display_tun_weight,
    }


@router.get("/mash/{profile_id}", response_model=dict)
async def get_mash_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get a specific mash profile by ID.
    """
    profile = (
        db.query(models.MashProfiles)
        .filter(models.MashProfiles.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Mash profile not found")

    return {
        "id": str(profile.id),
        "name": profile.name,
        "version": profile.version,
        "grain_temp": profile.grain_temp,
        "tun_temp": profile.tun_temp,
        "sparge_temp": profile.sparge_temp,
        "ph": profile.ph,
        "tun_weight": profile.tun_weight,
        "tun_specific_heat": profile.tun_specific_heat,
        "notes": profile.notes,
        "display_grain_temp": profile.display_grain_temp,
        "display_tun_temp": profile.display_tun_temp,
        "display_sparge_temp": profile.display_sparge_temp,
        "display_tun_weight": profile.display_tun_weight,
    }


@router.put("/mash/{profile_id}", response_model=dict)
async def update_mash_profile(
    profile_id: int,
    profile_update: schemas.MashProfileBase,
    db: Session = Depends(get_db),
):
    """
    Update an existing mash profile.
    """
    profile = (
        db.query(models.MashProfiles)
        .filter(models.MashProfiles.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Mash profile not found")

    # Check for name conflicts if name is being updated
    if profile_update.name and profile_update.name != profile.name:
        existing = (
            db.query(models.MashProfiles)
            .filter(
                models.MashProfiles.name == profile_update.name,
                models.MashProfiles.id != profile_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Mash profile with name '{profile_update.name}' already exists",
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
        "grain_temp": profile.grain_temp,
        "tun_temp": profile.tun_temp,
        "sparge_temp": profile.sparge_temp,
        "ph": profile.ph,
        "tun_weight": profile.tun_weight,
        "tun_specific_heat": profile.tun_specific_heat,
        "notes": profile.notes,
        "display_grain_temp": profile.display_grain_temp,
        "display_tun_temp": profile.display_tun_temp,
        "display_sparge_temp": profile.display_sparge_temp,
        "display_tun_weight": profile.display_tun_weight,
    }


@router.delete("/mash/{profile_id}", response_model=dict)
async def delete_mash_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Delete a mash profile.
    """
    profile = (
        db.query(models.MashProfiles)
        .filter(models.MashProfiles.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Mash profile not found")

    db.delete(profile)
    db.commit()

    return {
        "id": str(profile.id),
        "name": profile.name,
        "message": "Mash profile deleted successfully",
    }


# Mash Steps endpoints


@router.get("/mash/{profile_id}/steps", response_model=List[dict])
async def get_mash_steps(profile_id: int, db: Session = Depends(get_db)):
    """
    Get all mash steps for a specific mash profile.
    """
    # First verify the profile exists
    profile = (
        db.query(models.MashProfiles)
        .filter(models.MashProfiles.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Mash profile not found")

    steps = (
        db.query(models.MashStep)
        .filter(models.MashStep.mash_id == profile_id)
        .order_by(models.MashStep.id)
        .all()
    )

    result = []
    for step in steps:
        step_dict = {
            "id": step.id,
            "name": step.name,
            "version": step.version,
            "type": step.type,
            "infuse_amount": step.infuse_amount,
            "step_time": step.step_time,
            "step_temp": step.step_temp,
            "ramp_time": step.ramp_time,
            "end_temp": step.end_temp,
            "description": step.description,
            "water_grain_ratio": step.water_grain_ratio,
            "decoction_amt": step.decoction_amt,
            "infuse_temp": step.infuse_temp,
            "display_step_temp": step.display_step_temp,
            "display_infuse_amt": step.display_infuse_amt,
            "mash_id": step.mash_id,
        }
        result.append(step_dict)

    return result


@router.post("/mash/{profile_id}/steps", response_model=dict, status_code=201)
async def create_mash_step(
    profile_id: int, step: schemas.MashStepBase, db: Session = Depends(get_db)
):
    """
    Add a new step to a mash profile.
    """
    # First verify the profile exists
    profile = (
        db.query(models.MashProfiles)
        .filter(models.MashProfiles.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Mash profile not found")

    # Set the mash_id for the step
    step_data = step.model_dump()
    step_data["mash_id"] = profile_id

    db_step = models.MashStep(**step_data)
    db.add(db_step)
    db.commit()
    db.refresh(db_step)

    return {
        "id": db_step.id,
        "name": db_step.name,
        "version": db_step.version,
        "type": db_step.type,
        "infuse_amount": db_step.infuse_amount,
        "step_time": db_step.step_time,
        "step_temp": db_step.step_temp,
        "ramp_time": db_step.ramp_time,
        "end_temp": db_step.end_temp,
        "description": db_step.description,
        "water_grain_ratio": db_step.water_grain_ratio,
        "decoction_amt": db_step.decoction_amt,
        "infuse_temp": db_step.infuse_temp,
        "display_step_temp": db_step.display_step_temp,
        "display_infuse_amt": db_step.display_infuse_amt,
        "mash_id": db_step.mash_id,
    }


@router.put("/mash/steps/{step_id}", response_model=dict)
async def update_mash_step(
    step_id: int, step_update: schemas.MashStepBase, db: Session = Depends(get_db)
):
    """
    Update an existing mash step.
    """
    step = db.query(models.MashStep).filter(models.MashStep.id == step_id).first()

    if not step:
        raise HTTPException(status_code=404, detail="Mash step not found")

    # Update only provided fields
    update_data = step_update.model_dump(exclude_unset=True, exclude={"mash_id"})
    for key, value in update_data.items():
        if hasattr(step, key):
            setattr(step, key, value)

    db.commit()
    db.refresh(step)

    return {
        "id": step.id,
        "name": step.name,
        "version": step.version,
        "type": step.type,
        "infuse_amount": step.infuse_amount,
        "step_time": step.step_time,
        "step_temp": step.step_temp,
        "ramp_time": step.ramp_time,
        "end_temp": step.end_temp,
        "description": step.description,
        "water_grain_ratio": step.water_grain_ratio,
        "decoction_amt": step.decoction_amt,
        "infuse_temp": step.infuse_temp,
        "display_step_temp": step.display_step_temp,
        "display_infuse_amt": step.display_infuse_amt,
        "mash_id": step.mash_id,
    }


@router.delete("/mash/steps/{step_id}", response_model=dict)
async def delete_mash_step(step_id: int, db: Session = Depends(get_db)):
    """
    Delete a mash step.
    """
    step = db.query(models.MashStep).filter(models.MashStep.id == step_id).first()

    if not step:
        raise HTTPException(status_code=404, detail="Mash step not found")

    db.delete(step)
    db.commit()

    return {
        "id": step.id,
        "name": step.name,
        "message": "Mash step deleted successfully",
    }
