# services/backend/Database/Schemas/quality_control_tests.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class QualityControlTestBase(BaseModel):
    """Base schema for Quality Control Test"""
    
    test_date: datetime = Field(default_factory=datetime.now)
    final_gravity: Optional[float] = Field(None, ge=0.990, le=1.200, description="Final specific gravity")
    abv_actual: Optional[float] = Field(None, ge=0, le=20, description="Actual ABV percentage")
    color: Optional[str] = Field(None, max_length=50, description="Color description or SRM value")
    clarity: Optional[str] = Field(None, max_length=50, description="Clarity description")
    
    # Tasting notes
    taste_notes: Optional[str] = None
    aroma_notes: Optional[str] = None
    appearance_notes: Optional[str] = None
    flavor_notes: Optional[str] = None
    mouthfeel_notes: Optional[str] = None
    
    # BJCP Scoring
    score: Optional[float] = Field(None, ge=0, le=50, description="Overall BJCP score (0-50)")
    aroma_score: Optional[float] = Field(None, ge=0, le=12, description="Aroma score (0-12)")
    appearance_score: Optional[float] = Field(None, ge=0, le=3, description="Appearance score (0-3)")
    flavor_score: Optional[float] = Field(None, ge=0, le=20, description="Flavor score (0-20)")
    mouthfeel_score: Optional[float] = Field(None, ge=0, le=5, description="Mouthfeel score (0-5)")
    overall_impression_score: Optional[float] = Field(None, ge=0, le=10, description="Overall impression score (0-10)")
    
    tester_name: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class QualityControlTestCreate(QualityControlTestBase):
    """Schema for creating a Quality Control Test"""
    
    batch_id: int = Field(..., description="ID of the batch being tested")


class QualityControlTestUpdate(QualityControlTestBase):
    """Schema for updating a Quality Control Test"""
    
    test_date: Optional[datetime] = None


class QualityControlTest(QualityControlTestBase):
    """Schema for returning a Quality Control Test"""
    
    id: int
    batch_id: int
    photo_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class QualityControlTestWithBatch(QualityControlTest):
    """Schema for QC Test with batch information"""
    
    batch_name: Optional[str] = None
    batch_number: Optional[int] = None


# BJCP Score calculation helper
class BJCPScoreCalculation(BaseModel):
    """Helper schema for BJCP score calculation"""
    
    aroma_score: float = Field(..., ge=0, le=12)
    appearance_score: float = Field(..., ge=0, le=3)
    flavor_score: float = Field(..., ge=0, le=20)
    mouthfeel_score: float = Field(..., ge=0, le=5)
    overall_impression_score: float = Field(..., ge=0, le=10)
    
    @property
    def total_score(self) -> float:
        """Calculate total BJCP score"""
        return (
            self.aroma_score +
            self.appearance_score +
            self.flavor_score +
            self.mouthfeel_score +
            self.overall_impression_score
        )
    
    @property
    def score_category(self) -> str:
        """Get score category based on BJCP guidelines"""
        total = self.total_score
        if total >= 45:
            return "Outstanding"
        elif total >= 38:
            return "Excellent"
        elif total >= 30:
            return "Very Good"
        elif total >= 21:
            return "Good"
        elif total >= 14:
            return "Fair"
        else:
            return "Problematic"


# Tasting note template
class TastingNoteTemplate(BaseModel):
    """Template for structured tasting notes"""
    
    name: str
    aroma_prompts: list[str]
    appearance_prompts: list[str]
    flavor_prompts: list[str]
    mouthfeel_prompts: list[str]
    overall_prompts: list[str]


# Example templates
TASTING_NOTE_TEMPLATES = {
    "bjcp_standard": TastingNoteTemplate(
        name="BJCP Standard",
        aroma_prompts=[
            "Malt character (intensity, quality)",
            "Hop aroma (intensity, quality, character)",
            "Fermentation character (esters, phenols)",
            "Other aromatics"
        ],
        appearance_prompts=[
            "Color (SRM or description)",
            "Clarity (brilliant, clear, slight haze, hazy, opaque)",
            "Head (size, retention, color, texture)"
        ],
        flavor_prompts=[
            "Malt flavor (intensity, quality)",
            "Hop flavor (intensity, quality, character)",
            "Bitterness (level, quality)",
            "Balance",
            "Finish and aftertaste",
            "Fermentation character"
        ],
        mouthfeel_prompts=[
            "Body (light, medium, full)",
            "Carbonation (low, medium, high)",
            "Warmth (alcohol)",
            "Creaminess, astringency, or other sensations"
        ],
        overall_prompts=[
            "Harmony and balance",
            "Drinkability",
            "Style accuracy",
            "Overall impression"
        ]
    ),
    "simple": TastingNoteTemplate(
        name="Simple",
        aroma_prompts=["What do you smell?", "Any off-aromas?"],
        appearance_prompts=["Color?", "Clarity?", "Head retention?"],
        flavor_prompts=["First impression?", "Main flavors?", "Finish?"],
        mouthfeel_prompts=["Body?", "Carbonation?"],
        overall_prompts=["Would you brew this again?", "Overall thoughts?"]
    )
}
