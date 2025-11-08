# api/endpoints/brew_steps.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from datetime import datetime
from typing import List
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_brew_steps_from_recipe(batch_id: int, db: Session) -> List[models.BrewSteps]:
    """
    Generate brew steps from a batch's recipe.
    Creates steps for: Mash, Boil, Hop Additions, Chill, Transfer
    """
    # Get the batch with its recipe
    batch = (
        db.query(models.Batches)
        .filter(models.Batches.id == batch_id)
        .first()
    )
    
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # Get the recipe
    recipe = (
        db.query(models.Recipes)
        .filter(models.Recipes.id == batch.recipe_id)
        .first()
    )
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    steps = []
    order = 0
    
    # Step 1: Mash step (if applicable)
    if recipe.type and "grain" in recipe.type.lower():
        mash_step = models.BrewSteps(
            batch_id=batch_id,
            step_name="Mash",
            step_type="mash",
            duration=60,  # Default 60 minutes
            temperature=int(recipe.primary_temp) if recipe.primary_temp else 65,
            notes="Heat water and add grains. Maintain temperature for full mash duration.",
            order_index=order,
        )
        steps.append(mash_step)
        order += 1
        
        # Step 2: Sparge
        sparge_step = models.BrewSteps(
            batch_id=batch_id,
            step_name="Sparge",
            step_type="sparge",
            duration=30,  # Default 30 minutes
            notes="Rinse grains with hot water to extract remaining sugars.",
            order_index=order,
        )
        steps.append(sparge_step)
        order += 1
    
    # Step 3: Boil step
    boil_duration = recipe.boil_time if recipe.boil_time else 60
    boil_step = models.BrewSteps(
        batch_id=batch_id,
        step_name="Boil",
        step_type="boil",
        duration=boil_duration,
        notes=f"Bring wort to boil. Boil for {boil_duration} minutes.",
        order_index=order,
    )
    steps.append(boil_step)
    order += 1
    
    # Step 4: Hop additions (get from recipe hops)
    hops = (
        db.query(models.RecipeHop)
        .filter(models.RecipeHop.recipe_id == recipe.id)
        .order_by(models.RecipeHop.time.desc())
        .all()
    )
    
    for hop in hops:
        if hop.use and "boil" in hop.use.lower():
            hop_step = models.BrewSteps(
                batch_id=batch_id,
                step_name=f"Add {hop.name}",
                step_type="hop_addition",
                duration=hop.time if hop.time else 0,
                notes=f"Add {hop.amount}g of {hop.name} hops at {hop.time} minutes remaining",
                order_index=order,
            )
            steps.append(hop_step)
            order += 1
    
    # Step 5: Chill step
    chill_step = models.BrewSteps(
        batch_id=batch_id,
        step_name="Chill",
        step_type="chill",
        duration=30,  # Default 30 minutes
        temperature=20,  # Target temperature
        notes="Cool wort to pitching temperature as quickly as possible.",
        order_index=order,
    )
    steps.append(chill_step)
    order += 1
    
    # Step 6: Transfer and pitch yeast
    transfer_step = models.BrewSteps(
        batch_id=batch_id,
        step_name="Transfer & Pitch Yeast",
        step_type="transfer",
        duration=15,  # Default 15 minutes
        notes="Transfer wort to fermenter and pitch yeast. Aerate well.",
        order_index=order,
    )
    steps.append(transfer_step)
    order += 1
    
    return steps


@router.post("/batches/{batch_id}/brew-steps", response_model=List[schemas.BrewStep])
async def create_brew_steps(batch_id: int, db: Session = Depends(get_db)):
    """
    Generate brew steps from a batch's recipe.
    This will create a checklist of all brewing steps needed.
    """
    # Check if steps already exist
    existing_steps = (
        db.query(models.BrewSteps)
        .filter(models.BrewSteps.batch_id == batch_id)
        .count()
    )
    
    if existing_steps > 0:
        raise HTTPException(
            status_code=400,
            detail="Brew steps already exist for this batch. Use update endpoints to modify them.",
        )
    
    try:
        steps = generate_brew_steps_from_recipe(batch_id, db)
        
        # Add all steps to the database
        for step in steps:
            db.add(step)
        
        db.commit()
        
        # Refresh all steps to get their IDs
        for step in steps:
            db.refresh(step)
        
        return steps
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating brew steps: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating brew steps: {str(e)}")


@router.get("/batches/{batch_id}/brew-steps", response_model=List[schemas.BrewStep])
async def get_brew_steps(batch_id: int, db: Session = Depends(get_db)):
    """
    Get all brew steps for a batch.
    """
    # Verify batch exists
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    steps = (
        db.query(models.BrewSteps)
        .filter(models.BrewSteps.batch_id == batch_id)
        .order_by(models.BrewSteps.order_index)
        .all()
    )
    
    return steps


@router.get("/brew-steps/{step_id}", response_model=schemas.BrewStep)
async def get_brew_step(step_id: int, db: Session = Depends(get_db)):
    """
    Get a specific brew step by ID.
    """
    step = db.query(models.BrewSteps).filter(models.BrewSteps.id == step_id).first()
    
    if not step:
        raise HTTPException(status_code=404, detail="Brew step not found")
    
    return step


@router.patch("/brew-steps/{step_id}", response_model=schemas.BrewStep)
async def update_brew_step(
    step_id: int,
    step_update: schemas.BrewStepUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a brew step. Can be used to start/complete steps, update notes, etc.
    """
    step = db.query(models.BrewSteps).filter(models.BrewSteps.id == step_id).first()
    
    if not step:
        raise HTTPException(status_code=404, detail="Brew step not found")
    
    # Update fields that were provided
    update_data = step_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(step, field, value)
    
    # Update the updated_at timestamp
    step.updated_at = datetime.now()
    
    try:
        db.commit()
        db.refresh(step)
        return step
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating brew step: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating brew step: {str(e)}")


@router.delete("/brew-steps/{step_id}")
async def delete_brew_step(step_id: int, db: Session = Depends(get_db)):
    """
    Delete a brew step.
    """
    step = db.query(models.BrewSteps).filter(models.BrewSteps.id == step_id).first()
    
    if not step:
        raise HTTPException(status_code=404, detail="Brew step not found")
    
    try:
        db.delete(step)
        db.commit()
        return {"message": "Brew step deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting brew step: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting brew step: {str(e)}")


@router.post("/batches/{batch_id}/brew-steps/start")
async def start_brew_day(batch_id: int, db: Session = Depends(get_db)):
    """
    Start the brew day by starting the first incomplete step.
    """
    # Get the first incomplete step
    step = (
        db.query(models.BrewSteps)
        .filter(models.BrewSteps.batch_id == batch_id, models.BrewSteps.completed == False)
        .order_by(models.BrewSteps.order_index)
        .first()
    )
    
    if not step:
        raise HTTPException(
            status_code=404,
            detail="No incomplete steps found. All steps are completed or no steps exist.",
        )
    
    # Start the step
    step.started_at = datetime.now()
    step.updated_at = datetime.now()
    
    try:
        db.commit()
        db.refresh(step)
        return step
    except Exception as e:
        db.rollback()
        logger.error(f"Error starting brew day: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting brew day: {str(e)}")
