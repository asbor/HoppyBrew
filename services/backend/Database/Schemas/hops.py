from pydantic import BaseModel, ConfigDict
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
    barcode: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"example": HOP_BASE_EXAMPLE}
    )


class RecipeHopBase(HopBase):
    """Schema for recipe hops with additional fields"""

    stage: Optional[str] = None  # mash/boil/fermentation
    duration: Optional[int] = None  # duration in minutes


class RecipeHop(RecipeHopBase):
    id: int
    recipe_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {**HOP_BASE_EXAMPLE, "id": 1, "recipe_id": 1}},
    )


class InventoryHopBase(HopBase):
    model_config = ConfigDict(json_schema_extra={"example": HOP_BASE_EXAMPLE})


class InventoryHopCreate(InventoryHopBase):
    pass


class InventoryHop(InventoryHopBase):
    id: int
    batch_id: Optional[int] = None  # Allow batch_id to be None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {**HOP_BASE_EXAMPLE, "id": 7, "batch_id": 3}},
    )
