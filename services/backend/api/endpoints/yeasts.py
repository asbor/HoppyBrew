# api/endpoints/yeasts.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List

router = APIRouter()

# Recipe Yeasts Endpoints


@router.get("/recipes/yeasts", response_model=List[schemas.RecipeYeast])
async def get_all_recipe_yeasts(db: Session = Depends(get_db)):
    yeasts = db.query(models.RecipeYeast).all()
    return yeasts

# Inventory Yeasts Endpoints


@router.get("/inventory/yeasts", response_model=List[schemas.InventoryYeast])
async def get_all_inventory_yeasts(db: Session = Depends(get_db)):
    yeasts = db.query(models.InventoryYeast).all()
    return yeasts


@router.get(
    "/inventory/yeasts/{yeast_id}", response_model=schemas.InventoryYeast
)
async def get_inventory_yeast(yeast_id: int, db: Session = Depends(get_db)):
    yeast = (
        db.query(models.InventoryYeast)
        .filter(models.InventoryYeast.id == yeast_id)
        .first()
    )
    if not yeast:
        raise HTTPException(status_code=404, detail="Yeast not found")
    return yeast


@router.delete("/inventory/yeasts/{id}", response_model=schemas.InventoryYeast)
async def delete_inventory_yeast(id: int, db: Session = Depends(get_db)):
    yeast = (
        db.query(models.InventoryYeast)
        .filter(models.InventoryYeast.id == id)
        .first()
    )
    if not yeast:
        raise HTTPException(status_code=404, detail="Yeast not found")
    db.delete(yeast)
    db.commit()
    return yeast
