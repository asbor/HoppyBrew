"""
API endpoints for batch cost tracking and analysis.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from modules.cost_calculations import (
    calculate_utility_costs,
    calculate_cost_per_unit,
    calculate_profit_margin,
    calculate_batch_cost_summary,
)
from pydantic import BaseModel, Field

router = APIRouter()


# Request Models for utility cost calculation
class UtilityCostRequest(BaseModel):
    """Request model for calculating utility costs."""

    brew_time_hours: float = Field(5.0, gt=0, description="Total brewing time in hours")
    electricity_rate_per_kwh: float = Field(
        0.12, ge=0, description="Cost per kilowatt-hour"
    )
    water_volume_liters: float = Field(
        30.0, gt=0, description="Total water used in liters"
    )
    water_rate_per_liter: float = Field(
        0.001, ge=0, description="Cost per liter of water"
    )
    gas_usage_cubic_meters: float = Field(
        0.0, ge=0, description="Gas usage in cubic meters"
    )
    gas_rate_per_cubic_meter: float = Field(
        0.50, ge=0, description="Cost per cubic meter of gas"
    )
    heating_power_kw: float = Field(
        3.5, gt=0, description="Power consumption of heating element in kW"
    )


class CostPerUnitRequest(BaseModel):
    """Request model for calculating cost per unit."""

    total_cost: float = Field(..., ge=0, description="Total cost of the batch")
    yield_volume_liters: float = Field(
        ..., gt=0, description="Expected yield volume in liters"
    )
    unit_type: str = Field(
        "pint",
        description="Type of unit (pint, us_pint, liter, bottle, can, half_liter)",
    )


class ProfitMarginRequest(BaseModel):
    """Request model for calculating profit margin."""

    cost_per_unit: float = Field(..., ge=0, description="Cost per unit")
    selling_price_per_unit: float = Field(
        ..., gt=0, description="Selling price per unit"
    )


# GET batch cost by batch ID
@router.get("/batches/{batch_id}/costs", response_model=schemas.BatchCost)
async def get_batch_cost(batch_id: int, db: Session = Depends(get_db)):
    """Get cost tracking information for a specific batch."""
    batch_cost = (
        db.query(models.BatchCost).filter(models.BatchCost.batch_id == batch_id).first()
    )

    if not batch_cost:
        raise HTTPException(
            status_code=404,
            detail=f"Cost tracking not found for batch {batch_id}",
        )

    return batch_cost


# CREATE batch cost
@router.post("/batches/{batch_id}/costs", response_model=schemas.BatchCost)
async def create_batch_cost(
    batch_id: int,
    cost_data: schemas.BatchCostCreate,
    db: Session = Depends(get_db),
):
    """Create cost tracking for a batch."""
    # Check if batch exists
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found")

    # Check if cost tracking already exists
    existing_cost = (
        db.query(models.BatchCost).filter(models.BatchCost.batch_id == batch_id).first()
    )
    if existing_cost:
        raise HTTPException(
            status_code=400,
            detail=f"Cost tracking already exists for batch {batch_id}",
        )

    # Validate batch_id matches
    if cost_data.batch_id != batch_id:
        raise HTTPException(
            status_code=400,
            detail="batch_id in URL does not match batch_id in request body",
        )

    # Create new batch cost record
    db_batch_cost = models.BatchCost(**cost_data.model_dump())
    db.add(db_batch_cost)
    db.commit()
    db.refresh(db_batch_cost)

    return db_batch_cost


# UPDATE batch cost
@router.put("/batches/{batch_id}/costs", response_model=schemas.BatchCost)
async def update_batch_cost(
    batch_id: int,
    cost_update: schemas.BatchCostUpdate,
    db: Session = Depends(get_db),
):
    """Update cost tracking for a batch."""
    batch_cost = (
        db.query(models.BatchCost).filter(models.BatchCost.batch_id == batch_id).first()
    )

    if not batch_cost:
        raise HTTPException(
            status_code=404,
            detail=f"Cost tracking not found for batch {batch_id}",
        )

    # Update only provided fields
    update_data = cost_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(batch_cost, field, value)

    db.commit()
    db.refresh(batch_cost)

    return batch_cost


# DELETE batch cost
@router.delete("/batches/{batch_id}/costs")
async def delete_batch_cost(batch_id: int, db: Session = Depends(get_db)):
    """Delete cost tracking for a batch."""
    batch_cost = (
        db.query(models.BatchCost).filter(models.BatchCost.batch_id == batch_id).first()
    )

    if not batch_cost:
        raise HTTPException(
            status_code=404,
            detail=f"Cost tracking not found for batch {batch_id}",
        )

    db.delete(batch_cost)
    db.commit()

    return {"message": f"Cost tracking deleted for batch {batch_id}"}


# GET cost summary for a batch
@router.get("/batches/{batch_id}/costs/summary", response_model=schemas.CostSummary)
async def get_batch_cost_summary(batch_id: int, db: Session = Depends(get_db)):
    """Get comprehensive cost summary and analysis for a batch."""
    batch_cost = (
        db.query(models.BatchCost).filter(models.BatchCost.batch_id == batch_id).first()
    )

    if not batch_cost:
        raise HTTPException(
            status_code=404,
            detail=f"Cost tracking not found for batch {batch_id}",
        )

    # Calculate ingredient costs total
    ingredient_costs = {
        "total_ingredient_cost": (
            batch_cost.fermentables_cost
            + batch_cost.hops_cost
            + batch_cost.yeasts_cost
            + batch_cost.miscs_cost
        )
    }

    # Calculate utility costs total
    utility_costs = {
        "total_utility_cost": (
            batch_cost.electricity_cost
            + batch_cost.water_cost
            + batch_cost.gas_cost
        )
    }

    # Calculate comprehensive summary
    summary = calculate_batch_cost_summary(
        ingredient_costs=ingredient_costs,
        utility_costs=utility_costs,
        labor_cost=batch_cost.labor_cost,
        packaging_cost=batch_cost.packaging_cost,
        other_cost=batch_cost.other_cost,
        yield_volume_liters=batch_cost.expected_yield_volume,
        selling_price_per_unit=batch_cost.selling_price_per_unit,
        unit_type=batch_cost.unit_type,
    )

    return schemas.CostSummary(**summary)


# POST calculate utility costs
@router.post("/costs/calculate-utilities")
async def calculate_utilities(request: UtilityCostRequest):
    """Calculate utility costs based on brewing parameters."""
    result = calculate_utility_costs(
        brew_time_hours=request.brew_time_hours,
        electricity_rate_per_kwh=request.electricity_rate_per_kwh,
        water_volume_liters=request.water_volume_liters,
        water_rate_per_liter=request.water_rate_per_liter,
        gas_usage_cubic_meters=request.gas_usage_cubic_meters,
        gas_rate_per_cubic_meter=request.gas_rate_per_cubic_meter,
        heating_power_kw=request.heating_power_kw,
    )
    return result


# POST calculate cost per unit
@router.post("/costs/calculate-cost-per-unit")
async def calculate_cost_per_serving(request: CostPerUnitRequest):
    """Calculate cost per serving unit (pint, liter, bottle, etc.)."""
    cost_per_unit = calculate_cost_per_unit(
        total_cost=request.total_cost,
        yield_volume_liters=request.yield_volume_liters,
        unit_type=request.unit_type,
    )
    return {"cost_per_unit": cost_per_unit, "unit_type": request.unit_type}


# POST calculate profit margin
@router.post("/costs/calculate-profit-margin")
async def calculate_profit(request: ProfitMarginRequest):
    """Calculate profit margin and profit per unit."""
    result = calculate_profit_margin(
        cost_per_unit=request.cost_per_unit,
        selling_price_per_unit=request.selling_price_per_unit,
    )
    return result
