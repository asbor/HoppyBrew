# api/endpoints/inventory_yeasts.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import Database.Models as models
import Database.Schemas as schemas
from database import get_db

from .yeasts import router


@router.post("/inventory/yeasts", response_model=schemas.InventoryYeast)
async def create_inventory_yeast(
    yeast: schemas.InventoryYeastCreate, db: Session = Depends(get_db)
):
    try:
        db_yeast = models.InventoryYeast(**yeast.dict())
        db.add(db_yeast)
        db.commit()
        db.refresh(db_yeast)
        return db_yeast
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/inventory/yeasts/{id}", response_model=schemas.InventoryYeast)
async def update_inventory_yeast(
    id: int, yeast: schemas.InventoryYeastCreate, db: Session = Depends(get_db)
):
    db_yeast = (
        db.query(models.InventoryYeast)
        .filter(models.InventoryYeast.id == id)
        .first()
    )
    if not db_yeast:
        raise HTTPException(status_code=404, detail="Yeast not found")
    for key, value in yeast.dict().items():
        setattr(db_yeast, key, value)
    db.commit()
    db.refresh(db_yeast)
    return db_yeast

