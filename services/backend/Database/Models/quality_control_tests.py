# services/backend/Database/Models/quality_control_tests.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class QualityControlTest(Base):
    __tablename__ = "quality_control_tests"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(
        Integer,
        ForeignKey("batches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    test_date = Column(DateTime, nullable=False, default=datetime.now)
    
    # Measurements
    final_gravity = Column(Float, nullable=True)
    abv_actual = Column(Float, nullable=True)
    color = Column(String(100), nullable=True)  # e.g., "Golden", "Amber", "Dark"
    clarity = Column(String(100), nullable=True)  # e.g., "Clear", "Hazy", "Cloudy"
    
    # Tasting notes
    taste_notes = Column(Text, nullable=True)
    
    # BJCP score (0-50 scale)
    score = Column(Float, nullable=True)
    
    # Photo storage (file path or URL)
    photo_url = Column(String(500), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    batch = relationship("Batches", back_populates="quality_control_tests")
