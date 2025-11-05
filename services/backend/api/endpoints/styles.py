from fastapi import APIRouter
from database import SessionLocal
from typing import Annotated, List
from fastapi import Depends
from database import get_db
import Database.Models as models
import Database.Schemas as schemas

db_dependency = Annotated[SessionLocal, Depends(get_db)]
router = APIRouter()
db = SessionLocal()


@router.get(
    "/styles",
    response_model=List[schemas.StyleBase],
    summary="List beer style definitions",
    response_description="A collection of BJCP style entries defined in the system.",
)
async def get_all_styles(db: db_dependency) -> List[schemas.StyleBase]:
    """Return all BJCP style definitions available in the catalogue."""
    styles = db.query(models.Styles).all()
    return styles
