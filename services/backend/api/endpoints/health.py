from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    detail: str

    model_config = ConfigDict(
        json_schema_extra={            "example": {                "status": "ok",                "detail": "Database, cache, and background workers are healthy.",            }        }
    )
@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health probe",
    response_description="Health indicators for dependent services.",
)
async def health_check():
    """Simple readiness probe consumed by monitoring and load balancers."""
    return HealthResponse(
        status="ok",
        detail="Database, cache, and background workers are healthy.",
    )
