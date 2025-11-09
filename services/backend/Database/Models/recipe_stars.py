# services/backend/Database/Models/recipe_stars.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class RecipeStar(Base):
    """
    Recipe star/favorite model
    
    Allows users to star/favorite recipes for easy access later.
    """
    __tablename__ = "recipe_stars"
    __table_args__ = (
        Index("ix_recipe_stars_recipe_id", "recipe_id"),
        Index("ix_recipe_stars_user_id", "user_id"),
        Index("ix_recipe_stars_user_recipe", "user_id", "recipe_id", unique=True),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    recipe = relationship("Recipes", back_populates="stars")
    user = relationship("Users", back_populates="starred_recipes")
