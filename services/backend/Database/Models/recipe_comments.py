# services/backend/Database/Models/recipe_comments.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class RecipeComment(Base):
    """
    Comment threads for recipes.
    Supports nested comments via parent_comment_id for threaded discussions.
    """
    __tablename__ = "recipe_comments"
    __table_args__ = (
        Index('ix_recipe_comments_recipe_id', 'recipe_id'),
        Index('ix_recipe_comments_user_id', 'user_id'),
        Index('ix_recipe_comments_parent_id', 'parent_comment_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    comment_text = Column(Text, nullable=False)
    parent_comment_id = Column(Integer, ForeignKey("recipe_comments.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("Users", backref="comments")
    recipe = relationship("Recipes", back_populates="comments")
    parent_comment = relationship("RecipeComment", remote_side=[id], backref="replies")
