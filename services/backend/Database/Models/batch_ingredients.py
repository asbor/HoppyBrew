# services/backend/Database/Models/batch_ingredients.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class BatchIngredient(Base):
    """
    Tracks ingredient consumption for each batch.
    Links batches to inventory items with quantity used.
    """
    __tablename__ = "batch_ingredients"
    __table_args__ = (
        Index("ix_batch_ingredients_batch_id", "batch_id"),
        Index("ix_batch_ingredients_inventory_item_id", "inventory_item_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="CASCADE"), nullable=False)
    inventory_item_id = Column(Integer, nullable=False)  # ID from inventory table
    inventory_item_type = Column(String(50), nullable=False)  # 'hop', 'fermentable', 'yeast', 'misc'
    quantity_used = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)  # 'kg', 'g', 'L', 'ml', etc.
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # Relationships
    batch = relationship("Batches", back_populates="batch_ingredients")


class InventoryTransaction(Base):
    """
    Audit trail for all inventory changes.
    Tracks stock additions, consumption, and adjustments.
    """
    __tablename__ = "inventory_transactions"
    __table_args__ = (
        Index("ix_inventory_transactions_item_id", "inventory_item_id"),
        Index("ix_inventory_transactions_created_at", "created_at"),
        Index("ix_inventory_transactions_transaction_type", "transaction_type"),
    )

    id = Column(Integer, primary_key=True, index=True)
    inventory_item_id = Column(Integer, nullable=False)
    inventory_item_type = Column(String(50), nullable=False)  # 'hop', 'fermentable', 'yeast', 'misc'
    transaction_type = Column(String(50), nullable=False)  # 'addition', 'consumption', 'adjustment'
    quantity_change = Column(Float, nullable=False)  # Positive for addition, negative for consumption
    quantity_before = Column(Float, nullable=False)
    quantity_after = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    reference_type = Column(String(50), nullable=True)  # 'batch', 'manual', etc.
    reference_id = Column(Integer, nullable=True)  # ID of related entity (e.g., batch_id)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    created_by = Column(String, nullable=True)  # User who made the transaction
