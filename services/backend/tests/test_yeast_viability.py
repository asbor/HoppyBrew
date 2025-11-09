"""
Unit tests for yeast viability calculator.
"""
import pytest
from datetime import datetime, timedelta
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.yeast_viability import YeastViabilityCalculator


class TestYeastViabilityCalculator:
    """Test the yeast viability calculator"""
    
    def test_fresh_dry_yeast(self):
        """Test viability calculation for fresh dry yeast"""
        manufacture_date = datetime.now() - timedelta(days=30)
        
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form="Dry",
            manufacture_date=manufacture_date,
            initial_viability=100.0,
            storage_temperature=4.0,
            generation=0
        )
        
        # Dry yeast should have very high viability after 1 month
        assert result["current_viability"] >= 99.0
        assert result["viability_status"] == "excellent"
        assert "direct pitching" in result["recommendation"].lower()
    
    def test_old_dry_yeast(self):
        """Test viability calculation for old dry yeast"""
        manufacture_date = datetime.now() - timedelta(days=730)  # 2 years
        
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form="Dry",
            manufacture_date=manufacture_date,
            initial_viability=100.0,
            storage_temperature=4.0,
            generation=0
        )
        
        # Dry yeast degrades slowly but should show some loss after 2 years
        assert result["current_viability"] < 100.0
        assert result["current_viability"] > 80.0  # Still usable
        assert result["days_since_manufacture"] == 730
    
    def test_fresh_liquid_yeast(self):
        """Test viability calculation for fresh liquid yeast"""
        manufacture_date = datetime.now() - timedelta(days=30)
        
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form="Liquid",
            manufacture_date=manufacture_date,
            initial_viability=100.0,
            storage_temperature=4.0,
            generation=0
        )
        
        # Liquid yeast degrades faster than dry
        assert result["current_viability"] < 100.0
        assert result["current_viability"] >= 90.0
        assert result["viability_status"] in ["excellent", "good"]
    
    def test_old_liquid_yeast(self):
        """Test viability calculation for old liquid yeast"""
        manufacture_date = datetime.now() - timedelta(days=180)  # 6 months
        
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form="Liquid",
            manufacture_date=manufacture_date,
            initial_viability=100.0,
            storage_temperature=4.0,
            generation=0
        )
        
        # Liquid yeast should degrade significantly after 6 months
        assert result["current_viability"] < 90.0
        assert result["viability_status"] in ["good", "fair", "poor"]
        assert "starter" in result["recommendation"].lower()
    
    def test_temperature_effect(self):
        """Test that higher storage temperature increases decay"""
        manufacture_date = datetime.now() - timedelta(days=90)
        
        # Calculate at 4°C
        result_cold = YeastViabilityCalculator.calculate_viability(
            yeast_form="Liquid",
            manufacture_date=manufacture_date,
            initial_viability=100.0,
            storage_temperature=4.0,
            generation=0
        )
        
        # Calculate at 20°C
        result_warm = YeastViabilityCalculator.calculate_viability(
            yeast_form="Liquid",
            manufacture_date=manufacture_date,
            initial_viability=100.0,
            storage_temperature=20.0,
            generation=0
        )
        
        # Warmer storage should result in lower viability
        assert result_warm["current_viability"] < result_cold["current_viability"]
    
    def test_generation_effect(self):
        """Test that higher generation number decreases viability"""
        manufacture_date = datetime.now() - timedelta(days=30)
        
        # Generation 0 (commercial)
        result_gen0 = YeastViabilityCalculator.calculate_viability(
            yeast_form="Liquid",
            manufacture_date=manufacture_date,
            initial_viability=100.0,
            storage_temperature=4.0,
            generation=0
        )
        
        # Generation 3
        result_gen3 = YeastViabilityCalculator.calculate_viability(
            yeast_form="Liquid",
            manufacture_date=manufacture_date,
            initial_viability=100.0,
            storage_temperature=4.0,
            generation=3
        )
        
        # Higher generation should have lower viability
        assert result_gen3["current_viability"] < result_gen0["current_viability"]
        expected_loss = 3 * YeastViabilityCalculator.GENERATION_LOSS_PERCENT
        actual_loss = result_gen0["current_viability"] - result_gen3["current_viability"]
        assert abs(actual_loss - expected_loss) < 1.0  # Allow small rounding difference
    
    def test_expiry_date_calculation(self):
        """Test that expiry date is properly calculated"""
        manufacture_date = datetime.now() - timedelta(days=90)
        expiry_date = datetime.now() + timedelta(days=90)
        
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form="Liquid",
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            initial_viability=100.0,
            generation=0
        )
        
        assert result["days_since_manufacture"] == 90
        assert result["days_until_expiry"] == 90
    
    def test_viability_bounds(self):
        """Test that viability stays within 0-100% bounds"""
        # Very old yeast should not go below 0
        manufacture_date = datetime.now() - timedelta(days=3650)  # 10 years
        
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form="Liquid",
            manufacture_date=manufacture_date,
            initial_viability=100.0,
            storage_temperature=20.0,
            generation=10
        )
        
        assert result["current_viability"] >= 0.0
        assert result["current_viability"] <= 100.0
    
    def test_status_categories(self):
        """Test that viability status is correctly categorized"""
        # Test excellent (>= 95%)
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form="Dry",
            manufacture_date=datetime.now() - timedelta(days=1),
            initial_viability=100.0,
            generation=0
        )
        assert result["viability_status"] == "excellent"
        
        # Test good (85-94%)
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form="Liquid",
            manufacture_date=datetime.now() - timedelta(days=60),
            initial_viability=100.0,
            generation=0
        )
        assert result["viability_status"] in ["good", "excellent"]
        
        # Test with very low viability
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form="Liquid",
            manufacture_date=datetime.now() - timedelta(days=365),
            initial_viability=50.0,
            storage_temperature=25.0,
            generation=5
        )
        assert result["viability_status"] in ["poor", "expired"]
    
    def test_no_manufacture_date(self):
        """Test calculation when no manufacture date is provided"""
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form="Liquid",
            initial_viability=90.0,
            generation=2
        )
        
        # Should still calculate generation loss
        assert result["current_viability"] < 90.0
        assert result["days_since_manufacture"] is None
    
    def test_starter_size_calculation(self):
        """Test starter size recommendation"""
        # Good viability - no starter needed
        result = YeastViabilityCalculator.calculate_starter_size(
            viability=90.0,
            target_cells=200.0
        )
        assert result["starter_recommended"] is False
        
        # Low viability - starter needed
        result = YeastViabilityCalculator.calculate_starter_size(
            viability=60.0,
            target_cells=200.0
        )
        assert result["starter_recommended"] is True
        assert result["starter_size_liters"] > 0
        
        # Very low viability
        result = YeastViabilityCalculator.calculate_starter_size(
            viability=0.0,
            target_cells=200.0
        )
        assert result["starter_recommended"] is True
        assert result["starter_size_liters"] is None
        assert "fresh yeast" in result["message"].lower()
    
    def test_slant_yeast_viability(self):
        """Test viability calculation for yeast slants"""
        manufacture_date = datetime.now() - timedelta(days=365)  # 1 year
        
        result = YeastViabilityCalculator.calculate_viability(
            yeast_form="Slant",
            manufacture_date=manufacture_date,
            initial_viability=100.0,
            storage_temperature=4.0,
            generation=0
        )
        
        # Slants should degrade slower than liquid, faster than dry
        assert result["current_viability"] > 80.0
        assert result["current_viability"] < 95.0
        assert result["viability_status"] in ["good", "excellent"]
