# api/endpoints/fermentation_readings.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List
from modules.brewing_calculations import calculate_abv, calculate_attenuation
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post(
    "/batches/{batch_id}/fermentation/readings",
    response_model=schemas.FermentationReading,
    tags=["fermentation"],
    summary="Add fermentation reading",
    response_description="The created fermentation reading",
)
async def create_fermentation_reading(
    batch_id: int,
    reading: schemas.FermentationReadingCreate,
    db: Session = Depends(get_db),
):
    """
    Add a new fermentation reading to a batch.

    Records gravity, temperature, pH, and other fermentation metrics
    to track the progress of fermentation over time.
    """
    # Verify batch exists
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    # Create the reading
    db_reading = models.FermentationReadings(
        batch_id=batch_id,
        timestamp=reading.timestamp,
        gravity=reading.gravity,
        temperature=reading.temperature,
        ph=reading.ph,
        notes=reading.notes,
    )

    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    return db_reading


@router.get(
    "/batches/{batch_id}/fermentation/readings",
    response_model=List[schemas.FermentationReading],
    tags=["fermentation"],
    summary="Get all fermentation readings for a batch",
    response_description="List of fermentation readings ordered by timestamp",
)
async def get_fermentation_readings(batch_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all fermentation readings for a specific batch.

    Returns readings in chronological order (oldest to newest).
    """
    # Verify batch exists
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    # Get readings ordered by timestamp
    readings = (
        db.query(models.FermentationReadings)
        .filter(models.FermentationReadings.batch_id == batch_id)
        .order_by(models.FermentationReadings.timestamp)
        .all()
    )

    return readings


@router.put(
    "/fermentation/readings/{reading_id}",
    response_model=schemas.FermentationReading,
    tags=["fermentation"],
    summary="Update fermentation reading",
    response_description="The updated fermentation reading",
)
async def update_fermentation_reading(
    reading_id: int,
    reading: schemas.FermentationReadingUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing fermentation reading.

    Allows modifying any field of a previously recorded reading.
    """
    db_reading = (
        db.query(models.FermentationReadings)
        .filter(models.FermentationReadings.id == reading_id)
        .first()
    )

    if not db_reading:
        raise HTTPException(status_code=404, detail="Fermentation reading not found")

    # Update fields
    for key, value in reading.model_dump(exclude_unset=True).items():
        setattr(db_reading, key, value)

    db.commit()
    db.refresh(db_reading)

    return db_reading


@router.delete(
    "/fermentation/readings/{reading_id}",
    tags=["fermentation"],
    summary="Delete fermentation reading",
    response_description="Confirmation message",
)
async def delete_fermentation_reading(reading_id: int, db: Session = Depends(get_db)):
    """
    Delete a fermentation reading.

    Permanently removes the reading from the database.
    """
    db_reading = (
        db.query(models.FermentationReadings)
        .filter(models.FermentationReadings.id == reading_id)
        .first()
    )

    if not db_reading:
        raise HTTPException(status_code=404, detail="Fermentation reading not found")

    db.delete(db_reading)
    db.commit()

    return {"message": "Fermentation reading deleted successfully"}


@router.get(
    "/batches/{batch_id}/fermentation/chart-data",
    response_model=schemas.FermentationChartData,
    tags=["fermentation"],
    summary="Get formatted chart data for fermentation readings",
    response_description="Formatted data ready for charting libraries",
)
async def get_fermentation_chart_data(batch_id: int, db: Session = Depends(get_db)):
    """
    Get fermentation readings formatted for charting.

    Returns parallel arrays of timestamps, gravity, temperature, pH,
    and calculated metrics (ABV, attenuation) suitable for use with
    Chart.js, D3.js, or other visualization libraries.
    """
    # Verify batch exists and get original gravity
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()

    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    # Get the batch's recipe to access original gravity
    recipe = batch.recipe
    original_gravity = recipe.og if recipe and recipe.og else None

    # Get readings ordered by timestamp
    readings = (
        db.query(models.FermentationReadings)
        .filter(models.FermentationReadings.batch_id == batch_id)
        .order_by(models.FermentationReadings.timestamp)
        .all()
    )

    # Build parallel arrays for charting
    timestamps = []
    gravity = []
    temperature = []
    ph = []
    abv = []
    attenuation = []

    for reading in readings:
        timestamps.append(reading.timestamp.isoformat())
        gravity.append(reading.gravity)
        temperature.append(reading.temperature)
        ph.append(reading.ph)

        # Calculate ABV and attenuation if we have both OG and current gravity
        if original_gravity and reading.gravity:
            try:
                calculated_abv = calculate_abv(original_gravity, reading.gravity)
                calculated_attenuation = calculate_attenuation(
                    original_gravity, reading.gravity
                )
                abv.append(round(calculated_abv, 2))
                attenuation.append(round(calculated_attenuation, 1))
            except ValueError:
                # If gravity hasn't dropped yet or invalid values
                abv.append(0.0)
                attenuation.append(0.0)
        else:
            abv.append(0.0)
            attenuation.append(0.0)

    return schemas.FermentationChartData(
        timestamps=timestamps,
        gravity=gravity,
        temperature=temperature,
        ph=ph,
        abv=abv,
        attenuation=attenuation,
    )
