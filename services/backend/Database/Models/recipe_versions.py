# services/backend/Database/Models/recipe_versions.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class RecipeVersion(Base):
    __tablename__ = "recipe_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    version_name = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Snapshot of recipe data at this version (JSON stored as text)
    recipe_snapshot = Column(Text, nullable=True)
    
    # Relationship to the main recipe
    recipe = relationship("Recipes", back_populates="versions")
