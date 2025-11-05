from pydantic import BaseModel
from typing import Optional
from datetime import date


class FermentableBase(BaseModel):
    name: str
    type: Optional[str] = None
    yield_: Optional[float] = None
    color: Optional[int] = None
    origin: Optional[str] = None
    supplier: Optional[str] = None
    notes: Optional[str] = None
    potential: Optional[float] = None  # Change to float
    amount: Optional[float] = None
    cost_per_unit: Optional[float] = None
    manufacturing_date: Optional[date] = None
    expiry_date: Optional[date] = None
    lot_number: Optional[str] = None
    exclude_from_total: Optional[bool] = None
    not_fermentable: Optional[bool] = None
    description: Optional[str] = None
    substitutes: Optional[str] = None
    used_in: Optional[str] = None


class RecipeFermentable(FermentableBase):
    recipe_id: int

    class Config:
        orm_mode: bool = True


class InventoryFermentableBase(FermentableBase):
    alpha: Optional[float] = None  # Specific to hops
    beta: Optional[float] = None  # Specific to hops
    form: Optional[str] = None  # Specific to hops
    use: Optional[str] = None  # Specific to hops and miscs
    amount_is_weight: Optional[bool] = None  # Specific to miscs and yeasts
    product_id: Optional[str] = None  # Specific to yeasts
    min_temperature: Optional[float] = None  # Specific to yeasts
    max_temperature: Optional[float] = None  # Specific to yeasts
    flocculation: Optional[str] = None  # Specific to yeasts
    attenuation: Optional[float] = None  # Specific to yeasts
    max_reuse: Optional[int] = None  # Specific to yeasts
    inventory: Optional[float] = None  # Specific to all
    display_amount: Optional[str] = None  # Specific to all
    display_time: Optional[str] = None  # Specific to all
    batch_size: Optional[float] = None  # Specific to miscs


class InventoryFermentableCreate(InventoryFermentableBase):
    pass


class InventoryFermentable(InventoryFermentableBase):
    id: int
    batch_id: Optional[int] = None  # Allow batch_id to be None

    class Config:
        orm_mode: bool = True
