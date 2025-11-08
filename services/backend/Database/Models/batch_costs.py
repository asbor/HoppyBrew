# services/backend/Database/Models/batch_costs.py

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class BatchCost(Base):
    """Track all costs associated with a batch including ingredients and utilities"""

    __tablename__ = "batch_costs"
    __table_args__ = (
        Index("ix_batch_costs_batch_id", "batch_id"),
        Index("ix_batch_costs_created_at", "created_at"),
    )

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    
    # Ingredient costs (calculated from batch ingredients)
    fermentables_cost = Column(Float, default=0.0, nullable=False)
    hops_cost = Column(Float, default=0.0, nullable=False)
    yeasts_cost = Column(Float, default=0.0, nullable=False)
    miscs_cost = Column(Float, default=0.0, nullable=False)
    
    # Utility costs
    electricity_cost = Column(Float, default=0.0, nullable=False)
    water_cost = Column(Float, default=0.0, nullable=False)
    gas_cost = Column(Float, default=0.0, nullable=False)
    other_utility_cost = Column(Float, default=0.0, nullable=False)
    
    # Other costs
    labor_cost = Column(Float, default=0.0, nullable=False)
    packaging_cost = Column(Float, default=0.0, nullable=False)
    other_cost = Column(Float, default=0.0, nullable=False)
    
    # Total and per-unit calculations
    total_cost = Column(Float, default=0.0, nullable=False)
    cost_per_liter = Column(Float, default=0.0, nullable=False)
    cost_per_pint = Column(Float, default=0.0, nullable=False)
    
    # Profit analysis
    target_price_per_pint = Column(Float, nullable=True)
    profit_margin = Column(Float, nullable=True)
    
    # Metadata
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # Relationships
    batch = relationship("Batches", back_populates="batch_cost")


class UtilityCostConfig(Base):
    """Store utility cost rates for calculations"""

    __tablename__ = "utility_cost_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    
    # Cost rates per unit
    electricity_rate_per_kwh = Column(Float, nullable=True)  # Cost per kWh
    water_rate_per_liter = Column(Float, nullable=True)  # Cost per liter
    gas_rate_per_unit = Column(Float, nullable=True)  # Cost per unit (cubic meter, etc.)
    
    # Average consumption per batch (for quick calculations)
    avg_electricity_kwh_per_batch = Column(Float, nullable=True)
    avg_water_liters_per_batch = Column(Float, nullable=True)
    avg_gas_units_per_batch = Column(Float, nullable=True)
    
    # Metadata
    currency = Column(String, default="USD", nullable=False)
    is_active = Column(Integer, default=1, nullable=False)  # Use as boolean (1=True, 0=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
