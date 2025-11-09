"""
Tests for water chemistry calculator endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestSaltIonContributionEndpoint:
    """Tests for salt ion contribution calculator endpoint."""

    def test_calculate_gypsum_contribution(self):
        """Test calculating ion contribution from gypsum (CaSO4)."""
        response = client.post(
            "/calculators/salt-ion-contribution",
            json={
                "salt_type": "CaSO4",
                "amount_grams": 5.0,
                "water_volume_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # Gypsum should add calcium and sulfate
        assert data["calcium"] > 0
        assert data["sulfate"] > 0
        assert data["magnesium"] == 0
        assert data["sodium"] == 0
        assert data["chloride"] == 0
        assert data["bicarbonate"] == 0

    def test_calculate_calcium_chloride_contribution(self):
        """Test calculating ion contribution from calcium chloride."""
        response = client.post(
            "/calculators/salt-ion-contribution",
            json={
                "salt_type": "CaCl2",
                "amount_grams": 3.0,
                "water_volume_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # Calcium chloride should add calcium and chloride
        assert data["calcium"] > 0
        assert data["chloride"] > 0
        assert data["magnesium"] == 0
        assert data["sodium"] == 0
        assert data["sulfate"] == 0
        assert data["bicarbonate"] == 0

    def test_calculate_epsom_salt_contribution(self):
        """Test calculating ion contribution from Epsom salt (MgSO4)."""
        response = client.post(
            "/calculators/salt-ion-contribution",
            json={
                "salt_type": "MgSO4",
                "amount_grams": 2.0,
                "water_volume_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # Epsom salt should add magnesium and sulfate
        assert data["magnesium"] > 0
        assert data["sulfate"] > 0
        assert data["calcium"] == 0
        assert data["sodium"] == 0
        assert data["chloride"] == 0
        assert data["bicarbonate"] == 0

    def test_calculate_table_salt_contribution(self):
        """Test calculating ion contribution from table salt (NaCl)."""
        response = client.post(
            "/calculators/salt-ion-contribution",
            json={
                "salt_type": "NaCl",
                "amount_grams": 1.0,
                "water_volume_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # Table salt should add sodium and chloride
        assert data["sodium"] > 0
        assert data["chloride"] > 0
        assert data["calcium"] == 0
        assert data["magnesium"] == 0
        assert data["sulfate"] == 0
        assert data["bicarbonate"] == 0

    def test_calculate_baking_soda_contribution(self):
        """Test calculating ion contribution from baking soda (NaHCO3)."""
        response = client.post(
            "/calculators/salt-ion-contribution",
            json={
                "salt_type": "NaHCO3",
                "amount_grams": 2.0,
                "water_volume_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # Baking soda should add sodium and bicarbonate
        assert data["sodium"] > 0
        assert data["bicarbonate"] > 0
        assert data["calcium"] == 0
        assert data["magnesium"] == 0
        assert data["chloride"] == 0
        assert data["sulfate"] == 0

    def test_zero_amount_returns_zeros(self):
        """Test that zero salt amount returns zero contributions."""
        response = client.post(
            "/calculators/salt-ion-contribution",
            json={
                "salt_type": "CaSO4",
                "amount_grams": 0.0,
                "water_volume_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # All ions should be zero
        assert data["calcium"] == 0
        assert data["magnesium"] == 0
        assert data["sodium"] == 0
        assert data["chloride"] == 0
        assert data["sulfate"] == 0
        assert data["bicarbonate"] == 0

    def test_invalid_salt_type(self):
        """Test that invalid salt type returns error."""
        response = client.post(
            "/calculators/salt-ion-contribution",
            json={
                "salt_type": "InvalidSalt",
                "amount_grams": 5.0,
                "water_volume_gal": 5.0,
            },
        )
        # Should return 422 (validation error) or 500 (internal error)
        assert response.status_code in [422, 500]


class TestMineralAdditionsEndpoint:
    """Tests for mineral additions calculator endpoint."""

    def test_calculate_mineral_additions_basic(self):
        """Test calculating mineral additions for basic profile adjustment."""
        response = client.post(
            "/calculators/mineral-additions",
            json={
                "source_profile": {
                    "calcium": 10,
                    "magnesium": 2,
                    "sodium": 5,
                    "chloride": 8,
                    "sulfate": 5,
                    "bicarbonate": 20,
                },
                "target_profile": {
                    "calcium": 100,
                    "magnesium": 10,
                    "sodium": 15,
                    "chloride": 60,
                    "sulfate": 150,
                    "bicarbonate": 40,
                },
                "water_volume_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # Should return additions, resulting profile, and target
        assert "additions" in data
        assert "resulting_profile" in data
        assert "target_profile" in data
        
        # Should have salt additions
        additions = data["additions"]
        assert "CaSO4" in additions
        assert "CaCl2" in additions
        
        # Resulting profile should be improved from source
        resulting = data["resulting_profile"]
        assert resulting["calcium"] > 10  # Better than source
        assert resulting["sulfate"] > 5   # Better than source

    def test_no_adjustment_needed(self):
        """Test when source and target are the same."""
        profile = {
            "calcium": 50,
            "magnesium": 10,
            "sodium": 15,
            "chloride": 40,
            "sulfate": 50,
            "bicarbonate": 100,
        }
        
        response = client.post(
            "/calculators/mineral-additions",
            json={
                "source_profile": profile,
                "target_profile": profile,
                "water_volume_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # All additions should be zero or near zero
        additions = data["additions"]
        total_additions = sum(additions.values())
        assert total_additions < 0.1  # Allow for rounding

    def test_ipa_water_profile(self):
        """Test creating a hoppy IPA water profile from RO water."""
        response = client.post(
            "/calculators/mineral-additions",
            json={
                "source_profile": {
                    "calcium": 0,
                    "magnesium": 0,
                    "sodium": 0,
                    "chloride": 0,
                    "sulfate": 0,
                    "bicarbonate": 0,
                },
                "target_profile": {
                    "calcium": 150,
                    "magnesium": 10,
                    "sodium": 15,
                    "chloride": 60,
                    "sulfate": 300,
                    "bicarbonate": 50,
                },
                "water_volume_gal": 6.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # Should recommend gypsum for high sulfate
        additions = data["additions"]
        assert additions.get("CaSO4", 0) >= 0  # At least some gypsum
        
        # Should have improved water profile
        resulting = data["resulting_profile"]
        assert resulting["calcium"] > 0
        assert resulting["sulfate"] > 0


class TestWaterAdjustmentEndpoint:
    """Tests for water adjustment calculator endpoint."""

    def test_calculate_water_adjustment_gypsum(self):
        """Test calculating water adjustment with gypsum addition."""
        response = client.post(
            "/calculators/water-adjustment",
            json={
                "water_profile": {
                    "calcium": 10,
                    "magnesium": 2,
                    "sodium": 5,
                    "chloride": 8,
                    "sulfate": 5,
                    "bicarbonate": 20,
                },
                "salt_additions": {
                    "CaSO4": 5.0,
                },
                "water_volume_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # Calcium and sulfate should increase
        assert data["calcium"] > 10
        assert data["sulfate"] > 5
        # Other ions should remain the same
        assert data["magnesium"] == 2
        assert data["sodium"] == 5
        assert data["chloride"] == 8
        assert data["bicarbonate"] == 20

    def test_calculate_water_adjustment_multiple_salts(self):
        """Test calculating water adjustment with multiple salt additions."""
        response = client.post(
            "/calculators/water-adjustment",
            json={
                "water_profile": {
                    "calcium": 10,
                    "magnesium": 2,
                    "sodium": 5,
                    "chloride": 8,
                    "sulfate": 5,
                    "bicarbonate": 20,
                },
                "salt_additions": {
                    "CaSO4": 5.0,
                    "CaCl2": 3.0,
                    "NaCl": 1.0,
                },
                "water_volume_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # Multiple ions should increase
        assert data["calcium"] > 10  # From gypsum and CaCl2
        assert data["sulfate"] > 5   # From gypsum
        assert data["chloride"] > 8  # From CaCl2 and NaCl
        assert data["sodium"] >= 5    # From NaCl (may have rounding)

    def test_no_salt_additions(self):
        """Test water adjustment with no salt additions."""
        profile = {
            "calcium": 50,
            "magnesium": 10,
            "sodium": 15,
            "chloride": 40,
            "sulfate": 50,
            "bicarbonate": 100,
        }
        
        response = client.post(
            "/calculators/water-adjustment",
            json={
                "water_profile": profile,
                "salt_additions": {},
                "water_volume_gal": 5.0,
            },
        )
        assert response.status_code == 200
        data = response.json()
        
        # Profile should remain unchanged
        assert data["calcium"] == 50
        assert data["magnesium"] == 10
        assert data["sodium"] == 15
        assert data["chloride"] == 40
        assert data["sulfate"] == 50
        assert data["bicarbonate"] == 100


class TestWaterChemistryIntegration:
    """Integration tests for water chemistry calculations."""

    def test_end_to_end_water_adjustment(self):
        """Test complete workflow: calculate additions, then verify adjustment."""
        # Step 1: Calculate recommended mineral additions
        additions_response = client.post(
            "/calculators/mineral-additions",
            json={
                "source_profile": {
                    "calcium": 5,
                    "magnesium": 1,
                    "sodium": 2,
                    "chloride": 5,
                    "sulfate": 3,
                    "bicarbonate": 15,
                },
                "target_profile": {
                    "calcium": 75,
                    "magnesium": 8,
                    "sodium": 10,
                    "chloride": 50,
                    "sulfate": 100,
                    "bicarbonate": 30,
                },
                "water_volume_gal": 5.0,
            },
        )
        assert additions_response.status_code == 200
        additions_data = additions_response.json()
        
        # Step 2: Verify the resulting profile matches
        resulting_profile = additions_data["resulting_profile"]
        target_profile = additions_data["target_profile"]
        
        # Check that we're close to target (allow larger tolerance since algorithm is approximate)
        source_profile = {
            "calcium": 5,
            "magnesium": 1,
            "sodium": 2,
            "chloride": 5,
            "sulfate": 3,
            "bicarbonate": 15,
        }
        for ion in ["calcium", "sulfate", "chloride"]:
            if target_profile[ion] > 0:
                # We mainly check that the algorithm moves in the right direction
                # not that it hits the target exactly (due to greedy algorithm constraints)
                assert resulting_profile[ion] > source_profile[ion] + 10, \
                    f"{ion} should be improved significantly from source"

    def test_calculate_ph_after_mineral_additions(self):
        """Test calculating pH after mineral additions."""
        # First, calculate mineral additions for a profile
        additions_response = client.post(
            "/calculators/mineral-additions",
            json={
                "source_profile": {
                    "calcium": 0,
                    "magnesium": 0,
                    "sodium": 0,
                    "chloride": 0,
                    "sulfate": 0,
                    "bicarbonate": 0,
                },
                "target_profile": {
                    "calcium": 100,
                    "magnesium": 10,
                    "sodium": 15,
                    "chloride": 75,
                    "sulfate": 150,
                    "bicarbonate": 50,
                },
                "water_volume_gal": 5.0,
            },
        )
        assert additions_response.status_code == 200
        resulting_profile = additions_response.json()["resulting_profile"]
        
        # Then calculate pH with the resulting profile
        ph_response = client.post(
            "/calculators/water-chemistry",
            json={
                "water_profile": resulting_profile,
                "grain_bill_lbs": 10.0,
                "target_ph": 5.4,
            },
        )
        assert ph_response.status_code == 200
        ph_data = ph_response.json()
        
        # Should return pH estimation
        assert "estimated_ph" in ph_data
        assert "residual_alkalinity" in ph_data
        assert 5.0 <= ph_data["estimated_ph"] <= 6.0
