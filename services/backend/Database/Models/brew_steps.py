# services/backend/Database/Models/brew_steps.py

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class BrewSteps(Base):
    __tablename__ = "brew_steps"
    __table_args__ = (
        Index("ix_brew_steps_batch_id", "batch_id"),
        Index("ix_brew_steps_completed", "completed"),
    )
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(
        Integer,
        ForeignKey("batches.id", ondelete="CASCADE"),
        nullable=False,
    )
    step_name = Column(String(100), nullable=False)
    step_type = Column(String(50), nullable=False)  # mash, boil, hop_addition, chill, transfer, etc.
    duration = Column(Integer, nullable=True)  # Duration in minutes
    temperature = Column(Integer, nullable=True)  # Temperature if applicable (for mash steps)
    notes = Column(String, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    order_index = Column(Integer, nullable=False, default=0)  # Order of steps

    # Relationships
    batch = relationship("Batches", back_populates="brew_steps")
