from pydantic import BaseModel
from typing import Optional

HOP_BASE_EXAMPLE = {
    "name": "Cascade",
    "origin": "USA",
    "alpha": 5.5,
    "type": "Aroma",
    "form": "Pellet",
    "beta": 6.0,
    "hsi": 15.0,
    "amount": 28.0,
    "use": "Boil",
    "time": 60,
    "notes": "Classic citrus and grapefruit aroma.",
    "display_amount": "28 g",
    "inventory": "4.5 kg",
    "display_time": "60 min",
}


class HopBase(BaseModel):
    name: str
    origin: Optional[str] = None
    alpha: Optional[float] = None
    type: Optional[str] = None
    form: Optional[str] = None
    beta: Optional[float] = None
    hsi: Optional[float] = None
    amount: Optional[float] = None
    use: Optional[str] = None
    time: Optional[int] = None
    notes: Optional[str] = None
    display_amount: Optional[str] = None
    inventory: Optional[str] = None
    display_time: Optional[str] = None

    class Config:
        schema_extra = {"example": HOP_BASE_EXAMPLE}


class RecipeHop(HopBase):
    recipe_id: int

    class Config:
        orm_mode = True
        schema_extra = {"example": {**HOP_BASE_EXAMPLE, "recipe_id": 1}}


class InventoryHopBase(HopBase):
    class Config:
        schema_extra = {"example": HOP_BASE_EXAMPLE}


class InventoryHopCreate(InventoryHopBase):
    pass


class InventoryHop(InventoryHopBase):
    id: int
    batch_id: Optional[int] = None  # Allow batch_id to be None

    class Config:
        orm_mode = True
        schema_extra = {"example": {**HOP_BASE_EXAMPLE, "id": 7, "batch_id": 3}}
