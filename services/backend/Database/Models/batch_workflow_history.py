"""
Batch workflow history model for tracking status changes
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class BatchWorkflowHistory(Base):
    __tablename__ = "batch_workflow_history"
    __table_args__ = (
        Index("ix_batch_workflow_history_batch_id", "batch_id"),
        Index("ix_batch_workflow_history_changed_at", "changed_at"),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(
        Integer,
        ForeignKey("batches.id", ondelete="CASCADE"),
        nullable=False,
    )
    from_status = Column(String(50), nullable=True)  # Null for initial status
    to_status = Column(String(50), nullable=False)
    changed_at = Column(DateTime, default=datetime.now, nullable=False)
    notes = Column(String, nullable=True)
    
    # Relationship to Batches
    batch = relationship("Batches", back_populates="workflow_history")
