from sqlalchemy import Column, Integer, String, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from database import Base


class Styles(Base):
    """
    Description:

    This class represents the actual target style of a recipe.

    Relationships:

    - ONE style can have ZERO or MANY recipes

    """

    __tablename__ = "styles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    version = Column(Integer, nullable=True)
    category = Column(String(255), nullable=True)
    category_number = Column(Integer, nullable=True)
    style_letter = Column(String(255), nullable=True)
    style_guide = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    og_min = Column(String(255), nullable=True)
    og_max = Column(String(255), nullable=True)
    fg_min = Column(String(255), nullable=True)
    fg_max = Column(String(255), nullable=True)
    ibu_min = Column(String(255), nullable=True)
    ibu_max = Column(String(255), nullable=True)
    color_min = Column(String(255), nullable=True)
    color_max = Column(String(255), nullable=True)
    carb_min = Column(String(255), nullable=True)
    carb_max = Column(String(255), nullable=True)
    abv_max = Column(String(255), nullable=True)
    abv_min = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    profile = Column(Text, nullable=True)
    ingredients = Column(Text, nullable=True)
    examples = Column(Text, nullable=True)
    display_og_min = Column(String(255), nullable=True)
    display_og_max = Column(String(255), nullable=True)
    display_fg_min = Column(String(255), nullable=True)
    display_fg_max = Column(String(255), nullable=True)
    display_color_min = Column(String(255), nullable=True)
    display_color_max = Column(String(255), nullable=True)
    og_range = Column(String(255), nullable=True)
    fg_range = Column(String(255), nullable=True)
    ibu_range = Column(String(255), nullable=True)
    carb_range = Column(String(255), nullable=True)
    color_range = Column(String(255), nullable=True)
    abv_range = Column(String(255), nullable=True)
    # Relationships

    recipe_id = Column(Integer, ForeignKey("recipes.id"), index=True)
    recipe = relationship("Recipes", back_populates="style_profile")


# TODO: batch_id = Column(Integer, ForeignKey('batches.id'))
