"""
Brewing calculation utilities.

This module implements a minimal set of formulas that are useful when
estimating beer characteristics during recipe design.  Each function
performs light validation and raises ValueError when the provided inputs
are outside of reasonable brewing ranges.
"""

from __future__ import annotations

import math
from typing import Union


Number = Union[int, float]

__all__ = [
    "calculate_abv",
    "calculate_ibu_tinseth",
    "calculate_srm_morey",
]


def _coerce_positive(value: Number, name: str, allow_zero: bool = False) -> float:
    """Convert a numeric input to float and validate positivity."""
    try:
        numeric_value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric.") from exc

    if allow_zero:
        if numeric_value < 0:
            raise ValueError(f"{name} cannot be negative.")
    else:
        if numeric_value <= 0:
            raise ValueError(f"{name} must be greater than zero.")

    return numeric_value


def calculate_abv(original_gravity: Number, final_gravity: Number) -> float:
    """
    Calculate Alcohol by Volume (ABV) from original and final gravity readings.

    Formula: ABV = (OG - FG) * 131.25
    """
    og = _coerce_positive(original_gravity, "original_gravity")
    fg = _coerce_positive(final_gravity, "final_gravity")

    if og <= fg:
        raise ValueError("original_gravity must be greater than final_gravity.")

    return (og - fg) * 131.25


def calculate_ibu_tinseth(
    alpha_acid: Number,
    weight_oz: Number,
    boil_time_min: Number,
    batch_size_gal: Number,
    gravity: Number,
) -> float:
    """
    Estimate International Bitterness Units (IBU) using the Tinseth model.

    Args:
        alpha_acid: Hop alpha acid percentage (e.g., 12.0 for 12% AA).
        weight_oz: Hop weight in ounces.
        boil_time_min: Boil time for the hop addition in minutes.
        batch_size_gal: Batch size in gallons.
        gravity: Specific gravity of the wort during the boil.
    """
    aa_percent = _coerce_positive(alpha_acid, "alpha_acid", allow_zero=True)
    hop_weight = _coerce_positive(weight_oz, "weight_oz", allow_zero=True)
    boil_minutes = _coerce_positive(boil_time_min, "boil_time_min", allow_zero=True)
    batch_volume = _coerce_positive(batch_size_gal, "batch_size_gal")
    wort_gravity = _coerce_positive(gravity, "gravity")

    if aa_percent == 0 or hop_weight == 0 or boil_minutes == 0:
        return 0.0

    gravity_factor = 1.65 * math.pow(0.000125, wort_gravity - 1.0)
    time_factor = (1 - math.exp(-0.04 * boil_minutes)) / 4.15
    utilization = gravity_factor * time_factor
    alpha_fraction = aa_percent / 100.0

    # 7490 converts from ounces and gallons to milligrams per liter.
    ibu = (alpha_fraction * hop_weight * 7490 * utilization) / batch_volume
    return max(ibu, 0.0)


def calculate_srm_morey(
    grain_color: Number,
    grain_weight_lbs: Number,
    batch_size_gal: Number,
) -> float:
    """
    Estimate beer color using the Morey equation.

    Args:
        grain_color: Lovibond rating of the grain (or average for the grist).
        grain_weight_lbs: Total grain weight contributing to the color, in pounds.
        batch_size_gal: Batch size in gallons.
    """
    color = _coerce_positive(grain_color, "grain_color", allow_zero=True)
    grain_weight = _coerce_positive(grain_weight_lbs, "grain_weight_lbs", allow_zero=True)
    batch_volume = _coerce_positive(batch_size_gal, "batch_size_gal")

    if color == 0 or grain_weight == 0:
        return 0.0

    mcu = (grain_weight * color) / batch_volume
    return 1.4922 * math.pow(mcu, 0.6859)
