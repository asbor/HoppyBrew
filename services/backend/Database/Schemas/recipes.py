# Database/Schemas/recipes_hops.py

from pydantic import BaseModel, Field
from typing import List, Optional
from .hops import HopBase
from .fermentables import FermentableBase
from .miscs import MiscBase
from .yeasts import YeastBase


class RecipeBase(BaseModel):
    name: str
    version: Optional[int] = None
    type: Optional[str] = None
    brewer: Optional[str] = None
    asst_brewer: Optional[str] = None
    batch_size: Optional[float] = None
    boil_size: Optional[float] = None
    boil_time: Optional[int] = None
    efficiency: Optional[float] = None
    notes: Optional[str] = None
    taste_notes: Optional[str] = None
    taste_rating: Optional[int] = None
    og: Optional[float] = None
    fg: Optional[float] = None
    fermentation_stages: Optional[int] = None
    primary_age: Optional[int] = None
    primary_temp: Optional[float] = None
    secondary_age: Optional[int] = None
    secondary_temp: Optional[float] = None
    tertiary_age: Optional[int] = None
    age: Optional[int] = None
    age_temp: Optional[float] = None
    carbonation_used: Optional[str] = None
    est_og: Optional[float] = None
    est_fg: Optional[float] = None
    est_color: Optional[float] = None
    ibu: Optional[float] = None
    ibu_method: Optional[str] = None
    est_abv: Optional[float] = None
    abv: Optional[float] = None
    actual_efficiency: Optional[float] = None
    calories: Optional[float] = None
    display_batch_size: Optional[str] = None
    display_boil_size: Optional[str] = None
    display_og: Optional[str] = None
    display_fg: Optional[str] = None
    display_primary_temp: Optional[str] = None
    display_secondary_temp: Optional[str] = None
    display_tertiary_temp: Optional[str] = None
    display_age_temp: Optional[str] = None
    # List of objects for each ingredient type
    hops: List[HopBase] = Field(default_factory=list)
    fermentables: List[FermentableBase] = Field(default_factory=list)
    miscs: List[MiscBase] = Field(default_factory=list)
    yeasts: List[YeastBase] = Field(default_factory=list)


class Recipe(RecipeBase):
    id: int
    is_batch: Optional[bool] = False
    origin_recipe_id: Optional[int] = None

    class Config:
        orm_mode = True
