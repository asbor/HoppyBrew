from pydantic import BaseModel, ConfigDict
from typing import Optional

YEAST_BASE_EXAMPLE = {
    "name": "SafAle US-05",
    "type": "Ale",
    "form": "Dry",
    "amount": 11.5,
    "amount_is_weight": True,
    "laboratory": "Fermentis",
    "product_id": "US-05",
    "min_temperature": 18.0,
    "max_temperature": 28.0,
    "flocculation": "Medium",
    "attenuation": 78.0,
    "notes": "Clean fermenting American ale yeast with neutral profile.",
    "best_for": "American pale ales and IPAs",
    "times_cultured": 3,
    "max_reuse": 5,
    "add_to_secondary": False,
}


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

    model_config = ConfigDict(
        from_attributes=True,  # Pydantic v2: support ORM models
        json_schema_extra={"example": YEAST_BASE_EXAMPLE}
    )


class RecipeYeast(YeastBase):
    recipe_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {**YEAST_BASE_EXAMPLE, "recipe_id": 12}}
    )


class InventoryYeastBase(YeastBase):
    model_config = ConfigDict(
        json_schema_extra={"example": YEAST_BASE_EXAMPLE}
    )


class InventoryYeastCreate(InventoryYeastBase):
    pass


class InventoryYeast(InventoryYeastBase):
    id: int
    batch_id: Optional[int] = None  # Allow batch_id to be None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {**YEAST_BASE_EXAMPLE, "id": 22, "batch_id": 5}}
    )