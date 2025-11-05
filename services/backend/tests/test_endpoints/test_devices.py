import Database.Models as models


def test_create_and_get_device(client):
    """Test creating a new device and retrieving it"""
    payload = {
        "name": "Test iSpindel",
        "device_type": "ispindel",
        "description": "Test device for fermentation monitoring",
        "api_endpoint": "/api/devices/ispindel/data",
        "api_token": "test-token-123",
        "calibration_data": {
            "polynomial": [0.0, 0.0, 0.0, 1.0],
            "temp_correction": True
        },
        "configuration": {
            "update_interval": 900,
            "battery_warning_threshold": 3.5
        },
        "is_active": True
    }
    
    # Create device
    create_resp = client.post("/devices", json=payload)
    assert create_resp.status_code == 200, create_resp.text
    created = create_resp.json()
    
    assert created["name"] == "Test iSpindel"
    assert created["device_type"] == "ispindel"
    assert created["is_active"] is True
    assert "id" in created
    
    # Get device by ID
    detail_resp = client.get(f"/devices/{created['id']}")
    assert detail_resp.status_code == 200
    device = detail_resp.json()
    assert device["name"] == "Test iSpindel"
    assert device["calibration_data"]["polynomial"] == [0.0, 0.0, 0.0, 1.0]


def test_get_all_devices(client):
    """Test retrieving all devices"""
    # Create two devices
    device1 = {
        "name": "Device 1",
        "device_type": "ispindel",
        "is_active": True
    }
    device2 = {
        "name": "Device 2",
        "device_type": "tilt",
        "is_active": False
    }
    
    client.post("/devices", json=device1)
    client.post("/devices", json=device2)
    
    # Get all devices
    response = client.get("/devices")
    assert response.status_code == 200
    devices = response.json()
    assert len(devices) >= 2
    
    names = [d["name"] for d in devices]
    assert "Device 1" in names
    assert "Device 2" in names


def test_update_device(client):
    """Test updating a device"""
    # Create device
    payload = {
        "name": "Original Name",
        "device_type": "ispindel",
        "is_active": True
    }
    create_resp = client.post("/devices", json=payload)
    device_id = create_resp.json()["id"]
    
    # Update device
    update_payload = {
        "name": "Updated Name",
        "is_active": False
    }
    update_resp = client.put(f"/devices/{device_id}", json=update_payload)
    assert update_resp.status_code == 200
    updated = update_resp.json()
    
    assert updated["name"] == "Updated Name"
    assert updated["is_active"] is False
    assert updated["device_type"] == "ispindel"  # Should remain unchanged


def test_delete_device(client, db_session):
    """Test deleting a device"""
    # Create device
    payload = {
        "name": "Device to Delete",
        "device_type": "ispindel",
        "is_active": True
    }
    create_resp = client.post("/devices", json=payload)
    device_id = create_resp.json()["id"]
    
    # Delete device
    delete_resp = client.delete(f"/devices/{device_id}")
    assert delete_resp.status_code == 200
    
    # Verify deletion
    get_resp = client.get(f"/devices/{device_id}")
    assert get_resp.status_code == 404
    
    # Verify in database
    device = db_session.query(models.Device).filter_by(id=device_id).first()
    assert device is None


def test_device_not_found_returns_404(client):
    """Test that requesting a non-existent device returns 404"""
    response = client.get("/devices/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"


def test_update_device_not_found_returns_404(client):
    """Test that updating a non-existent device returns 404"""
    update_payload = {"name": "New Name"}
    response = client.put("/devices/9999", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"


def test_delete_device_not_found_returns_404(client):
    """Test that deleting a non-existent device returns 404"""
    response = client.delete("/devices/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"
