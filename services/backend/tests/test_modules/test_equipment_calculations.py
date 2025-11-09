"""Tests for equipment calculation utilities."""

import pytest
from utils.equipment_calculations import (
    calculate_pre_boil_volume,
    calculate_strike_water_volume,
    calculate_total_water_needed,
    calculate_efficiency,
    calculate_volume_loss,
)


def test_calculate_pre_boil_volume():
    """Test pre-boil volume calculation."""
    # Basic calculation: 20L batch + 10L evap loss + 2L trub loss = 32L
    result = calculate_pre_boil_volume(
        batch_size=20.0,
        boil_time=60,
        evap_rate=10.0,
        trub_chiller_loss=2.0,
        top_up_kettle=0.0,
    )
    assert result == 32.0


def test_calculate_pre_boil_volume_with_top_up():
    """Test pre-boil volume with top-up water."""
    # 20L batch + 10L evap + 2L trub - 5L top-up = 27L
    result = calculate_pre_boil_volume(
        batch_size=20.0,
        boil_time=60,
        evap_rate=10.0,
        trub_chiller_loss=2.0,
        top_up_kettle=5.0,
    )
    assert result == 27.0


def test_calculate_pre_boil_volume_invalid_inputs():
    """Test pre-boil volume with invalid inputs."""
    result = calculate_pre_boil_volume(
        batch_size=0,
        boil_time=60,
        evap_rate=10.0,
    )
    assert result == 0.0


def test_calculate_strike_water_volume():
    """Test strike water volume calculation."""
    # 5 kg grain * 3.0 L/kg = 15L
    result = calculate_strike_water_volume(
        grain_weight=5.0,
        mash_thickness=3.0,
    )
    assert result == 15.0


def test_calculate_strike_water_volume_thick_mash():
    """Test strike water with thick mash."""
    # 5 kg grain * 2.5 L/kg = 12.5L
    result = calculate_strike_water_volume(
        grain_weight=5.0,
        mash_thickness=2.5,
    )
    assert result == 12.5


def test_calculate_strike_water_volume_no_grain():
    """Test strike water with no grain."""
    result = calculate_strike_water_volume(grain_weight=0)
    assert result == 0.0


def test_calculate_total_water_needed():
    """Test total water calculation."""
    result = calculate_total_water_needed(
        batch_size=20.0,
        boil_time=60,
        evap_rate=10.0,
        grain_weight=5.0,
        grain_absorption_rate=1.0,
        trub_chiller_loss=2.0,
        lauter_deadspace=1.0,
        mash_thickness=3.0,
    )
    
    assert "strike_water" in result
    assert "sparge_water" in result
    assert "total_water" in result
    assert "pre_boil_volume" in result
    assert "grain_absorption" in result
    
    assert result["strike_water"] == 15.0  # 5kg * 3L/kg
    assert result["grain_absorption"] == 5.0  # 5kg * 1L/kg
    assert result["pre_boil_volume"] == 32.0  # 20L + 10L evap + 2L loss


def test_calculate_total_water_needed_no_grain():
    """Test total water calculation with no grain (extract brewing)."""
    result = calculate_total_water_needed(
        batch_size=20.0,
        boil_time=60,
        evap_rate=10.0,
        grain_weight=0,
        trub_chiller_loss=2.0,
    )
    
    assert result["strike_water"] == 0.0
    assert result["grain_absorption"] == 0.0
    # For extract brewing, we just need the pre-boil volume
    assert result["pre_boil_volume"] == 32.0


def test_calculate_total_water_needed_invalid():
    """Test total water calculation with invalid inputs."""
    result = calculate_total_water_needed(
        batch_size=0,
        boil_time=60,
        evap_rate=10.0,
    )
    
    assert result["strike_water"] == 0.0
    assert result["sparge_water"] == 0.0
    assert result["total_water"] == 0.0


def test_calculate_efficiency():
    """Test efficiency calculation."""
    # If we hit target exactly, efficiency is 100%
    result = calculate_efficiency(
        actual_og=1.050,
        target_og=1.050,
    )
    assert result == 100.0


def test_calculate_efficiency_lower():
    """Test efficiency when actual is lower than target."""
    # If actual is 1.040 but target was 1.050
    # (0.040 / 0.050) * 100 = 80%
    result = calculate_efficiency(
        actual_og=1.040,
        target_og=1.050,
    )
    assert result == 80.0


def test_calculate_efficiency_higher():
    """Test efficiency when actual is higher than target."""
    # If actual is 1.060 but target was 1.050
    # (0.060 / 0.050) * 100 = 120%
    result = calculate_efficiency(
        actual_og=1.060,
        target_og=1.050,
    )
    assert result == 120.0


def test_calculate_efficiency_invalid():
    """Test efficiency with invalid inputs."""
    result = calculate_efficiency(
        actual_og=0,
        target_og=1.050,
    )
    assert result == 0.0
    
    result = calculate_efficiency(
        actual_og=1.050,
        target_og=1.0,  # Target OG of 1.0 is invalid
    )
    assert result == 0.0


def test_calculate_volume_loss():
    """Test volume loss calculation."""
    result = calculate_volume_loss(
        trub_chiller_loss=2.0,
        lauter_deadspace=1.0,
        boil_time=60,
        evap_rate=10.0,
    )
    
    assert result["trub_chiller_loss"] == 2.0
    assert result["lauter_deadspace"] == 1.0
    assert result["evaporation_loss"] == 10.0  # 10L/hr * 1hr
    assert result["total_loss"] == 13.0  # 2 + 1 + 10


def test_calculate_volume_loss_no_evap():
    """Test volume loss with no evaporation."""
    result = calculate_volume_loss(
        trub_chiller_loss=2.0,
        lauter_deadspace=1.0,
        boil_time=0,
        evap_rate=10.0,
    )
    
    assert result["evaporation_loss"] == 0.0
    assert result["total_loss"] == 3.0  # 2 + 1


def test_calculate_volume_loss_minimal():
    """Test volume loss with minimal losses."""
    result = calculate_volume_loss(
        trub_chiller_loss=0,
        lauter_deadspace=0,
        boil_time=60,
        evap_rate=5.0,
    )
    
    assert result["trub_chiller_loss"] == 0.0
    assert result["lauter_deadspace"] == 0.0
    assert result["evaporation_loss"] == 5.0
    assert result["total_loss"] == 5.0
