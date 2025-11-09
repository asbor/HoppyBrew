# api/endpoints/packaging.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from datetime import datetime
from typing import Optional
import logging

from modules.brewing_calculations import calculate_priming_sugar, calculate_carbonation

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/batches/{batch_id}/packaging", response_model=schemas.PackagingDetails)
async def create_packaging_details(
    batch_id: int,
    packaging: schemas.PackagingDetailsCreate,
    db: Session = Depends(get_db),
):
    """
    Create packaging details for a batch.
    
    This endpoint logs bottling or kegging details including:
    - Packaging method (bottling/kegging)
    - Carbonation method (priming sugar/forced/natural)
    - Container count and size
    - Calculated priming sugar amounts or PSI
    """
    try:
        # Check if batch exists
        batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")

        # Check if packaging details already exist for this batch
        existing = (
            db.query(models.PackagingDetails)
            .filter(models.PackagingDetails.batch_id == batch_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Packaging details already exist for this batch. Use PUT to update.",
            )

        # Create packaging details
        db_packaging = models.PackagingDetails(
            batch_id=batch_id,
            **packaging.model_dump()
        )

        db.add(db_packaging)
        db.commit()
        db.refresh(db_packaging)

        logger.info(
            f"Created packaging details for batch {batch_id}: {packaging.method}"
        )

        return db_packaging

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating packaging details: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating packaging details: {str(e)}")


@router.get("/batches/{batch_id}/packaging", response_model=schemas.PackagingDetails)
async def get_packaging_details(batch_id: int, db: Session = Depends(get_db)):
    """
    Get packaging details for a specific batch.
    """
    packaging = (
        db.query(models.PackagingDetails)
        .filter(models.PackagingDetails.batch_id == batch_id)
        .first()
    )
    
    if not packaging:
        raise HTTPException(
            status_code=404, 
            detail="Packaging details not found for this batch"
        )
    
    return packaging


@router.put("/batches/{batch_id}/packaging", response_model=schemas.PackagingDetails)
async def update_packaging_details(
    batch_id: int,
    packaging_update: schemas.PackagingDetailsUpdate,
    db: Session = Depends(get_db),
):
    """
    Update packaging details for a batch.
    """
    packaging = (
        db.query(models.PackagingDetails)
        .filter(models.PackagingDetails.batch_id == batch_id)
        .first()
    )
    
    if not packaging:
        raise HTTPException(
            status_code=404,
            detail="Packaging details not found for this batch",
        )

    # Update fields
    update_data = packaging_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(packaging, field, value)

    packaging.updated_at = datetime.now()

    try:
        db.commit()
        db.refresh(packaging)
        logger.info(f"Updated packaging details for batch {batch_id}")
        return packaging
    except Exception as e:
        logger.error(f"Error updating packaging details: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error updating packaging details: {str(e)}"
        )


@router.delete("/batches/{batch_id}/packaging")
async def delete_packaging_details(batch_id: int, db: Session = Depends(get_db)):
    """
    Delete packaging details for a batch.
    """
    packaging = (
        db.query(models.PackagingDetails)
        .filter(models.PackagingDetails.batch_id == batch_id)
        .first()
    )
    
    if not packaging:
        raise HTTPException(
            status_code=404,
            detail="Packaging details not found for this batch",
        )

    try:
        db.delete(packaging)
        db.commit()
        logger.info(f"Deleted packaging details for batch {batch_id}")
        return {"message": "Packaging details deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting packaging details: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting packaging details: {str(e)}"
        )


@router.post("/packaging/calculate-priming-sugar")
async def calculate_priming_sugar_for_packaging(
    volume_gal: float,
    carbonation_level: float,
    sugar_type: str = "table",
):
    """
    Calculate priming sugar needed for bottle carbonation.
    
    This is a convenience endpoint that wraps the calculator.
    
    Args:
        volume_gal: Beer volume in gallons
        carbonation_level: Target CO2 volumes (typically 2.0-2.8)
        sugar_type: Type of sugar ('table', 'corn', 'dme', 'honey')
    
    Returns:
        Dictionary with grams and oz of priming sugar needed
    """
    try:
        result = calculate_priming_sugar(volume_gal, carbonation_level, sugar_type)
        return result
    except Exception as e:
        logger.error(f"Error calculating priming sugar: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating priming sugar: {str(e)}"
        )


@router.post("/packaging/calculate-carbonation-psi")
async def calculate_carbonation_psi_for_packaging(
    temp_f: float,
    co2_volumes: float,
):
    """
    Calculate carbonation pressure for kegging.
    
    This is a convenience endpoint that wraps the calculator.
    
    Args:
        temp_f: Beer temperature in Fahrenheit
        co2_volumes: Desired CO2 volumes
    
    Returns:
        Dictionary with psi and bar pressure values
    """
    try:
        result = calculate_carbonation(temp_f, co2_volumes)
        return result
    except Exception as e:
        logger.error(f"Error calculating carbonation pressure: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating carbonation pressure: {str(e)}"
        )
