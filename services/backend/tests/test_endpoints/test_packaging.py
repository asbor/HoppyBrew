"""
Tests for packaging API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)


class TestPackagingEndpoints:
    """Tests for packaging details endpoints."""

    def test_create_packaging_details_bottle(self, sample_batch):
        """Test creating packaging details for bottling."""
        response = client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "bottle",
                "date": datetime.now().isoformat(),
                "carbonation_method": "priming",
                "volumes": 2.5,
                "container_count": 48,
                "container_size": 0.5,
                "priming_sugar_type": "corn",
                "priming_sugar_amount": 150.0,
                "notes": "Bottled using 500ml bottles",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["method"] == "bottle"
        assert data["batch_id"] == sample_batch["id"]
        assert data["volumes"] == 2.5
        assert data["container_count"] == 48
        assert data["priming_sugar_type"] == "corn"

    def test_create_packaging_details_keg(self, sample_batch):
        """Test creating packaging details for kegging."""
        response = client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "keg",
                "date": datetime.now().isoformat(),
                "carbonation_method": "forced",
                "volumes": 2.4,
                "container_count": 1,
                "container_size": 5.0,
                "carbonation_temp": 38.0,
                "carbonation_psi": 12.5,
                "notes": "Kegged in 5-gallon corny keg",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["method"] == "keg"
        assert data["carbonation_method"] == "forced"
        assert data["carbonation_psi"] == 12.5

    def test_create_packaging_details_invalid_method(self, sample_batch):
        """Test creating packaging details with invalid method."""
        response = client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "invalid_method",
                "date": datetime.now().isoformat(),
                "volumes": 2.5,
            },
        )
        assert response.status_code == 400
        assert "Method must be 'bottle' or 'keg'" in response.json()["detail"]

    def test_create_packaging_details_invalid_carbonation_method(self, sample_batch):
        """Test creating packaging details with invalid carbonation method."""
        response = client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "bottle",
                "date": datetime.now().isoformat(),
                "carbonation_method": "invalid",
                "volumes": 2.5,
            },
        )
        assert response.status_code == 400
        assert "Carbonation method must be" in response.json()["detail"]

    def test_create_packaging_details_invalid_sugar_type(self, sample_batch):
        """Test creating packaging details with invalid priming sugar type."""
        response = client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "bottle",
                "date": datetime.now().isoformat(),
                "priming_sugar_type": "invalid",
                "volumes": 2.5,
            },
        )
        assert response.status_code == 400
        assert "Priming sugar type must be" in response.json()["detail"]

    def test_create_packaging_details_nonexistent_batch(self):
        """Test creating packaging details for a nonexistent batch."""
        response = client.post(
            "/packaging",
            json={
                "batch_id": 99999,
                "method": "bottle",
                "date": datetime.now().isoformat(),
                "volumes": 2.5,
            },
        )
        assert response.status_code == 404
        assert "Batch not found" in response.json()["detail"]

    def test_create_duplicate_packaging_details(self, sample_batch):
        """Test creating duplicate packaging details for the same batch."""
        # Create first packaging details
        client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "bottle",
                "date": datetime.now().isoformat(),
                "volumes": 2.5,
            },
        )
        
        # Try to create duplicate
        response = client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "keg",
                "date": datetime.now().isoformat(),
                "volumes": 2.4,
            },
        )
        assert response.status_code == 400
        assert "already exist" in response.json()["detail"]

    def test_get_packaging_details(self, sample_batch):
        """Test retrieving packaging details for a batch."""
        # Create packaging details first
        create_response = client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "bottle",
                "date": datetime.now().isoformat(),
                "volumes": 2.5,
                "container_count": 48,
            },
        )
        assert create_response.status_code == 201
        
        # Get packaging details
        response = client.get(f"/packaging/{sample_batch['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["batch_id"] == sample_batch["id"]
        assert data["method"] == "bottle"
        assert data["volumes"] == 2.5

    def test_get_packaging_details_not_found(self, sample_batch):
        """Test retrieving packaging details for a batch without any."""
        response = client.get(f"/packaging/{sample_batch['id']}")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_list_packaging_details(self, sample_batch):
        """Test listing all packaging details."""
        # Create packaging details
        client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "bottle",
                "date": datetime.now().isoformat(),
                "volumes": 2.5,
            },
        )
        
        # List all packaging details
        response = client.get("/packaging")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["batch_id"] == sample_batch["id"]

    def test_update_packaging_details(self, sample_batch):
        """Test updating packaging details."""
        # Create packaging details first
        client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "bottle",
                "date": datetime.now().isoformat(),
                "volumes": 2.5,
                "container_count": 48,
            },
        )
        
        # Update packaging details
        response = client.put(
            f"/packaging/{sample_batch['id']}",
            json={
                "volumes": 2.6,
                "container_count": 50,
                "notes": "Updated count",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["volumes"] == 2.6
        assert data["container_count"] == 50
        assert data["notes"] == "Updated count"
        # Original values should remain
        assert data["method"] == "bottle"

    def test_update_packaging_details_not_found(self, sample_batch):
        """Test updating packaging details that don't exist."""
        response = client.put(
            f"/packaging/{sample_batch['id']}",
            json={"volumes": 2.6},
        )
        assert response.status_code == 404

    def test_update_packaging_details_invalid_method(self, sample_batch):
        """Test updating packaging details with invalid method."""
        # Create packaging details first
        client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "bottle",
                "date": datetime.now().isoformat(),
                "volumes": 2.5,
            },
        )
        
        # Try to update with invalid method
        response = client.put(
            f"/packaging/{sample_batch['id']}",
            json={"method": "invalid"},
        )
        assert response.status_code == 400

    def test_delete_packaging_details(self, sample_batch):
        """Test deleting packaging details."""
        # Create packaging details first
        client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "bottle",
                "date": datetime.now().isoformat(),
                "volumes": 2.5,
            },
        )
        
        # Delete packaging details
        response = client.delete(f"/packaging/{sample_batch['id']}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/packaging/{sample_batch['id']}")
        assert get_response.status_code == 404

    def test_delete_packaging_details_not_found(self, sample_batch):
        """Test deleting packaging details that don't exist."""
        response = client.delete(f"/packaging/{sample_batch['id']}")
        assert response.status_code == 404


class TestPackagingIntegration:
    """Integration tests for packaging workflow."""

    def test_complete_bottling_workflow(self, sample_batch):
        """Test complete workflow for bottling."""
        # Create packaging details for bottling
        packaging_response = client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "bottle",
                "date": datetime.now().isoformat(),
                "carbonation_method": "priming",
                "volumes": 2.5,
                "container_count": 48,
                "container_size": 0.5,
                "priming_sugar_type": "corn",
                "priming_sugar_amount": 150.0,
            },
        )
        assert packaging_response.status_code == 201
        
        # Calculate priming sugar to verify accuracy
        calc_response = client.post(
            "/calculators/priming-sugar",
            json={
                "volume_gal": 5.0,
                "carbonation_level": 2.5,
                "sugar_type": "corn",
            },
        )
        assert calc_response.status_code == 200
        calc_data = calc_response.json()
        # The amount should be close to what we specified
        assert abs(calc_data["grams"] - 150.0) < 50.0  # Allow some variance

    def test_complete_kegging_workflow(self, sample_batch):
        """Test complete workflow for kegging."""
        # Calculate carbonation PSI
        calc_response = client.post(
            "/calculators/carbonation",
            json={
                "temp_f": 38.0,
                "co2_volumes": 2.4,
            },
        )
        assert calc_response.status_code == 200
        calc_data = calc_response.json()
        psi = calc_data["psi"]
        
        # Create packaging details for kegging using calculated PSI
        packaging_response = client.post(
            "/packaging",
            json={
                "batch_id": sample_batch["id"],
                "method": "keg",
                "date": datetime.now().isoformat(),
                "carbonation_method": "forced",
                "volumes": 2.4,
                "container_count": 1,
                "container_size": 5.0,
                "carbonation_temp": 38.0,
                "carbonation_psi": psi,
            },
        )
        assert packaging_response.status_code == 201
        packaging_data = packaging_response.json()
        assert packaging_data["carbonation_psi"] == pytest.approx(psi, rel=1e-4)
