import math

import pytest

from modules.brewing_calculations import (
    calculate_abv,
    calculate_ibu_tinseth,
    calculate_ingredient_cost,
    calculate_srm_morey,
    scale_recipe_by_volume,
)


def test_calculate_abv_standard_reading():
    abv = calculate_abv(1.050, 1.010)
    assert math.isclose(abv, 5.25, rel_tol=1e-4)


def test_calculate_abv_invalid_gravity_order():
    with pytest.raises(ValueError):
        calculate_abv(1.010, 1.050)


def test_calculate_ibu_tinseth_baseline():
    ibu = calculate_ibu_tinseth(
        original_gravity=1.050,
        boil_volume_liters=20.0,
        hop_alpha_acid=12.0,
        hop_mass_grams=50.0,
        boil_time_minutes=60.0,
    )

    gravity_factor = 1.65 * math.pow(0.000125, 1.050 - 1)
    time_factor = (1 - math.exp(-0.04 * 60)) / 4.15
    expected = (50.0 * 0.12 * gravity_factor * time_factor * 1000) / 20.0

    assert math.isclose(ibu, expected, rel_tol=1e-5)


def test_calculate_ibu_tinseth_zero_inputs():
    assert calculate_ibu_tinseth(1.050, 20.0, 12.0, 0.0, 60.0) == 0.0
    assert calculate_ibu_tinseth(1.050, 20.0, 0.0, 50.0, 60.0) == 0.0
    assert calculate_ibu_tinseth(1.050, 20.0, 12.0, 50.0, 0.0) == 0.0


def test_calculate_ibu_tinseth_negative_volume():
    with pytest.raises(ValueError):
        calculate_ibu_tinseth(1.050, -1.0, 12.0, 50.0, 60.0)


def test_calculate_srm_morey():
    grain_bill = [
        (10.0, 10.0),
        (1.0, 120.0),
    ]
    srm = calculate_srm_morey(grain_bill, batch_volume_gallons=5.0)

    mcu = ((10.0 * 10.0) + (1.0 * 120.0)) / 5.0
    expected = 1.4922 * math.pow(mcu, 0.6859)

    assert math.isclose(srm, expected, rel_tol=1e-5)


def test_calculate_srm_morey_handles_zero_grain():
    assert calculate_srm_morey([], batch_volume_gallons=5.0) == 0.0


def test_calculate_srm_morey_negative_weight():
    with pytest.raises(ValueError):
        calculate_srm_morey([(-1.0, 10.0)], batch_volume_gallons=5.0)


def test_scale_recipe_by_volume():
    ingredients = {
        "pale malt": 10.0,
        "crystal malt": 0.5,
        "cascade hops": 1.0,
    }
    scaled = scale_recipe_by_volume(ingredients, 5.0, 20.0)
    assert scaled == {
        "pale malt": 40.0,
        "crystal malt": 2.0,
        "cascade hops": 4.0,
    }


def test_scale_recipe_by_volume_invalid_volume():
    with pytest.raises(ValueError):
        scale_recipe_by_volume({"water": 1.0}, 0, 10.0)


def test_calculate_ingredient_cost():
    ingredients = [
        ("pale malt", 10.0, 1.5),
        ("crystal malt", 0.5, 2.0),
        ("yeast", 1.0, 4.0),
    ]
    total = calculate_ingredient_cost(ingredients)
    assert math.isclose(total, (10.0 * 1.5) + (0.5 * 2.0) + (1.0 * 4.0))


def test_calculate_ingredient_cost_negative_values():
    with pytest.raises(ValueError):
        calculate_ingredient_cost([("pale malt", -1.0, 1.0)])
