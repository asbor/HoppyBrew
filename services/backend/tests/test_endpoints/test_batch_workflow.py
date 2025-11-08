"""
Tests for batch status workflow system
"""

from datetime import datetime
import Database.Models as models


def create_test_batch(client, db_session, status="planning"):
    """Helper to create a test batch with a specific status"""
    # Create a recipe first
    recipe_payload = {
        "name": "Test Recipe",
        "version": 1,
        "type": "Ale",
        "brewer": "Tester",
        "batch_size": 20.0,
        "boil_size": 25.0,
        "boil_time": 60,
        "hops": [{"name": "Cascade"}],
        "fermentables": [{"name": "Pale Malt"}],
        "yeasts": [{"name": "Ale Yeast"}],
        "miscs": [{"name": "Irish Moss"}],
    }
    response = client.post("/recipes", json=recipe_payload)
    assert response.status_code == 200
    recipe = (
        db_session.query(models.Recipes)
        .filter(models.Recipes.name == "Test Recipe")
        .one()
    )

    # Create batch
    batch_payload = {
        "recipe_id": recipe.id,
        "batch_name": "Test Batch",
        "batch_number": 1,
        "batch_size": 18.5,
        "brewer": "Test Brewer",
        "brew_date": datetime(2024, 1, 1, 12, 0, 0).isoformat(),
        "status": status,
    }
    response = client.post("/batches", json=batch_payload)
    assert response.status_code == 200
    return response.json()


def test_batch_created_with_initial_workflow_entry(client, db_session):
    """Test that creating a batch creates an initial workflow history entry"""
    batch = create_test_batch(client, db_session)

    # Check that workflow history was created
    workflow_history = (
        db_session.query(models.BatchWorkflowHistory)
        .filter(models.BatchWorkflowHistory.batch_id == batch["id"])
        .all()
    )

    assert len(workflow_history) == 1
    assert workflow_history[0].from_status is None
    assert workflow_history[0].to_status == "planning"
    assert workflow_history[0].notes == "Batch created"


def test_update_batch_status_valid_transition(client, db_session):
    """Test updating batch status with a valid transition"""
    batch = create_test_batch(client, db_session, status="planning")

    # Update status from planning to brewing
    update_payload = {
        "status": "brewing",
        "notes": "Started brew day",
    }
    response = client.put(f"/batches/{batch['id']}/status", json=update_payload)
    assert response.status_code == 200

    updated_batch = response.json()
    assert updated_batch["status"] == "brewing"

    # Check workflow history
    workflow_history = (
        db_session.query(models.BatchWorkflowHistory)
        .filter(models.BatchWorkflowHistory.batch_id == batch["id"])
        .order_by(models.BatchWorkflowHistory.changed_at.asc())
        .all()
    )

    assert len(workflow_history) == 2
    assert workflow_history[1].from_status == "planning"
    assert workflow_history[1].to_status == "brewing"
    assert workflow_history[1].notes == "Started brew day"


def test_update_batch_status_invalid_transition(client, db_session):
    """Test that invalid status transitions are rejected"""
    batch = create_test_batch(client, db_session, status="planning")

    # Try to skip from planning directly to packaging (invalid)
    update_payload = {
        "status": "packaging",
    }
    response = client.put(f"/batches/{batch['id']}/status", json=update_payload)
    assert response.status_code == 400
    assert "Invalid status transition" in response.json()["detail"]


def test_update_batch_status_same_status(client, db_session):
    """Test that updating to the same status is rejected"""
    batch = create_test_batch(client, db_session, status="planning")

    update_payload = {
        "status": "planning",
    }
    response = client.put(f"/batches/{batch['id']}/status", json=update_payload)
    assert response.status_code == 400
    assert "already in planning status" in response.json()["detail"]


def test_update_batch_status_invalid_status_value(client, db_session):
    """Test that invalid status values are rejected"""
    batch = create_test_batch(client, db_session, status="planning")

    update_payload = {
        "status": "invalid_status",
    }
    response = client.put(f"/batches/{batch['id']}/status", json=update_payload)
    assert response.status_code == 400
    assert "Invalid status" in response.json()["detail"]


def test_update_batch_status_nonexistent_batch(client):
    """Test updating status of a non-existent batch"""
    update_payload = {
        "status": "brewing",
    }
    response = client.put("/batches/99999/status", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Batch not found"


def test_get_batch_workflow_history(client, db_session):
    """Test retrieving workflow history for a batch"""
    batch = create_test_batch(client, db_session, status="planning")

    # Make several status updates
    statuses = ["brewing", "fermenting", "conditioning"]
    for status in statuses:
        update_payload = {"status": status, "notes": f"Moving to {status}"}
        response = client.put(f"/batches/{batch['id']}/status", json=update_payload)
        assert response.status_code == 200

    # Get workflow history
    response = client.get(f"/batches/{batch['id']}/workflow")
    assert response.status_code == 200

    history = response.json()
    assert len(history) == 4  # Initial + 3 updates

    # Check that history is in descending order (most recent first)
    assert history[0]["to_status"] == "conditioning"
    assert history[1]["to_status"] == "fermenting"
    assert history[2]["to_status"] == "brewing"
    assert history[3]["to_status"] == "planning"


def test_get_workflow_history_nonexistent_batch(client):
    """Test retrieving workflow history for a non-existent batch"""
    response = client.get("/batches/99999/workflow")
    assert response.status_code == 404
    assert response.json()["detail"] == "Batch not found"


def test_get_valid_status_transitions(client, db_session):
    """Test retrieving valid transitions for a batch's current status"""
    batch = create_test_batch(client, db_session, status="planning")

    response = client.get(f"/batches/{batch['id']}/status/transitions")
    assert response.status_code == 200

    data = response.json()
    assert data["current_status"] == "planning"
    assert "brewing" in data["valid_transitions"]
    assert "archived" in data["valid_transitions"]
    assert len(data["valid_transitions"]) == 2


def test_complete_workflow_sequence(client, db_session):
    """Test a complete workflow from planning to complete"""
    batch = create_test_batch(client, db_session, status="planning")

    # Complete workflow sequence
    workflow = [
        "brewing",
        "fermenting",
        "conditioning",
        "packaging",
        "complete",
    ]

    for status in workflow:
        update_payload = {"status": status, "notes": f"Transitioning to {status}"}
        response = client.put(f"/batches/{batch['id']}/status", json=update_payload)
        assert response.status_code == 200, f"Failed to transition to {status}"
        assert response.json()["status"] == status

    # Verify final status
    response = client.get(f"/batches/{batch['id']}")
    assert response.status_code == 200
    assert response.json()["status"] == "complete"

    # Verify complete workflow history
    response = client.get(f"/batches/{batch['id']}/workflow")
    assert response.status_code == 200
    history = response.json()
    assert len(history) == 6  # Initial + 5 transitions


def test_archive_from_any_status(client, db_session):
    """Test that a batch can be archived from any status"""
    # Test archiving from planning
    batch1 = create_test_batch(client, db_session, status="planning")
    response = client.put(
        f"/batches/{batch1['id']}/status", json={"status": "archived"}
    )
    assert response.status_code == 200

    # Test archiving from fermenting - create a new batch with unique recipe
    recipe_payload = {
        "name": "Test Recipe 2",
        "version": 1,
        "type": "Ale",
        "brewer": "Tester",
        "batch_size": 20.0,
        "boil_size": 25.0,
        "boil_time": 60,
        "hops": [{"name": "Cascade"}],
        "fermentables": [{"name": "Pale Malt"}],
        "yeasts": [{"name": "Ale Yeast"}],
        "miscs": [{"name": "Irish Moss"}],
    }
    response = client.post("/recipes", json=recipe_payload)
    assert response.status_code == 200
    recipe2 = (
        db_session.query(models.Recipes)
        .filter(models.Recipes.name == "Test Recipe 2")
        .one()
    )

    batch_payload = {
        "recipe_id": recipe2.id,
        "batch_name": "Test Batch 2",
        "batch_number": 2,
        "batch_size": 18.5,
        "brewer": "Test Brewer",
        "brew_date": datetime(2024, 1, 1, 12, 0, 0).isoformat(),
        "status": "planning",
    }
    response = client.post("/batches", json=batch_payload)
    assert response.status_code == 200
    batch2 = response.json()

    client.put(f"/batches/{batch2['id']}/status", json={"status": "brewing"})
    client.put(f"/batches/{batch2['id']}/status", json={"status": "fermenting"})
    response = client.put(
        f"/batches/{batch2['id']}/status", json={"status": "archived"}
    )
    assert response.status_code == 200


def test_archived_batch_cannot_transition(client, db_session):
    """Test that an archived batch cannot transition to any other status"""
    batch = create_test_batch(client, db_session, status="planning")

    # Archive the batch
    response = client.put(f"/batches/{batch['id']}/status", json={"status": "archived"})
    assert response.status_code == 200

    # Try to transition from archived (should fail)
    response = client.put(f"/batches/{batch['id']}/status", json={"status": "planning"})
    assert response.status_code == 400
    assert "Invalid status transition" in response.json()["detail"]
