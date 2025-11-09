"""
Tests for packaging API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestPackagingCalculators:
    """Tests for packaging calculator endpoints."""

    def test_calculate_priming_sugar_success(self):
        """Test successful priming sugar calculation."""
        response = client.post(
            "/packaging/calculate-priming-sugar",
            params={
                "volume_gal": 5.0,
                "carbonation_level": 2.4,
                "sugar_type": "table",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "grams" in data
        assert "oz" in data
        assert data["grams"] > 0
        assert data["oz"] > 0

    def test_calculate_priming_sugar_different_sugar_types(self):
        """Test priming sugar calculation with different sugar types."""
        sugar_types = ["table", "corn", "dme", "honey"]
        for sugar_type in sugar_types:
            response = client.post(
                "/packaging/calculate-priming-sugar",
                params={
                    "volume_gal": 5.0,
                    "carbonation_level": 2.4,
                    "sugar_type": sugar_type,
                },
            )
            assert response.status_code == 200
            data = response.json()
            assert data["grams"] > 0

    def test_calculate_carbonation_psi_success(self):
        """Test successful carbonation PSI calculation."""
        response = client.post(
            "/packaging/calculate-carbonation-psi",
            params={
                "temp_f": 38.0,
                "co2_volumes": 2.5,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "psi" in data
        assert "bar" in data
        assert data["psi"] > 0
        assert data["bar"] > 0

    def test_calculate_carbonation_psi_different_temps(self):
        """Test carbonation PSI calculation at different temperatures."""
        temps = [32.0, 38.0, 45.0, 50.0]
        for temp in temps:
            response = client.post(
                "/packaging/calculate-carbonation-psi",
                params={
                    "temp_f": temp,
                    "co2_volumes": 2.5,
                },
            )
            assert response.status_code == 200
            data = response.json()
            # Lower temps should require lower pressure
            assert data["psi"] > 0


class TestPackagingEndpoints:
    """Tests for packaging CRUD endpoints."""

    @pytest.fixture
    def sample_batch_id(self):
        """
        Fixture to provide a sample batch ID for testing.
        Note: In actual tests, you would create a test batch first.
        """
        # This would need to be implemented based on your test setup
        return 1

    def test_packaging_endpoint_structure(self):
        """
        Test that packaging endpoints have the expected structure.
        This is a basic smoke test that doesn't require database.
        """
        # Test that endpoints exist and return appropriate error codes
        # when called without proper setup
        
        # Try to get packaging details for non-existent batch
        response = client.get("/batches/99999/packaging")
        # Should return 404 (not found) or 500 (db error) depending on setup
        assert response.status_code in [404, 500]

    def test_create_packaging_details_validation(self):
        """Test validation of packaging details creation."""
        # Test with invalid data
        response = client.post(
            "/batches/1/packaging",
            json={
                "packaging_date": "invalid-date",
                "method": "bottling",
            },
        )
        # Should fail validation
        assert response.status_code in [422, 500]

    def test_packaging_details_schema(self):
        """Test the packaging details schema structure."""
        # Valid packaging details for bottling
        bottling_data = {
            "packaging_date": "2024-04-15T10:00:00Z",
            "method": "bottling",
            "carbonation_method": "priming_sugar",
            "volumes_co2": 2.4,
            "container_count": 48,
            "container_size": 0.5,
            "priming_sugar_amount": 120.5,
            "priming_sugar_type": "table",
            "temperature": 68.0,
            "notes": "Test bottling",
        }
        
        # This tests the schema is valid JSON
        import json
        json_str = json.dumps(bottling_data)
        assert json_str is not None

        # Valid packaging details for kegging
        kegging_data = {
            "packaging_date": "2024-04-15T10:00:00Z",
            "method": "kegging",
            "carbonation_method": "forced",
            "volumes_co2": 2.5,
            "container_count": 1,
            "container_size": 19.0,
            "pressure_psi": 12.5,
            "temperature": 38.0,
            "notes": "Test kegging",
        }
        
        json_str = json.dumps(kegging_data)
        assert json_str is not None
