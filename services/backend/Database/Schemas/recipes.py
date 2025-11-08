# Database/Schemas/recipes_hops.py

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from .hops import RecipeHopBase, RecipeHop
from .fermentables import RecipeFermentableBase, RecipeFermentable
from .miscs import RecipeMiscBase, RecipeMisc
from .yeasts import RecipeYeastBase, RecipeYeast


RECIPE_SAMPLE_HOP = {
    "name": "Cascade",
    "origin": "USA",
    "alpha": 5.5,
    "form": "Pellet",
    "use": "Boil",
    "time": 60,
}

RECIPE_SAMPLE_FERMENTABLE = {
    "name": "Pilsner Malt",
    "type": "Grain",
    "amount": 4.5,
    "yield_": 80.0,
    "color": 2,
}

RECIPE_SAMPLE_MISC = {
    "name": "Irish Moss",
    "type": "Fining",
    "use": "Boil",
    "amount": 14,
    "time": 10,
}

RECIPE_SAMPLE_YEAST = {
    "name": "SafAle US-05",
    "type": "Ale",
    "form": "Dry",
    "attenuation": 78.0,
}

RECIPE_BASE_EXAMPLE = {
    "name": "Citrus IPA",
    "version": 1,
    "type": "All Grain",
    "brewer": "Alex Brewer",
    "batch_size": 20.0,
    "boil_size": 25.0,
    "boil_time": 60,
    "ibu_method": "Tinseth",
    "ibu": 65.0,
    "est_abv": 6.4,
    "notes": "Target a juicy hop profile with balanced bitterness.",
    "display_batch_size": "20 L",
    "display_boil_size": "25 L",
    "hops": [RECIPE_SAMPLE_HOP],
    "fermentables": [RECIPE_SAMPLE_FERMENTABLE],
    "miscs": [RECIPE_SAMPLE_MISC],
    "yeasts": [RECIPE_SAMPLE_YEAST],
}

RECIPE_SCALE_REQUEST_EXAMPLE = {
    "target_batch_size": 40.0,
    "target_boil_size": 50.0,
}

RECIPE_SCALE_RESPONSE_EXAMPLE = {
    "original_batch_size": 20.0,
    "target_batch_size": 40.0,
    "scale_factor": 2.0,
    "scaled_recipe": {
        **RECIPE_BASE_EXAMPLE,
        "id": 42,
        "batch_size": 40.0,
        "boil_size": 50.0,
    },
    "metrics": {"abv": 6.4, "ibu": 65.0, "srm": 8.0},
}


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
    hops: List[RecipeHopBase] = Field(default_factory=list)
    fermentables: List[RecipeFermentableBase] = Field(default_factory=list)
    miscs: List[RecipeMiscBase] = Field(default_factory=list)
    yeasts: List[RecipeYeastBase] = Field(default_factory=list)

    model_config = ConfigDict(json_schema_extra={"example": RECIPE_BASE_EXAMPLE})


class Recipe(RecipeBase):
    id: int
    is_batch: Optional[bool] = False
    origin_recipe_id: Optional[int] = None
    # Override with full schemas that include IDs
    hops: List[RecipeHop] = Field(default_factory=list)
    fermentables: List[RecipeFermentable] = Field(default_factory=list)
    miscs: List[RecipeMisc] = Field(default_factory=list)
    yeasts: List[RecipeYeast] = Field(default_factory=list)

    model_config = ConfigDict(
        from_attributes=True,  # Pydantic v2: renamed from orm_mode
        json_schema_extra={
            "example": {
                **RECIPE_BASE_EXAMPLE,
                "id": 42,
                "is_batch": False,
                "origin_recipe_id": None,
            }
        },
    )


class RecipeMetrics(BaseModel):
    abv: Optional[float] = None
    ibu: Optional[float] = None
    srm: Optional[float] = None


class RecipeScaleRequest(BaseModel):
    target_batch_size: float = Field(..., gt=0)
    target_boil_size: Optional[float] = Field(None, gt=0)

    model_config = ConfigDict(
        json_schema_extra={"example": RECIPE_SCALE_REQUEST_EXAMPLE}
    )


class RecipeScaleResponse(BaseModel):
    original_batch_size: float
    target_batch_size: float
    scale_factor: float
    scaled_recipe: Recipe
    metrics: RecipeMetrics

    model_config = ConfigDict(
        json_schema_extra={"example": RECIPE_SCALE_RESPONSE_EXAMPLE}
    )
