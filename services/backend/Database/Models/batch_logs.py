from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class BatchLogs(Base):
    __tablename__ = "batch_logs"
    __table_args__ = (
        Index("ix_batch_logs_batch_id", "batch_id"),
    )
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(
        Integer,
        ForeignKey("batches.id"),
        nullable=False,
        unique=True,
    )
    timestamp = Column(DateTime, default=datetime.now)
    activity = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    # Relationship to Batches

    batch = relationship("Batches", back_populates="batch_log")
