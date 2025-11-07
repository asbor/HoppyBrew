"""Tests for water profile endpoints."""

import pytest
from fastapi.testclient import TestClient
from decimal import Decimal


def test_create_water_profile(client: TestClient):
    """Test creating a new water profile."""
    profile_data = {
        "name": "Test Profile",
        "description": "A test water profile",
        "profile_type": "source",
        "calcium": 50,
        "magnesium": 10,
        "sodium": 15,
        "chloride": 40,
        "sulfate": 50,
        "bicarbonate": 100,
    }

    response = client.post("/water-profiles", json=profile_data)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Test Profile"
    assert data["profile_type"] == "source"
    assert data["is_custom"] == True
    assert "id" in data
    assert "created_at" in data


def test_get_all_water_profiles(client: TestClient):
    """Test getting all water profiles."""
    # Create a test profile first
    profile_data = {
        "name": "Test Profile 1",
        "profile_type": "source",
        "calcium": 50,
    }
    client.post("/water-profiles", json=profile_data)

    response = client.get("/water-profiles")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_water_profile_by_id(client: TestClient):
    """Test getting a specific water profile by ID."""
    # Create a profile
    profile_data = {
        "name": "Test Profile 2",
        "profile_type": "target",
        "style_category": "IPA",
        "calcium": 100,
    }
    create_response = client.post("/water-profiles", json=profile_data)
    profile_id = create_response.json()["id"]

    # Get the profile
    response = client.get(f"/water-profiles/{profile_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == profile_id
    assert data["name"] == "Test Profile 2"


def test_get_nonexistent_profile(client: TestClient):
    """Test getting a profile that doesn't exist."""
    response = client.get("/water-profiles/99999")
    assert response.status_code == 404


def test_update_water_profile(client: TestClient):
    """Test updating a water profile."""
    # Create a custom profile
    profile_data = {
        "name": "Test Profile 3",
        "profile_type": "source",
        "calcium": 50,
        "is_custom": True,
    }
    create_response = client.post("/water-profiles", json=profile_data)
    profile_id = create_response.json()["id"]

    # Update the profile
    update_data = {
        "name": "Updated Test Profile",
        "calcium": 75,
    }
    response = client.put(f"/water-profiles/{profile_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Updated Test Profile"
    assert float(data["calcium"]) == 75


def test_update_default_profile_fails(client: TestClient, db_session):
    """Test that updating a default profile is prevented."""
    from Database.Models.Profiles.water_profiles import WaterProfiles

    # Create a default profile
    default_profile = WaterProfiles(
        name="Default Profile",
        profile_type="source",
        calcium=50,
        is_default=True,
        is_custom=False,
    )
    db_session.add(default_profile)
    db_session.commit()
    db_session.refresh(default_profile)

    # Try to update it
    update_data = {"name": "Should Fail"}
    response = client.put(f"/water-profiles/{default_profile.id}", json=update_data)
    assert response.status_code == 403


def test_delete_water_profile(client: TestClient):
    """Test deleting a custom water profile."""
    # Create a custom profile
    profile_data = {
        "name": "Test Profile 4",
        "profile_type": "source",
        "is_custom": True,
    }
    create_response = client.post("/water-profiles", json=profile_data)
    profile_id = create_response.json()["id"]

    # Delete the profile
    response = client.delete(f"/water-profiles/{profile_id}")
    assert response.status_code == 200

    # Verify it's gone
    get_response = client.get(f"/water-profiles/{profile_id}")
    assert get_response.status_code == 404


def test_delete_default_profile_fails(client: TestClient, db_session):
    """Test that deleting a default profile is prevented."""
    from Database.Models.Profiles.water_profiles import WaterProfiles

    # Create a default profile
    default_profile = WaterProfiles(
        name="Default Profile 2",
        profile_type="source",
        calcium=50,
        is_default=True,
        is_custom=False,
    )
    db_session.add(default_profile)
    db_session.commit()
    db_session.refresh(default_profile)

    # Try to delete it
    response = client.delete(f"/water-profiles/{default_profile.id}")
    assert response.status_code == 403


def test_duplicate_water_profile(client: TestClient):
    """Test duplicating a water profile."""
    # Create a profile
    profile_data = {
        "name": "Original Profile",
        "description": "Original description",
        "profile_type": "target",
        "style_category": "IPA",
        "calcium": 100,
        "sulfate": 300,
    }
    create_response = client.post("/water-profiles", json=profile_data)
    profile_id = create_response.json()["id"]

    # Duplicate it
    response = client.post(f"/water-profiles/{profile_id}/duplicate")
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Original Profile (Copy)"
    assert data["description"] == "Original description"
    assert float(data["calcium"]) == 100
    assert data["is_custom"] == True
    assert data["is_default"] == False


def test_duplicate_with_custom_name(client: TestClient):
    """Test duplicating a profile with a custom name."""
    # Create a profile
    profile_data = {
        "name": "Original Profile 2",
        "profile_type": "source",
    }
    create_response = client.post("/water-profiles", json=profile_data)
    profile_id = create_response.json()["id"]

    # Duplicate with custom name
    response = client.post(
        f"/water-profiles/{profile_id}/duplicate", params={"new_name": "My Custom Duplicate"}
    )
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "My Custom Duplicate"


def test_filter_by_profile_type(client: TestClient):
    """Test filtering profiles by type."""
    # Create profiles of different types
    client.post(
        "/water-profiles",
        json={
            "name": "Source Profile",
            "profile_type": "source",
        },
    )
    client.post(
        "/water-profiles",
        json={
            "name": "Target Profile",
            "profile_type": "target",
        },
    )

    # Filter by source
    response = client.get("/water-profiles?profile_type=source")
    assert response.status_code == 200
    data = response.json()
    assert all(p["profile_type"] == "source" for p in data)

    # Filter by target
    response = client.get("/water-profiles?profile_type=target")
    assert response.status_code == 200
    data = response.json()
    assert all(p["profile_type"] == "target" for p in data)


def test_filter_by_style_category(client: TestClient):
    """Test filtering profiles by style category."""
    # Create profiles with different style categories
    client.post(
        "/water-profiles",
        json={
            "name": "IPA Profile",
            "profile_type": "target",
            "style_category": "IPA",
        },
    )
    client.post(
        "/water-profiles",
        json={
            "name": "Stout Profile",
            "profile_type": "target",
            "style_category": "Stout",
        },
    )

    # Filter by IPA
    response = client.get("/water-profiles?style_category=IPA")
    assert response.status_code == 200
    data = response.json()
    assert all(p["style_category"] == "IPA" for p in data)


def test_filter_by_is_default(client: TestClient, db_session):
    """Test filtering profiles by default status."""
    from Database.Models.Profiles.water_profiles import WaterProfiles

    # Create a default profile
    default_profile = WaterProfiles(
        name="Default Profile 3",
        profile_type="source",
        is_default=True,
        is_custom=False,
    )
    db_session.add(default_profile)
    db_session.commit()

    # Create a custom profile
    client.post(
        "/water-profiles",
        json={
            "name": "Custom Profile",
            "profile_type": "source",
            "is_custom": True,
        },
    )

    # Filter by default
    response = client.get("/water-profiles?is_default=true")
    assert response.status_code == 200
    data = response.json()
    assert all(p["is_default"] == True for p in data)

    # Filter by custom
    response = client.get("/water-profiles?is_default=false")
    assert response.status_code == 200
    data = response.json()
    assert all(p["is_default"] == False for p in data)


def test_create_duplicate_name_fails(client: TestClient):
    """Test that creating a profile with duplicate name and type fails."""
    profile_data = {
        "name": "Duplicate Test",
        "profile_type": "source",
    }

    # Create first profile
    response1 = client.post("/water-profiles", json=profile_data)
    assert response1.status_code == 201

    # Try to create duplicate
    response2 = client.post("/water-profiles", json=profile_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]


def test_ion_validation(client: TestClient):
    """Test that ion concentrations are validated."""
    # Test negative value
    profile_data = {
        "name": "Invalid Profile",
        "profile_type": "source",
        "calcium": -10,  # Invalid negative value
    }
    response = client.post("/water-profiles", json=profile_data)
    assert response.status_code == 422  # Validation error


def test_profile_type_validation(client: TestClient):
    """Test that profile_type is validated."""
    profile_data = {
        "name": "Invalid Type Profile",
        "profile_type": "invalid_type",  # Invalid type
    }
    response = client.post("/water-profiles", json=profile_data)
    assert response.status_code == 422  # Validation error
