# api/endpoints/fermentables.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List

router = APIRouter()

# Recipe Fermentables Endpoints


@router.get("/recipes/fermentables", response_model=List[schemas.RecipeFermentable])
async def get_all_recipe_fermentables(db: Session = Depends(get_db)):
    fermentables = db.query(models.RecipeFermentable).all()
    return fermentables


# Inventory Fermentables Endpoints


@router.get(
    "/inventory/fermentables",
    response_model=List[schemas.InventoryFermentable],
)
async def get_all_inventory_fermentables(db: Session = Depends(get_db)):
    fermentables = db.query(models.InventoryFermentable).all()
    return fermentables


@router.get(
    "/inventory/fermentables/{fermentable_id}",
    response_model=schemas.InventoryFermentable,
)
async def get_inventory_fermentable(fermentable_id: int, db: Session = Depends(get_db)):
    fermentable = (
        db.query(models.InventoryFermentable)
        .filter(models.InventoryFermentable.id == fermentable_id)
        .first()
    )
    if not fermentable:
        raise HTTPException(status_code=404, detail="Fermentable not found")
    return fermentable


@router.delete("/inventory/fermentables/{id}", response_model=schemas.InventoryFermentable)
async def delete_inventory_fermentable(id: int, db: Session = Depends(get_db)):
    fermentable = (
        db.query(models.InventoryFermentable).filter(models.InventoryFermentable.id == id).first()
    )
    if not fermentable:
        raise HTTPException(status_code=404, detail="Fermentable not found")
    db.delete(fermentable)
    db.commit()
    return fermentable
