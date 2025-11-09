# services/backend/Database/Schemas/quality_control_tests.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class QualityControlTestBase(BaseModel):
    batch_id: int
    test_date: datetime = Field(default_factory=datetime.now)
    final_gravity: Optional[float] = None
    abv_actual: Optional[float] = None
    color: Optional[str] = None
    clarity: Optional[str] = None
    taste_notes: Optional[str] = None
    score: Optional[float] = Field(None, ge=0, le=50)  # BJCP score 0-50
    photo_url: Optional[str] = None


class QualityControlTestCreate(QualityControlTestBase):
    pass


class QualityControlTestUpdate(BaseModel):
    test_date: Optional[datetime] = None
    final_gravity: Optional[float] = None
    abv_actual: Optional[float] = None
    color: Optional[str] = None
    clarity: Optional[str] = None
    taste_notes: Optional[str] = None
    score: Optional[float] = Field(None, ge=0, le=50)
    photo_url: Optional[str] = None


class QualityControlTest(QualityControlTestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BJCPScoreInput(BaseModel):
    """Input for BJCP score calculation"""
    aroma: float = Field(..., ge=0, le=12)  # Max 12 points
    appearance: float = Field(..., ge=0, le=3)  # Max 3 points
    flavor: float = Field(..., ge=0, le=20)  # Max 20 points
    mouthfeel: float = Field(..., ge=0, le=5)  # Max 5 points
    overall_impression: float = Field(..., ge=0, le=10)  # Max 10 points


class BJCPScoreResult(BaseModel):
    """Result of BJCP score calculation"""
    total_score: float
    aroma: float
    appearance: float
    flavor: float
    mouthfeel: float
    overall_impression: float
    rating: str  # Outstanding, Excellent, Very Good, Good, Fair, Problematic, Flawed
