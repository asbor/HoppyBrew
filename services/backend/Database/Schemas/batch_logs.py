from pydantic import BaseModel, ConfigDict
from datetime import datetime

BATCH_LOG_EXAMPLE = {
    "activity": "Gravity checked at 1.012 before dry hop addition.",
    "notes": "Dry hop scheduled tomorrow.",
    "timestamp": "2024-03-22T09:00:00Z",
}


class BatchLogBase(BaseModel):
    activity: str
    notes: str | None = None

    model_config = ConfigDict(json_schema_extra={"example": BATCH_LOG_EXAMPLE})


class BatchLogCreate(BatchLogBase):
    batch_id: int

    model_config = ConfigDict(
        json_schema_extra={"example": {**BATCH_LOG_EXAMPLE, "batch_id": 11}}
    )


class BatchLog(BatchLogBase):
    id: int
    timestamp: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **BATCH_LOG_EXAMPLE,
                "id": 5,
            }
        },
    )
