import math

import pytest

from modules.brewing_calculations import (
    calculate_abv,
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
