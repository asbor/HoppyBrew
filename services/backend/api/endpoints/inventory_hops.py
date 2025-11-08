# api/endpoints/inventory_hops.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import Database.Models as models
import Database.Schemas as schemas
from database import get_db

from .hops import router


@router.post("/inventory/hops", response_model=schemas.InventoryHop)
async def create_inventory_hop(
    hop: schemas.InventoryHopCreate, db: Session = Depends(get_db)
):
    try:
        db_hop = models.InventoryHop(**hop.model_dump())
        db.add(db_hop)
        db.commit()
        db.refresh(db_hop)
        return db_hop
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/inventory/hops/{id}", response_model=schemas.InventoryHop)
async def update_inventory_hop(
    id: int, hop: schemas.InventoryHopCreate, db: Session = Depends(get_db)
):
    db_hop = db.query(models.InventoryHop).filter(models.InventoryHop.id == id).first()
    if not db_hop:
        raise HTTPException(status_code=404, detail="Hop not found")
    for key, value in hop.model_dump().items():
        setattr(db_hop, key, value)
    db.commit()
    db.refresh(db_hop)
    return db_hop
