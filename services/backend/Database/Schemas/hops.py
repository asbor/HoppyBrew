from pydantic import BaseModel
from typing import Optional


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


class RecipeHop(HopBase):
    recipe_id: int

    class Config:
        orm_mode: bool = True


class InventoryHopBase(HopBase):
    pass


class InventoryHopCreate(InventoryHopBase):
    pass


class InventoryHop(InventoryHopBase):
    id: int
    batch_id: Optional[int] = None  # Allow batch_id to be None

    class Config:
        orm_mode: bool = True
