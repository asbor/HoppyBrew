# api/endpoints/water_profiles.py

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List, Optional
from datetime import datetime, timezone

router = APIRouter()


@router.get("/water-profiles", response_model=List[schemas.WaterProfile])
async def get_water_profiles(
    profile_type: Optional[str] = Query(None, pattern="^(source|target)$"),
    style_category: Optional[str] = None,
    is_default: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    List all water profiles with optional filtering.

    - **profile_type**: Filter by 'source' or 'target' profile type
    - **style_category**: Filter by beer style category
    - **is_default**: Filter by default profiles (True) or custom profiles (False)
    """
    query = db.query(models.WaterProfiles)

    if profile_type:
        query = query.filter(models.WaterProfiles.profile_type == profile_type)

    if style_category:
        query = query.filter(models.WaterProfiles.style_category == style_category)

    if is_default is not None:
        query = query.filter(models.WaterProfiles.is_default == is_default)

    profiles = query.order_by(models.WaterProfiles.name).all()
    return profiles


@router.post("/water-profiles", response_model=schemas.WaterProfile, status_code=201)
async def create_water_profile(
    profile: schemas.WaterProfileCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new water profile.

    - **name**: Unique name for the water profile
    - **profile_type**: Either 'source' (starting water) or 'target' (desired brewing water)
    - **calcium**, **magnesium**, **sodium**, **chloride**, **sulfate**, **bicarbonate**: Ion concentrations in ppm
    """
    # Check if profile with same name and type already exists
    existing = db.query(models.WaterProfiles).filter(
        models.WaterProfiles.name == profile.name,
        models.WaterProfiles.profile_type == profile.profile_type
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Water profile with name '{profile.name}' and type '{profile.profile_type}' already exists"
        )

    db_profile = models.WaterProfiles(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.get("/water-profiles/{profile_id}", response_model=schemas.WaterProfile)
async def get_water_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific water profile by ID.
    """
    profile = db.query(models.WaterProfiles).filter(
        models.WaterProfiles.id == profile_id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Water profile not found")

    return profile


@router.put("/water-profiles/{profile_id}", response_model=schemas.WaterProfile)
async def update_water_profile(
    profile_id: int,
    profile_update: schemas.WaterProfileUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing water profile.

    Only custom profiles can be updated. Default profiles are read-only.
    """
    profile = db.query(models.WaterProfiles).filter(
        models.WaterProfiles.id == profile_id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Water profile not found")

    if profile.is_default:
        raise HTTPException(
            status_code=403,
            detail="Cannot update default profiles. Duplicate the profile to make changes."
        )

    # Update only provided fields
    update_data = profile_update.model_dump(exclude_unset=True)

    # Check for name conflicts if name is being updated
    if 'name' in update_data and update_data['name'] != profile.name:
        existing = db.query(models.WaterProfiles).filter(
            models.WaterProfiles.name == update_data['name'],
            models.WaterProfiles.profile_type == profile.profile_type,
            models.WaterProfiles.id != profile_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Water profile with name '{update_data['name']}' already exists"
            )

    for key, value in update_data.items():
        setattr(profile, key, value)

    profile.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(profile)
    return profile


@router.delete("/water-profiles/{profile_id}", response_model=schemas.WaterProfile)
async def delete_water_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a water profile.

    Only custom profiles can be deleted. Default profiles are protected.
    """
    profile = db.query(models.WaterProfiles).filter(
        models.WaterProfiles.id == profile_id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Water profile not found")

    if profile.is_default:
        raise HTTPException(
            status_code=403,
            detail="Cannot delete default profiles"
        )

    db.delete(profile)
    db.commit()
    return profile


@router.post("/water-profiles/{profile_id}/duplicate", response_model=schemas.WaterProfile, status_code=201)
async def duplicate_water_profile(
    profile_id: int,
    new_name: Optional[str] = Query(None, description="Name for the duplicated profile"),
    db: Session = Depends(get_db)
):
    """
    Duplicate an existing water profile.

    This is useful for creating custom variants of default profiles.
    """
    original = db.query(models.WaterProfiles).filter(
        models.WaterProfiles.id == profile_id
    ).first()

    if not original:
        raise HTTPException(status_code=404, detail="Water profile not found")

    # Generate a name for the duplicate
    duplicate_name = new_name or f"{original.name} (Copy)"

    # Check if name already exists
    counter = 1
    final_name = duplicate_name
    while db.query(models.WaterProfiles).filter(
        models.WaterProfiles.name == final_name,
        models.WaterProfiles.profile_type == original.profile_type
    ).first():
        final_name = f"{duplicate_name} {counter}"
        counter += 1

    # Create duplicate with all properties except id, timestamps, and metadata
    duplicate_data = {
        "name": final_name,
        "description": original.description,
        "profile_type": original.profile_type,
        "style_category": original.style_category,
        "calcium": original.calcium,
        "magnesium": original.magnesium,
        "sodium": original.sodium,
        "chloride": original.chloride,
        "sulfate": original.sulfate,
        "bicarbonate": original.bicarbonate,
        "ph": original.ph,
        "total_alkalinity": original.total_alkalinity,
        "residual_alkalinity": original.residual_alkalinity,
        "version": original.version,
        "amount": original.amount,
        "notes": original.notes,
        "display_amount": original.display_amount,
        "inventory": original.inventory,
        "is_default": False,
        "is_custom": True,
    }

    duplicate = models.WaterProfiles(**duplicate_data)
    db.add(duplicate)
    db.commit()
    db.refresh(duplicate)
    return duplicate
