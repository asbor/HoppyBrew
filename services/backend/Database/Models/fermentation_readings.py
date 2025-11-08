# services/backend/Database/Models/fermentation_readings.py

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Index, Text, String
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class FermentationReadings(Base):
    __tablename__ = "fermentation_readings"
    __table_args__ = (
        Index("ix_fermentation_readings_batch_id", "batch_id"),
        Index("ix_fermentation_readings_timestamp", "timestamp"),
        Index("ix_fermentation_readings_batch_timestamp", "batch_id", "timestamp"),
        Index("ix_fermentation_readings_device_id", "device_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(
        Integer,
        ForeignKey("batches.id", ondelete="CASCADE"),
        nullable=False,
    )
    device_id = Column(
        Integer,
        ForeignKey("devices.id", ondelete="SET NULL"),
        nullable=True,
    )
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    gravity = Column(Float, nullable=True)  # Specific gravity reading
    temperature = Column(Float, nullable=True)  # Temperature in Celsius or Fahrenheit
    ph = Column(Float, nullable=True)  # pH reading
    notes = Column(Text, nullable=True)  # User notes
    source = Column(String(50), nullable=True, default="manual")  # manual, tilt, ispindel, etc.
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # Relationships
    batch = relationship("Batches", back_populates="fermentation_readings")
    device = relationship("Device", back_populates="fermentation_readings")
