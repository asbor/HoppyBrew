# services/backend/Database/Models/batches.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from Database.enums import BatchStatus as BatchStatusEnum


class Batches(Base):
    __tablename__ = "batches"
    __table_args__ = (
        Index("ix_batches_recipe_id", "recipe_id"),
        Index("ix_batches_recipe_id_batch_number", "recipe_id", "batch_number"),
        Index("ix_batches_status", "status"),
    )
    id = Column(Integer, primary_key=True, index=True)
    batch_name = Column(String, nullable=False)
    batch_number = Column(Integer, nullable=False)
    batch_size = Column(Float, nullable=False)
    status = Column(String(50), default=BatchStatusEnum.PLANNING.value, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    brewer = Column(String, nullable=False)
    brew_date = Column(DateTime, nullable=False)
    # Relationships:

    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id"),
        nullable=False,
    )
    recipe = relationship("Recipes", back_populates="batches")
    batch_log = relationship(
        "BatchLogs",
        back_populates="batch",
        uselist=False,
        cascade="all, delete-orphan",
    )
    workflow_history = relationship(
        "BatchWorkflowHistory",
        back_populates="batch",
        cascade="all, delete-orphan",
        order_by="BatchWorkflowHistory.changed_at.desc()",
    )
    inventory_fermentables = relationship(
        "InventoryFermentable",
        back_populates="batch",
        cascade="all, delete-orphan",
    )
    inventory_hops = relationship(
        "InventoryHop",
        back_populates="batch",
        cascade="all, delete-orphan",
    )
    inventory_miscs = relationship(
        "InventoryMisc",
        back_populates="batch",
        cascade="all, delete-orphan",
    )
    inventory_yeasts = relationship(
        "InventoryYeast",
        back_populates="batch",
        cascade="all, delete-orphan",
    )
    fermentation_readings = relationship(
        "FermentationReadings",
        back_populates="batch",
        cascade="all, delete-orphan",
        order_by="FermentationReadings.timestamp",
    )
    batch_ingredients = relationship(
        "BatchIngredient",
        back_populates="batch",
        cascade="all, delete-orphan",
    )
