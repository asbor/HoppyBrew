from pydantic import BaseModel
from typing import Optional


class YeastBase(BaseModel):
    name: str
    type: Optional[str] = None
    form: Optional[str] = None
    amount: Optional[float] = None
    amount_is_weight: Optional[bool] = None
    laboratory: Optional[str] = None
    product_id: Optional[str] = None
    min_temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    flocculation: Optional[str] = None
    attenuation: Optional[float] = None
    notes: Optional[str] = None
    best_for: Optional[str] = None
    times_cultured: Optional[int] = None
    max_reuse: Optional[int] = None
    add_to_secondary: Optional[bool] = None


class RecipeYeast(YeastBase):
    recipe_id: int

    class Config:
        orm_mode: bool = True


class InventoryYeastBase(YeastBase):
    pass


class InventoryYeastCreate(InventoryYeastBase):
    pass


class InventoryYeast(InventoryYeastBase):
    id: int
    batch_id: Optional[int] = None  # Allow batch_id to be None

    class Config:
        orm_mode: bool = True
