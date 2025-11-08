# api/endpoints/inventory_fermentables.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import Database.Models as models
import Database.Schemas as schemas
from database import get_db

from .fermentables import router


@router.post("/inventory/fermentables", response_model=schemas.InventoryFermentable)
async def create_inventory_fermentable(
    fermentable: schemas.InventoryFermentableCreate,
    db: Session = Depends(get_db),
):
    try:
        db_fermentable = models.InventoryFermentable(**fermentable.model_dump())
        db.add(db_fermentable)
        db.commit()
        db.refresh(db_fermentable)
        return db_fermentable
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/inventory/fermentables/{id}", response_model=schemas.InventoryFermentable)
async def update_inventory_fermentable(
    id: int,
    fermentable: schemas.InventoryFermentableCreate,
    db: Session = Depends(get_db),
):
    db_fermentable = (
        db.query(models.InventoryFermentable)
        .filter(models.InventoryFermentable.id == id)
        .first()
    )
    if not db_fermentable:
        raise HTTPException(status_code=404, detail="Fermentable not found")
    for key, value in fermentable.model_dump().items():
        setattr(db_fermentable, key, value)
    db.commit()
    db.refresh(db_fermentable)
    return db_fermentable
