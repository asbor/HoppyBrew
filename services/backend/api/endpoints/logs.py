from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

router = APIRouter()


class LogContentResponse(BaseModel):
    log_content: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "log_content": "[2024-03-21 10:15:09] INFO - Server started on port 8000\n"
                "[2024-03-21 10:17:45] ERROR - Failed to connect to fermentation sensor",
            }
        }
    )


@router.get(
    "/api/logs",
    response_model=LogContentResponse,
    summary="Download backend logs",
    response_description="Raw application logs collected from the service host.",
)
async def get_logs():
    """Return the application log stream for debugging and support."""
    log_paths = [
        "logs.log",  # default relative path
        "logs/logs.log",  # common logs directory
        "/home/app/logs/logs.log",  # explicit container path
    ]

    for path in log_paths:
        try:
            with open(path, "r", encoding="utf-8") as file:
                log_content = file.read()
                return LogContentResponse(log_content=log_content)
        except FileNotFoundError:
            continue
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to read log file: {e}"
            ) from e

    # No log file found; return empty log content instead of erroring
    return LogContentResponse(log_content="")
