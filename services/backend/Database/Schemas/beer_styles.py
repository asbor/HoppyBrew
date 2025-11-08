from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class StyleGuidelineSourceBase(BaseModel):
    """Base schema for style guideline sources"""

    name: str
    year: Optional[int] = None
    abbreviation: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True


class StyleGuidelineSourceCreate(StyleGuidelineSourceBase):
    """Schema for creating a new style guideline source"""


class StyleGuidelineSourceUpdate(BaseModel):
    """Schema for updating a style guideline source"""

    name: Optional[str] = None
    year: Optional[int] = None
    abbreviation: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class StyleGuidelineSource(StyleGuidelineSourceBase):
    """Schema for style guideline source responses"""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StyleCategoryBase(BaseModel):
    """Base schema for style categories"""

    guideline_source_id: int
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    parent_category_id: Optional[int] = None


class StyleCategoryCreate(StyleCategoryBase):
    """Schema for creating a new style category"""


class StyleCategoryUpdate(BaseModel):
    """Schema for updating a style category"""

    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    parent_category_id: Optional[int] = None


class StyleCategory(StyleCategoryBase):
    """Schema for style category responses"""

    id: int

    model_config = ConfigDict(from_attributes=True)


class BeerStyleBase(BaseModel):
    """Base schema for beer styles"""

    guideline_source_id: Optional[int] = None
    category_id: Optional[int] = None
    name: str
    style_code: Optional[str] = None
    subcategory: Optional[str] = None

    # Basic Parameters
    abv_min: Optional[float] = None
    abv_max: Optional[float] = None
    og_min: Optional[float] = None
    og_max: Optional[float] = None
    fg_min: Optional[float] = None
    fg_max: Optional[float] = None
    ibu_min: Optional[int] = None
    ibu_max: Optional[int] = None
    color_min_ebc: Optional[float] = None
    color_max_ebc: Optional[float] = None
    color_min_srm: Optional[float] = None
    color_max_srm: Optional[float] = None

    # Descriptions
    description: Optional[str] = None
    aroma: Optional[str] = None
    appearance: Optional[str] = None
    flavor: Optional[str] = None
    mouthfeel: Optional[str] = None
    overall_impression: Optional[str] = None
    comments: Optional[str] = None
    history: Optional[str] = None
    ingredients: Optional[str] = None
    comparison: Optional[str] = None
    examples: Optional[str] = None

    is_custom: bool = False


class BeerStyleCreate(BeerStyleBase):
    """Schema for creating a new beer style"""


class BeerStyleUpdate(BaseModel):
    """Schema for updating a beer style"""

    guideline_source_id: Optional[int] = None
    category_id: Optional[int] = None
    name: Optional[str] = None
    style_code: Optional[str] = None
    subcategory: Optional[str] = None

    # Basic Parameters
    abv_min: Optional[float] = None
    abv_max: Optional[float] = None
    og_min: Optional[float] = None
    og_max: Optional[float] = None
    fg_min: Optional[float] = None
    fg_max: Optional[float] = None
    ibu_min: Optional[int] = None
    ibu_max: Optional[int] = None
    color_min_ebc: Optional[float] = None
    color_max_ebc: Optional[float] = None
    color_min_srm: Optional[float] = None
    color_max_srm: Optional[float] = None

    # Descriptions
    description: Optional[str] = None
    aroma: Optional[str] = None
    appearance: Optional[str] = None
    flavor: Optional[str] = None
    mouthfeel: Optional[str] = None
    overall_impression: Optional[str] = None
    comments: Optional[str] = None
    history: Optional[str] = None
    ingredients: Optional[str] = None
    comparison: Optional[str] = None
    examples: Optional[str] = None

    is_custom: Optional[bool] = None


class BeerStyle(BeerStyleBase):
    """Schema for beer style responses"""

    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BeerStyleSearch(BaseModel):
    """Schema for beer style search parameters"""

    query: Optional[str] = None
    guideline_source_id: Optional[int] = None
    category_id: Optional[int] = None
    abv_min: Optional[float] = None
    abv_max: Optional[float] = None
    ibu_min: Optional[int] = None
    ibu_max: Optional[int] = None
    color_min_srm: Optional[float] = None
    color_max_srm: Optional[float] = None
    is_custom: Optional[bool] = None
    limit: int = 100
    offset: int = 0
