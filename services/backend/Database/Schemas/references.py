from pydantic import BaseModel
from typing import Optional
from datetime import datetime

REFERENCE_BASE_EXAMPLE = {
    "name": "Water Chemistry Primer",
    "url": "https://example.com/water-chemistry-primer",
    "description": "Guidelines for adjusting brewing water profiles.",
    "category": "Education",
    "favicon_url": "https://example.com/favicon.ico",
}


class ReferenceBase(BaseModel):
    name: str
    url: str
    description: Optional[str] = None
    category: Optional[str] = None
    favicon_url: Optional[str] = None

    class Config:
        schema_extra = {"example": REFERENCE_BASE_EXAMPLE}


class ReferenceCreate(ReferenceBase):
    class Config:
        schema_extra = {"example": REFERENCE_BASE_EXAMPLE}


class ReferenceUpdate(ReferenceBase):
    class Config:
        schema_extra = {"example": REFERENCE_BASE_EXAMPLE}


class ReferenceInDBBase(ReferenceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                **REFERENCE_BASE_EXAMPLE,
                "id": 8,
                "created_at": "2024-03-01T10:00:00Z",
                "updated_at": "2024-03-15T09:30:00Z",
            }
        }


class Reference(ReferenceInDBBase):
    pass
