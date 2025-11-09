"""
API endpoints for yeast management features:
- Yeast strain database
- Viability calculator
- Harvesting logs
- Generation tracking
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from utils.yeast_viability import YeastViabilityCalculator

router = APIRouter()


# ========== Yeast Strain Endpoints ==========

@router.get("/yeast-strains", response_model=List[schemas.YeastStrain])
async def get_yeast_strains(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    laboratory: Optional[str] = None,
    yeast_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all yeast strains with optional filtering"""
    query = db.query(models.YeastStrain)
    
    if laboratory:
        query = query.filter(models.YeastStrain.laboratory.ilike(f"%{laboratory}%"))
    
    if yeast_type:
        query = query.filter(models.YeastStrain.type.ilike(f"%{yeast_type}%"))
    
    strains = query.offset(skip).limit(limit).all()
    return strains


@router.get("/yeast-strains/{strain_id}", response_model=schemas.YeastStrain)
async def get_yeast_strain(strain_id: int, db: Session = Depends(get_db)):
    """Get a specific yeast strain by ID"""
    strain = db.query(models.YeastStrain).filter(models.YeastStrain.id == strain_id).first()
    if not strain:
        raise HTTPException(status_code=404, detail="Yeast strain not found")
    return strain


@router.post("/yeast-strains", response_model=schemas.YeastStrain, status_code=201)
async def create_yeast_strain(
    strain: schemas.YeastStrainCreate,
    db: Session = Depends(get_db)
):
    """Create a new yeast strain"""
    try:
        db_strain = models.YeastStrain(**strain.model_dump())
        db.add(db_strain)
        db.commit()
        db.refresh(db_strain)
        return db_strain
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/yeast-strains/{strain_id}", response_model=schemas.YeastStrain)
async def update_yeast_strain(
    strain_id: int,
    strain: schemas.YeastStrainUpdate,
    db: Session = Depends(get_db)
):
    """Update a yeast strain"""
    db_strain = db.query(models.YeastStrain).filter(models.YeastStrain.id == strain_id).first()
    if not db_strain:
        raise HTTPException(status_code=404, detail="Yeast strain not found")
    
    update_data = strain.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_strain, key, value)
    
    try:
        db.commit()
        db.refresh(db_strain)
        return db_strain
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/yeast-strains/{strain_id}")
async def delete_yeast_strain(strain_id: int, db: Session = Depends(get_db)):
    """Delete a yeast strain"""
    db_strain = db.query(models.YeastStrain).filter(models.YeastStrain.id == strain_id).first()
    if not db_strain:
        raise HTTPException(status_code=404, detail="Yeast strain not found")
    
    try:
        db.delete(db_strain)
        db.commit()
        return {"message": "Yeast strain deleted successfully"}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


# ========== Yeast Harvest Endpoints ==========

@router.get("/yeast-harvests", response_model=List[schemas.YeastHarvest])
async def get_yeast_harvests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    yeast_strain_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all yeast harvests with optional filtering"""
    query = db.query(models.YeastHarvest)
    
    if yeast_strain_id:
        query = query.filter(models.YeastHarvest.yeast_strain_id == yeast_strain_id)
    
    if status:
        query = query.filter(models.YeastHarvest.status == status)
    
    harvests = query.order_by(models.YeastHarvest.harvest_date.desc()).offset(skip).limit(limit).all()
    return harvests


@router.get("/yeast-harvests/{harvest_id}", response_model=schemas.YeastHarvest)
async def get_yeast_harvest(harvest_id: int, db: Session = Depends(get_db)):
    """Get a specific yeast harvest by ID"""
    harvest = db.query(models.YeastHarvest).filter(models.YeastHarvest.id == harvest_id).first()
    if not harvest:
        raise HTTPException(status_code=404, detail="Yeast harvest not found")
    return harvest


@router.post("/yeast-harvests", response_model=schemas.YeastHarvest, status_code=201)
async def create_yeast_harvest(
    harvest: schemas.YeastHarvestCreate,
    db: Session = Depends(get_db)
):
    """Create a new yeast harvest record"""
    # Verify yeast strain exists
    strain = db.query(models.YeastStrain).filter(
        models.YeastStrain.id == harvest.yeast_strain_id
    ).first()
    if not strain:
        raise HTTPException(status_code=404, detail="Yeast strain not found")
    
    # If parent harvest specified, verify it exists and increment generation
    if harvest.parent_harvest_id:
        parent = db.query(models.YeastHarvest).filter(
            models.YeastHarvest.id == harvest.parent_harvest_id
        ).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent harvest not found")
        # Auto-increment generation from parent
        if harvest.generation <= parent.generation:
            harvest.generation = parent.generation + 1
    
    try:
        harvest_data = harvest.model_dump()
        if harvest_data.get("harvest_date") is None:
            harvest_data["harvest_date"] = datetime.now()
            
        db_harvest = models.YeastHarvest(**harvest_data)
        db.add(db_harvest)
        db.commit()
        db.refresh(db_harvest)
        return db_harvest
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/yeast-harvests/{harvest_id}", response_model=schemas.YeastHarvest)
async def update_yeast_harvest(
    harvest_id: int,
    harvest: schemas.YeastHarvestUpdate,
    db: Session = Depends(get_db)
):
    """Update a yeast harvest"""
    db_harvest = db.query(models.YeastHarvest).filter(models.YeastHarvest.id == harvest_id).first()
    if not db_harvest:
        raise HTTPException(status_code=404, detail="Yeast harvest not found")
    
    update_data = harvest.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_harvest, key, value)
    
    try:
        db.commit()
        db.refresh(db_harvest)
        return db_harvest
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/yeast-harvests/{harvest_id}")
async def delete_yeast_harvest(harvest_id: int, db: Session = Depends(get_db)):
    """Delete a yeast harvest"""
    db_harvest = db.query(models.YeastHarvest).filter(models.YeastHarvest.id == harvest_id).first()
    if not db_harvest:
        raise HTTPException(status_code=404, detail="Yeast harvest not found")
    
    try:
        db.delete(db_harvest)
        db.commit()
        return {"message": "Yeast harvest deleted successfully"}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/yeast-harvests/{harvest_id}/genealogy")
async def get_harvest_genealogy(harvest_id: int, db: Session = Depends(get_db)):
    """Get the genealogy tree for a yeast harvest"""
    harvest = db.query(models.YeastHarvest).filter(models.YeastHarvest.id == harvest_id).first()
    if not harvest:
        raise HTTPException(status_code=404, detail="Yeast harvest not found")
    
    # Build genealogy tree
    genealogy = {
        "current": harvest,
        "ancestors": [],
        "descendants": []
    }
    
    # Get ancestors
    current = harvest
    while current.parent_harvest_id:
        parent = db.query(models.YeastHarvest).filter(
            models.YeastHarvest.id == current.parent_harvest_id
        ).first()
        if parent:
            genealogy["ancestors"].append(parent)
            current = parent
        else:
            break
    
    # Get descendants (recursive function would be better for deep trees)
    def get_children(parent_id):
        return db.query(models.YeastHarvest).filter(
            models.YeastHarvest.parent_harvest_id == parent_id
        ).all()
    
    def build_descendants(parent_id):
        children = get_children(parent_id)
        result = []
        for child in children:
            result.append({
                "harvest": child,
                "children": build_descendants(child.id)
            })
        return result
    
    genealogy["descendants"] = build_descendants(harvest_id)
    
    return genealogy


# ========== Viability Calculator Endpoint ==========

@router.post("/yeasts/calculate-viability", response_model=schemas.ViabilityCalculationResponse)
async def calculate_yeast_viability(request: schemas.ViabilityCalculationRequest):
    """
    Calculate yeast viability based on age, storage conditions, and generation.
    
    This endpoint helps brewers determine if their yeast is still viable
    and whether a starter is needed.
    """
    try:
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form=request.yeast_form,
            manufacture_date=request.manufacture_date,
            expiry_date=request.expiry_date,
            current_date=request.current_date,
            initial_viability=request.initial_viability,
            storage_temperature=request.storage_temperature,
            generation=request.generation
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/yeasts/inventory/{inventory_id}/viability")
async def get_inventory_yeast_viability(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    """
    Calculate current viability for an inventory yeast item.
    
    Uses stored information about the yeast to calculate current viability.
    """
    yeast = db.query(models.InventoryYeast).filter(
        models.InventoryYeast.id == inventory_id
    ).first()
    if not yeast:
        raise HTTPException(status_code=404, detail="Inventory yeast not found")
    
    # Determine form from yeast data
    yeast_form = yeast.form or "Liquid"
    
    # Use stored viability or default to 100
    initial_viability = yeast.current_viability or 100.0
    
    # Calculate viability
    result = YeastViabilityCalculator.calculate_viability(
        yeast_form=yeast_form,
        manufacture_date=yeast.manufacture_date,
        expiry_date=yeast.expiry_date,
        initial_viability=initial_viability,
        generation=yeast.generation or 0
    )
    
    # Update stored viability
    try:
        yeast.current_viability = result["current_viability"]
        yeast.last_viability_check = datetime.now()
        db.commit()
    except Exception:
        db.rollback()
    
    return result
