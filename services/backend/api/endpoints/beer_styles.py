from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from database import get_db
import Database.Models as models
import Database.Schemas as schemas
from typing import List, Optional

router = APIRouter()


# ============================================================================
# Style Guideline Sources Endpoints
# ============================================================================


@router.get(
    "/style-guideline-sources",
    response_model=List[schemas.StyleGuidelineSource],
    summary="List all style guideline sources",
    response_description="A list of style guideline sources (BJCP, BA, etc.)",
)
async def get_style_guideline_sources(
    is_active: Optional[bool] = None, db: Session = Depends(get_db)
):
    """Get all style guideline sources, optionally filtered by active status."""
    query = db.query(models.StyleGuidelineSource)
    if is_active is not None:
        query = query.filter(models.StyleGuidelineSource.is_active == is_active)
    return query.all()


@router.get(
    "/style-guideline-sources/{source_id}",
    response_model=schemas.StyleGuidelineSource,
    summary="Get a specific style guideline source",
)
async def get_style_guideline_source(source_id: int, db: Session = Depends(get_db)):
    """Get details of a specific style guideline source."""
    source = (
        db.query(models.StyleGuidelineSource)
        .filter(models.StyleGuidelineSource.id == source_id)
        .first()
    )
    if not source:
        raise HTTPException(status_code=404, detail="Style guideline source not found")
    return source


@router.post(
    "/style-guideline-sources",
    response_model=schemas.StyleGuidelineSource,
    summary="Create a new style guideline source",
)
async def create_style_guideline_source(
    source: schemas.StyleGuidelineSourceCreate, db: Session = Depends(get_db)
):
    """Create a new style guideline source."""
    try:
        db_source = models.StyleGuidelineSource(**source.model_dump())
        db.add(db_source)
        db.commit()
        db.refresh(db_source)
        return db_source
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/style-guideline-sources/{source_id}",
    response_model=schemas.StyleGuidelineSource,
    summary="Update a style guideline source",
)
async def update_style_guideline_source(
    source_id: int, source: schemas.StyleGuidelineSourceUpdate, db: Session = Depends(get_db)
):
    """Update an existing style guideline source."""
    db_source = (
        db.query(models.StyleGuidelineSource)
        .filter(models.StyleGuidelineSource.id == source_id)
        .first()
    )
    if not db_source:
        raise HTTPException(status_code=404, detail="Style guideline source not found")

    # Only update fields that are provided in the request
    update_data = source.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(db_source, key):
            setattr(db_source, key, value)

    try:
        db.commit()
        db.refresh(db_source)
        return db_source
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/style-guideline-sources/{source_id}", summary="Delete a style guideline source")
async def delete_style_guideline_source(source_id: int, db: Session = Depends(get_db)):
    """Delete a style guideline source."""
    db_source = (
        db.query(models.StyleGuidelineSource)
        .filter(models.StyleGuidelineSource.id == source_id)
        .first()
    )
    if not db_source:
        raise HTTPException(status_code=404, detail="Style guideline source not found")

    try:
        db.delete(db_source)
        db.commit()
        return {"message": "Style guideline source deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Style Categories Endpoints
# ============================================================================


@router.get(
    "/style-categories",
    response_model=List[schemas.StyleCategory],
    summary="List all style categories",
)
async def get_style_categories(
    guideline_source_id: Optional[int] = None,
    parent_category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Get all style categories, optionally filtered by guideline source or parent category."""
    query = db.query(models.StyleCategory)
    if guideline_source_id is not None:
        query = query.filter(models.StyleCategory.guideline_source_id == guideline_source_id)
    if parent_category_id is not None:
        query = query.filter(models.StyleCategory.parent_category_id == parent_category_id)
    return query.all()


@router.get(
    "/style-categories/{category_id}",
    response_model=schemas.StyleCategory,
    summary="Get a specific style category",
)
async def get_style_category(category_id: int, db: Session = Depends(get_db)):
    """Get details of a specific style category."""
    category = db.query(models.StyleCategory).filter(models.StyleCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Style category not found")
    return category


@router.post(
    "/style-categories", response_model=schemas.StyleCategory, summary="Create a new style category"
)
async def create_style_category(
    category: schemas.StyleCategoryCreate, db: Session = Depends(get_db)
):
    """Create a new style category."""
    try:
        db_category = models.StyleCategory(**category.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/style-categories/{category_id}",
    response_model=schemas.StyleCategory,
    summary="Update a style category",
)
async def update_style_category(
    category_id: int, category: schemas.StyleCategoryUpdate, db: Session = Depends(get_db)
):
    """Update an existing style category."""
    db_category = (
        db.query(models.StyleCategory).filter(models.StyleCategory.id == category_id).first()
    )
    if not db_category:
        raise HTTPException(status_code=404, detail="Style category not found")

    # Only update fields that are provided and exist on the model
    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(db_category, key):
            setattr(db_category, key, value)

    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/style-categories/{category_id}", summary="Delete a style category")
async def delete_style_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a style category."""
    db_category = (
        db.query(models.StyleCategory).filter(models.StyleCategory.id == category_id).first()
    )
    if not db_category:
        raise HTTPException(status_code=404, detail="Style category not found")

    try:
        db.delete(db_category)
        db.commit()
        return {"message": "Style category deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Beer Styles Endpoints
# ============================================================================


@router.get(
    "/beer-styles",
    response_model=List[schemas.BeerStyle],
    summary="List all beer styles with filtering",
    response_description="A collection of beer styles with optional filters",
)
async def get_beer_styles(
    guideline_source_id: Optional[int] = Query(None, description="Filter by guideline source"),
    category_id: Optional[int] = Query(None, description="Filter by category"),
    is_custom: Optional[bool] = Query(None, description="Filter by custom/standard styles"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db),
):
    """Get all beer styles with optional filtering."""
    query = db.query(models.BeerStyle).options(
        joinedload(models.BeerStyle.guideline_source), joinedload(models.BeerStyle.category)
    )

    if guideline_source_id is not None:
        query = query.filter(models.BeerStyle.guideline_source_id == guideline_source_id)
    if category_id is not None:
        query = query.filter(models.BeerStyle.category_id == category_id)
    if is_custom is not None:
        query = query.filter(models.BeerStyle.is_custom == is_custom)

    return query.offset(offset).limit(limit).all()


@router.get(
    "/beer-styles/search",
    response_model=List[schemas.BeerStyle],
    summary="Search beer styles",
    response_description="Beer styles matching search criteria",
)
async def search_beer_styles(
    query: Optional[str] = Query(None, description="Search in name, description, or examples"),
    guideline_source_id: Optional[int] = Query(None, description="Filter by guideline source"),
    category_id: Optional[int] = Query(None, description="Filter by category"),
    abv_min: Optional[float] = Query(None, description="Minimum ABV"),
    abv_max: Optional[float] = Query(None, description="Maximum ABV"),
    ibu_min: Optional[int] = Query(None, description="Minimum IBU"),
    ibu_max: Optional[int] = Query(None, description="Maximum IBU"),
    color_min_srm: Optional[float] = Query(None, description="Minimum color (SRM)"),
    color_max_srm: Optional[float] = Query(None, description="Maximum color (SRM)"),
    is_custom: Optional[bool] = Query(None, description="Filter by custom/standard styles"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db),
):
    """Search beer styles by various criteria."""
    db_query = db.query(models.BeerStyle).options(
        joinedload(models.BeerStyle.guideline_source), joinedload(models.BeerStyle.category)
    )

    # Text search
    if query:
        search_filter = or_(
            models.BeerStyle.name.ilike(f"%{query}%"),
            models.BeerStyle.description.ilike(f"%{query}%"),
            models.BeerStyle.examples.ilike(f"%{query}%"),
            models.BeerStyle.style_code.ilike(f"%{query}%"),
        )
        db_query = db_query.filter(search_filter)

    # Guideline source filter
    if guideline_source_id is not None:
        db_query = db_query.filter(models.BeerStyle.guideline_source_id == guideline_source_id)

    # Category filter
    if category_id is not None:
        db_query = db_query.filter(models.BeerStyle.category_id == category_id)

    # ABV range filter
    if abv_min is not None or abv_max is not None:
        if abv_min is not None and abv_max is not None:
            db_query = db_query.filter(
                and_(models.BeerStyle.abv_max >= abv_min, models.BeerStyle.abv_min <= abv_max)
            )
        elif abv_min is not None:
            db_query = db_query.filter(models.BeerStyle.abv_max >= abv_min)
        elif abv_max is not None:
            db_query = db_query.filter(models.BeerStyle.abv_min <= abv_max)

    # IBU range filter
    if ibu_min is not None or ibu_max is not None:
        if ibu_min is not None and ibu_max is not None:
            db_query = db_query.filter(
                and_(models.BeerStyle.ibu_max >= ibu_min, models.BeerStyle.ibu_min <= ibu_max)
            )
        elif ibu_min is not None:
            db_query = db_query.filter(models.BeerStyle.ibu_max >= ibu_min)
        elif ibu_max is not None:
            db_query = db_query.filter(models.BeerStyle.ibu_min <= ibu_max)

    # Color range filter
    if color_min_srm is not None or color_max_srm is not None:
        if color_min_srm is not None and color_max_srm is not None:
            db_query = db_query.filter(
                and_(
                    models.BeerStyle.color_max_srm >= color_min_srm,
                    models.BeerStyle.color_min_srm <= color_max_srm,
                )
            )
        elif color_min_srm is not None:
            db_query = db_query.filter(models.BeerStyle.color_max_srm >= color_min_srm)
        elif color_max_srm is not None:
            db_query = db_query.filter(models.BeerStyle.color_min_srm <= color_max_srm)

    # Custom filter
    if is_custom is not None:
        db_query = db_query.filter(models.BeerStyle.is_custom == is_custom)

    return db_query.offset(offset).limit(limit).all()


@router.get(
    "/beer-styles/{style_id}", response_model=schemas.BeerStyle, summary="Get a specific beer style"
)
async def get_beer_style(style_id: int, db: Session = Depends(get_db)):
    """Get details of a specific beer style."""
    style = (
        db.query(models.BeerStyle)
        .options(
            joinedload(models.BeerStyle.guideline_source), joinedload(models.BeerStyle.category)
        )
        .filter(models.BeerStyle.id == style_id)
        .first()
    )

    if not style:
        raise HTTPException(status_code=404, detail="Beer style not found")
    return style


@router.post(
    "/beer-styles", response_model=schemas.BeerStyle, summary="Create a new beer style (custom)"
)
async def create_beer_style(style: schemas.BeerStyleCreate, db: Session = Depends(get_db)):
    """Create a new custom beer style."""
    try:
        # Force custom flag for user-created styles
        style_data = style.model_dump()
        style_data["is_custom"] = True

        db_style = models.BeerStyle(**style_data)
        db.add(db_style)
        db.commit()
        db.refresh(db_style)
        return db_style
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/beer-styles/{style_id}", response_model=schemas.BeerStyle, summary="Update a beer style"
)
async def update_beer_style(
    style_id: int, style: schemas.BeerStyleUpdate, db: Session = Depends(get_db)
):
    """Update an existing beer style. Only custom styles can be updated."""
    db_style = db.query(models.BeerStyle).filter(models.BeerStyle.id == style_id).first()

    if not db_style:
        raise HTTPException(status_code=404, detail="Beer style not found")

    # Only allow updating custom styles
    if not db_style.is_custom:
        raise HTTPException(
            status_code=403,
            detail="Cannot modify standard beer styles. Create a custom style instead.",
        )

    # Only update fields that are provided and exist on the model
    update_data = style.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(db_style, key):
            setattr(db_style, key, value)

    try:
        db.commit()
        db.refresh(db_style)
        return db_style
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/beer-styles/{style_id}", summary="Delete a beer style")
async def delete_beer_style(style_id: int, db: Session = Depends(get_db)):
    """Delete a beer style. Only custom styles can be deleted."""
    db_style = db.query(models.BeerStyle).filter(models.BeerStyle.id == style_id).first()

    if not db_style:
        raise HTTPException(status_code=404, detail="Beer style not found")

    # Only allow deleting custom styles
    if not db_style.is_custom:
        raise HTTPException(status_code=403, detail="Cannot delete standard beer styles")

    try:
        db.delete(db_style)
        db.commit()
        return {"message": "Beer style deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
