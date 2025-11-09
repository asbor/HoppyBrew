# services/backend/Database/Models/recipe_ratings.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class RecipeRating(Base):
    """
    Recipe rating and review system.
    Users can rate recipes on a 1-5 star scale and leave reviews.
    One rating per user per recipe (enforced by unique constraint).
    """
    __tablename__ = "recipe_ratings"
    __table_args__ = (
        UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe_rating'),
        Index('ix_recipe_ratings_recipe_id', 'recipe_id'),
        Index('ix_recipe_ratings_user_id', 'user_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Float, nullable=False)  # 1-5 stars, can have decimals
    review_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("Users", backref="ratings")
    recipe = relationship("Recipes", back_populates="ratings")
