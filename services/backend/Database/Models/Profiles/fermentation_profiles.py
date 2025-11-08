from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DECIMAL,
    TIMESTAMP,
    text,
)
from sqlalchemy.orm import relationship
from database import Base


class FermentationProfiles(Base):
    """
    Description:

    This class represents the FermentationProfile table in the database.

    The fermentation profile NAME needs to be unique.

    Relationships:

    - ONE fermentation_profile can have ZERO or MANY fermentation_steps
    - ONE fermentation_profile can have ZERO or MANY recipes
    - ONE fermentation_profile can have ZERO or MANY batches

    """

    __tablename__ = "fermentation_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    is_pressurized = Column(Boolean, default=False)
    is_template = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    # Relationships
    steps = relationship(
        "FermentationSteps",
        back_populates="profile",
        cascade="all, delete-orphan",
        order_by="FermentationSteps.step_order",
    )


class FermentationSteps(Base):
    """
    Description:

    This class represents the FermentationStep table in the database.

    Relationships:

    - ONE fermentation_step belongs to ONE fermentation_profile

    """

    __tablename__ = "fermentation_steps"

    id = Column(Integer, primary_key=True, index=True)
    fermentation_profile_id = Column(
        Integer,
        ForeignKey("fermentation_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    step_order = Column(Integer, nullable=False)
    name = Column(String(255), nullable=True)
    step_type = Column(String(50), default="primary")
    temperature = Column(DECIMAL(5, 2), nullable=True)
    duration_days = Column(Integer, nullable=True)
    ramp_days = Column(Integer, default=0)
    pressure_psi = Column(DECIMAL(5, 2), nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )

    # Relationships
    profile = relationship("FermentationProfiles", back_populates="steps")
