# Database/Schemas/recipe_versions.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class RecipeVersionBase(BaseModel):
    version_name: Optional[str] = None
    notes: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "version_name": "v1.2 - Increased hop profile",
                "notes": "Adjusted Cascade addition from 1.5 oz to 2.0 oz for more citrus character"
            }
        }
    )


class RecipeVersionCreate(RecipeVersionBase):
    pass


class RecipeVersion(RecipeVersionBase):
    id: int
    recipe_id: int
    version_number: int
    created_at: datetime
    recipe_snapshot: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 42,
                "recipe_id": 7,
                "version_number": 2,
                "version_name": "v1.2 - Increased hop profile",
                "notes": "Adjusted Cascade addition from 1.5 oz to 2.0 oz for more citrus character",
                "created_at": "2024-03-15T10:30:00Z",
                "recipe_snapshot": '{"name":"Test Recipe","version":2,...}'
            }
        }
    )
