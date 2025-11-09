"""
Yeast Management Models for tracking yeast strains, viability, harvesting, and generations.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class YeastStrain(Base):
    """
    Master database of yeast strains with detailed characteristics.
    This is the reference database that inventory yeasts link to.
    """
    __tablename__ = "yeast_strains"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    laboratory = Column(String, nullable=True)
    product_id = Column(String, nullable=True, index=True)
    type = Column(String, nullable=True)  # Ale, Lager, Wine, Champagne, etc.
    form = Column(String, nullable=True)  # Liquid, Dry, Slant, Culture
    
    # Temperature ranges
    min_temperature = Column(Float, nullable=True)
    max_temperature = Column(Float, nullable=True)
    
    # Performance characteristics
    flocculation = Column(String, nullable=True)  # Low, Medium, High, Very High
    attenuation_min = Column(Float, nullable=True)  # Minimum attenuation %
    attenuation_max = Column(Float, nullable=True)  # Maximum attenuation %
    alcohol_tolerance = Column(Float, nullable=True)  # ABV %
    
    # Usage info
    best_for = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Reuse characteristics
    max_reuse = Column(Integer, nullable=True, default=5)
    
    # Viability characteristics (days)
    viability_days_dry = Column(Integer, nullable=True, default=1095)  # ~3 years for dry
    viability_days_liquid = Column(Integer, nullable=True, default=180)  # ~6 months for liquid
    viability_days_slant = Column(Integer, nullable=True, default=730)  # ~2 years for slant
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # Relationships
    inventory_items = relationship("InventoryYeast", back_populates="strain")


class YeastHarvest(Base):
    """
    Tracks yeast harvesting operations and propagation history.
    """
    __tablename__ = "yeast_harvests"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Source information
    source_batch_id = Column(Integer, ForeignKey("batches.id"), nullable=True)
    source_inventory_id = Column(Integer, nullable=True)  # Source inventory yeast
    yeast_strain_id = Column(Integer, ForeignKey("yeast_strains.id"), nullable=False)
    
    # Harvest details
    harvest_date = Column(DateTime, default=datetime.now, nullable=False)
    generation = Column(Integer, nullable=False, default=1)  # Generation number
    parent_harvest_id = Column(Integer, ForeignKey("yeast_harvests.id"), nullable=True)
    
    # Quantity harvested
    quantity_harvested = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False, default="ml")  # ml, g, cells
    
    # Viability tracking
    viability_at_harvest = Column(Float, nullable=True)  # Percentage 0-100
    cell_count = Column(Float, nullable=True)  # billion cells
    
    # Storage info
    storage_method = Column(String, nullable=True)  # refrigerated, frozen, slant, etc.
    storage_temperature = Column(Float, nullable=True)  # Celsius
    
    # Status
    status = Column(String, nullable=False, default="active")  # active, used, discarded
    used_date = Column(DateTime, nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # Relationships
    source_batch = relationship("Batches", foreign_keys=[source_batch_id])
    yeast_strain = relationship("YeastStrain")
    parent_harvest = relationship("YeastHarvest", remote_side=[id], foreign_keys=[parent_harvest_id])
    child_harvests = relationship("YeastHarvest", foreign_keys=[parent_harvest_id], remote_side=[parent_harvest_id])
