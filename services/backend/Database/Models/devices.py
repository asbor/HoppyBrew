from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Index
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

    The Tilt is a Bluetooth hydrometer and thermometer that logs data to
    your smartphone or cloud services.

    Relationships:

    - ONE device can be associated with ONE batch (current fermentation)
    - ONE device can create MANY fermentation readings

    Notes:
    - Device types include: ispindel, tilt, etc.
    - Configuration data is stored as JSON for flexibility
    - Calibration data is device-specific (e.g., polynomial coefficients for iSpindel)
    - Alert configuration stores temperature thresholds and notification settings
    """

    __tablename__ = "devices"
    __table_args__ = (
        Index("ix_devices_batch_id", "batch_id"),
    )

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
    is_active = Column(Boolean, default=True)
    
    # Batch association
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="SET NULL"), nullable=True)
    
    # Auto-import settings
    auto_import_enabled = Column(Boolean, default=True, nullable=False)
    import_interval_seconds = Column(Integer, default=900, nullable=False)  # 15 minutes
    last_import_at = Column(DateTime(timezone=True), nullable=True)
    
    # Alert configuration
    alert_config = Column(JSON, nullable=True)  # {temp_min, temp_max, gravity_alert, etc.}
    
    # Manual override
    manual_override = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    batch = relationship("Batches", back_populates="devices")
    fermentation_readings = relationship("FermentationReadings", back_populates="device")
