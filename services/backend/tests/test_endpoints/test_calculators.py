"""
Tests for calculator API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestABVEndpoint:
    """Tests for ABV calculator endpoint."""

    def test_calculate_abv_success(self):
        """Test successful ABV calculation."""
        response = client.post(
            "/calculators/abv",
            json={"original_gravity": 1.050, "final_gravity": 1.010},
        )
        assert response.status_code == 200
        data = response.json()
        assert "abv" in data
        assert data["abv"] == pytest.approx(5.25, rel=1e-4)


class TestIBUEndpoint:
    """Tests for IBU calculator endpoint."""

    def test_calculate_ibu_success(self):
        """Test successful IBU calculation."""
        response = client.post(
            "/calculators/ibu",
            json={
                "alpha_acid": 12.0,
                "weight_oz": 2.0,
                "boil_time_min": 60.0,
                "batch_size_gal": 5.0,
                "gravity": 1.050,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "ibu" in data
        assert data["ibu"] > 0

    def test_calculate_ibu_zero_hops(self):
        """Test IBU calculation with zero hop weight."""
        response = client.post(
            "/calculators/ibu",
            json={
                "alpha_acid": 12.0,
                "weight_oz": 0.0,
                "boil_time_min": 60.0,
                "batch_size_gal": 5.0,
                "gravity": 1.050,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["ibu"] == 0.0


class TestSRMEndpoint:
    """Tests for SRM calculator endpoint."""

    def test_calculate_srm_success(self):
        """Test successful SRM calculation."""
        response = client.post(
            "/calculators/srm",
            json={
                "grain_color": 3.0,
                "grain_weight_lbs": 10.0,
                "batch_size_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "srm" in data
        assert data["srm"] > 0


class TestStrikeWaterEndpoint:
    """Tests for strike water calculator endpoint."""

    def test_calculate_strike_water_success(self):
        """Test successful strike water calculation."""
        response = client.post(
            "/calculators/strike-water",
            json={
                "grain_weight_lbs": 11.0,
                "mash_temp_f": 152.0,
                "grain_temp_f": 68.0,
                "water_to_grain_ratio": 1.25,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "volume_quarts" in data
        assert "temperature_f" in data
        assert data["volume_quarts"] == pytest.approx(13.75, rel=1e-4)
        assert data["temperature_f"] > 152.0

    def test_calculate_strike_water_default_ratio(self):
        """Test strike water calculation with default ratio."""
        response = client.post(
            "/calculators/strike-water",
            json={
                "grain_weight_lbs": 10.0,
                "mash_temp_f": 150.0,
                "grain_temp_f": 70.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "volume_quarts" in data
        assert "temperature_f" in data


class TestPrimingSugarEndpoint:
    """Tests for priming sugar calculator endpoint."""

    def test_calculate_priming_sugar_table(self):
        """Test priming sugar calculation with table sugar."""
        response = client.post(
            "/calculators/priming-sugar",
            json={
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

    def test_calculate_priming_sugar_corn(self):
        """Test priming sugar calculation with corn sugar."""
        response = client.post(
            "/calculators/priming-sugar",
            json={
                "volume_gal": 5.0,
                "carbonation_level": 2.4,
                "sugar_type": "corn",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "grams" in data


class TestYeastStarterEndpoint:
    """Tests for yeast starter calculator endpoint."""

    def test_calculate_yeast_starter_success(self):
        """Test successful yeast starter calculation."""
        response = client.post(
            "/calculators/yeast-starter",
            json={
                "og": 1.050,
                "volume_gal": 5.0,
                "yeast_age_months": 2.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "cells_needed_billions" in data
        assert "packages" in data
        assert "starter_size_ml" in data
        assert data["cells_needed_billions"] > 0
        assert data["packages"] >= 1

    def test_calculate_yeast_starter_with_target(self):
        """Test yeast starter calculation with custom target."""
        response = client.post(
            "/calculators/yeast-starter",
            json={
                "og": 1.050,
                "volume_gal": 5.0,
                "yeast_age_months": 0.0,
                "target_cell_count": 200.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["cells_needed_billions"] == pytest.approx(200.0, rel=1e-4)


class TestDilutionEndpoint:
    """Tests for dilution calculator endpoint."""

    def test_calculate_dilution_success(self):
        """Test successful dilution calculation."""
        response = client.post(
            "/calculators/dilution",
            json={
                "current_og": 1.060,
                "current_volume_gal": 5.0,
                "target_og": 1.050,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "water_to_add_gal" in data
        assert "final_volume_gal" in data
        assert data["water_to_add_gal"] > 0
        assert data["final_volume_gal"] > 5.0

    def test_calculate_dilution_no_dilution_needed(self):
        """Test dilution calculation when no dilution is needed."""
        response = client.post(
            "/calculators/dilution",
            json={
                "current_og": 1.050,
                "current_volume_gal": 5.0,
                "target_og": 1.060,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["water_to_add_gal"] == 0.0
        assert data["final_volume_gal"] == 5.0


class TestCarbonationEndpoint:
    """Tests for carbonation calculator endpoint."""

    def test_calculate_carbonation_success(self):
        """Test successful carbonation calculation."""
        response = client.post(
            "/calculators/carbonation",
            json={
                "temp_f": 38.0,
                "co2_volumes": 2.5,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "psi" in data
        assert "bar" in data
        assert data["psi"] >= 0
        assert data["bar"] >= 0

    def test_calculate_carbonation_temperature_effect(self):
        """Test that higher temperature requires higher pressure."""
        cold_response = client.post(
            "/calculators/carbonation",
            json={"temp_f": 38.0, "co2_volumes": 2.5},
        )
        warm_response = client.post(
            "/calculators/carbonation",
            json={"temp_f": 68.0, "co2_volumes": 2.5},
        )

        assert cold_response.status_code == 200
        assert warm_response.status_code == 200

        cold_data = cold_response.json()
        warm_data = warm_response.json()

        assert warm_data["psi"] > cold_data["psi"]


class TestWaterChemistryEndpoint:
    """Tests for water chemistry calculator endpoint."""

    def test_calculate_water_chemistry_success(self):
        """Test successful water chemistry calculation."""
        response = client.post(
            "/calculators/water-chemistry",
            json={
                "water_profile": {
                    "calcium": 50,
                    "magnesium": 10,
                    "sodium": 15,
                    "chloride": 60,
                    "sulfate": 120,
                    "bicarbonate": 80,
                },
                "grain_bill_lbs": 11.0,
                "target_ph": 5.4,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "residual_alkalinity" in data
        assert "estimated_ph" in data
        assert "ph_target" in data
        assert "ph_difference" in data
        assert 5.0 <= data["estimated_ph"] <= 6.0
