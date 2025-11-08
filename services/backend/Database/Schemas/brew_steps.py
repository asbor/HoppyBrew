from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


BREW_STEP_BASE_EXAMPLE = {
    "step_name": "Mash",
    "step_type": "mash",
    "duration": 60,
    "temperature": 65,
    "notes": "Single infusion mash at 65°C for 60 minutes",
    "order_index": 0,
}

BREW_STEP_FULL_EXAMPLE = {
    **BREW_STEP_BASE_EXAMPLE,
    "id": 1,
    "batch_id": 11,
    "completed": False,
    "started_at": None,
    "completed_at": None,
    "created_at": "2024-03-21T08:00:00Z",
    "updated_at": "2024-03-21T08:00:00Z",
}


class BrewStepBase(BaseModel):
    step_name: str
    step_type: str
    duration: Optional[int] = None
    temperature: Optional[int] = None
    notes: Optional[str] = None
    order_index: int = 0

    model_config = ConfigDict(json_schema_extra={"example": BREW_STEP_BASE_EXAMPLE})


class BrewStepCreate(BrewStepBase):
    batch_id: int

    model_config = ConfigDict(
        json_schema_extra={"example": {**BREW_STEP_BASE_EXAMPLE, "batch_id": 11}}
    )


class BrewStepUpdate(BaseModel):
    step_name: Optional[str] = None
    step_type: Optional[str] = None
    duration: Optional[int] = None
    temperature: Optional[int] = None
    notes: Optional[str] = None
    completed: Optional[bool] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    order_index: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "completed": True,
                "completed_at": "2024-03-21T09:00:00Z",
            }
        }
    )


class BrewStep(BrewStepBase):
    id: int
    batch_id: int
    completed: bool
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True, json_schema_extra={"example": BREW_STEP_FULL_EXAMPLE}
    )
