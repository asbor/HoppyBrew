# api/endpoints/packaging.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/packaging", response_model=schemas.PackagingDetails, status_code=201)
async def create_packaging_details(
    packaging: schemas.PackagingDetailsCreate, db: Session = Depends(get_db)
):
    """
    Create packaging details for a batch.
    
    This endpoint logs the packaging method (bottling/kegging), carbonation details,
    and container information for a batch.
    """
    try:
        # Verify batch exists
        batch = (
            db.query(models.Batches)
            .filter(models.Batches.id == packaging.batch_id)
            .first()
        )
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")

        # Check if packaging details already exist for this batch
        existing = (
            db.query(models.PackagingDetails)
            .filter(models.PackagingDetails.batch_id == packaging.batch_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Packaging details already exist for this batch. Use PUT to update.",
            )

        # Validate method
        if packaging.method not in ["bottle", "keg"]:
            raise HTTPException(
                status_code=400,
                detail="Method must be 'bottle' or 'keg'",
            )

        # Validate carbonation method if provided
        if packaging.carbonation_method and packaging.carbonation_method not in [
            "priming",
            "forced",
            "natural",
        ]:
            raise HTTPException(
                status_code=400,
                detail="Carbonation method must be 'priming', 'forced', or 'natural'",
            )

        # Validate priming sugar type if provided
        if packaging.priming_sugar_type and packaging.priming_sugar_type not in [
            "table",
            "corn",
            "dme",
            "honey",
        ]:
            raise HTTPException(
                status_code=400,
                detail="Priming sugar type must be 'table', 'corn', 'dme', or 'honey'",
            )

        # Create the packaging details
        db_packaging = models.PackagingDetails(**packaging.model_dump())
        db.add(db_packaging)
        db.commit()
        db.refresh(db_packaging)

        logger.info(f"Created packaging details for batch {packaging.batch_id}")
        return db_packaging

    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Error creating packaging details: {exc}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/packaging/{batch_id}", response_model=schemas.PackagingDetails)
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
            status_code=404, detail="Packaging details not found for this batch"
        )
    return packaging


@router.get("/packaging", response_model=List[schemas.PackagingDetails])
async def list_packaging_details(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    List all packaging details with pagination.
    """
    packaging_list = (
        db.query(models.PackagingDetails)
        .order_by(models.PackagingDetails.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return packaging_list


@router.put("/packaging/{batch_id}", response_model=schemas.PackagingDetails)
async def update_packaging_details(
    batch_id: int,
    packaging: schemas.PackagingDetailsUpdate,
    db: Session = Depends(get_db),
):
    """
    Update packaging details for a batch.
    """
    db_packaging = (
        db.query(models.PackagingDetails)
        .filter(models.PackagingDetails.batch_id == batch_id)
        .first()
    )
    if not db_packaging:
        raise HTTPException(
            status_code=404, detail="Packaging details not found for this batch"
        )

    # Update only provided fields
    update_data = packaging.model_dump(exclude_unset=True)
    
    # Validate method if being updated
    if "method" in update_data and update_data["method"] not in ["bottle", "keg"]:
        raise HTTPException(
            status_code=400,
            detail="Method must be 'bottle' or 'keg'",
        )

    # Validate carbonation method if being updated
    if (
        "carbonation_method" in update_data
        and update_data["carbonation_method"] is not None
        and update_data["carbonation_method"] not in ["priming", "forced", "natural"]
    ):
        raise HTTPException(
            status_code=400,
            detail="Carbonation method must be 'priming', 'forced', or 'natural'",
        )

    # Validate priming sugar type if being updated
    if (
        "priming_sugar_type" in update_data
        and update_data["priming_sugar_type"] is not None
        and update_data["priming_sugar_type"] not in ["table", "corn", "dme", "honey"]
    ):
        raise HTTPException(
            status_code=400,
            detail="Priming sugar type must be 'table', 'corn', 'dme', or 'honey'",
        )

    for key, value in update_data.items():
        setattr(db_packaging, key, value)

    try:
        db.commit()
        db.refresh(db_packaging)
        logger.info(f"Updated packaging details for batch {batch_id}")
        return db_packaging
    except Exception as exc:
        logger.error(f"Error updating packaging details: {exc}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("/packaging/{batch_id}", status_code=204)
async def delete_packaging_details(batch_id: int, db: Session = Depends(get_db)):
    """
    Delete packaging details for a batch.
    """
    db_packaging = (
        db.query(models.PackagingDetails)
        .filter(models.PackagingDetails.batch_id == batch_id)
        .first()
    )
    if not db_packaging:
        raise HTTPException(
            status_code=404, detail="Packaging details not found for this batch"
        )

    try:
        db.delete(db_packaging)
        db.commit()
        logger.info(f"Deleted packaging details for batch {batch_id}")
        return None
    except Exception as exc:
        logger.error(f"Error deleting packaging details: {exc}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
