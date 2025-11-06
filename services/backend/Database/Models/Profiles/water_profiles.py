from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class WaterProfiles(Base):
    """
    Description:

    This class represents the WaterProfile table in the database.

    The water profile NAME needs to be unique within a profile type.

    This model supports two types of water profiles:
    - Source water profiles (e.g., RO water, tap water, distilled water)
    - Target brewing profiles (e.g., style-specific profiles like Amber Balanced, Hoppy NEIPA)

    Relationships:

    - ONE water_profile can have ZERO or MANY recipes

    TODO: - ONE water_profile can have ZERO or MANY batches

    """

    __tablename__ = "water"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Profile categorization
    profile_type = Column(String(50), nullable=False, default='source')  # 'source' or 'target'
    style_category = Column(String(100), nullable=True)
    
    # Ion concentrations (ppm) - using Numeric for precise decimal values
    calcium = Column(Numeric(8, 2), nullable=False, default=0)
    magnesium = Column(Numeric(8, 2), nullable=False, default=0)
    sodium = Column(Numeric(8, 2), nullable=False, default=0)
    chloride = Column(Numeric(8, 2), nullable=False, default=0)
    sulfate = Column(Numeric(8, 2), nullable=False, default=0)
    bicarbonate = Column(Numeric(8, 2), nullable=False, default=0)
    
    # Additional water properties
    ph = Column(Numeric(4, 2), nullable=True)
    total_alkalinity = Column(Numeric(8, 2), nullable=True)
    residual_alkalinity = Column(Numeric(8, 2), nullable=True)
    
    # Legacy fields (kept for backward compatibility)
    version = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    display_amount = Column(String(255), nullable=True)
    inventory = Column(Integer, nullable=True)
    
    # Metadata
    is_default = Column(Boolean, nullable=False, default=False)
    is_custom = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("Recipes", back_populates="water_profiles")

# TODO: batch_id = Column(Integer, ForeignKey('batches.id'))
