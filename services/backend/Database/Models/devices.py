from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from database import Base


class Device(Base):
    """
    Description:
    
    This class represents the Device table in the database.
    It stores configuration for external brewing devices such as iSpindel.
    
    The iSpindel is a smart hydrometer that measures specific gravity,
    temperature, and battery level during fermentation.
    
    Relationships:
    
    - ONE device can be associated with ZERO or MANY batches
    
    Notes:
    - Device types include: ispindel, tilt, etc.
    - Configuration data is stored as JSON for flexibility
    - Calibration data is device-specific (e.g., polynomial coefficients for iSpindel)
    """

    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)  # ispindel, tilt, etc.
    description = Column(Text, nullable=True)
    api_endpoint = Column(String, nullable=True)  # Endpoint to receive data
    api_token = Column(String, nullable=True)  # Authentication token if needed
    calibration_data = Column(JSON, nullable=True)  # Device-specific calibration
    configuration = Column(JSON, nullable=True)  # Additional device settings
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
