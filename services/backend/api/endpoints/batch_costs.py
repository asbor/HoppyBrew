# api/endpoints/batch_costs.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Constants for calculations
PINT_IN_LITERS = 0.473176  # US pint


def calculate_batch_cost_totals(batch_cost: models.BatchCost, batch_size: float) -> models.BatchCost:
    """Calculate total cost and per-unit costs for a batch"""
    
    # Calculate ingredient costs total (handle None values)
    ingredients_total = (
        (batch_cost.fermentables_cost or 0.0)
        + (batch_cost.hops_cost or 0.0)
        + (batch_cost.yeasts_cost or 0.0)
        + (batch_cost.miscs_cost or 0.0)
    )
    
    # Calculate utility costs total
    utilities_total = (
        (batch_cost.electricity_cost or 0.0)
        + (batch_cost.water_cost or 0.0)
        + (batch_cost.gas_cost or 0.0)
        + (batch_cost.other_utility_cost or 0.0)
    )
    
    # Calculate other costs total
    other_total = (
        (batch_cost.labor_cost or 0.0)
        + (batch_cost.packaging_cost or 0.0)
        + (batch_cost.other_cost or 0.0)
    )
    
    # Total cost
    batch_cost.total_cost = ingredients_total + utilities_total + other_total
    
    # Per-unit costs
    if batch_size > 0:
        batch_cost.cost_per_liter = batch_cost.total_cost / batch_size
        batch_cost.cost_per_pint = batch_cost.cost_per_liter * PINT_IN_LITERS
    else:
        batch_cost.cost_per_liter = 0.0
        batch_cost.cost_per_pint = 0.0
    
    # Calculate profit margin if target price is set
    if batch_cost.target_price_per_pint and batch_cost.cost_per_pint > 0:
        profit = batch_cost.target_price_per_pint - batch_cost.cost_per_pint
        batch_cost.profit_margin = (profit / batch_cost.target_price_per_pint) * 100
    else:
        batch_cost.profit_margin = None
    
    return batch_cost


def calculate_ingredient_costs_from_batch(batch_id: int, db: Session) -> dict:
    """Calculate ingredient costs from batch inventory items"""
    
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        return {
            "fermentables_cost": 0.0,
            "hops_cost": 0.0,
            "yeasts_cost": 0.0,
            "miscs_cost": 0.0,
        }
    
    fermentables_cost = sum(
        (item.amount or 0.0) * (item.cost_per_unit or 0.0)
        for item in batch.inventory_fermentables
    )
    
    hops_cost = sum(
        (item.amount or 0.0) * (item.cost_per_unit or 0.0)
        for item in batch.inventory_hops
    )
    
    yeasts_cost = sum(
        (item.cost_per_unit or 0.0)  # Yeasts typically counted by package
        for item in batch.inventory_yeasts
    )
    
    miscs_cost = sum(
        (item.amount or 0.0) * (item.cost_per_unit or 0.0)
        for item in batch.inventory_miscs
    )
    
    return {
        "fermentables_cost": round(fermentables_cost, 2),
        "hops_cost": round(hops_cost, 2),
        "yeasts_cost": round(yeasts_cost, 2),
        "miscs_cost": round(miscs_cost, 2),
    }


@router.post("/batch-costs", response_model=schemas.BatchCost)
async def create_batch_cost(
    batch_cost: schemas.BatchCostCreate,
    db: Session = Depends(get_db)
):
    """Create a cost tracking record for a batch"""
    
    # Check if batch exists
    batch = db.query(models.Batches).filter(models.Batches.id == batch_cost.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # Check if cost record already exists
    existing = db.query(models.BatchCost).filter(
        models.BatchCost.batch_id == batch_cost.batch_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Cost record already exists for this batch. Use PUT to update."
        )
    
    # Create the cost record
    db_batch_cost = models.BatchCost(**batch_cost.model_dump())
    
    # Calculate totals
    db_batch_cost = calculate_batch_cost_totals(db_batch_cost, batch.batch_size)
    
    db.add(db_batch_cost)
    db.commit()
    db.refresh(db_batch_cost)
    
    return db_batch_cost


@router.get("/batch-costs/{batch_id}", response_model=schemas.BatchCost)
async def get_batch_cost(batch_id: int, db: Session = Depends(get_db)):
    """Get cost information for a specific batch"""
    
    batch_cost = db.query(models.BatchCost).filter(
        models.BatchCost.batch_id == batch_id
    ).first()
    
    if not batch_cost:
        raise HTTPException(status_code=404, detail="Cost record not found for this batch")
    
    return batch_cost


@router.put("/batch-costs/{batch_id}", response_model=schemas.BatchCost)
async def update_batch_cost(
    batch_id: int,
    batch_cost_update: schemas.BatchCostUpdate,
    db: Session = Depends(get_db)
):
    """Update cost information for a batch"""
    
    batch_cost = db.query(models.BatchCost).filter(
        models.BatchCost.batch_id == batch_id
    ).first()
    
    if not batch_cost:
        raise HTTPException(status_code=404, detail="Cost record not found for this batch")
    
    # Get the batch for size calculation
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # Update fields
    update_data = batch_cost_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(batch_cost, field, value)
    
    # Recalculate totals
    batch_cost = calculate_batch_cost_totals(batch_cost, batch.batch_size)
    
    db.commit()
    db.refresh(batch_cost)
    
    return batch_cost


@router.delete("/batch-costs/{batch_id}")
async def delete_batch_cost(batch_id: int, db: Session = Depends(get_db)):
    """Delete cost information for a batch"""
    
    batch_cost = db.query(models.BatchCost).filter(
        models.BatchCost.batch_id == batch_id
    ).first()
    
    if not batch_cost:
        raise HTTPException(status_code=404, detail="Cost record not found for this batch")
    
    db.delete(batch_cost)
    db.commit()
    
    return {"message": "Batch cost record deleted successfully"}


@router.get("/batch-costs/{batch_id}/summary", response_model=schemas.BatchCostSummary)
async def get_batch_cost_summary(batch_id: int, db: Session = Depends(get_db)):
    """Get a summary of costs for a batch"""
    
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    batch_cost = db.query(models.BatchCost).filter(
        models.BatchCost.batch_id == batch_id
    ).first()
    
    if not batch_cost:
        raise HTTPException(status_code=404, detail="Cost record not found for this batch")
    
    # Calculate cost categories
    total_ingredients = (
        batch_cost.fermentables_cost
        + batch_cost.hops_cost
        + batch_cost.yeasts_cost
        + batch_cost.miscs_cost
    )
    
    total_utilities = (
        batch_cost.electricity_cost
        + batch_cost.water_cost
        + batch_cost.gas_cost
        + batch_cost.other_utility_cost
    )
    
    total_other = (
        batch_cost.labor_cost
        + batch_cost.packaging_cost
        + batch_cost.other_cost
    )
    
    return schemas.BatchCostSummary(
        batch_id=batch.id,
        batch_name=batch.batch_name,
        batch_size=batch.batch_size,
        total_ingredients_cost=total_ingredients,
        total_utilities_cost=total_utilities,
        total_other_costs=total_other,
        total_cost=batch_cost.total_cost,
        cost_per_liter=batch_cost.cost_per_liter,
        cost_per_pint=batch_cost.cost_per_pint,
        target_price_per_pint=batch_cost.target_price_per_pint,
        profit_margin=batch_cost.profit_margin,
    )


@router.post("/batch-costs/{batch_id}/calculate-from-ingredients", response_model=schemas.BatchCost)
async def calculate_costs_from_ingredients(
    batch_id: int,
    db: Session = Depends(get_db)
):
    """Calculate and create/update batch costs based on ingredient cost_per_unit values"""
    
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # Calculate ingredient costs from batch inventory
    ingredient_costs = calculate_ingredient_costs_from_batch(batch_id, db)
    
    # Check if cost record exists
    batch_cost = db.query(models.BatchCost).filter(
        models.BatchCost.batch_id == batch_id
    ).first()
    
    if batch_cost:
        # Update existing record
        batch_cost.fermentables_cost = ingredient_costs["fermentables_cost"]
        batch_cost.hops_cost = ingredient_costs["hops_cost"]
        batch_cost.yeasts_cost = ingredient_costs["yeasts_cost"]
        batch_cost.miscs_cost = ingredient_costs["miscs_cost"]
        
        # Recalculate totals
        batch_cost = calculate_batch_cost_totals(batch_cost, batch.batch_size)
    else:
        # Create new record
        batch_cost = models.BatchCost(
            batch_id=batch_id,
            **ingredient_costs
        )
        batch_cost = calculate_batch_cost_totals(batch_cost, batch.batch_size)
        db.add(batch_cost)
    
    db.commit()
    db.refresh(batch_cost)
    
    return batch_cost


# Utility Cost Configuration Endpoints

@router.post("/utility-cost-configs", response_model=schemas.UtilityCostConfig)
async def create_utility_cost_config(
    config: schemas.UtilityCostConfigCreate,
    db: Session = Depends(get_db)
):
    """Create a new utility cost configuration"""
    
    # Check if name already exists
    existing = db.query(models.UtilityCostConfig).filter(
        models.UtilityCostConfig.name == config.name
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Utility cost config with name '{config.name}' already exists"
        )
    
    db_config = models.UtilityCostConfig(**config.model_dump())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    
    return db_config


@router.get("/utility-cost-configs", response_model=List[schemas.UtilityCostConfig])
async def get_utility_cost_configs(
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all utility cost configurations"""
    
    query = db.query(models.UtilityCostConfig)
    if active_only:
        query = query.filter(models.UtilityCostConfig.is_active == 1)
    
    return query.all()


@router.get("/utility-cost-configs/{config_id}", response_model=schemas.UtilityCostConfig)
async def get_utility_cost_config(config_id: int, db: Session = Depends(get_db)):
    """Get a specific utility cost configuration"""
    
    config = db.query(models.UtilityCostConfig).filter(
        models.UtilityCostConfig.id == config_id
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Utility cost config not found")
    
    return config


@router.put("/utility-cost-configs/{config_id}", response_model=schemas.UtilityCostConfig)
async def update_utility_cost_config(
    config_id: int,
    config_update: schemas.UtilityCostConfigUpdate,
    db: Session = Depends(get_db)
):
    """Update a utility cost configuration"""
    
    config = db.query(models.UtilityCostConfig).filter(
        models.UtilityCostConfig.id == config_id
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Utility cost config not found")
    
    # Update fields
    update_data = config_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)
    
    db.commit()
    db.refresh(config)
    
    return config


@router.delete("/utility-cost-configs/{config_id}")
async def delete_utility_cost_config(config_id: int, db: Session = Depends(get_db)):
    """Delete a utility cost configuration"""
    
    config = db.query(models.UtilityCostConfig).filter(
        models.UtilityCostConfig.id == config_id
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Utility cost config not found")
    
    db.delete(config)
    db.commit()
    
    return {"message": "Utility cost config deleted successfully"}


@router.post("/batch-costs/{batch_id}/apply-utility-config/{config_id}", response_model=schemas.BatchCost)
async def apply_utility_config_to_batch(
    batch_id: int,
    config_id: int,
    db: Session = Depends(get_db)
):
    """Apply utility cost configuration to a batch cost record"""
    
    # Get the batch
    batch = db.query(models.Batches).filter(models.Batches.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # Get the utility config
    config = db.query(models.UtilityCostConfig).filter(
        models.UtilityCostConfig.id == config_id
    ).first()
    if not config:
        raise HTTPException(status_code=404, detail="Utility cost config not found")
    
    # Get or create batch cost record
    batch_cost = db.query(models.BatchCost).filter(
        models.BatchCost.batch_id == batch_id
    ).first()
    
    if not batch_cost:
        batch_cost = models.BatchCost(batch_id=batch_id)
        db.add(batch_cost)
    
    # Apply utility costs from config
    if config.avg_electricity_kwh_per_batch and config.electricity_rate_per_kwh:
        batch_cost.electricity_cost = (
            config.avg_electricity_kwh_per_batch * config.electricity_rate_per_kwh
        )
    
    if config.avg_water_liters_per_batch and config.water_rate_per_liter:
        batch_cost.water_cost = (
            config.avg_water_liters_per_batch * config.water_rate_per_liter
        )
    
    if config.avg_gas_units_per_batch and config.gas_rate_per_unit:
        batch_cost.gas_cost = (
            config.avg_gas_units_per_batch * config.gas_rate_per_unit
        )
    
    # Recalculate totals
    batch_cost = calculate_batch_cost_totals(batch_cost, batch.batch_size)
    
    db.commit()
    db.refresh(batch_cost)
    
    return batch_cost
