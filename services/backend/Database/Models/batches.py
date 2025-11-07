# services/backend/Database/Models/batches.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Index, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum


class BatchStatus(str, enum.Enum):
    """Batch workflow status enum"""
    PLANNING = "planning"
    BREW_DAY = "brew_day"
    PRIMARY_FERMENTATION = "primary_fermentation"
    SECONDARY_FERMENTATION = "secondary_fermentation"
    CONDITIONING = "conditioning"
    PACKAGED = "packaged"
    COMPLETED = "completed"
    ARCHIVED = "archived"


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
    status = Column(
        String(50),
        default='planning',
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime,
                        default=datetime.now,
                        onupdate=datetime.now)
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
