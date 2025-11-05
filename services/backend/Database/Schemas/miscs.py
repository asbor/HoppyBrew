from pydantic import BaseModel
from typing import Optional


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


class RecipeMisc(MiscBase):
    recipe_id: int

    class Config:
        orm_mode: bool = True


class InventoryMiscBase(MiscBase):
    pass


class InventoryMiscCreate(InventoryMiscBase):
    pass


class InventoryMisc(InventoryMiscBase):
    id: int
    batch_id: Optional[int] = None  # Allow batch_id to be None

    class Config:
        orm_mode: bool = True
