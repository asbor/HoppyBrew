from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List, Annotated
from database import get_db
import Database.Models as models
import Database.Schemas.fermentation_profiles as schemas

db_dependency = Annotated[Session, Depends(get_db)]
router = APIRouter()


def _with_steps(query):
    """Apply joinedload to include steps in the query."""
    return query.options(joinedload(models.FermentationProfiles.steps))


@router.get(
    "/fermentation-profiles",
    response_model=List[schemas.FermentationProfile],
    summary="List all fermentation profiles",
    response_description="A collection of fermentation profiles defined in the system.",
)
async def get_all_fermentation_profiles(
    db: db_dependency,
) -> List[schemas.FermentationProfile]:
    """Return all fermentation profiles with their steps."""
    profiles = _with_steps(db.query(models.FermentationProfiles)).all()
    return profiles


@router.get(
    "/fermentation-profiles/{profile_id}",
    response_model=schemas.FermentationProfile,
    summary="Get a specific fermentation profile",
    response_description="The fermentation profile with all its steps.",
)
async def get_fermentation_profile(
    profile_id: int, db: db_dependency
) -> schemas.FermentationProfile:
    """Return a specific fermentation profile by ID."""
    profile = (
        _with_steps(db.query(models.FermentationProfiles))
        .filter(models.FermentationProfiles.id == profile_id)
        .first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Fermentation profile not found")
    return profile


@router.post(
    "/fermentation-profiles",
    response_model=schemas.FermentationProfile,
    status_code=201,
    summary="Create a new fermentation profile",
    response_description="The newly created fermentation profile with its steps.",
)
async def create_fermentation_profile(
    profile: schemas.FermentationProfileCreate, db: db_dependency
) -> schemas.FermentationProfile:
    """Create a new fermentation profile with optional steps."""
    # Create the profile
    db_profile = models.FermentationProfiles(
        name=profile.name,
        description=profile.description,
        is_pressurized=profile.is_pressurized,
        is_template=profile.is_template,
    )
    db.add(db_profile)
    db.flush()  # Get the profile ID before adding steps

    # Create the steps if provided
    if profile.steps:
        for step_data in profile.steps:
            db_step = models.FermentationSteps(
                fermentation_profile_id=db_profile.id,
                step_order=step_data.step_order,
                name=step_data.name,
                step_type=step_data.step_type,
                temperature=step_data.temperature,
                duration_days=step_data.duration_days,
                ramp_days=step_data.ramp_days,
                pressure_psi=step_data.pressure_psi,
                notes=step_data.notes,
            )
            db.add(db_step)

    db.commit()
    db.refresh(db_profile)

    # Fetch with relationships loaded
    result = (
        _with_steps(db.query(models.FermentationProfiles))
        .filter(models.FermentationProfiles.id == db_profile.id)
        .first()
    )
    return result


@router.put(
    "/fermentation-profiles/{profile_id}",
    response_model=schemas.FermentationProfile,
    summary="Update a fermentation profile",
    response_description="The updated fermentation profile.",
)
async def update_fermentation_profile(
    profile_id: int, profile: schemas.FermentationProfileUpdate, db: db_dependency
) -> schemas.FermentationProfile:
    """Update an existing fermentation profile."""
    db_profile = (
        db.query(models.FermentationProfiles)
        .filter(models.FermentationProfiles.id == profile_id)
        .first()
    )

    if not db_profile:
        raise HTTPException(status_code=404, detail="Fermentation profile not found")

    # Update only provided fields
    update_data = profile.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_profile, field, value)

    db.commit()
    db.refresh(db_profile)

    # Fetch with relationships loaded
    result = (
        _with_steps(db.query(models.FermentationProfiles))
        .filter(models.FermentationProfiles.id == profile_id)
        .first()
    )
    return result


@router.delete(
    "/fermentation-profiles/{profile_id}",
    status_code=204,
    summary="Delete a fermentation profile",
    response_description="No content on successful deletion.",
)
async def delete_fermentation_profile(profile_id: int, db: db_dependency):
    """Delete a fermentation profile and all its steps (cascade)."""
    db_profile = (
        db.query(models.FermentationProfiles)
        .filter(models.FermentationProfiles.id == profile_id)
        .first()
    )

    if not db_profile:
        raise HTTPException(status_code=404, detail="Fermentation profile not found")

    db.delete(db_profile)
    db.commit()
    return


@router.get(
    "/fermentation-profiles/{profile_id}/steps",
    response_model=List[schemas.FermentationStep],
    summary="Get steps for a fermentation profile",
    response_description="A list of fermentation steps for the profile.",
)
async def get_fermentation_steps(
    profile_id: int, db: db_dependency
) -> List[schemas.FermentationStep]:
    """Return all steps for a specific fermentation profile."""
    # Verify profile exists
    profile = (
        db.query(models.FermentationProfiles)
        .filter(models.FermentationProfiles.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Fermentation profile not found")

    steps = (
        db.query(models.FermentationSteps)
        .filter(models.FermentationSteps.fermentation_profile_id == profile_id)
        .order_by(models.FermentationSteps.step_order)
        .all()
    )
    return steps


@router.post(
    "/fermentation-profiles/{profile_id}/steps",
    response_model=schemas.FermentationStep,
    status_code=201,
    summary="Add a step to a fermentation profile",
    response_description="The newly created fermentation step.",
)
async def add_fermentation_step(
    profile_id: int, step: schemas.FermentationStepCreate, db: db_dependency
) -> schemas.FermentationStep:
    """Add a new step to an existing fermentation profile."""
    # Verify profile exists
    profile = (
        db.query(models.FermentationProfiles)
        .filter(models.FermentationProfiles.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Fermentation profile not found")

    db_step = models.FermentationSteps(
        fermentation_profile_id=profile_id,
        step_order=step.step_order,
        name=step.name,
        step_type=step.step_type,
        temperature=step.temperature,
        duration_days=step.duration_days,
        ramp_days=step.ramp_days,
        pressure_psi=step.pressure_psi,
        notes=step.notes,
    )
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step


@router.put(
    "/fermentation-steps/{step_id}",
    response_model=schemas.FermentationStep,
    summary="Update a fermentation step",
    response_description="The updated fermentation step.",
)
async def update_fermentation_step(
    step_id: int, step: schemas.FermentationStepUpdate, db: db_dependency
) -> schemas.FermentationStep:
    """Update an existing fermentation step."""
    db_step = (
        db.query(models.FermentationSteps).filter(models.FermentationSteps.id == step_id).first()
    )

    if not db_step:
        raise HTTPException(status_code=404, detail="Fermentation step not found")

    # Update only provided fields
    update_data = step.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_step, field, value)

    db.commit()
    db.refresh(db_step)
    return db_step


@router.delete(
    "/fermentation-steps/{step_id}",
    status_code=204,
    summary="Delete a fermentation step",
    response_description="No content on successful deletion.",
)
async def delete_fermentation_step(step_id: int, db: db_dependency):
    """Delete a fermentation step."""
    db_step = (
        db.query(models.FermentationSteps).filter(models.FermentationSteps.id == step_id).first()
    )

    if not db_step:
        raise HTTPException(status_code=404, detail="Fermentation step not found")

    db.delete(db_step)
    db.commit()
    return
