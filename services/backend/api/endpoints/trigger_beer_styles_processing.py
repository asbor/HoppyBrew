# api/endpoints/trigger_beer_styles_processing.py

from datetime import datetime, timezone
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, ConfigDict
from api.scripts.beer_styles_processing import scrape_and_process_beer_styles

router = APIRouter()


class BeerStyleRefreshResponse(BaseModel):
    message: str
    task_id: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Beer style refresh queued for processing.",
                "task_id": "refresh-beer-styles-20240321T101500Z",
            }
        }
    )


def run_beer_styles_script():
    scrape_and_process_beer_styles()


@router.post(
    "/refresh-beer-styles",
    response_model=BeerStyleRefreshResponse,
    summary="Refresh cached beer style data",
    response_description="Acknowledgement that the refresh has been queued.",
)
async def trigger_script(background_tasks: BackgroundTasks):
    """Queue the beer styles update job that scrapes and normalises BJCP data."""
    background_tasks.add_task(run_beer_styles_script)
    task_id = f"refresh-beer-styles-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    return BeerStyleRefreshResponse(
        message="Beer style refresh queued for processing.", task_id=task_id
    )
