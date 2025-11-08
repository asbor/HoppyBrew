import pytest
from datetime import datetime, timedelta
import Database.Models as models


def create_test_batch(client, db_session, batch_name="Test Batch"):
    """Helper function to create a test batch with recipe"""
    # Create a recipe first
    recipe_payload = {
        "name": "Test IPA",
        "version": 1,
        "type": "All Grain",
        "brewer": "Test Brewer",
        "batch_size": 20.0,
        "boil_size": 25.0,
        "boil_time": 60,
        "og": 1.048,
        "fg": 1.012,
        "hops": [{"name": "Cascade"}],
        "fermentables": [{"name": "Pale Malt"}],
        "yeasts": [{"name": "Ale Yeast"}],
        "miscs": [{"name": "Irish Moss"}],
    }
    
    recipe_response = client.post("/recipes", json=recipe_payload)
    assert recipe_response.status_code == 200, recipe_response.text
    
    # Create a batch
    batch_payload = {
        "recipe_id": recipe_response.json()["id"],
        "batch_name": batch_name,
        "batch_number": 1,
        "batch_size": 20.0,
        "brewer": "Test Brewer",
        "brew_date": datetime(2024, 3, 21, 12, 0, 0).isoformat(),
    }
    
    batch_response = client.post("/batches", json=batch_payload)
    assert batch_response.status_code == 200, batch_response.text
    
    return batch_response.json()


def test_create_fermentation_reading(client, db_session):
    """Test creating a fermentation reading"""
    batch = create_test_batch(client, db_session)
    batch_id = batch["id"]
    
    reading_payload = {
        "timestamp": datetime(2024, 3, 21, 14, 30, 0).isoformat(),
        "gravity": 1.048,
        "temperature": 18.5,
        "ph": 5.4,
        "notes": "Initial reading after pitching yeast",
    }
    
    response = client.post(f"/batches/{batch_id}/fermentation/readings", json=reading_payload)
    assert response.status_code == 200, response.text
    
    reading = response.json()
    assert reading["batch_id"] == batch_id
    assert reading["gravity"] == 1.048
    assert reading["temperature"] == 18.5
    assert reading["ph"] == 5.4
    assert reading["notes"] == "Initial reading after pitching yeast"
    assert "id" in reading
    assert "created_at" in reading


def test_create_fermentation_reading_nonexistent_batch(client):
    """Test creating a reading for a non-existent batch returns 404"""
    reading_payload = {
        "timestamp": datetime.now().isoformat(),
        "gravity": 1.048,
        "temperature": 18.5,
    }
    
    response = client.post("/batches/99999/fermentation/readings", json=reading_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Batch not found"


def test_get_fermentation_readings(client, db_session):
    """Test retrieving all fermentation readings for a batch"""
    batch = create_test_batch(client, db_session)
    batch_id = batch["id"]
    
    # Create multiple readings
    readings_data = [
        {
            "timestamp": (datetime.now() - timedelta(days=3)).isoformat(),
            "gravity": 1.048,
            "temperature": 18.0,
        },
        {
            "timestamp": (datetime.now() - timedelta(days=2)).isoformat(),
            "gravity": 1.032,
            "temperature": 19.0,
        },
        {
            "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
            "gravity": 1.020,
            "temperature": 18.5,
        },
    ]
    
    for reading_data in readings_data:
        response = client.post(f"/batches/{batch_id}/fermentation/readings", json=reading_data)
        assert response.status_code == 200
    
    # Get all readings
    response = client.get(f"/batches/{batch_id}/fermentation/readings")
    assert response.status_code == 200
    
    readings = response.json()
    assert len(readings) == 3
    
    # Verify they're in chronological order
    assert readings[0]["gravity"] == 1.048
    assert readings[1]["gravity"] == 1.032
    assert readings[2]["gravity"] == 1.020


def test_get_fermentation_readings_nonexistent_batch(client):
    """Test getting readings for a non-existent batch returns 404"""
    response = client.get("/batches/99999/fermentation/readings")
    assert response.status_code == 404


def test_update_fermentation_reading(client, db_session):
    """Test updating a fermentation reading"""
    batch = create_test_batch(client, db_session)
    batch_id = batch["id"]
    
    # Create a reading
    reading_payload = {
        "timestamp": datetime.now().isoformat(),
        "gravity": 1.048,
        "temperature": 18.5,
        "notes": "Initial notes",
    }
    
    create_response = client.post(f"/batches/{batch_id}/fermentation/readings", json=reading_payload)
    assert create_response.status_code == 200
    reading_id = create_response.json()["id"]
    
    # Update the reading
    update_payload = {
        "gravity": 1.046,
        "notes": "Corrected gravity reading",
    }
    
    update_response = client.put(f"/fermentation/readings/{reading_id}", json=update_payload)
    assert update_response.status_code == 200
    
    updated_reading = update_response.json()
    assert updated_reading["gravity"] == 1.046
    assert updated_reading["temperature"] == 18.5  # Unchanged
    assert updated_reading["notes"] == "Corrected gravity reading"


def test_update_nonexistent_reading(client):
    """Test updating a non-existent reading returns 404"""
    update_payload = {"gravity": 1.020}
    
    response = client.put("/fermentation/readings/99999", json=update_payload)
    assert response.status_code == 404


def test_delete_fermentation_reading(client, db_session):
    """Test deleting a fermentation reading"""
    batch = create_test_batch(client, db_session)
    batch_id = batch["id"]
    
    # Create a reading
    reading_payload = {
        "timestamp": datetime.now().isoformat(),
        "gravity": 1.048,
    }
    
    create_response = client.post(f"/batches/{batch_id}/fermentation/readings", json=reading_payload)
    assert create_response.status_code == 200
    reading_id = create_response.json()["id"]
    
    # Delete the reading
    delete_response = client.delete(f"/fermentation/readings/{reading_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Fermentation reading deleted successfully"
    
    # Verify it's deleted
    get_response = client.get(f"/batches/{batch_id}/fermentation/readings")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0


def test_delete_nonexistent_reading(client):
    """Test deleting a non-existent reading returns 404"""
    response = client.delete("/fermentation/readings/99999")
    assert response.status_code == 404


def test_get_fermentation_chart_data(client, db_session):
    """Test getting formatted chart data"""
    batch = create_test_batch(client, db_session)
    batch_id = batch["id"]
    
    # Create readings with varying gravity
    base_time = datetime.now() - timedelta(days=5)
    readings_data = [
        {
            "timestamp": base_time.isoformat(),
            "gravity": 1.048,
            "temperature": 18.0,
            "ph": 5.4,
        },
        {
            "timestamp": (base_time + timedelta(days=2)).isoformat(),
            "gravity": 1.032,
            "temperature": 19.0,
            "ph": 5.2,
        },
        {
            "timestamp": (base_time + timedelta(days=4)).isoformat(),
            "gravity": 1.012,
            "temperature": 18.5,
            "ph": 5.0,
        },
    ]
    
    for reading_data in readings_data:
        response = client.post(f"/batches/{batch_id}/fermentation/readings", json=reading_data)
        assert response.status_code == 200
    
    # Get chart data
    response = client.get(f"/batches/{batch_id}/fermentation/chart-data")
    assert response.status_code == 200
    
    chart_data = response.json()
    
    # Verify structure
    assert "timestamps" in chart_data
    assert "gravity" in chart_data
    assert "temperature" in chart_data
    assert "ph" in chart_data
    assert "abv" in chart_data
    assert "attenuation" in chart_data
    
    # Verify data
    assert len(chart_data["timestamps"]) == 3
    assert len(chart_data["gravity"]) == 3
    assert chart_data["gravity"] == [1.048, 1.032, 1.012]
    assert chart_data["temperature"] == [18.0, 19.0, 18.5]
    assert chart_data["ph"] == [5.4, 5.2, 5.0]
    
    # Verify ABV calculations (OG=1.048, FG progresses to 1.012)
    # First reading: no fermentation yet (OG == current)
    assert chart_data["abv"][0] == 0.0
    
    # Second reading: partial fermentation
    # ABV = (1.048 - 1.032) * 131.25 = 2.1
    assert chart_data["abv"][1] == pytest.approx(2.1, abs=0.1)
    
    # Third reading: near complete fermentation
    # ABV = (1.048 - 1.012) * 131.25 = 4.725
    assert chart_data["abv"][2] == pytest.approx(4.73, abs=0.1)
    
    # Verify attenuation calculations
    # Attenuation = ((OG - FG) / (OG - 1.0)) * 100
    # First: 0%
    assert chart_data["attenuation"][0] == 0.0
    # Second: ((1.048 - 1.032) / (1.048 - 1.0)) * 100 = 33.3%
    assert chart_data["attenuation"][1] == pytest.approx(33.3, abs=0.5)
    # Third: ((1.048 - 1.012) / (1.048 - 1.0)) * 100 = 75%
    assert chart_data["attenuation"][2] == pytest.approx(75.0, abs=0.5)


def test_get_chart_data_nonexistent_batch(client):
    """Test getting chart data for non-existent batch returns 404"""
    response = client.get("/batches/99999/fermentation/chart-data")
    assert response.status_code == 404


def test_cascade_delete_fermentation_readings(client, db_session):
    """Test that deleting a batch also deletes its fermentation readings"""
    batch = create_test_batch(client, db_session)
    batch_id = batch["id"]
    
    # Create readings
    reading_payload = {
        "timestamp": datetime.now().isoformat(),
        "gravity": 1.048,
    }
    
    client.post(f"/batches/{batch_id}/fermentation/readings", json=reading_payload)
    client.post(f"/batches/{batch_id}/fermentation/readings", json=reading_payload)
    
    # Verify readings exist
    readings = db_session.query(models.FermentationReadings).filter_by(batch_id=batch_id).all()
    assert len(readings) == 2
    
    # Delete the batch
    delete_response = client.delete(f"/batches/{batch_id}")
    assert delete_response.status_code == 200
    
    # Verify readings are also deleted
    readings = db_session.query(models.FermentationReadings).filter_by(batch_id=batch_id).all()
    assert len(readings) == 0
