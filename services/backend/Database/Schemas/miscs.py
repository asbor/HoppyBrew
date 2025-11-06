from pydantic import BaseModel, ConfigDict
from typing import Optional

MISC_BASE_EXAMPLE = {
    "name": "Irish Moss",
    "type": "Fining",
    "use": "Boil",
    "amount_is_weight": True,
    "use_for": "Wort clarification",
    "notes": "Add during the last 10 minutes of the boil.",
    "amount": 14,
    "time": 10,
    "display_amount": "14 g",
    "inventory": 240,
    "display_time": "10 min",
    "batch_size": 20,
}


class MiscBase(BaseModel):
    name: str
    type: Optional[str] = None
    use: Optional[str] = None
    amount_is_weight: Optional[bool] = None
    use_for: Optional[str] = None
    notes: Optional[str] = None
    amount: Optional[int] = None
    time: Optional[int] = None
    display_amount: Optional[str] = None
    inventory: Optional[int] = None
    display_time: Optional[str] = None
    batch_size: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,  # Pydantic v2: support ORM models
        json_schema_extra={"example": MISC_BASE_EXAMPLE}
    )


class RecipeMisc(MiscBase):
    recipe_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {**MISC_BASE_EXAMPLE, "recipe_id": 12}}
    )


class InventoryMiscBase(MiscBase):
    model_config = ConfigDict(
        json_schema_extra={"example": MISC_BASE_EXAMPLE}
    )


class InventoryMiscCreate(InventoryMiscBase):
    pass


class InventoryMisc(InventoryMiscBase):
    id: int
    batch_id: Optional[int] = None  # Allow batch_id to be None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {**MISC_BASE_EXAMPLE, "id": 15, "batch_id": 5}}
    )