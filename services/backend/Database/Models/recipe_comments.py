# services/backend/Database/Models/recipe_comments.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class RecipeComment(Base):
    """
    Recipe comment model with threading support
    
    Allows users to comment on recipes and reply to other comments.
    Threading is supported via parent_id for nested conversations.
    """
    __tablename__ = "recipe_comments"
    __table_args__ = (
        Index("ix_recipe_comments_recipe_id", "recipe_id"),
        Index("ix_recipe_comments_user_id", "user_id"),
        Index("ix_recipe_comments_parent_id", "parent_id"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("recipe_comments.id", ondelete="CASCADE"), nullable=True)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    
    # Relationships
    recipe = relationship("Recipes", back_populates="comments")
    user = relationship("Users", back_populates="recipe_comments")
    parent = relationship(
        "RecipeComment",
        remote_side=[id],
        back_populates="replies"
    )
    replies = relationship(
        "RecipeComment",
        back_populates="parent",
        cascade="all, delete-orphan"
    )
