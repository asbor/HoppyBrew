"""
Tests for device data ingestion endpoints
"""
import pytest
from datetime import datetime
import Database.Models as models


def create_test_device(client, db_session, device_type="ispindel", name="Test Device"):
    """Helper to create a test device"""
    payload = {
        "name": name,
        "device_type": device_type,
        "api_token": "test-token-123",
        "is_active": True,
        "alert_config": {
            "enable_alerts": True,
            "temperature_min": 16.0,
            "temperature_max": 22.0
        }
    }
    response = client.post("/devices", json=payload)
    assert response.status_code == 200
    return response.json()


def create_test_batch(client, db_session):
    """Helper to create a test batch with recipe"""
    # Create recipe
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
    assert recipe_response.status_code == 200
    
    # Create batch
    batch_payload = {
        "recipe_id": recipe_response.json()["id"],
        "batch_name": "Test Batch",
        "batch_number": 1,
        "batch_size": 20.0,
        "brewer": "Test Brewer",
        "brew_date": datetime(2024, 3, 21, 12, 0, 0).isoformat(),
    }
    batch_response = client.post("/batches", json=batch_payload)
    assert batch_response.status_code == 200
    return batch_response.json()


def test_associate_device_with_batch(client, db_session):
    """Test associating a device with a batch"""
    device = create_test_device(client, db_session)
    batch = create_test_batch(client, db_session)
    
    response = client.post(f"/devices/{device['id']}/batch/{batch['id']}/associate")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify association
    device_check = client.get(f"/devices/{device['id']}")
    assert device_check.json()["batch_id"] == batch["id"]


def test_dissociate_device_from_batch(client, db_session):
    """Test dissociating a device from a batch (manual override)"""
    device = create_test_device(client, db_session)
    batch = create_test_batch(client, db_session)
    
    # Associate first
    client.post(f"/devices/{device['id']}/batch/{batch['id']}/associate")
    
    # Dissociate
    response = client.delete(f"/devices/{device['id']}/batch")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify dissociation
    device_check = client.get(f"/devices/{device['id']}")
    assert device_check.json()["batch_id"] is None


def test_ispindel_data_ingestion_no_device(client, db_session):
    """Test iSpindel data ingestion without configured device"""
    data = {
        "name": "iSpindel999",
        "angle": 45.2,
        "temperature": 20.5,
        "battery": 3.8,
        "gravity": 1.048
    }
    
    response = client.post("/devices/ispindel/data", json=data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_ispindel_data_ingestion_success(client, db_session):
    """Test successful iSpindel data ingestion"""
    device = create_test_device(client, db_session, device_type="ispindel", name="iSpindel000")
    batch = create_test_batch(client, db_session)
    
    # Associate device with batch
    client.post(f"/devices/{device['id']}/batch/{batch['id']}/associate")
    
    # Send data
    data = {
        "name": "iSpindel000",
        "angle": 45.2,
        "temperature": 20.5,
        "temp_units": "C",
        "battery": 3.8,
        "gravity": 1.048,
        "interval": 900
    }
    
    response = client.post("/devices/ispindel/data", json=data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["batch_id"] == batch["id"]
    assert "reading_id" in response.json()
    
    # Verify reading was created
    readings_response = client.get(f"/batches/{batch['id']}/fermentation/readings")
    readings = readings_response.json()
    assert len(readings) == 1
    assert readings[0]["source"] == "ispindel"
    assert readings[0]["gravity"] == 1.048
    assert readings[0]["temperature"] == 20.5
    assert readings[0]["device_id"] == device["id"]


def test_ispindel_data_with_api_key(client, db_session):
    """Test iSpindel data ingestion using API key authentication"""
    device = create_test_device(client, db_session, device_type="ispindel")
    batch = create_test_batch(client, db_session)
    client.post(f"/devices/{device['id']}/batch/{batch['id']}/associate")
    
    data = {
        "name": "Unknown",
        "temperature": 19.0,
        "gravity": 1.045
    }
    
    headers = {"X-API-Key": "test-token-123"}
    response = client.post("/devices/ispindel/data", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_ispindel_data_inactive_device(client, db_session):
    """Test iSpindel data ingestion with inactive device"""
    device = create_test_device(client, db_session, device_type="ispindel")
    
    # Deactivate device
    client.put(f"/devices/{device['id']}", json={"is_active": False})
    
    data = {
        "name": device["name"],
        "temperature": 20.0,
        "gravity": 1.050
    }
    
    response = client.post("/devices/ispindel/data", json=data)
    assert response.status_code == 403
    assert "not active" in response.json()["detail"].lower()


def test_ispindel_data_no_batch_assigned(client, db_session):
    """Test iSpindel data ingestion without batch assignment"""
    device = create_test_device(client, db_session, device_type="ispindel", name="iSpindel001")
    
    data = {
        "name": "iSpindel001",
        "temperature": 20.0,
        "gravity": 1.050
    }
    
    response = client.post("/devices/ispindel/data", json=data)
    assert response.status_code == 200
    assert response.json()["status"] == "received"
    assert "no batch" in response.json()["message"].lower()


def test_tilt_data_ingestion_success(client, db_session):
    """Test successful Tilt data ingestion"""
    device = create_test_device(client, db_session, device_type="tilt", name="Tilt Red")
    batch = create_test_batch(client, db_session)
    client.post(f"/devices/{device['id']}/batch/{batch['id']}/associate")
    
    # Tilt sends temperature in Fahrenheit
    data = {
        "Color": "Red",
        "Temp": 68,  # 20°C
        "SG": 1.048,
        "Timepoint": "2024-03-21T14:30:00Z",
        "Beer": "Test IPA"
    }
    
    response = client.post("/devices/tilt/data", json=data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify reading
    readings_response = client.get(f"/batches/{batch['id']}/fermentation/readings")
    readings = readings_response.json()
    assert len(readings) == 1
    assert readings[0]["source"] == "tilt"
    assert readings[0]["gravity"] == 1.048
    # Check temperature conversion (68°F ≈ 20°C)
    assert 19.9 <= readings[0]["temperature"] <= 20.1


def test_temperature_alerts_triggered(client, db_session):
    """Test that temperature alerts are triggered when outside range"""
    device = create_test_device(client, db_session, device_type="ispindel", name="iSpindel002")
    batch = create_test_batch(client, db_session)
    client.post(f"/devices/{device['id']}/batch/{batch['id']}/associate")
    
    # Send data with high temperature (above 22°C max)
    data = {
        "name": "iSpindel002",
        "temperature": 25.0,  # Above max of 22
        "gravity": 1.048
    }
    
    response = client.post("/devices/ispindel/data", json=data)
    assert response.status_code == 200
    alerts = response.json().get("alerts", [])
    assert len(alerts) > 0
    assert any("high" in alert.get("type", "").lower() for alert in alerts)


def test_temperature_alerts_within_range(client, db_session):
    """Test that no alerts are triggered when temperature is within range"""
    device = create_test_device(client, db_session, device_type="ispindel", name="iSpindel003")
    batch = create_test_batch(client, db_session)
    client.post(f"/devices/{device['id']}/batch/{batch['id']}/associate")
    
    # Send data with temperature in range (16-22°C)
    data = {
        "name": "iSpindel003",
        "temperature": 19.0,
        "gravity": 1.048
    }
    
    response = client.post("/devices/ispindel/data", json=data)
    assert response.status_code == 200
    alerts = response.json().get("alerts", [])
    assert len(alerts) == 0


def test_device_last_reading_timestamp_updated(client, db_session):
    """Test that device last_reading_at is updated on data ingestion"""
    device = create_test_device(client, db_session, device_type="ispindel", name="iSpindel004")
    batch = create_test_batch(client, db_session)
    client.post(f"/devices/{device['id']}/batch/{batch['id']}/associate")
    
    # Check initial state
    initial_device = client.get(f"/devices/{device['id']}").json()
    assert initial_device["last_reading_at"] is None
    
    # Send data
    data = {
        "name": "iSpindel004",
        "temperature": 19.0,
        "gravity": 1.048
    }
    
    client.post("/devices/ispindel/data", json=data)
    
    # Check updated timestamp
    updated_device = client.get(f"/devices/{device['id']}").json()
    assert updated_device["last_reading_at"] is not None
