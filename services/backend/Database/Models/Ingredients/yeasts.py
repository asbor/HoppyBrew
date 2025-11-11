from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base


class RecipeYeast(Base):
    __tablename__ = "recipe_yeasts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    version = Column(Integer, nullable=True)
    type = Column(String, nullable=True)
    form = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    amount_is_weight = Column(Boolean, nullable=True)
    laboratory = Column(String, nullable=True)
    product_id = Column(String, nullable=True)
    min_temperature = Column(Float, nullable=True)
    max_temperature = Column(Float, nullable=True)
    flocculation = Column(String, nullable=True)
    attenuation = Column(Float, nullable=True)
    notes = Column(String, nullable=True)
    best_for = Column(String, nullable=True)
    times_cultured = Column(Integer, nullable=True)
    max_reuse = Column(Integer, nullable=True)
    add_to_secondary = Column(Boolean, nullable=True)
    stage = Column(String, nullable=True)  # mash/boil/fermentation
    duration = Column(Integer, nullable=True)  # duration in minutes
    display_amount = Column(String, nullable=True)
    disp_min_temp = Column(String, nullable=True)
    disp_max_temp = Column(String, nullable=True)
    inventory = Column(String, nullable=True)
    culture_date = Column(String, nullable=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipes", back_populates="yeasts")


class InventoryYeast(Base):
    __tablename__ = "inventory_yeasts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    form = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    amount_is_weight = Column(Boolean, nullable=True)
    laboratory = Column(String, nullable=True)
    product_id = Column(String, nullable=True)
    min_temperature = Column(Float, nullable=True)
    max_temperature = Column(Float, nullable=True)
    flocculation = Column(String, nullable=True)
    attenuation = Column(Float, nullable=True)
    notes = Column(String, nullable=True)
    best_for = Column(String, nullable=True)
    times_cultured = Column(Integer, nullable=True)
    max_reuse = Column(Integer, nullable=True)
    add_to_secondary = Column(Boolean, nullable=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))

    # Yeast management fields
    yeast_strain_id = Column(Integer, ForeignKey("yeast_strains.id"), nullable=True)
    manufacture_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    generation = Column(Integer, nullable=True, default=0)  # 0 for commercial, >0 for harvested
    harvest_id = Column(Integer, ForeignKey("yeast_harvests.id"), nullable=True)
    current_viability = Column(Float, nullable=True)  # Percentage 0-100
    last_viability_check = Column(DateTime, nullable=True)

    # Relationships
    batch = relationship("Batches", back_populates="inventory_yeasts")
    strain = relationship("YeastStrain", back_populates="inventory_items")
    harvest = relationship("YeastHarvest", foreign_keys=[harvest_id])
