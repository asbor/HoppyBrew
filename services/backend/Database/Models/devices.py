from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Device(Base):
    """
    Description:

    This class represents the Device table in the database.
    It stores configuration for external brewing devices such as iSpindel and Tilt.

    The iSpindel is a smart hydrometer that measures specific gravity,
    temperature, and battery level during fermentation.
    
    The Tilt hydrometer is a Bluetooth device that monitors fermentation.

    Relationships:

    - ONE device can be associated with ZERO or ONE active batch
    - ONE device can have MANY fermentation readings

    Notes:
    - Device types include: ispindel, tilt, etc.
    - Configuration data is stored as JSON for flexibility
    - Calibration data is device-specific (e.g., polynomial coefficients for iSpindel)
    - Alert configuration stored as JSON with temperature thresholds
    """

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)  # ispindel, tilt, etc.
    description = Column(Text, nullable=True)
    api_endpoint = Column(String, nullable=True)  # Endpoint to receive data
    # DEPRECATED: Use api_token_encrypted
    api_token = Column(String, nullable=True)
    # Encrypted storage for API tokens
    api_token_encrypted = Column(Text, nullable=True)
    token_salt = Column(String(64), nullable=True)  # Salt for token encryption
    # Device-specific calibration
    calibration_data = Column(JSON, nullable=True)
    configuration = Column(JSON, nullable=True)  # Additional device settings
    alert_config = Column(JSON, nullable=True)  # Alert thresholds and settings
    is_active = Column(Boolean, default=True)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="SET NULL"), nullable=True)
    last_reading_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    batch = relationship("Batches", back_populates="devices")
    fermentation_readings = relationship("FermentationReadings", back_populates="device")
