# api/endpoints/analytics.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, case, extract, and_, or_
from database import get_db
import Database.Models as models
from Database.enums import BatchStatus
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import logging
from fastapi.responses import StreamingResponse
import csv
import io

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/analytics/batches/summary")
async def get_batch_analytics_summary(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    recipe_id: Optional[int] = Query(None, description="Filter by recipe ID"),
    style: Optional[str] = Query(None, description="Filter by beer style"),
    db: Session = Depends(get_db),
):
    """
    Get comprehensive analytics summary for batches including:
    - Success rate by recipe/style
    - Cost per batch/pint analysis
    - Fermentation time trends
    - OG/FG accuracy tracking
    - Seasonal brewing patterns
    """
    try:
        # Build base query
        query = db.query(models.Batches).options(
            joinedload(models.Batches.recipe),
            joinedload(models.Batches.fermentation_readings),
            joinedload(models.Batches.inventory_fermentables),
            joinedload(models.Batches.inventory_hops),
            joinedload(models.Batches.inventory_yeasts),
            joinedload(models.Batches.inventory_miscs),
        )

        # Apply date filters
        if start_date:
            start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            query = query.filter(models.Batches.brew_date >= start)
        if end_date:
            end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            query = query.filter(models.Batches.brew_date <= end)

        # Apply recipe/style filters
        if recipe_id:
            query = query.filter(models.Batches.recipe_id == recipe_id)
        if style:
            query = query.join(models.Recipes).filter(
                models.Recipes.type.ilike(f"%{style}%")
            )

        batches = query.all()

        # Calculate metrics
        total_batches = len(batches)
        completed_batches = [
            b for b in batches if b.status in [BatchStatus.COMPLETE, BatchStatus.ARCHIVED]
        ]
        success_count = len(completed_batches)
        success_rate = (success_count / total_batches * 100) if total_batches > 0 else 0

        # Calculate costs
        batch_costs = []
        for batch in batches:
            cost = calculate_batch_cost(batch)
            if cost > 0:
                batch_costs.append({
                    "batch_id": batch.id,
                    "batch_name": batch.batch_name,
                    "total_cost": cost,
                    "cost_per_liter": cost / batch.batch_size if batch.batch_size > 0 else 0,
                    "cost_per_pint": cost / (batch.batch_size * 2.11338) if batch.batch_size > 0 else 0,  # 1 liter = 2.11338 pints
                })

        avg_cost_per_batch = sum(b["total_cost"] for b in batch_costs) / len(batch_costs) if batch_costs else 0
        avg_cost_per_liter = sum(b["cost_per_liter"] for b in batch_costs) / len(batch_costs) if batch_costs else 0
        avg_cost_per_pint = sum(b["cost_per_pint"] for b in batch_costs) / len(batch_costs) if batch_costs else 0

        # Calculate fermentation times
        fermentation_times = []
        for batch in batches:
            if batch.status in [BatchStatus.COMPLETE, BatchStatus.ARCHIVED]:
                readings = sorted(batch.fermentation_readings, key=lambda r: r.timestamp)
                if len(readings) >= 2:
                    start_time = readings[0].timestamp
                    end_time = readings[-1].timestamp
                    duration_days = (end_time - start_time).days
                    fermentation_times.append({
                        "batch_id": batch.id,
                        "batch_name": batch.batch_name,
                        "duration_days": duration_days,
                        "recipe_name": batch.recipe.name if batch.recipe else None,
                    })

        avg_fermentation_days = (
            sum(f["duration_days"] for f in fermentation_times) / len(fermentation_times)
            if fermentation_times else 0
        )

        # Calculate OG/FG accuracy
        og_fg_accuracy = []
        for batch in batches:
            if batch.recipe:
                # Get actual OG/FG from fermentation readings
                readings = sorted(batch.fermentation_readings, key=lambda r: r.timestamp)
                actual_og = readings[0].gravity if readings and readings[0].gravity else None
                actual_fg = readings[-1].gravity if readings and readings[-1].gravity else None

                if actual_og and actual_fg and batch.recipe.est_og and batch.recipe.est_fg:
                    og_accuracy = abs(actual_og - batch.recipe.est_og) / batch.recipe.est_og * 100
                    fg_accuracy = abs(actual_fg - batch.recipe.est_fg) / batch.recipe.est_fg * 100
                    og_fg_accuracy.append({
                        "batch_id": batch.id,
                        "batch_name": batch.batch_name,
                        "estimated_og": batch.recipe.est_og,
                        "actual_og": actual_og,
                        "og_accuracy_percent": 100 - og_accuracy,
                        "estimated_fg": batch.recipe.est_fg,
                        "actual_fg": actual_fg,
                        "fg_accuracy_percent": 100 - fg_accuracy,
                    })

        avg_og_accuracy = (
            sum(a["og_accuracy_percent"] for a in og_fg_accuracy) / len(og_fg_accuracy)
            if og_fg_accuracy else 0
        )
        avg_fg_accuracy = (
            sum(a["fg_accuracy_percent"] for a in og_fg_accuracy) / len(og_fg_accuracy)
            if og_fg_accuracy else 0
        )

        # Calculate seasonal patterns
        seasonal_data = {}
        for batch in batches:
            if batch.brew_date:
                month = batch.brew_date.month
                season = get_season(month)
                if season not in seasonal_data:
                    seasonal_data[season] = {
                        "season": season,
                        "batch_count": 0,
                        "total_volume": 0,
                    }
                seasonal_data[season]["batch_count"] += 1
                seasonal_data[season]["total_volume"] += batch.batch_size

        # Success rate by recipe
        recipe_stats = {}
        for batch in batches:
            if batch.recipe:
                recipe_name = batch.recipe.name
                if recipe_name not in recipe_stats:
                    recipe_stats[recipe_name] = {
                        "recipe_name": recipe_name,
                        "recipe_id": batch.recipe_id,
                        "total_batches": 0,
                        "completed_batches": 0,
                        "success_rate": 0,
                    }
                recipe_stats[recipe_name]["total_batches"] += 1
                if batch.status in [BatchStatus.COMPLETE, BatchStatus.ARCHIVED]:
                    recipe_stats[recipe_name]["completed_batches"] += 1

        for recipe_name, stats in recipe_stats.items():
            stats["success_rate"] = (
                stats["completed_batches"] / stats["total_batches"] * 100
                if stats["total_batches"] > 0 else 0
            )

        # Success rate by style
        style_stats = {}
        for batch in batches:
            if batch.recipe and batch.recipe.type:
                style = batch.recipe.type
                if style not in style_stats:
                    style_stats[style] = {
                        "style": style,
                        "total_batches": 0,
                        "completed_batches": 0,
                        "success_rate": 0,
                    }
                style_stats[style]["total_batches"] += 1
                if batch.status in [BatchStatus.COMPLETE, BatchStatus.ARCHIVED]:
                    style_stats[style]["completed_batches"] += 1

        for style, stats in style_stats.items():
            stats["success_rate"] = (
                stats["completed_batches"] / stats["total_batches"] * 100
                if stats["total_batches"] > 0 else 0
            )

        return {
            "summary": {
                "total_batches": total_batches,
                "completed_batches": success_count,
                "success_rate": round(success_rate, 2),
                "avg_cost_per_batch": round(avg_cost_per_batch, 2),
                "avg_cost_per_liter": round(avg_cost_per_liter, 2),
                "avg_cost_per_pint": round(avg_cost_per_pint, 2),
                "avg_fermentation_days": round(avg_fermentation_days, 1),
                "avg_og_accuracy": round(avg_og_accuracy, 2),
                "avg_fg_accuracy": round(avg_fg_accuracy, 2),
            },
            "cost_breakdown": batch_costs,
            "fermentation_times": fermentation_times,
            "og_fg_accuracy": og_fg_accuracy,
            "seasonal_patterns": list(seasonal_data.values()),
            "success_by_recipe": list(recipe_stats.values()),
            "success_by_style": list(style_stats.values()),
        }

    except Exception as e:
        logger.error(f"Error getting batch analytics: {str(e)}")
        raise


@router.get("/analytics/batches/export/csv")
async def export_batch_analytics_csv(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    recipe_id: Optional[int] = Query(None, description="Filter by recipe ID"),
    style: Optional[str] = Query(None, description="Filter by beer style"),
    db: Session = Depends(get_db),
):
    """Export batch analytics as CSV"""
    # Get analytics data
    analytics = await get_batch_analytics_summary(start_date, end_date, recipe_id, style, db)
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write summary section
    writer.writerow(["Batch Analytics Summary"])
    writer.writerow([])
    writer.writerow(["Metric", "Value"])
    for key, value in analytics["summary"].items():
        writer.writerow([key.replace("_", " ").title(), value])
    
    writer.writerow([])
    writer.writerow(["Cost Breakdown by Batch"])
    writer.writerow(["Batch ID", "Batch Name", "Total Cost", "Cost per Liter", "Cost per Pint"])
    for cost in analytics["cost_breakdown"]:
        writer.writerow([
            cost["batch_id"],
            cost["batch_name"],
            f"${cost['total_cost']:.2f}",
            f"${cost['cost_per_liter']:.2f}",
            f"${cost['cost_per_pint']:.2f}",
        ])
    
    writer.writerow([])
    writer.writerow(["Fermentation Times"])
    writer.writerow(["Batch ID", "Batch Name", "Recipe Name", "Duration (Days)"])
    for ferm in analytics["fermentation_times"]:
        writer.writerow([
            ferm["batch_id"],
            ferm["batch_name"],
            ferm["recipe_name"],
            ferm["duration_days"],
        ])
    
    writer.writerow([])
    writer.writerow(["OG/FG Accuracy"])
    writer.writerow(["Batch ID", "Batch Name", "Est. OG", "Actual OG", "OG Accuracy %", "Est. FG", "Actual FG", "FG Accuracy %"])
    for acc in analytics["og_fg_accuracy"]:
        writer.writerow([
            acc["batch_id"],
            acc["batch_name"],
            f"{acc['estimated_og']:.3f}",
            f"{acc['actual_og']:.3f}",
            f"{acc['og_accuracy_percent']:.2f}%",
            f"{acc['estimated_fg']:.3f}",
            f"{acc['actual_fg']:.3f}",
            f"{acc['fg_accuracy_percent']:.2f}%",
        ])
    
    writer.writerow([])
    writer.writerow(["Success Rate by Recipe"])
    writer.writerow(["Recipe Name", "Total Batches", "Completed Batches", "Success Rate %"])
    for recipe in analytics["success_by_recipe"]:
        writer.writerow([
            recipe["recipe_name"],
            recipe["total_batches"],
            recipe["completed_batches"],
            f"{recipe['success_rate']:.2f}%",
        ])
    
    writer.writerow([])
    writer.writerow(["Success Rate by Style"])
    writer.writerow(["Style", "Total Batches", "Completed Batches", "Success Rate %"])
    for style in analytics["success_by_style"]:
        writer.writerow([
            style["style"],
            style["total_batches"],
            style["completed_batches"],
            f"{style['success_rate']:.2f}%",
        ])
    
    writer.writerow([])
    writer.writerow(["Seasonal Brewing Patterns"])
    writer.writerow(["Season", "Batch Count", "Total Volume (L)"])
    for season in analytics["seasonal_patterns"]:
        writer.writerow([
            season["season"],
            season["batch_count"],
            f"{season['total_volume']:.2f}",
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=batch_analytics_{datetime.now().strftime('%Y%m%d')}.csv"
        },
    )


def calculate_batch_cost(batch: models.Batches) -> float:
    """Calculate total cost of a batch based on ingredient costs"""
    total_cost = 0.0
    
    # Fermentables
    for fermentable in batch.inventory_fermentables:
        if fermentable.cost_per_unit and fermentable.amount:
            total_cost += fermentable.cost_per_unit * fermentable.amount
    
    # Hops - assuming cost_per_unit exists (though not in current model)
    # This would need to be added to the model for accurate cost tracking
    
    # Yeasts
    # Similar to hops, would need cost tracking
    
    # Miscs
    # Similar to hops, would need cost tracking
    
    return total_cost


def get_season(month: int) -> str:
    """Get season name from month number"""
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"
