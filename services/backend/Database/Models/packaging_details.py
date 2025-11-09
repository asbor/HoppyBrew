# services/backend/Database/Models/packaging_details.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class PackagingDetails(Base):
    """
    Stores packaging information for batches (bottling/kegging details).
    """

    __tablename__ = "packaging_details"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(
        Integer,
        ForeignKey("batches.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    
    # Packaging method: 'bottle' or 'keg'
    method = Column(String(50), nullable=False)
    
    # Packaging date
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    # Carbonation details
    carbonation_method = Column(String(50), nullable=True)  # 'priming', 'forced', 'natural'
    volumes = Column(Float, nullable=True)  # Target CO2 volumes (e.g., 2.5)
    
    # Container information
    container_count = Column(Integer, nullable=True)  # Number of bottles/kegs
    container_size = Column(Float, nullable=True)  # Size in liters or gallons
    
    # Priming sugar details (for bottle conditioning)
    priming_sugar_type = Column(String(50), nullable=True)  # 'table', 'corn', 'dme', 'honey'
    priming_sugar_amount = Column(Float, nullable=True)  # Amount in grams
    
    # Kegging pressure details (for forced carbonation)
    carbonation_temp = Column(Float, nullable=True)  # Temperature in Fahrenheit
    carbonation_psi = Column(Float, nullable=True)  # PSI for kegging
    
    # Notes
    notes = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    batch = relationship("Batches", back_populates="packaging_details")
