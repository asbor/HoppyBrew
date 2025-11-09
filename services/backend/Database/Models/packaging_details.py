# services/backend/Database/Models/packaging_details.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class PackagingDetails(Base):
    __tablename__ = "packaging_details"
    __table_args__ = (
        Index("ix_packaging_details_batch_id", "batch_id"),
        Index("ix_packaging_details_date", "packaging_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(
        Integer,
        ForeignKey("batches.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # One packaging record per batch
    )
    packaging_date = Column(DateTime, nullable=False)
    method = Column(String(50), nullable=False)  # 'bottling' or 'kegging'
    carbonation_method = Column(String(50), nullable=False)  # 'priming_sugar', 'forced', 'natural'
    volumes_co2 = Column(Float, nullable=True)  # Target CO2 volumes
    container_count = Column(Integer, nullable=True)  # Number of bottles or kegs
    container_size = Column(Float, nullable=True)  # Size in liters or gallons
    priming_sugar_amount = Column(Float, nullable=True)  # Grams of priming sugar (for bottling)
    priming_sugar_type = Column(String(50), nullable=True)  # 'table', 'corn', 'dme', 'honey'
    pressure_psi = Column(Float, nullable=True)  # PSI for kegging
    temperature = Column(Float, nullable=True)  # Temperature at packaging (Fahrenheit)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationship to Batches
    batch = relationship("Batches", back_populates="packaging_details")
