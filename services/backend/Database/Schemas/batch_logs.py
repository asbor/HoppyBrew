from pydantic import BaseModel
from datetime import datetime

BATCH_LOG_EXAMPLE = {
    "log_entry": "Gravity checked at 1.012 before dry hop addition.",
}


class BatchLogBase(BaseModel):
    log_entry: str

    class Config:
        schema_extra = {"example": BATCH_LOG_EXAMPLE}


class BatchLogCreate(BatchLogBase):
    batch_id: int

    class Config:
        schema_extra = {"example": {**BATCH_LOG_EXAMPLE, "batch_id": 11}}


class BatchLog(BatchLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                **BATCH_LOG_EXAMPLE,
                "id": 5,
                "created_at": "2024-03-22T09:00:00Z",
            }
        }
