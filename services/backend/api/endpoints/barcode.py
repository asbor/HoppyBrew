# api/endpoints/barcode.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Union

import Database.Models as models
import Database.Schemas as schemas
from database import get_db

router = APIRouter()


@router.get("/inventory/barcode/{barcode}")
async def lookup_by_barcode(barcode: str, db: Session = Depends(get_db)):
    """
    Look up an inventory item by its barcode.
    Returns the item with its type and details.
    """
    # Search in all inventory tables
    hop = db.query(models.InventoryHop).filter(models.InventoryHop.barcode == barcode).first()
    if hop:
        return {
            "type": "hop",
            "item": schemas.InventoryHop.model_validate(hop).model_dump()
        }

    fermentable = db.query(models.InventoryFermentable).filter(
        models.InventoryFermentable.barcode == barcode
    ).first()
    if fermentable:
        return {
            "type": "fermentable",
            "item": schemas.InventoryFermentable.model_validate(fermentable).model_dump()
        }

    yeast = db.query(models.InventoryYeast).filter(
        models.InventoryYeast.barcode == barcode
    ).first()
    if yeast:
        return {
            "type": "yeast",
            "item": schemas.InventoryYeast.model_validate(yeast).model_dump()
        }

    misc = db.query(models.InventoryMisc).filter(
        models.InventoryMisc.barcode == barcode
    ).first()
    if misc:
        return {
            "type": "misc",
            "item": schemas.InventoryMisc.model_validate(misc).model_dump()
        }

    raise HTTPException(status_code=404, detail="No inventory item found with this barcode")


@router.put("/inventory/{item_type}/{item_id}/barcode")
async def update_barcode(
    item_type: str,
    item_id: int,
    barcode: Optional[str],
    db: Session = Depends(get_db)
):
    """
    Update or set the barcode for an inventory item.
    item_type: 'hop', 'fermentable', 'yeast', or 'misc'
    barcode: The barcode value (or null to remove)
    """
    # Validate barcode uniqueness across all inventory types if setting a new one
    if barcode:
        existing = None
        if item_type != "hop":
            existing = db.query(models.InventoryHop).filter(
                models.InventoryHop.barcode == barcode
            ).first()
        if not existing and item_type != "fermentable":
            existing = db.query(models.InventoryFermentable).filter(
                models.InventoryFermentable.barcode == barcode
            ).first()
        if not existing and item_type != "yeast":
            existing = db.query(models.InventoryYeast).filter(
                models.InventoryYeast.barcode == barcode
            ).first()
        if not existing and item_type != "misc":
            existing = db.query(models.InventoryMisc).filter(
                models.InventoryMisc.barcode == barcode
            ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Barcode already in use by another inventory item"
            )

    # Update the appropriate inventory item
    if item_type == "hop":
        item = db.query(models.InventoryHop).filter(models.InventoryHop.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Hop not found")
        item.barcode = barcode
        db.commit()
        db.refresh(item)
        return schemas.InventoryHop.model_validate(item)

    elif item_type == "fermentable":
        item = db.query(models.InventoryFermentable).filter(
            models.InventoryFermentable.id == item_id
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail="Fermentable not found")
        item.barcode = barcode
        db.commit()
        db.refresh(item)
        return schemas.InventoryFermentable.model_validate(item)

    elif item_type == "yeast":
        item = db.query(models.InventoryYeast).filter(
            models.InventoryYeast.id == item_id
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail="Yeast not found")
        item.barcode = barcode
        db.commit()
        db.refresh(item)
        return schemas.InventoryYeast.model_validate(item)

    elif item_type == "misc":
        item = db.query(models.InventoryMisc).filter(
            models.InventoryMisc.id == item_id
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail="Misc item not found")
        item.barcode = barcode
        db.commit()
        db.refresh(item)
        return schemas.InventoryMisc.model_validate(item)

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid item_type. Must be 'hop', 'fermentable', 'yeast', or 'misc'"
        )
