"""
Tests for batch cost tracking API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestBatchCostEndpoints:
    """Tests for batch cost CRUD endpoints."""

    @pytest.fixture
    def sample_batch_cost(self):
        """Sample batch cost data for testing."""
        return {
            "batch_id": 1,
            "fermentables_cost": 25.50,
            "hops_cost": 15.00,
            "yeasts_cost": 8.50,
            "miscs_cost": 5.00,
            "electricity_cost": 3.50,
            "water_cost": 2.00,
            "gas_cost": 4.00,
            "labor_cost": 0.0,
            "packaging_cost": 10.00,
            "other_cost": 2.00,
            "expected_yield_volume": 20.0,
            "selling_price_per_unit": 5.00,
            "unit_type": "pint",
        }

    @pytest.mark.skip(reason="Requires database migration to be run first")
    def test_create_batch_cost(self, sample_batch_cost):
        """Test creating batch cost tracking."""
        # This test would need a real batch to exist
        # In a real test environment, you would create a batch first
        # For now, we'll test the validation and structure
        response = client.post(
            "/batches/999/costs",  # Using non-existent batch
            json=sample_batch_cost,
        )
        # Expect 404 because batch doesn't exist
        assert response.status_code == 404

    @pytest.mark.skip(reason="Requires database migration to be run first")
    def test_create_batch_cost_mismatched_id(self):
        """Test creating batch cost with mismatched batch_id."""
        data = {
            "batch_id": 2,
            "fermentables_cost": 25.50,
        }
        response = client.post("/batches/1/costs", json=data)
        # Should fail validation
        assert response.status_code in [400, 404, 422]


class TestCostCalculatorEndpoints:
    """Tests for cost calculator endpoints."""

    def test_calculate_utility_costs(self):
        """Test utility cost calculation endpoint."""
        request_data = {
            "brew_time_hours": 5.0,
            "electricity_rate_per_kwh": 0.12,
            "water_volume_liters": 30.0,
            "water_rate_per_liter": 0.001,
            "gas_usage_cubic_meters": 0.0,
            "gas_rate_per_cubic_meter": 0.50,
            "heating_power_kw": 3.5,
        }
        response = client.post("/costs/calculate-utilities", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert "electricity_cost" in data
        assert "water_cost" in data
        assert "gas_cost" in data
        assert "total_utility_cost" in data
        assert data["electricity_cost"] > 0
        assert data["water_cost"] > 0
        assert data["gas_cost"] == 0.0

    def test_calculate_utility_costs_with_gas(self):
        """Test utility cost calculation with gas usage."""
        request_data = {
            "brew_time_hours": 6.0,
            "electricity_rate_per_kwh": 0.15,
            "water_volume_liters": 40.0,
            "water_rate_per_liter": 0.002,
            "gas_usage_cubic_meters": 2.0,
            "gas_rate_per_cubic_meter": 0.60,
            "heating_power_kw": 4.0,
        }
        response = client.post("/costs/calculate-utilities", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["gas_cost"] == 1.2
        assert data["total_utility_cost"] == pytest.approx(3.98, rel=0.01)

    def test_calculate_cost_per_unit_pint(self):
        """Test cost per unit calculation for pints."""
        request_data = {
            "total_cost": 75.50,
            "yield_volume_liters": 20.0,
            "unit_type": "pint",
        }
        response = client.post("/costs/calculate-cost-per-unit", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert "cost_per_unit" in data
        assert "unit_type" in data
        assert data["unit_type"] == "pint"
        assert data["cost_per_unit"] == pytest.approx(2.14, rel=0.01)

    def test_calculate_cost_per_unit_liter(self):
        """Test cost per unit calculation for liters."""
        request_data = {
            "total_cost": 75.50,
            "yield_volume_liters": 20.0,
            "unit_type": "liter",
        }
        response = client.post("/costs/calculate-cost-per-unit", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["unit_type"] == "liter"
        assert data["cost_per_unit"] == 3.77

    def test_calculate_cost_per_unit_bottle(self):
        """Test cost per unit calculation for bottles."""
        request_data = {
            "total_cost": 75.50,
            "yield_volume_liters": 20.0,
            "unit_type": "bottle",
        }
        response = client.post("/costs/calculate-cost-per-unit", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["unit_type"] == "bottle"
        assert data["cost_per_unit"] == pytest.approx(1.25, rel=0.01)

    def test_calculate_profit_margin(self):
        """Test profit margin calculation."""
        request_data = {
            "cost_per_unit": 2.14,
            "selling_price_per_unit": 5.00,
        }
        response = client.post("/costs/calculate-profit-margin", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert "profit_per_unit" in data
        assert "profit_margin_percentage" in data
        assert data["profit_per_unit"] == 2.86
        assert data["profit_margin_percentage"] == 57.2

    def test_calculate_profit_margin_loss(self):
        """Test profit margin calculation with loss."""
        request_data = {
            "cost_per_unit": 6.00,
            "selling_price_per_unit": 5.00,
        }
        response = client.post("/costs/calculate-profit-margin", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["profit_per_unit"] == -1.00
        assert data["profit_margin_percentage"] == -20.0

    def test_calculate_profit_margin_break_even(self):
        """Test profit margin calculation at break even."""
        request_data = {
            "cost_per_unit": 5.00,
            "selling_price_per_unit": 5.00,
        }
        response = client.post("/costs/calculate-profit-margin", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["profit_per_unit"] == 0.0
        assert data["profit_margin_percentage"] == 0.0


class TestCostCalculatorValidation:
    """Tests for cost calculator input validation."""

    def test_calculate_utility_costs_negative_values(self):
        """Test that negative values are rejected."""
        request_data = {
            "brew_time_hours": -5.0,  # Invalid negative
            "electricity_rate_per_kwh": 0.12,
            "water_volume_liters": 30.0,
            "water_rate_per_liter": 0.001,
            "gas_usage_cubic_meters": 0.0,
            "gas_rate_per_cubic_meter": 0.50,
            "heating_power_kw": 3.5,
        }
        response = client.post("/costs/calculate-utilities", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_calculate_cost_per_unit_zero_volume(self):
        """Test cost per unit with zero volume."""
        request_data = {
            "total_cost": 75.50,
            "yield_volume_liters": 0.0,  # Invalid zero
            "unit_type": "pint",
        }
        response = client.post("/costs/calculate-cost-per-unit", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_calculate_cost_per_unit_negative_cost(self):
        """Test cost per unit with negative cost."""
        request_data = {
            "total_cost": -75.50,  # Invalid negative
            "yield_volume_liters": 20.0,
            "unit_type": "pint",
        }
        response = client.post("/costs/calculate-cost-per-unit", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_calculate_profit_margin_negative_selling_price(self):
        """Test profit margin with negative selling price."""
        request_data = {
            "cost_per_unit": 2.14,
            "selling_price_per_unit": -5.00,  # Invalid negative
        }
        response = client.post("/costs/calculate-profit-margin", json=request_data)
        assert response.status_code == 422  # Validation error
