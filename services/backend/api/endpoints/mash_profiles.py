# api/endpoints/mash_profiles.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List, Dict, Any

router = APIRouter()

# Mash profile templates with common brewing profiles
MASH_TEMPLATES = [
    {
        "id": "single_infusion",
        "name": "Single Infusion - Medium Body",
        "description": "Standard single infusion mash for most ales. Targets medium body with good fermentability.",
        "grain_temp": 20,
        "tun_temp": 20,
        "sparge_temp": 76,
        "ph": 5.4,
        "notes": "Most common mash profile for ales. Simple and effective.",
        "steps": [
            {
                "name": "Saccharification Rest",
                "type": "Infusion",
                "step_temp": 66,
                "step_time": 60,
                "ramp_time": 2,
                "description": "Main conversion step at 66°C for balanced body and fermentability"
            },
            {
                "name": "Mash Out",
                "type": "Temperature",
                "step_temp": 76,
                "step_time": 10,
                "ramp_time": 5,
                "description": "Raise to 76°C to stop enzymatic activity and improve lautering"
            }
        ]
    },
    {
        "id": "step_mash",
        "name": "Step Mash - Full Body",
        "description": "Multi-step mash for fuller body beers like stouts and porters.",
        "grain_temp": 20,
        "tun_temp": 20,
        "sparge_temp": 76,
        "ph": 5.4,
        "notes": "Protein rest and higher saccharification temperature for fuller body.",
        "steps": [
            {
                "name": "Protein Rest",
                "type": "Infusion",
                "step_temp": 55,
                "step_time": 15,
                "ramp_time": 2,
                "description": "Protein rest at 55°C to improve head retention"
            },
            {
                "name": "Saccharification Rest",
                "type": "Temperature",
                "step_temp": 68,
                "step_time": 60,
                "ramp_time": 10,
                "description": "Higher temperature rest at 68°C for fuller body"
            },
            {
                "name": "Mash Out",
                "type": "Temperature",
                "step_temp": 76,
                "step_time": 10,
                "ramp_time": 5,
                "description": "Mash out at 76°C"
            }
        ]
    },
    {
        "id": "hochkurz",
        "name": "Hochkurz - Dry/Crisp",
        "description": "German hochkurz (high-short) mash for highly fermentable, dry beers.",
        "grain_temp": 20,
        "tun_temp": 20,
        "sparge_temp": 76,
        "ph": 5.4,
        "notes": "High temperature short mash for German lagers and pilsners. Creates dry, crisp beer.",
        "steps": [
            {
                "name": "Beta Glucan Rest",
                "type": "Infusion",
                "step_temp": 45,
                "step_time": 20,
                "ramp_time": 2,
                "description": "Beta glucan rest at 45°C for better lautering"
            },
            {
                "name": "High Temperature Rest",
                "type": "Temperature",
                "step_temp": 72,
                "step_time": 30,
                "ramp_time": 15,
                "description": "Short high-temperature rest at 72°C for quick conversion"
            },
            {
                "name": "Mash Out",
                "type": "Temperature",
                "step_temp": 76,
                "step_time": 10,
                "ramp_time": 5,
                "description": "Mash out at 76°C"
            }
        ]
    },
    {
        "id": "decoction",
        "name": "Traditional Decoction",
        "description": "Traditional three-decoction mash for authentic German lagers.",
        "grain_temp": 20,
        "tun_temp": 20,
        "sparge_temp": 76,
        "ph": 5.4,
        "notes": "Traditional decoction mash. Labor intensive but creates unique malt character.",
        "steps": [
            {
                "name": "Acid Rest",
                "type": "Infusion",
                "step_temp": 40,
                "step_time": 20,
                "ramp_time": 2,
                "description": "Acid rest at 40°C"
            },
            {
                "name": "Protein Rest",
                "type": "Decoction",
                "step_temp": 55,
                "step_time": 30,
                "ramp_time": 15,
                "decoction_amt": "30%",
                "description": "First decoction - protein rest at 55°C"
            },
            {
                "name": "Saccharification Rest 1",
                "type": "Decoction",
                "step_temp": 63,
                "step_time": 30,
                "ramp_time": 10,
                "decoction_amt": "30%",
                "description": "Second decoction - beta amylase rest at 63°C"
            },
            {
                "name": "Saccharification Rest 2",
                "type": "Decoction",
                "step_temp": 72,
                "step_time": 20,
                "ramp_time": 10,
                "decoction_amt": "30%",
                "description": "Third decoction - alpha amylase rest at 72°C"
            },
            {
                "name": "Mash Out",
                "type": "Temperature",
                "step_temp": 76,
                "step_time": 10,
                "ramp_time": 5,
                "description": "Mash out at 76°C"
            }
        ]
    },
    {
        "id": "light_lager",
        "name": "Light Lager - Highly Attenuative",
        "description": "Optimized for light lagers with high attenuation and crisp finish.",
        "grain_temp": 20,
        "tun_temp": 20,
        "sparge_temp": 76,
        "ph": 5.4,
        "notes": "Designed for light, crisp lagers with high fermentability.",
        "steps": [
            {
                "name": "Beta Amylase Rest",
                "type": "Infusion",
                "step_temp": 63,
                "step_time": 45,
                "ramp_time": 2,
                "description": "Extended beta amylase rest at 63°C for high fermentability"
            },
            {
                "name": "Alpha Amylase Rest",
                "type": "Temperature",
                "step_temp": 70,
                "step_time": 30,
                "ramp_time": 5,
                "description": "Brief alpha amylase rest at 70°C"
            },
            {
                "name": "Mash Out",
                "type": "Temperature",
                "step_temp": 76,
                "step_time": 10,
                "ramp_time": 5,
                "description": "Mash out at 76°C"
            }
        ]
    }
]


# ============================================================================
# TEMPLATE ROUTES - Must come BEFORE parameterized routes like /mash/{profile_id}
# ============================================================================

@router.get("/mash/templates", response_model=List[Dict[str, Any]])
async def get_mash_templates():
    """
    Get all available mash profile templates.
    Returns pre-configured mash profiles with common brewing schedules.
    """
    return MASH_TEMPLATES


@router.post("/mash/from-template/{template_id}", response_model=dict, status_code=201)
async def create_mash_from_template(
    template_id: str, custom_name: str = None, db: Session = Depends(get_db)
):
    """
    Create a new mash profile from a template.

    Args:
        template_id: ID of the template to use
        custom_name: Optional custom name for the profile (defaults to template name)
    """
    # Find the template
    template = next(
        (t for t in MASH_TEMPLATES if t["id"] == template_id), None)

    if not template:
        raise HTTPException(
            status_code=404, detail=f"Template '{template_id}' not found")

    # Use custom name or template name
    profile_name = custom_name if custom_name else template["name"]

    # Check if profile with same name already exists
    existing = (
        db.query(models.MashProfiles)
        .filter(models.MashProfiles.name == profile_name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Mash profile with name '{profile_name}' already exists",
        )

    # Create the mash profile
    profile_data = {
        "name": profile_name,
        "version": 1,
        "grain_temp": template["grain_temp"],
        "tun_temp": template["tun_temp"],
        "sparge_temp": template["sparge_temp"],
        "ph": template["ph"],
        "notes": template.get("notes", "") + f" (Created from template: {template['name']})",
        "display_grain_temp": f"{template['grain_temp']} °C",
        "display_tun_temp": f"{template['tun_temp']} °C",
        "display_sparge_temp": f"{template['sparge_temp']} °C",
    }

    db_profile = models.MashProfiles(**profile_data)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    # Create mash steps from template
    for step_data in template.get("steps", []):
        step = models.MashStep(
            name=step_data["name"],
            type=step_data["type"],
            step_temp=step_data["step_temp"],
            step_time=step_data["step_time"],
            ramp_time=step_data.get("ramp_time", 0),
            description=step_data.get("description", ""),
            display_step_temp=f"{step_data['step_temp']} °C",
            display_step_time=f"{step_data['step_time']} min",
            display_ramp_time=f"{step_data.get('ramp_time', 0)} min",
            mash_profile_id=db_profile.id,
        )
        db.add(step)

    db.commit()

    return {
        "id": str(db_profile.id),
        "name": db_profile.name,
        "message": f"Mash profile created from template: {template['name']}",
    }


# ============================================================================
# MASH PROFILE CRUD ROUTES
# ============================================================================

@router.get("/mash", response_model=List[dict])
async def get_mash_profiles(db: Session = Depends(get_db)):
    """
    List all mash profiles.
    """
    profiles = db.query(models.MashProfiles).order_by(
        models.MashProfiles.name).all()

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
    step = db.query(models.MashStep).filter(
        models.MashStep.id == step_id).first()

    if not step:
        raise HTTPException(status_code=404, detail="Mash step not found")

    # Update only provided fields
    update_data = step_update.model_dump(
        exclude_unset=True, exclude={"mash_id"})
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
    step = db.query(models.MashStep).filter(
        models.MashStep.id == step_id).first()

    if not step:
        raise HTTPException(status_code=404, detail="Mash step not found")

    db.delete(step)
    db.commit()

    return {
        "id": step.id,
        "name": step.name,
        "message": "Mash step deleted successfully",
    }
