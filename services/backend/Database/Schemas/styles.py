from pydantic import BaseModel, ConfigDict
from typing import Optional

STYLE_BASE_EXAMPLE = {
    "name": "American IPA",
    "version": 1,
    "category": "IPA",
    "category_number": 21,
    "style_letter": "A",
    "style_guide": "BJCP 2021",
    "type": "Ale",
    "og_min": "1.056",
    "og_max": "1.070",
    "fg_min": "1.008",
    "fg_max": "1.014",
    "ibu_min": "40",
    "ibu_max": "70",
    "color_min": "6",
    "color_max": "14",
    "carb_min": "2.2",
    "carb_max": "2.7",
    "abv_min": "5.5",
    "abv_max": "7.5",
    "notes": "Showcases hop flavor and bitterness backed by clean malt.",
    "profile": "Prominent American hop character with clean fermentation.",
    "ingredients": "American hops, American or English ale yeast, clean base malt.",
    "examples": "Russian River Blind Pig, Bell's Two Hearted Ale",
    "display_og_min": "1.056",
    "display_og_max": "1.070",
    "display_fg_min": "1.008",
    "display_fg_max": "1.014",
    "display_color_min": "6 SRM",
    "display_color_max": "14 SRM",
    "og_range": "1.056 - 1.070",
    "fg_range": "1.008 - 1.014",
    "ibu_range": "40 - 70",
    "carb_range": "2.2 - 2.7",
    "color_range": "6 - 14 SRM",
    "abv_range": "5.5% - 7.5%",
}


class StyleBase(BaseModel):
    """
    Description:

    This class represents the actual style of a beer.

    Use cases:

    - Validate the data of a new Style object

    - Validate the data of a Style object to be updated

    """

    name: str
    version: Optional[int] = None
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

    model_config = ConfigDict(
        from_attributes=True,# Pydantic v2: support ORM models
        json_schema_extra={"example": STYLE_BASE_EXAMPLE}
    )


class Style(StyleBase):
    """Style schema with ID for responses"""
    id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,# Pydantic v2: support ORM models
        json_schema_extra={"example": {**STYLE_BASE_EXAMPLE, "id": 1}}
    )