# services/backend/Database/Models/quality_control_tests.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class QualityControlTest(Base):
    """
    Quality Control Test results for batches.
    Stores test results, BJCP scores, tasting notes, and appearance photos.
    """

    __tablename__ = "quality_control_tests"
    __table_args__ = (
        Index("ix_qc_tests_batch_id", "batch_id"),
        Index("ix_qc_tests_test_date", "test_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(
        Integer,
        ForeignKey("batches.id", ondelete="CASCADE"),
        nullable=False,
    )
    test_date = Column(DateTime, nullable=False, default=datetime.now)
    
    # Measured values
    final_gravity = Column(Float, nullable=True)  # Specific gravity
    abv_actual = Column(Float, nullable=True)  # Actual ABV%
    color = Column(String(50), nullable=True)  # Color description or SRM value
    clarity = Column(String(50), nullable=True)  # e.g., "Clear", "Slight Haze", "Opaque"
    
    # Tasting notes
    taste_notes = Column(Text, nullable=True)
    aroma_notes = Column(Text, nullable=True)
    appearance_notes = Column(Text, nullable=True)
    flavor_notes = Column(Text, nullable=True)
    mouthfeel_notes = Column(Text, nullable=True)
    
    # BJCP Scoring (0-50 scale)
    score = Column(Float, nullable=True)  # Overall score
    aroma_score = Column(Float, nullable=True)  # Max 12 points
    appearance_score = Column(Float, nullable=True)  # Max 3 points
    flavor_score = Column(Float, nullable=True)  # Max 20 points
    mouthfeel_score = Column(Float, nullable=True)  # Max 5 points
    overall_impression_score = Column(Float, nullable=True)  # Max 10 points
    
    # Photo storage
    photo_path = Column(String(500), nullable=True)  # Path to stored photo
    
    # Additional metadata
    tester_name = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)  # General notes
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    batch = relationship("Batches", back_populates="quality_control_tests")
