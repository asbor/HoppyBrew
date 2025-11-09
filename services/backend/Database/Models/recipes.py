# services/backend/Database/Models/recipes.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Index, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class RecipeVisibility(enum.Enum):
    """Recipe visibility options"""
    private = "private"
    public = "public"
    unlisted = "unlisted"  # Public but not in listings


class Recipes(Base):
    __tablename__ = "recipes"
    __table_args__ = (
        Index("ix_recipes_origin_recipe_id", "origin_recipe_id"),
        Index("ix_recipes_name_version", "name", "version"),
        Index("ix_recipes_user_id", "user_id"),
        Index("ix_recipes_visibility", "visibility"),
    )
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_batch = Column(Boolean, default=False)
    origin_recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    visibility = Column(Enum(RecipeVisibility), default=RecipeVisibility.private, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True
    )
    origin_recipe = relationship(
        "Recipes",
        remote_side=[id],
        back_populates="derived_recipes",
    )
    derived_recipes = relationship(
        "Recipes",
        back_populates="origin_recipe",
        cascade="all, delete-orphan",
    )
    version = Column(Integer)
    type = Column(String)
    brewer = Column(String)
    asst_brewer = Column(String)
    batch_size = Column(Float)
    boil_size = Column(Float)
    boil_time = Column(Integer)
    efficiency = Column(Float)
    notes = Column(String)
    taste_notes = Column(String)
    taste_rating = Column(Integer)
    og = Column(Float)
    fg = Column(Float)
    fermentation_stages = Column(Integer)
    primary_age = Column(Integer)
    primary_temp = Column(Float)
    secondary_age = Column(Integer)
    secondary_temp = Column(Float)
    tertiary_age = Column(Integer)
    age = Column(Integer)
    age_temp = Column(Float)
    carbonation_used = Column(String)
    est_og = Column(Float)
    est_fg = Column(Float)
    est_color = Column(Float)
    ibu = Column(Float)
    ibu_method = Column(String)
    est_abv = Column(Float)
    abv = Column(Float)
    actual_efficiency = Column(Float)
    calories = Column(Float)
    display_batch_size = Column(String)
    display_boil_size = Column(String)
    display_og = Column(String)
    display_fg = Column(String)
    display_primary_temp = Column(String)
    display_secondary_temp = Column(String)
    display_tertiary_temp = Column(String)
    display_age_temp = Column(String)
    hops = relationship(
        "RecipeHop",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    fermentables = relationship(
        "RecipeFermentable",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    yeasts = relationship(
        "RecipeYeast",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    miscs = relationship(
        "RecipeMisc",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    batches = relationship(
        "Batches",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    style_guideline = relationship(
        "StyleGuidelines",
        back_populates="recipe",
        uselist=False,
        cascade="all, delete-orphan",
    )
    style_profile = relationship(
        "Styles",
        back_populates="recipe",
        uselist=False,
        cascade="all, delete-orphan",
    )
    equipment_profiles = relationship(
        "EquipmentProfiles",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    water_profiles = relationship(
        "WaterProfiles",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    versions = relationship(
        "RecipeVersion",
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeVersion.version_number.desc()",
    )
    # Community features relationships
    owner = relationship("Users", back_populates="recipes")
    ratings = relationship(
        "RecipeRating",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    comments = relationship(
        "RecipeComment",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
    stars = relationship(
        "RecipeStar",
        back_populates="recipe",
        cascade="all, delete-orphan",
    )
