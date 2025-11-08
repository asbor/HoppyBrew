from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Text,
    Numeric,
    DateTime,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class StyleCategory(Base):
    """
    Represents hierarchical beer style categories

    Relationships:
    - ONE category can have MANY sub-categories (self-referential)
    - ONE category can have MANY beer styles
    - ONE category belongs to ONE guideline source
    """

    __tablename__ = "style_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    guideline_source_id = Column(
        Integer, ForeignKey("style_guideline_sources.id"), nullable=False
    )
    name = Column(String(255), nullable=False)
    code = Column(String(20), nullable=True)  # e.g., "1", "21", etc.
    description = Column(Text, nullable=True)
    parent_category_id = Column(
        Integer, ForeignKey("style_categories.id"), nullable=True
    )

    # Relationships
    guideline_source = relationship("StyleGuidelineSource", back_populates="categories")
    parent_category = relationship(
        "StyleCategory", remote_side=[id], backref="subcategories"
    )
    beer_styles = relationship("BeerStyle", back_populates="category")

    __table_args__ = (
        Index("idx_category_guideline", "guideline_source_id"),
        Index("idx_category_parent", "parent_category_id"),
        Index("idx_category_code", "code"),
    )


class BeerStyle(Base):
    """
    Comprehensive beer style information based on BJCP and other guidelines

    Relationships:
    - ONE style belongs to ONE guideline source
    - ONE style belongs to ONE category
    - ONE style can be associated with MANY recipes
    """

    __tablename__ = "beer_styles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    guideline_source_id = Column(
        Integer, ForeignKey("style_guideline_sources.id"), nullable=True
    )
    category_id = Column(Integer, ForeignKey("style_categories.id"), nullable=True)

    # Basic Information
    name = Column(String(255), nullable=False)
    style_code = Column(String(20), nullable=True)  # e.g., "21A"
    subcategory = Column(String(100), nullable=True)

    # Basic Parameters with proper numeric types
    abv_min = Column(Numeric(4, 2), nullable=True)
    abv_max = Column(Numeric(4, 2), nullable=True)
    og_min = Column(Numeric(5, 3), nullable=True)
    og_max = Column(Numeric(5, 3), nullable=True)
    fg_min = Column(Numeric(5, 3), nullable=True)
    fg_max = Column(Numeric(5, 3), nullable=True)
    ibu_min = Column(Integer, nullable=True)
    ibu_max = Column(Integer, nullable=True)
    color_min_ebc = Column(Numeric(6, 2), nullable=True)
    color_max_ebc = Column(Numeric(6, 2), nullable=True)
    color_min_srm = Column(Numeric(6, 2), nullable=True)
    color_max_srm = Column(Numeric(6, 2), nullable=True)

    # Detailed Descriptions
    description = Column(Text, nullable=True)
    aroma = Column(Text, nullable=True)
    appearance = Column(Text, nullable=True)
    flavor = Column(Text, nullable=True)
    mouthfeel = Column(Text, nullable=True)
    overall_impression = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    history = Column(Text, nullable=True)
    ingredients = Column(Text, nullable=True)
    comparison = Column(Text, nullable=True)
    examples = Column(Text, nullable=True)  # Comma-separated commercial examples

    # Metadata
    is_custom = Column(Boolean, default=False)
    created_by = Column(Integer, nullable=True)  # user reference (future)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    guideline_source = relationship(
        "StyleGuidelineSource", back_populates="beer_styles"
    )
    category = relationship("StyleCategory", back_populates="beer_styles")

    __table_args__ = (
        Index("idx_beer_style_name", "name"),
        Index("idx_beer_style_code", "style_code"),
        Index("idx_beer_style_guideline", "guideline_source_id"),
        Index("idx_beer_style_category", "category_id"),
        Index("idx_beer_style_custom", "is_custom"),
        Index("idx_beer_style_abv", "abv_min", "abv_max"),
        Index("idx_beer_style_ibu", "ibu_min", "ibu_max"),
    )
