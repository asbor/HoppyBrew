import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from Database.Models.recipes import Recipes
from Database.Models.batches import Batches
from Database.Models.brew_steps import BrewSteps
from Database.Models.Ingredients.hops import RecipeHop


def test_create_brew_steps(client, db_session):
    """Test creating brew steps from a recipe"""
    # Create a recipe first
    recipe = Recipes(
        name="Test IPA",
        version=1,
        type="All Grain",
        brewer="Test Brewer",
        batch_size=20.0,
        boil_size=25.0,
        boil_time=60,
        efficiency=75.0,
        primary_temp=65.0,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)
    
    # Add some hops to the recipe
    hop1 = RecipeHop(
        recipe_id=recipe.id,
        name="Cascade",
        amount=50.0,
        time=60,
        use="Boil",
    )
    hop2 = RecipeHop(
        recipe_id=recipe.id,
        name="Citra",
        amount=30.0,
        time=10,
        use="Boil",
    )
    db_session.add(hop1)
    db_session.add(hop2)
    db_session.commit()
    
    # Create a batch
    batch = Batches(
        recipe_id=recipe.id,
        batch_name="Test Batch IPA",
        batch_number=1,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now(),
        status="brewing",
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)
    
    # Create brew steps
    response = client.post(f"/batches/{batch.id}/brew-steps")
    
    assert response.status_code == 200
    steps = response.json()
    
    # Should have mash, sparge, boil, 2 hop additions, chill, and transfer steps
    assert len(steps) >= 6
    
    # Check that steps are ordered
    for i in range(len(steps) - 1):
        assert steps[i]["order_index"] <= steps[i + 1]["order_index"]
    
    # Check that mash step exists
    mash_steps = [s for s in steps if s["step_type"] == "mash"]
    assert len(mash_steps) == 1
    assert mash_steps[0]["duration"] == 60
    
    # Check that boil step exists
    boil_steps = [s for s in steps if s["step_type"] == "boil"]
    assert len(boil_steps) == 1
    assert boil_steps[0]["duration"] == 60
    
    # Check that hop additions exist
    hop_steps = [s for s in steps if s["step_type"] == "hop_addition"]
    assert len(hop_steps) == 2


def test_create_brew_steps_duplicate(client, db_session):
    """Test that creating brew steps twice fails"""
    # Create a recipe and batch
    recipe = Recipes(
        name="Test IPA",
        version=1,
        type="All Grain",
        brewer="Test Brewer",
        batch_size=20.0,
        boil_size=25.0,
        boil_time=60,
        efficiency=75.0,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)
    
    batch = Batches(
        recipe_id=recipe.id,
        batch_name="Test Batch IPA",
        batch_number=1,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now(),
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)
    
    # Create brew steps first time
    response1 = client.post(f"/batches/{batch.id}/brew-steps")
    assert response1.status_code == 200
    
    # Try to create again
    response2 = client.post(f"/batches/{batch.id}/brew-steps")
    assert response2.status_code == 400
    assert "already exist" in response2.json()["detail"]


def test_get_brew_steps(client, db_session):
    """Test getting brew steps for a batch"""
    # Create a recipe and batch
    recipe = Recipes(
        name="Test IPA",
        version=1,
        type="All Grain",
        brewer="Test Brewer",
        batch_size=20.0,
        boil_size=25.0,
        boil_time=60,
        efficiency=75.0,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)
    
    batch = Batches(
        recipe_id=recipe.id,
        batch_name="Test Batch IPA",
        batch_number=1,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now(),
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)
    
    # Create some brew steps manually
    step1 = BrewSteps(
        batch_id=batch.id,
        step_name="Mash",
        step_type="mash",
        duration=60,
        order_index=0,
    )
    step2 = BrewSteps(
        batch_id=batch.id,
        step_name="Boil",
        step_type="boil",
        duration=60,
        order_index=1,
    )
    db_session.add(step1)
    db_session.add(step2)
    db_session.commit()
    
    # Get brew steps
    response = client.get(f"/batches/{batch.id}/brew-steps")
    
    assert response.status_code == 200
    steps = response.json()
    assert len(steps) == 2
    assert steps[0]["step_name"] == "Mash"
    assert steps[1]["step_name"] == "Boil"


def test_get_single_brew_step(client, db_session):
    """Test getting a single brew step"""
    # Create a recipe and batch
    recipe = Recipes(
        name="Test IPA",
        version=1,
        type="All Grain",
        brewer="Test Brewer",
        batch_size=20.0,
        boil_size=25.0,
        boil_time=60,
        efficiency=75.0,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)
    
    batch = Batches(
        recipe_id=recipe.id,
        batch_name="Test Batch IPA",
        batch_number=1,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now(),
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)
    
    # Create a brew step
    step = BrewSteps(
        batch_id=batch.id,
        step_name="Mash",
        step_type="mash",
        duration=60,
        temperature=65,
        notes="Test notes",
        order_index=0,
    )
    db_session.add(step)
    db_session.commit()
    db_session.refresh(step)
    
    # Get the brew step
    response = client.get(f"/brew-steps/{step.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["step_name"] == "Mash"
    assert data["step_type"] == "mash"
    assert data["duration"] == 60
    assert data["temperature"] == 65


def test_update_brew_step(client, db_session):
    """Test updating a brew step"""
    # Create a recipe and batch
    recipe = Recipes(
        name="Test IPA",
        version=1,
        type="All Grain",
        brewer="Test Brewer",
        batch_size=20.0,
        boil_size=25.0,
        boil_time=60,
        efficiency=75.0,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)
    
    batch = Batches(
        recipe_id=recipe.id,
        batch_name="Test Batch IPA",
        batch_number=1,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now(),
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)
    
    # Create a brew step
    step = BrewSteps(
        batch_id=batch.id,
        step_name="Mash",
        step_type="mash",
        duration=60,
        order_index=0,
        completed=False,
    )
    db_session.add(step)
    db_session.commit()
    db_session.refresh(step)
    
    # Update the brew step to mark it as completed
    update_data = {
        "completed": True,
        "completed_at": datetime.now().isoformat(),
    }
    response = client.patch(f"/brew-steps/{step.id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["completed_at"] is not None


def test_delete_brew_step(client, db_session):
    """Test deleting a brew step"""
    # Create a recipe and batch
    recipe = Recipes(
        name="Test IPA",
        version=1,
        type="All Grain",
        brewer="Test Brewer",
        batch_size=20.0,
        boil_size=25.0,
        boil_time=60,
        efficiency=75.0,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)
    
    batch = Batches(
        recipe_id=recipe.id,
        batch_name="Test Batch IPA",
        batch_number=1,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now(),
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)
    
    # Create a brew step
    step = BrewSteps(
        batch_id=batch.id,
        step_name="Mash",
        step_type="mash",
        duration=60,
        order_index=0,
    )
    db_session.add(step)
    db_session.commit()
    db_session.refresh(step)
    
    step_id = step.id
    
    # Delete the brew step
    response = client.delete(f"/brew-steps/{step_id}")
    
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verify it's deleted
    response = client.get(f"/brew-steps/{step_id}")
    assert response.status_code == 404


def test_start_brew_day(client, db_session):
    """Test starting a brew day"""
    # Create a recipe and batch
    recipe = Recipes(
        name="Test IPA",
        version=1,
        type="All Grain",
        brewer="Test Brewer",
        batch_size=20.0,
        boil_size=25.0,
        boil_time=60,
        efficiency=75.0,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)
    
    batch = Batches(
        recipe_id=recipe.id,
        batch_name="Test Batch IPA",
        batch_number=1,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now(),
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)
    
    # Create some brew steps
    step1 = BrewSteps(
        batch_id=batch.id,
        step_name="Mash",
        step_type="mash",
        duration=60,
        order_index=0,
        completed=False,
    )
    step2 = BrewSteps(
        batch_id=batch.id,
        step_name="Boil",
        step_type="boil",
        duration=60,
        order_index=1,
        completed=False,
    )
    db_session.add(step1)
    db_session.add(step2)
    db_session.commit()
    
    # Start brew day
    response = client.post(f"/batches/{batch.id}/brew-steps/start")
    
    assert response.status_code == 200
    data = response.json()
    assert data["step_name"] == "Mash"
    assert data["started_at"] is not None
    assert data["completed"] is False
