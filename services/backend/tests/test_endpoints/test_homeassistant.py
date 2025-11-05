"""
Tests for HomeAssistant integration endpoints
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from sqlalchemy.orm import Session


def test_homeassistant_summary_empty(client: TestClient):
    """Test brewery summary with no batches"""
    response = client.get("/homeassistant/summary")
    assert response.status_code == 200
    data = response.json()
    
    assert data["active_batches"] == 0
    assert data["total_batches"] == 0
    assert data["state"] == "idle"
    assert "icon" in data


def test_homeassistant_batches_empty(client: TestClient):
    """Test batches endpoint with no batches"""
    response = client.get("/homeassistant/batches")
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) == 0


def test_homeassistant_batch_not_found(client: TestClient):
    """Test getting a non-existent batch"""
    response = client.get("/homeassistant/batches/999")
    assert response.status_code == 404


def test_homeassistant_batch_sensor_format(client: TestClient, sample_batch):
    """Test that batch sensor has correct format"""
    batch_id = sample_batch["id"]
    response = client.get(f"/homeassistant/batches/{batch_id}")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check required fields
    assert "entity_id" in data
    assert "name" in data
    assert "state" in data
    assert "attributes" in data
    assert "icon" in data
    
    # Validate entity_id format
    assert data["entity_id"].startswith("sensor.hoppybrew_batch_")
    
    # Validate state is one of the expected values
    assert data["state"] in ["brewing", "fermenting", "conditioning", "ready"]
    
    # Validate attributes
    attrs = data["attributes"]
    assert "batch_id" in attrs
    assert "batch_name" in attrs
    assert "batch_size" in attrs
    assert "age_days" in attrs
    assert "recipe_name" in attrs


def test_homeassistant_batches_list(client: TestClient, sample_batch):
    """Test getting all batches as sensors"""
    response = client.get("/homeassistant/batches")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Check first batch has correct structure
    batch_sensor = data[0]
    assert "entity_id" in batch_sensor
    assert "name" in batch_sensor
    assert "state" in batch_sensor
    assert "attributes" in batch_sensor


def test_homeassistant_summary_with_batches(client: TestClient, sample_batch):
    """Test brewery summary with active batches"""
    response = client.get("/homeassistant/summary")
    assert response.status_code == 200
    
    data = response.json()
    
    assert data["active_batches"] >= 1
    assert data["total_batches"] >= 1
    assert data["state"] == "active"
    assert "brewing_batches" in data
    assert "fermenting_batches" in data
    assert "conditioning_batches" in data
    assert "ready_batches" in data


def test_homeassistant_batch_state_transitions(client: TestClient, db_session: Session):
    """Test that batch state changes based on age"""
    from Database.Models.batches import Batches
    from Database.Models.recipes import Recipes
    
    # Create a recipe first
    recipe = Recipes(
        name="Test Recipe",
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
    
    # Test brewing state (age: 0 days)
    brewing_batch = Batches(
        recipe_id=recipe.id,
        batch_name="Fresh Batch",
        batch_number=1,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db_session.add(brewing_batch)
    db_session.commit()
    db_session.refresh(brewing_batch)
    
    response = client.get(f"/homeassistant/batches/{brewing_batch.id}")
    assert response.status_code == 200
    assert response.json()["state"] == "brewing"
    
    # Test fermenting state (age: 7 days)
    fermenting_batch = Batches(
        recipe_id=recipe.id,
        batch_name="Fermenting Batch",
        batch_number=2,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now() - timedelta(days=7),
        created_at=datetime.now() - timedelta(days=7),
        updated_at=datetime.now(),
    )
    db_session.add(fermenting_batch)
    db_session.commit()
    db_session.refresh(fermenting_batch)
    
    response = client.get(f"/homeassistant/batches/{fermenting_batch.id}")
    assert response.status_code == 200
    assert response.json()["state"] == "fermenting"
    
    # Test conditioning state (age: 21 days)
    conditioning_batch = Batches(
        recipe_id=recipe.id,
        batch_name="Conditioning Batch",
        batch_number=3,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now() - timedelta(days=21),
        created_at=datetime.now() - timedelta(days=21),
        updated_at=datetime.now(),
    )
    db_session.add(conditioning_batch)
    db_session.commit()
    db_session.refresh(conditioning_batch)
    
    response = client.get(f"/homeassistant/batches/{conditioning_batch.id}")
    assert response.status_code == 200
    assert response.json()["state"] == "conditioning"
    
    # Test ready state (age: 30 days)
    ready_batch = Batches(
        recipe_id=recipe.id,
        batch_name="Ready Batch",
        batch_number=4,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now() - timedelta(days=30),
        created_at=datetime.now() - timedelta(days=30),
        updated_at=datetime.now(),
    )
    db_session.add(ready_batch)
    db_session.commit()
    db_session.refresh(ready_batch)
    
    response = client.get(f"/homeassistant/batches/{ready_batch.id}")
    assert response.status_code == 200
    assert response.json()["state"] == "ready"


def test_homeassistant_mqtt_discovery(client: TestClient, sample_batch):
    """Test MQTT discovery configuration endpoint"""
    batch_id = sample_batch["id"]
    response = client.get(f"/homeassistant/discovery/batch/{batch_id}")
    assert response.status_code == 200
    
    data = response.json()
    
    # Check required MQTT discovery fields
    assert "name" in data
    assert "state_topic" in data
    assert "unique_id" in data
    assert "device" in data
    
    # Validate topics
    assert f"hoppybrew/batch/{batch_id}" in data["state_topic"]
    
    # Validate device info
    device = data["device"]
    assert "identifiers" in device
    assert "name" in device
    assert "manufacturer" in device
    assert device["manufacturer"] == "HoppyBrew"


def test_homeassistant_batch_attributes_completeness(client: TestClient, sample_batch):
    """Test that batch attributes include all expected fields"""
    batch_id = sample_batch["id"]
    response = client.get(f"/homeassistant/batches/{batch_id}")
    assert response.status_code == 200
    
    attrs = response.json()["attributes"]
    
    # Essential attributes
    required_attrs = [
        "batch_id",
        "batch_name",
        "batch_number",
        "batch_size",
        "batch_size_unit",
        "brewer",
        "brew_date",
        "created_at",
        "updated_at",
        "age_days",
        "recipe_id",
        "recipe_name",
    ]
    
    for attr in required_attrs:
        assert attr in attrs, f"Missing required attribute: {attr}"
    
    # Validate types
    assert isinstance(attrs["batch_id"], int)
    assert isinstance(attrs["batch_number"], int)
    assert isinstance(attrs["batch_size"], (int, float))
    assert isinstance(attrs["age_days"], int)
    assert attrs["batch_size_unit"] == "L"


def test_homeassistant_summary_counts(client: TestClient, db_session: Session):
    """Test that summary counts are accurate"""
    from Database.Models.batches import Batches
    from Database.Models.recipes import Recipes
    
    # Create a recipe
    recipe = Recipes(
        name="Test Recipe",
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
    
    # Create batches in different states
    # 1 brewing (0 days)
    batch1 = Batches(
        recipe_id=recipe.id,
        batch_name="Batch 1",
        batch_number=1,
        batch_size=20.0,
        brewer="Test",
        brew_date=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    
    # 1 fermenting (7 days)
    batch2 = Batches(
        recipe_id=recipe.id,
        batch_name="Batch 2",
        batch_number=2,
        batch_size=20.0,
        brewer="Test",
        brew_date=datetime.now() - timedelta(days=7),
        created_at=datetime.now() - timedelta(days=7),
        updated_at=datetime.now(),
    )
    
    db_session.add_all([batch1, batch2])
    db_session.commit()
    
    response = client.get("/homeassistant/summary")
    assert response.status_code == 200
    
    data = response.json()
    
    # Should have at least our 2 batches
    assert data["total_batches"] >= 2
    assert data["brewing_batches"] >= 1
    assert data["fermenting_batches"] >= 1
