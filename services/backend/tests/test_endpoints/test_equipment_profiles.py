"""Tests for equipment profile endpoints."""

from fastapi.testclient import TestClient


def test_create_equipment_profile(client: TestClient):
    """Test creating a new equipment profile."""
    profile_data = {
        "name": "Test Brewery",
        "version": 1,
        "boil_size": 30,
        "batch_size": 20,
        "tun_volume": 40,
        "evap_rate": 10,
        "boil_time": 60,
        "brewhouse_efficiency": 75.0,
        "mash_efficiency": 85.0,
        "trub_chiller_loss": 2,
        "lauter_deadspace": 1,
    }

    response = client.post("/equipment", json=profile_data)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Test Brewery"
    assert data["brewhouse_efficiency"] == 75.0
    assert data["mash_efficiency"] == 85.0
    assert "id" in data


def test_get_all_equipment_profiles(client: TestClient):
    """Test getting all equipment profiles."""
    # Create a test profile first
    profile_data = {
        "name": "Test Brewery 2",
        "batch_size": 20,
        "brewhouse_efficiency": 70.0,
    }
    client.post("/equipment", json=profile_data)

    response = client.get("/equipment")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_equipment_profile_by_id(client: TestClient):
    """Test getting a specific equipment profile by ID."""
    # Create a profile
    profile_data = {
        "name": "Test Brewery 3",
        "batch_size": 25,
        "brewhouse_efficiency": 78.5,
        "mash_efficiency": 88.0,
    }
    create_response = client.post("/equipment", json=profile_data)
    profile_id = create_response.json()["id"]

    # Get the profile
    response = client.get(f"/equipment/{profile_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == profile_id
    assert data["name"] == "Test Brewery 3"
    assert data["brewhouse_efficiency"] == 78.5


def test_get_nonexistent_equipment_profile(client: TestClient):
    """Test getting a profile that doesn't exist."""
    response = client.get("/equipment/99999")
    assert response.status_code == 404


def test_update_equipment_profile(client: TestClient):
    """Test updating an equipment profile."""
    # Create a profile
    profile_data = {
        "name": "Test Brewery 4",
        "batch_size": 20,
        "brewhouse_efficiency": 70.0,
    }
    create_response = client.post("/equipment", json=profile_data)
    profile_id = create_response.json()["id"]

    # Update the profile
    update_data = {
        "name": "Updated Brewery",
        "brewhouse_efficiency": 80.0,
        "mash_efficiency": 90.0,
    }
    response = client.put(f"/equipment/{profile_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Updated Brewery"
    assert data["brewhouse_efficiency"] == 80.0
    assert data["mash_efficiency"] == 90.0


def test_update_nonexistent_equipment_profile(client: TestClient):
    """Test updating a profile that doesn't exist."""
    update_data = {"name": "Should Fail"}
    response = client.put("/equipment/99999", json=update_data)
    assert response.status_code == 404


def test_delete_equipment_profile(client: TestClient):
    """Test deleting an equipment profile."""
    # Create a profile
    profile_data = {
        "name": "Test Brewery 5",
        "batch_size": 20,
    }
    create_response = client.post("/equipment", json=profile_data)
    profile_id = create_response.json()["id"]

    # Delete the profile
    response = client.delete(f"/equipment/{profile_id}")
    assert response.status_code == 200

    # Verify it's gone
    get_response = client.get(f"/equipment/{profile_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_equipment_profile(client: TestClient):
    """Test deleting a profile that doesn't exist."""
    response = client.delete("/equipment/99999")
    assert response.status_code == 404


def test_create_duplicate_name_fails(client: TestClient):
    """Test that creating a profile with duplicate name fails."""
    profile_data = {
        "name": "Duplicate Test",
        "batch_size": 20,
    }

    # Create first profile
    response1 = client.post("/equipment", json=profile_data)
    assert response1.status_code == 201

    # Try to create duplicate
    response2 = client.post("/equipment", json=profile_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]


def test_update_to_duplicate_name_fails(client: TestClient):
    """Test that updating to an existing name fails."""
    # Create two profiles
    profile1_data = {"name": "Profile A", "batch_size": 20}
    profile2_data = {"name": "Profile B", "batch_size": 25}

    client.post("/equipment", json=profile1_data)
    create_response = client.post("/equipment", json=profile2_data)
    profile2_id = create_response.json()["id"]

    # Try to update profile2 to have the same name as profile1
    update_data = {"name": "Profile A"}
    response = client.put(f"/equipment/{profile2_id}", json=update_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_efficiency_tracking(client: TestClient):
    """Test that efficiency values are properly stored and retrieved."""
    profile_data = {
        "name": "Efficiency Test Brewery",
        "batch_size": 20,
        "brewhouse_efficiency": 72.5,
        "mash_efficiency": 82.5,
    }

    # Create profile
    create_response = client.post("/equipment", json=profile_data)
    assert create_response.status_code == 201
    profile_id = create_response.json()["id"]

    # Verify efficiency values are returned
    data = create_response.json()
    assert data["brewhouse_efficiency"] == 72.5
    assert data["mash_efficiency"] == 82.5

    # Get profile and verify efficiency values persist
    get_response = client.get(f"/equipment/{profile_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["brewhouse_efficiency"] == 72.5
    assert data["mash_efficiency"] == 82.5


def test_partial_update_preserves_fields(client: TestClient):
    """Test that partial updates don't overwrite other fields."""
    profile_data = {
        "name": "Partial Update Test",
        "batch_size": 20,
        "boil_size": 30,
        "brewhouse_efficiency": 75.0,
        "mash_efficiency": 85.0,
    }

    # Create profile
    create_response = client.post("/equipment", json=profile_data)
    profile_id = create_response.json()["id"]

    # Update only efficiency
    update_data = {"brewhouse_efficiency": 80.0}
    response = client.put(f"/equipment/{profile_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["brewhouse_efficiency"] == 80.0
    assert data["mash_efficiency"] == 85.0  # Should be preserved
    assert data["batch_size"] == 20  # Should be preserved
    assert data["name"] == "Partial Update Test"  # Should be preserved


def test_volume_fields(client: TestClient):
    """Test that volume and loss fields are properly handled."""
    profile_data = {
        "name": "Volume Test Brewery",
        "batch_size": 20,
        "boil_size": 30,
        "tun_volume": 40,
        "trub_chiller_loss": 2,
        "lauter_deadspace": 1,
        "top_up_kettle": 0,
        "top_up_water": 0,
    }

    response = client.post("/equipment", json=profile_data)
    assert response.status_code == 201

    data = response.json()
    assert data["batch_size"] == 20
    assert data["boil_size"] == 30
    assert data["tun_volume"] == 40
    assert data["trub_chiller_loss"] == 2
    assert data["lauter_deadspace"] == 1


def test_batch_equipment_association(client: TestClient, db_session):
    """Test that batches can be associated with equipment profiles."""
    from Database.Models import Batches, EquipmentProfiles, Recipes
    from datetime import datetime

    # Create a recipe first (needed for batch)
    recipe = Recipes(
        name="Test Recipe for Equipment",
        version=1,
        type="Ale",
        brewer="Test Brewer",
        batch_size=20.0,
        boil_size=25.0,
        boil_time=60,
    )
    db_session.add(recipe)
    db_session.commit()
    db_session.refresh(recipe)

    # Create an equipment profile
    profile_data = {
        "name": "Test Equipment for Batch",
        "batch_size": 20,
        "brewhouse_efficiency": 75.0,
    }
    equipment_response = client.post("/equipment", json=profile_data)
    assert equipment_response.status_code == 201
    equipment_id = int(equipment_response.json()["id"])

    # Create a batch with equipment association
    batch = Batches(
        batch_name="Test Batch with Equipment",
        batch_number=1,
        batch_size=20.0,
        brewer="Test Brewer",
        brew_date=datetime.now(),
        recipe_id=recipe.id,
        equipment_id=equipment_id,
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)

    # Verify the association
    assert batch.equipment_id == equipment_id
    assert batch.equipment_profile is not None
    assert batch.equipment_profile.name == "Test Equipment for Batch"
    assert batch.equipment_profile.brewhouse_efficiency == 75.0

    # Verify from equipment side
    equipment = db_session.query(EquipmentProfiles).filter(
        EquipmentProfiles.id == equipment_id
    ).first()
    assert equipment is not None
    assert len(equipment.batches) == 1
    assert equipment.batches[0].id == batch.id
