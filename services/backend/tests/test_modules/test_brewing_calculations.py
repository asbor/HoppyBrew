import math

import pytest

from modules.brewing_calculations import (
    calculate_abv,
    calculate_attenuation,
    calculate_ibu_tinseth,
    calculate_srm_morey,
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


def test_calculate_attenuation_standard():
    """Test standard attenuation calculation"""
    # OG = 1.050, FG = 1.010
    # Attenuation = ((1.050 - 1.010) / (1.050 - 1.0)) * 100 = 80%
    attenuation = calculate_attenuation(1.050, 1.010)
    assert math.isclose(attenuation, 80.0, rel_tol=1e-3)


def test_calculate_attenuation_high():
    """Test high attenuation"""
    # OG = 1.048, FG = 1.008
    attenuation = calculate_attenuation(1.048, 1.008)
    assert math.isclose(attenuation, 83.33, rel_tol=1e-2)


def test_calculate_attenuation_partial():
    """Test partial attenuation (mid-fermentation)"""
    # OG = 1.048, current = 1.032
    attenuation = calculate_attenuation(1.048, 1.032)
    assert math.isclose(attenuation, 33.33, rel_tol=1e-2)


def test_calculate_attenuation_invalid_gravity_order():
    """Test that FG > OG raises error"""
    with pytest.raises(ValueError):
        calculate_attenuation(1.010, 1.050)


def test_calculate_attenuation_same_gravity():
    """Test that OG == FG raises error"""
    with pytest.raises(ValueError):
        calculate_attenuation(1.050, 1.050)


def test_calculate_attenuation_og_too_low():
    """Test that OG <= 1.0 raises error"""
    with pytest.raises(ValueError):
        calculate_attenuation(1.0, 0.998)


def test_calculate_attenuation_negative_values():
    """Test that negative values raise error"""
    with pytest.raises(ValueError):
        calculate_attenuation(-1.050, 1.010)


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
