# services/backend/Database/Models/recipe_ratings.py

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class RecipeRating(Base):
    """
    Recipe rating and review model
    
    Allows users to rate recipes and leave reviews.
    Ratings are on a scale of 1-5 stars.
    """
    __tablename__ = "recipe_ratings"
    __table_args__ = (
        Index("ix_recipe_ratings_recipe_id", "recipe_id"),
        Index("ix_recipe_ratings_user_id", "user_id"),
        Index("ix_recipe_ratings_user_recipe", "user_id", "recipe_id", unique=True),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Float, nullable=False)  # 1-5 stars
    review_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    
    # Relationships
    recipe = relationship("Recipes", back_populates="ratings")
    user = relationship("Users", back_populates="recipe_ratings")
