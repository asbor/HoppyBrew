# services/backend/Database/Models/batch_costs.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class BatchCost(Base):
    """Track costs associated with a brewing batch."""

    __tablename__ = "batch_costs"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False, unique=True)

    # Ingredient costs
    fermentables_cost = Column(Float, default=0.0, nullable=False)
    hops_cost = Column(Float, default=0.0, nullable=False)
    yeasts_cost = Column(Float, default=0.0, nullable=False)
    miscs_cost = Column(Float, default=0.0, nullable=False)

    # Utility costs
    electricity_cost = Column(Float, default=0.0, nullable=False)
    water_cost = Column(Float, default=0.0, nullable=False)
    gas_cost = Column(Float, default=0.0, nullable=False)

    # Other costs
    labor_cost = Column(Float, default=0.0, nullable=False)
    packaging_cost = Column(Float, default=0.0, nullable=False)
    other_cost = Column(Float, default=0.0, nullable=False)

    # Sales information
    expected_yield_volume = Column(Float, nullable=True)  # Volume in liters
    selling_price_per_unit = Column(Float, nullable=True)  # Price per pint/liter
    unit_type = Column(
        String, default="pint", nullable=False
    )  # 'pint', 'liter', 'bottle', etc.

    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    # Relationships
    batch = relationship("Batches", back_populates="batch_cost")
