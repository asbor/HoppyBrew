# services/backend/Database/Schemas/batch_ingredients.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BatchIngredientBase(BaseModel):
    """Base schema for batch ingredient"""
    batch_id: int
    inventory_item_id: int
    inventory_item_type: str  # 'hop', 'fermentable', 'yeast', 'misc'
    quantity_used: float
    unit: str


class BatchIngredientCreate(BatchIngredientBase):
    """Schema for creating a batch ingredient"""
    pass


class BatchIngredient(BatchIngredientBase):
    """Schema for batch ingredient with ID"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class InventoryTransactionBase(BaseModel):
    """Base schema for inventory transaction"""
    inventory_item_id: int
    inventory_item_type: str  # 'hop', 'fermentable', 'yeast', 'misc'
    transaction_type: str  # 'addition', 'consumption', 'adjustment'
    quantity_change: float
    quantity_before: float
    quantity_after: float
    unit: str
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    notes: Optional[str] = None
    created_by: Optional[str] = None


class InventoryTransactionCreate(InventoryTransactionBase):
    """Schema for creating an inventory transaction"""
    pass


class InventoryTransaction(InventoryTransactionBase):
    """Schema for inventory transaction with ID"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ConsumeIngredientsRequest(BaseModel):
    """Request schema for consuming ingredients for a batch"""
    ingredients: list[BatchIngredientCreate]


class IngredientTrackingResponse(BaseModel):
    """Response schema for ingredient tracking"""
    batch_id: int
    batch_name: str
    consumed_ingredients: list[BatchIngredient]
    transactions: list[InventoryTransaction]

    class Config:
        from_attributes = True


class InventoryAvailability(BaseModel):
    """Schema for checking inventory availability"""
    inventory_item_id: int
    inventory_item_type: str
    name: str
    available_quantity: float
    required_quantity: float
    unit: str
    is_available: bool
    warning_level: Optional[str] = None  # 'low_stock', 'out_of_stock', None
