from pydantic import BaseModel
from typing import Optional


class StyleBase(BaseModel):
    """
    Description:

    This class represents the actual style of a beer.

    Use cases:

    - Validate the data of a new Style object

    - Validate the data of a Style object to be updated

    """

    name: str
    version: int
    category: Optional[str] = None
    category_number: Optional[int] = None
    style_letter: Optional[str] = None
    style_guide: Optional[str] = None
    type: Optional[str] = None
    og_min: Optional[str] = None
    og_max: Optional[str] = None
    fg_min: Optional[str] = None
    fg_max: Optional[str] = None
    ibu_min: Optional[str] = None
    ibu_max: Optional[str] = None
    color_min: Optional[str] = None
    color_max: Optional[str] = None
    carb_min: Optional[str] = None
    carb_max: Optional[str] = None
    abv_max: Optional[str] = None
    abv_min: Optional[str] = None
    notes: Optional[str] = None
    profile: Optional[str] = None
    ingredients: Optional[str] = None
    examples: Optional[str] = None
    display_og_min: Optional[str] = None
    display_og_max: Optional[str] = None
    display_fg_min: Optional[str] = None
    display_fg_max: Optional[str] = None
    display_color_min: Optional[str] = None
    display_color_max: Optional[str] = None
    og_range: Optional[str] = None
    fg_range: Optional[str] = None
    ibu_range: Optional[str] = None
    carb_range: Optional[str] = None
    color_range: Optional[str] = None
    abv_range: Optional[str] = None
