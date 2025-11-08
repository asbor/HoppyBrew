from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

FERMENTABLE_BASE_EXAMPLE = {
    "name": "Pilsner Malt",
    "type": "Grain",
    "yield_": 80.0,
    "color": 2,
    "origin": "Germany",
    "supplier": "Weyermann",
    "notes": "Light-bodied base malt ideal for lagers.",
    "potential": 1.037,
    "amount": 4.5,
    "cost_per_unit": 1.25,
    "manufacturing_date": "2024-01-15",
    "expiry_date": "2025-01-15",
    "lot_number": "LOT-20240115",
    "exclude_from_total": False,
    "not_fermentable": False,
    "description": "Highly modified malt delivering a clean malt backbone.",
    "substitutes": "German Pils, Bohemian Pilsner",
    "used_in": "Hoppy Lager",
}

INVENTORY_FERMENTABLE_EXAMPLE = {
    **FERMENTABLE_BASE_EXAMPLE,
    "alpha": 0.0,
    "beta": 0.0,
    "form": "Grain",
    "use": "Mash",
    "amount_is_weight": True,
    "product_id": "MALT-PLS-001",
    "min_temperature": 10.0,
    "max_temperature": 25.0,
    "flocculation": None,
    "attenuation": None,
    "max_reuse": None,
    "inventory": 18.0,
    "display_amount": "4.5 kg",
    "display_time": "Mash",
    "batch_size": 20.0,
}


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

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": FERMENTABLE_BASE_EXAMPLE},
    )


class RecipeFermentable(FermentableBase):
    recipe_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {**FERMENTABLE_BASE_EXAMPLE, "recipe_id": 12}},
    )


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

    model_config = ConfigDict(
        json_schema_extra={"example": INVENTORY_FERMENTABLE_EXAMPLE}
    )


class InventoryFermentableCreate(InventoryFermentableBase):
    pass


class InventoryFermentable(InventoryFermentableBase):
    id: int
    batch_id: Optional[int] = None  # Allow batch_id to be None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {**INVENTORY_FERMENTABLE_EXAMPLE, "id": 3, "batch_id": 7}
        },
    )
