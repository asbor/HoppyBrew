from fastapi import APIRouter
from typing import Annotated, List
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
import Database.Models as models
import Database.Schemas as schemas

db_dependency = Annotated[Session, Depends(get_db)]
router = APIRouter()


@router.get(
    "/styles",
    response_model=List[schemas.Style],
    summary="List beer style definitions",
    response_description="A collection of BJCP style entries defined in the system.",
)
async def get_all_styles(db: db_dependency) -> List[schemas.Style]:
    """Return all BJCP style definitions available in the catalogue."""
    styles = db.query(models.Styles).all()
    return styles
