# api/endpoints/inventory_miscs.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import Database.Models as models
import Database.Schemas as schemas
from database import get_db

from .miscs import router


@router.post("/inventory/miscs", response_model=schemas.InventoryMisc)
async def create_inventory_misc(
    misc: schemas.InventoryMiscCreate, db: Session = Depends(get_db)
):
    try:
        db_misc = models.InventoryMisc(**misc.dict())
        db.add(db_misc)
        db.commit()
        db.refresh(db_misc)
        return db_misc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/inventory/miscs/{id}", response_model=schemas.InventoryMisc)
async def update_inventory_misc(
    id: int, misc: schemas.InventoryMiscCreate, db: Session = Depends(get_db)
):
    db_misc = (
        db.query(models.InventoryMisc)
        .filter(models.InventoryMisc.id == id)
        .first()
    )
    if not db_misc:
        raise HTTPException(status_code=404, detail="Misc not found")
    for key, value in misc.dict().items():
        setattr(db_misc, key, value)
    db.commit()
    db.refresh(db_misc)
    return db_misc

