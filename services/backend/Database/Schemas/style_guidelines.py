from pydantic import BaseModel
from typing import Optional

STYLE_GUIDELINE_EXAMPLE = {
    "block_heading": "21A - American IPA",
    "circle_image": "https://cdn.hoppybrew.io/styles/american-ipa.png",
    "category": "IPA",
    "color": "Gold to amber",
    "clarity": "Generally clear with possible hop haze.",
    "perceived_malt_and_aroma": "Low to medium maltiness supporting hop aroma.",
    "perceived_hop_and_aroma": "Citrus, fruit, and pine hop character dominates.",
    "perceived_bitterness": "Assertive but clean bitterness.",
    "fermentation_characteristics": "Clean fermentation profile with minimal esters.",
    "body": "Medium-light to medium body.",
    "additional_notes": "Dry hopping is common and expected.",
    "og": "1.056 - 1.070",
    "fg": "1.008 - 1.014",
    "abv": "5.5% - 7.5%",
    "ibu": "40 - 70",
    "ebc": "8 - 20",
}


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

    class Config:
        schema_extra = {"example": STYLE_GUIDELINE_EXAMPLE}


class StyleGuidelineBaseCreate(StyleGuidelineBase):
    class Config:
        schema_extra = {"example": STYLE_GUIDELINE_EXAMPLE}
