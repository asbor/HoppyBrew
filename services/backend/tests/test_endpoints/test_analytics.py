import pytest
from datetime import datetime, timedelta
import Database.Models as models
from Database.enums import BatchStatus


def create_recipe_with_style(db_session, name="Test Recipe", style_name="IPA"):
    """Helper to create a recipe with style"""
    recipe = models.Recipes(
        name=name,
        version=1,
        type="Ale",
        brewer="Tester",
        batch_size=20.0,
        boil_size=25.0,
        boil_time=60,
        est_og=1.050,
        est_fg=1.010,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)
    
    # Add style
    style = models.Styles(
        name=style_name,
        category="American IPA",
        recipe_id=recipe.id,
    )
    db_session.add(style)
    db_session.commit()
    
    return recipe.id


def create_batch(db_session, recipe_id, batch_name, brew_date, status=BatchStatus.PLANNING.value):
    """Helper to create a batch"""
    batch = models.Batches(
        recipe_id=recipe_id,
        batch_name=batch_name,
        batch_number=1,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=brew_date,
        status=status,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)
    return batch.id


def test_analytics_summary_empty_database(client):
    """Test analytics summary with no batches"""
    response = client.get("/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_batches"] == 0
    assert data["completed_batches"] == 0
    assert data["active_batches"] == 0
    assert data["total_recipes_used"] == 0


def test_analytics_summary_with_batches(client, db_session):
    """Test analytics summary with multiple batches"""
    recipe_id = create_recipe_with_style(db_session, "Test IPA", "American IPA")
    
    # Create batches with different statuses
    create_batch(db_session, recipe_id, "Batch 1", datetime.now() - timedelta(days=30), BatchStatus.COMPLETE.value)
    create_batch(db_session, recipe_id, "Batch 2", datetime.now() - timedelta(days=15), BatchStatus.FERMENTING.value)
    create_batch(db_session, recipe_id, "Batch 3", datetime.now() - timedelta(days=5), BatchStatus.PLANNING.value)
    
    response = client.get("/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_batches"] == 3
    assert data["completed_batches"] == 1
    assert data["active_batches"] == 2
    assert data["total_recipes_used"] == 1
    assert data["average_batch_size"] == 20.0


def test_analytics_summary_with_date_filter(client, db_session):
    """Test analytics summary with date range filter"""
    recipe_id = create_recipe_with_style(db_session, "Test IPA", "American IPA")
    
    # Create batches at different dates
    old_date = datetime.now() - timedelta(days=90)
    recent_date = datetime.now() - timedelta(days=15)
    
    create_batch(db_session, recipe_id, "Old Batch", old_date, BatchStatus.COMPLETE.value)
    create_batch(db_session, recipe_id, "Recent Batch", recent_date, BatchStatus.FERMENTING.value)
    
    # Filter to only recent batches (last 30 days)
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    response = client.get(f"/analytics/summary?start_date={start_date}")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_batches"] == 1


def test_success_rate_by_recipe(client, db_session):
    """Test success rate calculation by recipe"""
    recipe1_id = create_recipe_with_style(db_session, "IPA Recipe", "American IPA")
    recipe2_id = create_recipe_with_style(db_session, "Stout Recipe", "Stout")
    
    # Recipe 1: 2 completed, 1 in progress
    create_batch(db_session, recipe1_id, "IPA Batch 1", datetime.now() - timedelta(days=30), BatchStatus.COMPLETE.value)
    create_batch(db_session, recipe1_id, "IPA Batch 2", datetime.now() - timedelta(days=20), BatchStatus.COMPLETE.value)
    create_batch(db_session, recipe1_id, "IPA Batch 3", datetime.now() - timedelta(days=10), BatchStatus.FERMENTING.value)
    
    # Recipe 2: 1 completed
    create_batch(db_session, recipe2_id, "Stout Batch 1", datetime.now() - timedelta(days=25), BatchStatus.COMPLETE.value)
    
    response = client.get("/analytics/success-rate")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2
    
    # Find IPA recipe stats
    ipa_stats = next(r for r in data if r["recipe_name"] == "IPA Recipe")
    assert ipa_stats["total_batches"] == 3
    assert ipa_stats["completed_batches"] == 2
    assert ipa_stats["success_rate"] == pytest.approx(66.67, rel=0.1)
    assert ipa_stats["style_name"] == "American IPA"
    
    # Find Stout recipe stats
    stout_stats = next(r for r in data if r["recipe_name"] == "Stout Recipe")
    assert stout_stats["total_batches"] == 1
    assert stout_stats["completed_batches"] == 1
    assert stout_stats["success_rate"] == 100.0


def test_cost_analysis(client, db_session):
    """Test cost analysis per batch"""
    recipe_id = create_recipe_with_style(db_session, "Test IPA", "American IPA")
    batch_id = create_batch(db_session, recipe_id, "Cost Test Batch", datetime.now() - timedelta(days=15))
    
    # Add fermentable with cost
    fermentable = models.InventoryFermentable(
        name="Pale Malt",
        type="Grain",
        amount=5.0,  # kg
        yield_=80.0,
        color=2,
        cost_per_unit=2.50,  # $2.50 per kg
        batch_id=batch_id,
    )
    db_session.add(fermentable)
    db_session.commit()
    
    response = client.get("/analytics/cost-analysis")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    batch_cost = data[0]
    
    assert batch_cost["batch_id"] == batch_id
    assert batch_cost["total_cost"] == 12.50  # 5 kg * $2.50
    assert batch_cost["batch_size"] == 20.0
    assert batch_cost["cost_per_liter"] == pytest.approx(0.625, rel=0.01)


def test_fermentation_time_trends(client, db_session):
    """Test fermentation time tracking"""
    recipe_id = create_recipe_with_style(db_session, "Test IPA", "American IPA")
    
    # Create a completed batch
    brew_date = datetime.now() - timedelta(days=21)
    batch_id = create_batch(db_session, recipe_id, "Completed Batch", brew_date, BatchStatus.COMPLETE.value)
    
    # Add workflow history for completion
    completion_date = brew_date + timedelta(days=14)
    workflow = models.BatchWorkflowHistory(
        batch_id=batch_id,
        from_status=BatchStatus.FERMENTING.value,
        to_status=BatchStatus.COMPLETE.value,
        changed_at=completion_date,
        notes="Completed fermentation",
    )
    db_session.add(workflow)
    db_session.commit()
    
    response = client.get("/analytics/fermentation-time")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    batch_data = data[0]
    
    assert batch_data["batch_id"] == batch_id
    assert batch_data["days_in_fermentation"] == 14


def test_og_fg_accuracy(client, db_session):
    """Test OG/FG accuracy tracking"""
    recipe_id = create_recipe_with_style(db_session, "Test IPA", "American IPA")
    batch_id = create_batch(db_session, recipe_id, "Accuracy Test", datetime.now() - timedelta(days=15))
    
    # Add fermentation readings
    og_reading = models.FermentationReadings(
        batch_id=batch_id,
        timestamp=datetime.now() - timedelta(days=15),
        gravity=1.052,  # Target was 1.050
        temperature=20.0,
        notes="Initial OG reading",
    )
    db_session.add(og_reading)
    
    fg_reading = models.FermentationReadings(
        batch_id=batch_id,
        timestamp=datetime.now() - timedelta(days=1),
        gravity=1.012,  # Target was 1.010
        temperature=20.0,
        notes="Final FG reading",
    )
    db_session.add(fg_reading)
    db_session.commit()
    
    response = client.get("/analytics/og-fg-accuracy")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    batch_data = data[0]
    
    assert batch_data["batch_id"] == batch_id
    assert batch_data["target_og"] == 1.050
    assert batch_data["actual_og"] == 1.052
    assert batch_data["target_fg"] == 1.010
    assert batch_data["actual_fg"] == 1.012
    assert batch_data["og_accuracy"] is not None
    assert batch_data["fg_accuracy"] is not None


def test_seasonal_patterns(client, db_session):
    """Test seasonal brewing patterns"""
    recipe_id = create_recipe_with_style(db_session, "Test IPA", "American IPA")
    
    # Create batches in different months
    create_batch(db_session, recipe_id, "Jan Batch", datetime(2024, 1, 15), BatchStatus.COMPLETE.value)
    create_batch(db_session, recipe_id, "Jan Batch 2", datetime(2024, 1, 25), BatchStatus.COMPLETE.value)
    create_batch(db_session, recipe_id, "Feb Batch", datetime(2024, 2, 10), BatchStatus.COMPLETE.value)
    create_batch(db_session, recipe_id, "Mar Batch", datetime(2024, 3, 5), BatchStatus.FERMENTING.value)
    
    response = client.get("/analytics/seasonal-patterns")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) >= 3  # At least 3 months with batches
    
    # Check January has 2 batches
    jan_data = next((d for d in data if d["month"] == 1 and d["year"] == 2024), None)
    assert jan_data is not None
    assert jan_data["batch_count"] == 2
    assert jan_data["month_name"] == "January"


def test_seasonal_patterns_with_date_filter(client, db_session):
    """Test seasonal patterns with date filtering"""
    recipe_id = create_recipe_with_style(db_session, "Test IPA", "American IPA")
    
    # Create batches across different years
    create_batch(db_session, recipe_id, "2023 Batch", datetime(2023, 12, 15), BatchStatus.COMPLETE.value)
    create_batch(db_session, recipe_id, "2024 Batch", datetime(2024, 1, 15), BatchStatus.COMPLETE.value)
    
    # Filter to only 2024
    start_date = "2024-01-01"
    response = client.get(f"/analytics/seasonal-patterns?start_date={start_date}")
    assert response.status_code == 200
    data = response.json()
    
    # Should only have 2024 data
    for pattern in data:
        assert pattern["year"] >= 2024
