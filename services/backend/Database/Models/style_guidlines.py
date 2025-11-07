from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class StyleGuidelineSource(Base):
    """
    Represents different style guideline sources (BJCP, Brewers Association, etc.)

    Relationships:
    - ONE guideline source can have MANY categories
    - ONE guideline source can have MANY beer styles
    """

    __tablename__ = "style_guideline_sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # e.g., "BJCP 2021", "Brewers Association 2025"
    year = Column(Integer, nullable=True)
    abbreviation = Column(String(20), nullable=True)  # e.g., "BJCP", "BA"
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    categories = relationship(
        "StyleCategory", back_populates="guideline_source", cascade="all, delete-orphan"
    )
    beer_styles = relationship("BeerStyle", back_populates="guideline_source")

    __table_args__ = (
        Index("idx_guideline_source_name", "name"),
        Index("idx_guideline_source_active", "is_active"),
    )


class StyleGuidelines(Base):
    """
    Legacy class for backwards compatibility.
    This represents the style guidelines provided by the BJCP.
    """

    __tablename__ = "style_guidelines"
    id = Column(Integer, primary_key=True, autoincrement=True)
    block_heading = Column(String(255), nullable=True)
    circle_image = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    color = Column(String(255), nullable=True)
    clarity = Column(String(255), nullable=True)
    perceived_malt_and_aroma = Column(Text, nullable=True)
    perceived_hop_and_aroma = Column(Text, nullable=True)
    perceived_bitterness = Column(Text, nullable=True)
    fermentation_characteristics = Column(Text, nullable=True)
    body = Column(String(255), nullable=True)
    additional_notes = Column(Text, nullable=True)
    # Vitals

    og = Column(String(255), nullable=True)
    fg = Column(String(255), nullable=True)
    abv = Column(String(255), nullable=True)
    ibu = Column(String(255), nullable=True)
    ebc = Column(String(255), nullable=True)

    # Legacy relationship - kept for backward compatibility
    recipe_id = Column(Integer, ForeignKey("recipes.id"), index=True)
    recipe = relationship("Recipes", back_populates="style_guideline")
