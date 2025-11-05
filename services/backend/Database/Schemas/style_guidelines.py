from pydantic import BaseModel
from typing import Optional


class StyleGuidelineBase(BaseModel):
    block_heading: str
    circle_image: str
    category: str
    color: Optional[str] = None
    clarity: Optional[str] = None
    perceived_malt_and_aroma: Optional[str] = None
    perceived_hop_and_aroma: Optional[str] = None
    perceived_bitterness: Optional[str] = None
    fermentation_characteristics: Optional[str] = None
    body: Optional[str] = None
    additional_notes: Optional[str] = None
    og: Optional[str] = None
    fg: Optional[str] = None
    abv: Optional[str] = None
    ibu: Optional[str] = None
    ebc: Optional[str] = None


class StyleGuidelineBaseCreate(StyleGuidelineBase):
    pass
