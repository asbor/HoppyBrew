"""
Schema for batch workflow history
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


WORKFLOW_HISTORY_EXAMPLE = {
    "id": 1,
    "batch_id": 11,
    "from_status": "planning",
    "to_status": "brewing",
    "changed_at": "2024-03-21T08:00:00Z",
    "notes": "Started brew day",
}


class BatchWorkflowHistoryBase(BaseModel):
    from_status: Optional[str] = None
    to_status: str
    notes: Optional[str] = None


class BatchWorkflowHistoryCreate(BatchWorkflowHistoryBase):
    batch_id: int


class BatchWorkflowHistory(BatchWorkflowHistoryBase):
    id: int
    batch_id: int
    changed_at: datetime

    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"example": WORKFLOW_HISTORY_EXAMPLE}
    )


class StatusUpdateRequest(BaseModel):
    """Request schema for updating batch status"""

    status: str
    notes: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"status": "brewing", "notes": "Started brew day at 8am"}
        }
    )
