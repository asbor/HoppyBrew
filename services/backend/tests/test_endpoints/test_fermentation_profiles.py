import Database.Models as models


def test_create_fermentation_profile_without_steps(client, db_session):
    """Test creating a basic fermentation profile without steps"""
    profile_data = {
        "name": "Test Ale Profile",
        "description": "A test fermentation profile",
        "is_pressurized": False,
        "is_template": True,
    }

    response = client.post("/fermentation-profiles", json=profile_data)
    assert response.status_code == 201

    payload = response.json()
    assert payload["name"] == "Test Ale Profile"
    assert payload["description"] == "A test fermentation profile"
    assert payload["is_pressurized"] is False
    assert payload["is_template"] is True
    assert "id" in payload
    assert "created_at" in payload
    assert "updated_at" in payload
    assert payload["steps"] == []


def test_create_fermentation_profile_with_steps(client, db_session):
    """Test creating a fermentation profile with steps"""
    profile_data = {
        "name": "Complete Ale Profile",
        "description": "Ale profile with fermentation steps",
        "is_pressurized": False,
        "is_template": True,
        "steps": [
            {
                "step_order": 1,
                "name": "Primary Fermentation",
                "step_type": "primary",
                "temperature": 20,
                "duration_days": 7,
                "ramp_days": 0,
                "notes": "Primary fermentation phase",
            },
            {
                "step_order": 2,
                "name": "Conditioning",
                "step_type": "conditioning",
                "temperature": 18,
                "duration_days": 7,
                "ramp_days": 1,
            },
        ],
    }

    response = client.post("/fermentation-profiles", json=profile_data)
    assert response.status_code == 201

    payload = response.json()
    assert payload["name"] == "Complete Ale Profile"
    assert len(payload["steps"]) == 2
    assert payload["steps"][0]["name"] == "Primary Fermentation"
    assert payload["steps"][0]["temperature"] == "20.00"
    assert payload["steps"][0]["duration_days"] == 7
    assert payload["steps"][1]["name"] == "Conditioning"
    assert payload["steps"][1]["ramp_days"] == 1


def test_get_all_fermentation_profiles(client, db_session):
    """Test getting all fermentation profiles"""
    # Create test profiles
    profile1 = models.FermentationProfiles(
        name="Ale Profile",
        description="Standard ale",
        is_pressurized=False,
        is_template=True,
    )
    profile2 = models.FermentationProfiles(
        name="Lager Profile",
        description="Standard lager",
        is_pressurized=False,
        is_template=True,
    )
    db_session.add(profile1)
    db_session.add(profile2)
    db_session.commit()

    response = client.get("/fermentation-profiles")
    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) == 2
    assert any(p["name"] == "Ale Profile" for p in payload)
    assert any(p["name"] == "Lager Profile" for p in payload)


def test_get_fermentation_profile_by_id(client, db_session):
    """Test getting a specific fermentation profile by ID"""
    profile = models.FermentationProfiles(
        name="Test Profile",
        description="Test description",
        is_pressurized=False,
        is_template=False,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)

    # Add a step
    step = models.FermentationSteps(
        fermentation_profile_id=profile.id,
        step_order=1,
        name="Primary",
        step_type="primary",
        temperature=20,
        duration_days=7,
    )
    db_session.add(step)
    db_session.commit()

    response = client.get(f"/fermentation-profiles/{profile.id}")
    assert response.status_code == 200

    payload = response.json()
    assert payload["name"] == "Test Profile"
    assert len(payload["steps"]) == 1
    assert payload["steps"][0]["name"] == "Primary"


def test_get_fermentation_profile_not_found(client, db_session):
    """Test getting a non-existent fermentation profile"""
    response = client.get("/fermentation-profiles/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_fermentation_profile(client, db_session):
    """Test updating a fermentation profile"""
    profile = models.FermentationProfiles(
        name="Original Name",
        description="Original description",
        is_pressurized=False,
        is_template=False,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)

    update_data = {
        "name": "Updated Name",
        "description": "Updated description",
        "is_pressurized": True,
    }

    response = client.put(f"/fermentation-profiles/{profile.id}", json=update_data)
    assert response.status_code == 200

    payload = response.json()
    assert payload["name"] == "Updated Name"
    assert payload["description"] == "Updated description"
    assert payload["is_pressurized"] is True


def test_delete_fermentation_profile(client, db_session):
    """Test deleting a fermentation profile"""
    profile = models.FermentationProfiles(
        name="To Delete",
        description="Will be deleted",
        is_pressurized=False,
        is_template=False,
    )
    db_session.add(profile)
    db_session.commit()
    profile_id = profile.id

    response = client.delete(f"/fermentation-profiles/{profile_id}")
    assert response.status_code == 204

    # Verify it's deleted
    deleted_profile = (
        db_session.query(models.FermentationProfiles)
        .filter(models.FermentationProfiles.id == profile_id)
        .first()
    )
    assert deleted_profile is None


def test_delete_fermentation_profile_cascades_to_steps(client, db_session):
    """Test that deleting a profile also deletes its steps"""
    profile = models.FermentationProfiles(
        name="Profile with Steps",
        is_pressurized=False,
        is_template=False,
    )
    db_session.add(profile)
    db_session.commit()
    profile_id = profile.id

    # Add steps
    step1 = models.FermentationSteps(
        fermentation_profile_id=profile_id,
        step_order=1,
        name="Step 1",
        step_type="primary",
    )
    step2 = models.FermentationSteps(
        fermentation_profile_id=profile_id,
        step_order=2,
        name="Step 2",
        step_type="conditioning",
    )
    db_session.add(step1)
    db_session.add(step2)
    db_session.commit()

    # Delete the profile
    response = client.delete(f"/fermentation-profiles/{profile_id}")
    assert response.status_code == 204

    # Verify steps are also deleted
    remaining_steps = (
        db_session.query(models.FermentationSteps)
        .filter(models.FermentationSteps.fermentation_profile_id == profile_id)
        .all()
    )
    assert len(remaining_steps) == 0


def test_get_fermentation_steps(client, db_session):
    """Test getting steps for a profile"""
    profile = models.FermentationProfiles(
        name="Test Profile",
        is_pressurized=False,
        is_template=False,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)

    # Add steps
    step1 = models.FermentationSteps(
        fermentation_profile_id=profile.id,
        step_order=1,
        name="Primary",
        step_type="primary",
        temperature=20,
        duration_days=7,
    )
    step2 = models.FermentationSteps(
        fermentation_profile_id=profile.id,
        step_order=2,
        name="Secondary",
        step_type="secondary",
        temperature=18,
        duration_days=14,
    )
    db_session.add(step1)
    db_session.add(step2)
    db_session.commit()

    response = client.get(f"/fermentation-profiles/{profile.id}/steps")
    assert response.status_code == 200

    payload = response.json()
    assert len(payload) == 2
    assert payload[0]["name"] == "Primary"
    assert payload[1]["name"] == "Secondary"


def test_add_fermentation_step(client, db_session):
    """Test adding a step to a profile"""
    profile = models.FermentationProfiles(
        name="Test Profile",
        is_pressurized=False,
        is_template=False,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)

    step_data = {
        "step_order": 1,
        "name": "New Step",
        "step_type": "primary",
        "temperature": 20,
        "duration_days": 7,
        "ramp_days": 0,
        "notes": "Test step",
    }

    response = client.post(f"/fermentation-profiles/{profile.id}/steps", json=step_data)
    assert response.status_code == 201

    payload = response.json()
    assert payload["name"] == "New Step"
    assert payload["fermentation_profile_id"] == profile.id
    assert payload["temperature"] == "20.00"


def test_update_fermentation_step(client, db_session):
    """Test updating a fermentation step"""
    profile = models.FermentationProfiles(
        name="Test Profile",
        is_pressurized=False,
        is_template=False,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)

    step = models.FermentationSteps(
        fermentation_profile_id=profile.id,
        step_order=1,
        name="Original Step",
        step_type="primary",
        temperature=20,
        duration_days=7,
    )
    db_session.add(step)
    db_session.commit()
    db_session.refresh(step)

    update_data = {
        "name": "Updated Step",
        "temperature": 22,
        "duration_days": 10,
    }

    response = client.put(f"/fermentation-steps/{step.id}", json=update_data)
    assert response.status_code == 200

    payload = response.json()
    assert payload["name"] == "Updated Step"
    assert payload["temperature"] == "22.00"
    assert payload["duration_days"] == 10


def test_delete_fermentation_step(client, db_session):
    """Test deleting a fermentation step"""
    profile = models.FermentationProfiles(
        name="Test Profile",
        is_pressurized=False,
        is_template=False,
    )
    db_session.add(profile)
    db_session.commit()
    profile_id = profile.id

    step = models.FermentationSteps(
        fermentation_profile_id=profile_id,
        step_order=1,
        name="To Delete",
        step_type="primary",
    )
    db_session.add(step)
    db_session.commit()
    step_id = step.id

    response = client.delete(f"/fermentation-steps/{step_id}")
    assert response.status_code == 204

    # Verify it's deleted
    deleted_step = (
        db_session.query(models.FermentationSteps)
        .filter(models.FermentationSteps.id == step_id)
        .first()
    )
    assert deleted_step is None


def test_pressurized_fermentation_with_pressure(client, db_session):
    """Test creating a pressurized fermentation profile with pressure values"""
    profile_data = {
        "name": "Pressurized Lager",
        "description": "Lager with pressurized fermentation",
        "is_pressurized": True,
        "is_template": True,
        "steps": [
            {
                "step_order": 1,
                "name": "Primary Fermentation",
                "step_type": "primary",
                "temperature": 10,
                "duration_days": 14,
                "ramp_days": 0,
                "pressure_psi": 15,
            },
        ],
    }

    response = client.post("/fermentation-profiles", json=profile_data)
    assert response.status_code == 201

    payload = response.json()
    assert payload["is_pressurized"] is True
    assert payload["steps"][0]["pressure_psi"] == "15.00"
