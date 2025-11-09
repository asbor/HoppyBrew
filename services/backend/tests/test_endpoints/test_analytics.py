# tests/test_endpoints/test_analytics.py

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from main import app

client = TestClient(app)


def test_get_batch_analytics_summary():
    """Test getting batch analytics summary"""
    response = client.get("/analytics/batches/summary")
    assert response.status_code == 200
    
    data = response.json()
    assert "summary" in data
    assert "cost_breakdown" in data
    assert "fermentation_times" in data
    assert "og_fg_accuracy" in data
    assert "seasonal_patterns" in data
    assert "success_by_recipe" in data
    assert "success_by_style" in data
    
    # Check summary structure
    summary = data["summary"]
    assert "total_batches" in summary
    assert "completed_batches" in summary
    assert "success_rate" in summary
    assert "avg_cost_per_batch" in summary
    assert "avg_cost_per_liter" in summary
    assert "avg_cost_per_pint" in summary
    assert "avg_fermentation_days" in summary
    assert "avg_og_accuracy" in summary
    assert "avg_fg_accuracy" in summary


def test_get_batch_analytics_with_date_filter():
    """Test analytics with date range filter"""
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    
    response = client.get(
        f"/analytics/batches/summary?start_date={start_date}&end_date={end_date}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data


def test_get_batch_analytics_with_recipe_filter():
    """Test analytics with recipe filter"""
    response = client.get("/analytics/batches/summary?recipe_id=1")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data


def test_get_batch_analytics_with_style_filter():
    """Test analytics with style filter"""
    response = client.get("/analytics/batches/summary?style=IPA")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data


def test_export_batch_analytics_csv():
    """Test exporting analytics as CSV"""
    response = client.get("/analytics/batches/export/csv")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "attachment" in response.headers["content-disposition"]
    
    # Check that CSV contains expected headers
    csv_content = response.text
    assert "Batch Analytics Summary" in csv_content
    assert "Cost Breakdown by Batch" in csv_content
    assert "Fermentation Times" in csv_content
    assert "OG/FG Accuracy" in csv_content
    assert "Success Rate by Recipe" in csv_content
    assert "Success Rate by Style" in csv_content
    assert "Seasonal Brewing Patterns" in csv_content


def test_export_analytics_csv_with_filters():
    """Test exporting analytics CSV with filters"""
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    
    response = client.get(
        f"/analytics/batches/export/csv?start_date={start_date}&end_date={end_date}"
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
