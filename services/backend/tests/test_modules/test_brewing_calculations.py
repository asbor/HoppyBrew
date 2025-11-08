import math

import pytest

from modules.brewing_calculations import (
    calculate_abv,
    calculate_ibu_tinseth,
    calculate_srm_morey,
    calculate_strike_water,
    calculate_priming_sugar,
    calculate_yeast_starter,
    calculate_dilution,
    calculate_carbonation,
    calculate_water_chemistry,
)


def test_calculate_abv_standard_reading():
    abv = calculate_abv(1.050, 1.010)
    assert math.isclose(abv, 5.25, rel_tol=1e-4)


def test_calculate_abv_invalid_gravity_order():
    with pytest.raises(ValueError):
        calculate_abv(1.010, 1.050)


def test_calculate_abv_requires_positive_values():
    with pytest.raises(ValueError):
        calculate_abv(-1.050, 1.010)


def test_calculate_ibu_tinseth_baseline():
    ibu = calculate_ibu_tinseth(
        alpha_acid=12.0,
        weight_oz=2.0,
        boil_time_min=60.0,
        batch_size_gal=5.0,
        gravity=1.050,
    )

    gravity_factor = 1.65 * math.pow(0.000125, 1.050 - 1)
    time_factor = (1 - math.exp(-0.04 * 60.0)) / 4.15
    expected = (0.12 * 2.0 * 7490 * gravity_factor * time_factor) / 5.0

    assert math.isclose(ibu, expected, rel_tol=1e-5)


def test_calculate_ibu_tinseth_zero_inputs():
    assert calculate_ibu_tinseth(0.0, 2.0, 60.0, 5.0, 1.050) == 0.0
    assert calculate_ibu_tinseth(12.0, 0.0, 60.0, 5.0, 1.050) == 0.0
    assert calculate_ibu_tinseth(12.0, 2.0, 0.0, 5.0, 1.050) == 0.0


def test_calculate_ibu_tinseth_negative_volume():
    with pytest.raises(ValueError):
        calculate_ibu_tinseth(12.0, 2.0, 60.0, -5.0, 1.050)


def test_calculate_srm_morey():
    srm = calculate_srm_morey(
        grain_color=50.0,
        grain_weight_lbs=12.0,
        batch_size_gal=5.0,
    )

    mcu = (12.0 * 50.0) / 5.0
    expected = 1.4922 * math.pow(mcu, 0.6859)

    assert math.isclose(srm, expected, rel_tol=1e-5)


def test_calculate_srm_morey_handles_zero_inputs():
    assert calculate_srm_morey(0.0, 12.0, 5.0) == 0.0
    assert calculate_srm_morey(10.0, 0.0, 5.0) == 0.0


def test_calculate_srm_morey_negative_batch_size():
    with pytest.raises(ValueError):
        calculate_srm_morey(10.0, 5.0, 0.0)


# Strike Water Calculator Tests


def test_calculate_strike_water_baseline():
    result = calculate_strike_water(
        grain_weight_lbs=11.0,
        mash_temp_f=152.0,
        grain_temp_f=68.0,
        water_to_grain_ratio=1.25,
    )
    
    assert "volume_quarts" in result
    assert "temperature_f" in result
    assert math.isclose(result["volume_quarts"], 13.75, rel_tol=1e-4)
    # Strike temp should be higher than mash temp
    assert result["temperature_f"] > 152.0


def test_calculate_strike_water_different_ratio():
    result = calculate_strike_water(
        grain_weight_lbs=10.0,
        mash_temp_f=150.0,
        grain_temp_f=70.0,
        water_to_grain_ratio=2.0,
    )
    
    assert math.isclose(result["volume_quarts"], 20.0, rel_tol=1e-4)


def test_calculate_strike_water_invalid_inputs():
    with pytest.raises(ValueError):
        calculate_strike_water(-10.0, 152.0, 68.0)


# Priming Sugar Calculator Tests


def test_calculate_priming_sugar_table_sugar():
    result = calculate_priming_sugar(
        volume_gal=5.0,
        carbonation_level=2.4,
        sugar_type="table",
    )
    
    assert "grams" in result
    assert "oz" in result
    assert result["grams"] > 0
    assert result["oz"] > 0


def test_calculate_priming_sugar_corn_sugar():
    result = calculate_priming_sugar(
        volume_gal=5.0,
        carbonation_level=2.4,
        sugar_type="corn",
    )
    
    # Corn sugar should require less than table sugar
    table_result = calculate_priming_sugar(5.0, 2.4, "table")
    assert result["grams"] < table_result["grams"]


def test_calculate_priming_sugar_invalid_type():
    with pytest.raises(ValueError):
        calculate_priming_sugar(5.0, 2.4, "invalid")


# Yeast Starter Calculator Tests


def test_calculate_yeast_starter_baseline():
    result = calculate_yeast_starter(
        og=1.050,
        volume_gal=5.0,
        yeast_age_months=2.0,
    )
    
    assert "cells_needed_billions" in result
    assert "packages" in result
    assert "starter_size_ml" in result
    assert result["cells_needed_billions"] > 0
    assert result["packages"] >= 1


def test_calculate_yeast_starter_fresh_yeast():
    result = calculate_yeast_starter(
        og=1.050,
        volume_gal=5.0,
        yeast_age_months=0.0,
    )
    
    # Fresh yeast should require fewer packages
    assert result["packages"] >= 1


def test_calculate_yeast_starter_custom_cell_count():
    result = calculate_yeast_starter(
        og=1.050,
        volume_gal=5.0,
        yeast_age_months=0.0,
        target_cell_count=200.0,
    )
    
    assert math.isclose(result["cells_needed_billions"], 200.0, rel_tol=1e-4)


# Dilution Calculator Tests


def test_calculate_dilution_baseline():
    result = calculate_dilution(
        current_og=1.060,
        current_volume_gal=5.0,
        target_og=1.050,
    )
    
    assert "water_to_add_gal" in result
    assert "final_volume_gal" in result
    assert result["water_to_add_gal"] > 0
    assert result["final_volume_gal"] > 5.0


def test_calculate_dilution_no_dilution_needed():
    result = calculate_dilution(
        current_og=1.050,
        current_volume_gal=5.0,
        target_og=1.060,
    )
    
    assert result["water_to_add_gal"] == 0.0
    assert result["final_volume_gal"] == 5.0


def test_calculate_dilution_gravity_conservation():
    # Test that gravity * volume is conserved
    current_og = 1.060
    current_volume = 5.0
    target_og = 1.050
    
    result = calculate_dilution(current_og, current_volume, target_og)
    
    current_points = (current_og - 1) * 1000
    target_points = (target_og - 1) * 1000
    
    # Points before = points after
    points_before = current_points * current_volume
    points_after = target_points * result["final_volume_gal"]
    
    assert math.isclose(points_before, points_after, rel_tol=1e-3)


# Carbonation Calculator Tests


def test_calculate_carbonation_baseline():
    result = calculate_carbonation(
        temp_f=38.0,
        co2_volumes=2.5,
    )
    
    assert "psi" in result
    assert "bar" in result
    assert result["psi"] >= 0
    assert result["bar"] >= 0


def test_calculate_carbonation_higher_temp():
    cold_result = calculate_carbonation(38.0, 2.5)
    warm_result = calculate_carbonation(68.0, 2.5)
    
    # Higher temp requires higher pressure for same CO2 volumes
    assert warm_result["psi"] > cold_result["psi"]


def test_calculate_carbonation_bar_conversion():
    result = calculate_carbonation(38.0, 2.5)
    
    # Verify PSI to bar conversion (1 PSI = 0.0689476 bar)
    assert math.isclose(result["bar"], result["psi"] * 0.0689476, rel_tol=1e-4)


# Water Chemistry Calculator Tests


def test_calculate_water_chemistry_baseline():
    water_profile = {
        "calcium": 50,
        "magnesium": 10,
        "sodium": 15,
        "chloride": 60,
        "sulfate": 120,
        "bicarbonate": 80,
    }
    
    result = calculate_water_chemistry(
        water_profile=water_profile,
        grain_bill_lbs=11.0,
        target_ph=5.4,
    )
    
    assert "residual_alkalinity" in result
    assert "estimated_ph" in result
    assert "ph_target" in result
    assert "ph_difference" in result
    
    # pH should be in reasonable brewing range
    assert 5.0 <= result["estimated_ph"] <= 6.0


def test_calculate_water_chemistry_missing_key():
    water_profile = {
        "calcium": 50,
        "magnesium": 10,
        # Missing bicarbonate
    }
    
    with pytest.raises(ValueError):
        calculate_water_chemistry(water_profile, 11.0, 5.4)


def test_calculate_water_chemistry_high_alkalinity():
    water_profile = {
        "calcium": 20,
        "magnesium": 5,
        "sodium": 15,
        "chloride": 60,
        "sulfate": 120,
        "bicarbonate": 200,  # High alkalinity
    }
    
    result = calculate_water_chemistry(water_profile, 11.0, 5.4)
    
    # High alkalinity should result in higher pH
    assert result["estimated_ph"] > 5.5
