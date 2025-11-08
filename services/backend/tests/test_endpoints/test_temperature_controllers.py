import pytest
import Database.Models as models
from datetime import datetime, timezone


def test_create_device_with_temperature_control_fields(client, db_session):
    """Test creating a device with temperature control integration fields"""
    payload = {
        "name": "Test Tilt",
        "device_type": "tilt",
        "description": "Tilt for fermentation monitoring",
        "batch_id": None,
        "auto_import_enabled": True,
        "import_interval_seconds": 900,
        "alert_config": {
            "temp_min": 18.0,
            "temp_max": 22.0,
            "notification_enabled": True,
        },
        "manual_override": False,
        "is_active": True,
    }

    response = client.post("/devices", json=payload)
    assert response.status_code == 200, response.text
    created = response.json()

    assert created["name"] == "Test Tilt"
    assert created["auto_import_enabled"] is True
    assert created["import_interval_seconds"] == 900
    assert created["alert_config"]["temp_min"] == 18.0
    assert created["manual_override"] is False


def test_tilt_webhook_data_ingestion(client, db_session):
    """Test Tilt webhook endpoint creates fermentation reading"""
    # Create a batch first
    batch = models.Batches(
        batch_name="IPA Batch",
        batch_number=1,
        batch_size=20.0,
        status="fermenting",
        brewer="Test Brewer",
        brew_date=datetime.now(timezone.utc),
        recipe_id=1,  # Assumes recipe exists
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)

    # Create a Tilt device associated with the batch
    device = models.Device(
        name="Test Tilt Red",
        device_type="tilt",
        batch_id=batch.id,
        auto_import_enabled=True,
        import_interval_seconds=900,
        is_active=True,
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)

    # Send Tilt data to webhook
    tilt_data = {
        "color": "Red",
        "temp_fahrenheit": 68.5,
        "temp_celsius": 20.3,
        "gravity": 1.048,
        "rssi": -45,
    }

    response = client.post(
        f"/temperature-controllers/tilt/webhook/{device.id}", json=tilt_data
    )
    assert response.status_code == 200, response.text
    result = response.json()

    assert result["status"] == "success"
    assert "reading_id" in result
    assert result["alerts"] == []  # No alerts by default

    # Verify the reading was created
    reading = (
        db_session.query(models.FermentationReadings)
        .filter_by(id=result["reading_id"])
        .first()
    )
    assert reading is not None
    assert reading.batch_id == batch.id
    assert reading.device_id == device.id
    assert reading.source == "tilt"
    assert reading.gravity == 1.048
    assert abs(reading.temperature - 20.3) < 0.1


def test_ispindel_webhook_data_ingestion(client, db_session):
    """Test iSpindel webhook endpoint creates fermentation reading with calibration"""
    # Create a batch first
    batch = models.Batches(
        batch_name="Stout Batch",
        batch_number=2,
        batch_size=20.0,
        status="fermenting",
        brewer="Test Brewer",
        brew_date=datetime.now(timezone.utc),
        recipe_id=1,
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)

    # Create an iSpindel device with calibration data
    device = models.Device(
        name="iSpindel001",
        device_type="ispindel",
        batch_id=batch.id,
        calibration_data={
            "polynomial": [0.0, 0.001, 0.0, 1.0],  # Simple calibration
        },
        auto_import_enabled=True,
        import_interval_seconds=900,
        is_active=True,
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)

    # Send iSpindel data to webhook
    ispindel_data = {
        "name": "iSpindel001",
        "angle": 45.23,
        "temperature": 20.5,
        "battery": 3.87,
        "gravity": 1.050,
        "interval": 900,
        "RSSI": -62,
    }

    response = client.post(
        f"/temperature-controllers/ispindel/webhook/{device.id}", json=ispindel_data
    )
    assert response.status_code == 200, response.text
    result = response.json()

    assert result["status"] == "success"
    assert "reading_id" in result
    assert "calibrated_gravity" in result

    # Verify the reading was created
    reading = (
        db_session.query(models.FermentationReadings)
        .filter_by(id=result["reading_id"])
        .first()
    )
    assert reading is not None
    assert reading.batch_id == batch.id
    assert reading.device_id == device.id
    assert reading.source == "ispindel"
    assert reading.temperature == 20.5


def test_temperature_alert_triggers(client, db_session):
    """Test that temperature alerts are triggered when thresholds are exceeded"""
    # Create a batch
    batch = models.Batches(
        batch_name="Alert Test Batch",
        batch_number=3,
        batch_size=20.0,
        status="fermenting",
        brewer="Test Brewer",
        brew_date=datetime.now(timezone.utc),
        recipe_id=1,
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)

    # Create device with alert configuration
    device = models.Device(
        name="Alert Test Tilt",
        device_type="tilt",
        batch_id=batch.id,
        alert_config={
            "temp_min": 18.0,
            "temp_max": 22.0,
            "notification_enabled": True,
        },
        auto_import_enabled=True,
        is_active=True,
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)

    # Send data with temperature too high
    tilt_data = {
        "color": "Red",
        "temp_celsius": 25.0,  # Above max threshold
        "gravity": 1.048,
    }

    response = client.post(
        f"/temperature-controllers/tilt/webhook/{device.id}", json=tilt_data
    )
    assert response.status_code == 200
    result = response.json()

    assert result["status"] == "success"
    assert len(result["alerts"]) > 0
    assert "too high" in result["alerts"][0].lower()


def test_manual_override_prevents_auto_import(client, db_session):
    """Test that manual override flag prevents automatic data import"""
    # Create a batch
    batch = models.Batches(
        batch_name="Override Test Batch",
        batch_number=4,
        batch_size=20.0,
        status="fermenting",
        brewer="Test Brewer",
        brew_date=datetime.now(timezone.utc),
        recipe_id=1,
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)

    # Create device with manual override enabled
    device = models.Device(
        name="Override Test Device",
        device_type="tilt",
        batch_id=batch.id,
        manual_override=True,  # Manual override enabled
        auto_import_enabled=True,
        is_active=True,
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)

    # Try to send data
    tilt_data = {
        "color": "Red",
        "temp_celsius": 20.0,
        "gravity": 1.048,
    }

    response = client.post(
        f"/temperature-controllers/tilt/webhook/{device.id}", json=tilt_data
    )
    assert response.status_code == 200
    result = response.json()

    assert result["status"] == "skipped"
    assert result["reason"] == "manual_override"


def test_manual_reading_creation(client, db_session):
    """Test creating a manual fermentation reading"""
    # Create a batch
    batch = models.Batches(
        batch_name="Manual Reading Batch",
        batch_number=5,
        batch_size=20.0,
        status="fermenting",
        brewer="Test Brewer",
        brew_date=datetime.now(timezone.utc),
        recipe_id=1,
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)

    # Create device
    device = models.Device(
        name="Manual Test Device",
        device_type="tilt",
        batch_id=batch.id,
        manual_override=True,
        is_active=True,
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)

    # Create manual reading
    reading_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "gravity": 1.020,
        "temperature": 19.5,
        "notes": "Manual reading during override",
    }

    response = client.post(
        f"/temperature-controllers/manual-reading/{device.id}", json=reading_data
    )
    assert response.status_code == 200, response.text
    result = response.json()

    assert result["batch_id"] == batch.id
    assert result["device_id"] == device.id
    assert result["source"] == "manual_override"
    assert result["gravity"] == 1.020


def test_get_device_alerts(client, db_session):
    """Test retrieving current alert status for a device"""
    # Create a batch
    batch = models.Batches(
        batch_name="Alert Query Batch",
        batch_number=6,
        batch_size=20.0,
        status="fermenting",
        brewer="Test Brewer",
        brew_date=datetime.now(timezone.utc),
        recipe_id=1,
    )
    db_session.add(batch)
    db_session.commit()
    db_session.refresh(batch)

    # Create device with alert config
    device = models.Device(
        name="Alert Query Device",
        device_type="tilt",
        batch_id=batch.id,
        alert_config={
            "temp_min": 18.0,
            "temp_max": 22.0,
        },
        is_active=True,
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)

    # Create a reading with high temperature
    reading = models.FermentationReadings(
        batch_id=batch.id,
        device_id=device.id,
        timestamp=datetime.now(timezone.utc),
        gravity=1.048,
        temperature=24.0,  # Above threshold
        source="tilt",
    )
    db_session.add(reading)
    db_session.commit()

    # Get alerts
    response = client.get(f"/temperature-controllers/alerts/{device.id}")
    assert response.status_code == 200
    result = response.json()

    assert result["device_id"] == device.id
    assert result["batch_id"] == batch.id
    assert "latest_reading" in result
    assert len(result["alerts"]) > 0


def test_device_not_associated_with_batch_error(client, db_session):
    """Test that webhook fails if device is not associated with a batch"""
    # Create device without batch
    device = models.Device(
        name="No Batch Device",
        device_type="tilt",
        batch_id=None,  # No batch association
        is_active=True,
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)

    # Try to send data
    tilt_data = {
        "color": "Red",
        "temp_celsius": 20.0,
        "gravity": 1.048,
    }

    response = client.post(
        f"/temperature-controllers/tilt/webhook/{device.id}", json=tilt_data
    )
    assert response.status_code == 400
    assert "not associated with a batch" in response.json()["detail"]


def test_wrong_device_type_error(client, db_session):
    """Test that using wrong webhook endpoint returns error"""
    batch = models.Batches(
        batch_name="Wrong Type Batch",
        batch_number=7,
        batch_size=20.0,
        status="fermenting",
        brewer="Test Brewer",
        brew_date=datetime.now(timezone.utc),
        recipe_id=1,
    )
    db_session.add(batch)
    db_session.commit()

    # Create an iSpindel device
    device = models.Device(
        name="iSpindel Device",
        device_type="ispindel",  # iSpindel type
        batch_id=batch.id,
        is_active=True,
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)

    # Try to send Tilt data to iSpindel device
    tilt_data = {
        "color": "Red",
        "temp_celsius": 20.0,
        "gravity": 1.048,
    }

    response = client.post(
        f"/temperature-controllers/tilt/webhook/{device.id}", json=tilt_data
    )
    assert response.status_code == 400
    assert "not a Tilt" in response.json()["detail"]


def test_inactive_device_error(client, db_session):
    """Test that inactive device returns error"""
    batch = models.Batches(
        batch_name="Inactive Device Batch",
        batch_number=8,
        batch_size=20.0,
        status="fermenting",
        brewer="Test Brewer",
        brew_date=datetime.now(timezone.utc),
        recipe_id=1,
    )
    db_session.add(batch)
    db_session.commit()

    # Create inactive device
    device = models.Device(
        name="Inactive Device",
        device_type="tilt",
        batch_id=batch.id,
        is_active=False,  # Inactive
    )
    db_session.add(device)
    db_session.commit()
    db_session.refresh(device)

    # Try to send data
    tilt_data = {
        "color": "Red",
        "temp_celsius": 20.0,
        "gravity": 1.048,
    }

    response = client.post(
        f"/temperature-controllers/tilt/webhook/{device.id}", json=tilt_data
    )
    assert response.status_code == 400
    assert "not active" in response.json()["detail"]
