# api/endpoints/analytics.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, case, extract, and_
from database import get_db
import Database.Models as models
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from Database.enums import BatchStatus

router = APIRouter()


# Pydantic models for response schemas
class SuccessRateByRecipe(BaseModel):
    recipe_id: int
    recipe_name: str
    style_name: Optional[str]
    total_batches: int
    completed_batches: int
    success_rate: float


class CostAnalysis(BaseModel):
    batch_id: int
    batch_name: str
    recipe_name: str
    total_cost: float
    batch_size: float
    cost_per_liter: float
    cost_per_pint: float


class FermentationTimeTrend(BaseModel):
    batch_id: int
    batch_name: str
    recipe_name: str
    brew_date: datetime
    days_in_fermentation: Optional[int]
    status: str


class OGFGAccuracy(BaseModel):
    batch_id: int
    batch_name: str
    recipe_name: str
    target_og: Optional[float]
    actual_og: Optional[float]
    target_fg: Optional[float]
    actual_fg: Optional[float]
    og_accuracy: Optional[float]
    fg_accuracy: Optional[float]


class SeasonalPattern(BaseModel):
    month: int
    month_name: str
    year: int
    batch_count: int


class AnalyticsSummary(BaseModel):
    total_batches: int
    completed_batches: int
    active_batches: int
    total_recipes_used: int
    average_batch_size: float
    most_brewed_recipe: Optional[Dict[str, Any]]
    most_brewed_style: Optional[Dict[str, Any]]


@router.get("/analytics/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """
    Get summary analytics for batches
    """
    # Parse dates
    query = db.query(models.Batches).options(joinedload(models.Batches.recipe))
    
    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.filter(models.Batches.brew_date >= start_dt)
    
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.filter(models.Batches.brew_date <= end_dt)
    
    batches = query.all()
    
    total_batches = len(batches)
    completed_batches = len([b for b in batches if b.status == BatchStatus.COMPLETE.value])
    active_batches = len([b for b in batches if b.status not in [BatchStatus.COMPLETE.value, BatchStatus.ARCHIVED.value]])
    
    # Get unique recipes used
    recipe_ids = set(b.recipe_id for b in batches)
    total_recipes_used = len(recipe_ids)
    
    # Calculate average batch size
    avg_batch_size = sum(b.batch_size for b in batches) / total_batches if total_batches > 0 else 0.0
    
    # Find most brewed recipe
    recipe_counts: Dict[int, int] = {}
    recipe_data: Dict[int, Any] = {}
    for batch in batches:
        if batch.recipe_id:
            recipe_counts[batch.recipe_id] = recipe_counts.get(batch.recipe_id, 0) + 1
            if batch.recipe_id not in recipe_data and batch.recipe:
                recipe_data[batch.recipe_id] = {
                    "id": batch.recipe.id,
                    "name": batch.recipe.name,
                    "count": 0
                }
    
    most_brewed_recipe = None
    if recipe_counts:
        most_brewed_id = max(recipe_counts, key=recipe_counts.get)
        most_brewed_recipe = {
            "id": most_brewed_id,
            "name": recipe_data.get(most_brewed_id, {}).get("name", "Unknown"),
            "count": recipe_counts[most_brewed_id]
        }
    
    # Find most brewed style
    style_counts: Dict[str, int] = {}
    for batch in batches:
        if batch.recipe and batch.recipe.style_profile:
            style_name = batch.recipe.style_profile.name or "Unknown"
            style_counts[style_name] = style_counts.get(style_name, 0) + 1
    
    most_brewed_style = None
    if style_counts:
        most_brewed_style_name = max(style_counts, key=style_counts.get)
        most_brewed_style = {
            "name": most_brewed_style_name,
            "count": style_counts[most_brewed_style_name]
        }
    
    return AnalyticsSummary(
        total_batches=total_batches,
        completed_batches=completed_batches,
        active_batches=active_batches,
        total_recipes_used=total_recipes_used,
        average_batch_size=round(avg_batch_size, 2),
        most_brewed_recipe=most_brewed_recipe,
        most_brewed_style=most_brewed_style
    )


@router.get("/analytics/success-rate", response_model=List[SuccessRateByRecipe])
async def get_success_rate_by_recipe(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """
    Get success rate (completion rate) by recipe and style
    """
    query = db.query(models.Batches).options(
        joinedload(models.Batches.recipe).joinedload(models.Recipes.style_profile)
    )
    
    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.filter(models.Batches.brew_date >= start_dt)
    
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.filter(models.Batches.brew_date <= end_dt)
    
    batches = query.all()
    
    # Group by recipe
    recipe_stats: Dict[int, Dict[str, Any]] = {}
    
    for batch in batches:
        recipe_id = batch.recipe_id
        if recipe_id not in recipe_stats:
            recipe_stats[recipe_id] = {
                "recipe_name": batch.recipe.name if batch.recipe else "Unknown",
                "style_name": batch.recipe.style_profile.name if batch.recipe and batch.recipe.style_profile else None,
                "total": 0,
                "completed": 0
            }
        
        recipe_stats[recipe_id]["total"] += 1
        if batch.status == BatchStatus.COMPLETE.value:
            recipe_stats[recipe_id]["completed"] += 1
    
    # Build response
    result = []
    for recipe_id, stats in recipe_stats.items():
        success_rate = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0.0
        result.append(SuccessRateByRecipe(
            recipe_id=recipe_id,
            recipe_name=stats["recipe_name"],
            style_name=stats["style_name"],
            total_batches=stats["total"],
            completed_batches=stats["completed"],
            success_rate=round(success_rate, 2)
        ))
    
    # Sort by total batches descending
    result.sort(key=lambda x: x.total_batches, reverse=True)
    
    return result


@router.get("/analytics/cost-analysis", response_model=List[CostAnalysis])
async def get_cost_analysis(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """
    Get cost analysis per batch including cost per liter and pint
    """
    query = db.query(models.Batches).options(
        joinedload(models.Batches.recipe),
        joinedload(models.Batches.inventory_fermentables),
        joinedload(models.Batches.inventory_hops),
        joinedload(models.Batches.inventory_yeasts),
        joinedload(models.Batches.inventory_miscs)
    )
    
    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.filter(models.Batches.brew_date >= start_dt)
    
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.filter(models.Batches.brew_date <= end_dt)
    
    batches = query.all()
    
    result = []
    for batch in batches:
        # Calculate total cost from ingredients
        total_cost = 0.0
        
        # Sum fermentables cost
        for fermentable in batch.inventory_fermentables:
            if fermentable.cost_per_unit and fermentable.amount:
                total_cost += fermentable.cost_per_unit * fermentable.amount
        
        # Note: Hops, yeasts, and miscs don't have cost_per_unit in current schema
        # This would need to be added for complete cost tracking
        
        batch_size = batch.batch_size if batch.batch_size else 0.0
        cost_per_liter = total_cost / batch_size if batch_size > 0 else 0.0
        # 1 pint ≈ 0.473176 liters
        cost_per_pint = cost_per_liter * 0.473176
        
        result.append(CostAnalysis(
            batch_id=batch.id,
            batch_name=batch.batch_name,
            recipe_name=batch.recipe.name if batch.recipe else "Unknown",
            total_cost=round(total_cost, 2),
            batch_size=batch_size,
            cost_per_liter=round(cost_per_liter, 2),
            cost_per_pint=round(cost_per_pint, 2)
        ))
    
    return result


@router.get("/analytics/fermentation-time", response_model=List[FermentationTimeTrend])
async def get_fermentation_time_trends(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """
    Get fermentation time trends for batches
    """
    query = db.query(models.Batches).options(
        joinedload(models.Batches.recipe),
        joinedload(models.Batches.workflow_history)
    )
    
    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.filter(models.Batches.brew_date >= start_dt)
    
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.filter(models.Batches.brew_date <= end_dt)
    
    batches = query.all()
    
    result = []
    for batch in batches:
        days_in_fermentation = None
        
        # Calculate days from brew date to completion or current date
        if batch.brew_date:
            if batch.status == BatchStatus.COMPLETE.value:
                # Find completion date from workflow history
                completion_entry = None
                for entry in batch.workflow_history:
                    if entry.to_status == BatchStatus.COMPLETE.value:
                        completion_entry = entry
                        break
                
                if completion_entry:
                    days_in_fermentation = (completion_entry.changed_at - batch.brew_date).days
            elif batch.status in [BatchStatus.FERMENTING.value, BatchStatus.CONDITIONING.value]:
                # Still in fermentation
                days_in_fermentation = (datetime.now() - batch.brew_date).days
        
        result.append(FermentationTimeTrend(
            batch_id=batch.id,
            batch_name=batch.batch_name,
            recipe_name=batch.recipe.name if batch.recipe else "Unknown",
            brew_date=batch.brew_date,
            days_in_fermentation=days_in_fermentation,
            status=batch.status
        ))
    
    return result


@router.get("/analytics/og-fg-accuracy", response_model=List[OGFGAccuracy])
async def get_og_fg_accuracy(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """
    Get OG/FG accuracy tracking comparing targets to actual readings
    """
    query = db.query(models.Batches).options(
        joinedload(models.Batches.recipe),
        joinedload(models.Batches.fermentation_readings)
    )
    
    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.filter(models.Batches.brew_date >= start_dt)
    
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.filter(models.Batches.brew_date <= end_dt)
    
    batches = query.all()
    
    result = []
    for batch in batches:
        target_og = None
        target_fg = None
        actual_og = None
        actual_fg = None
        
        if batch.recipe:
            target_og = batch.recipe.est_og or batch.recipe.og
            target_fg = batch.recipe.est_fg or batch.recipe.fg
        
        # Get actual OG (first reading) and FG (last reading)
        if batch.fermentation_readings:
            sorted_readings = sorted(batch.fermentation_readings, key=lambda r: r.timestamp)
            if len(sorted_readings) > 0 and sorted_readings[0].gravity:
                actual_og = sorted_readings[0].gravity
            if len(sorted_readings) > 1 and sorted_readings[-1].gravity:
                actual_fg = sorted_readings[-1].gravity
        
        # Calculate accuracy (percentage difference from target)
        og_accuracy = None
        fg_accuracy = None
        
        if target_og and actual_og:
            og_accuracy = (1 - abs(target_og - actual_og) / target_og) * 100
        
        if target_fg and actual_fg:
            fg_accuracy = (1 - abs(target_fg - actual_fg) / target_fg) * 100
        
        result.append(OGFGAccuracy(
            batch_id=batch.id,
            batch_name=batch.batch_name,
            recipe_name=batch.recipe.name if batch.recipe else "Unknown",
            target_og=target_og,
            actual_og=actual_og,
            target_fg=target_fg,
            actual_fg=actual_fg,
            og_accuracy=round(og_accuracy, 2) if og_accuracy else None,
            fg_accuracy=round(fg_accuracy, 2) if fg_accuracy else None
        ))
    
    return result


@router.get("/analytics/seasonal-patterns", response_model=List[SeasonalPattern])
async def get_seasonal_patterns(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """
    Get seasonal brewing patterns (batches per month)
    """
    query = db.query(
        extract('year', models.Batches.brew_date).label('year'),
        extract('month', models.Batches.brew_date).label('month'),
        func.count(models.Batches.id).label('batch_count')
    ).group_by('year', 'month').order_by('year', 'month')
    
    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.filter(models.Batches.brew_date >= start_dt)
    
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.filter(models.Batches.brew_date <= end_dt)
    
    results = query.all()
    
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    return [
        SeasonalPattern(
            month=int(row.month),
            month_name=month_names[int(row.month) - 1],
            year=int(row.year),
            batch_count=row.batch_count
        )
        for row in results
    ]
