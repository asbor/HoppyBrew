"""
Utility functions for common brewing calculations.

The formulas implemented here follow industry-standard references:

- Alcohol by Volume (ABV): American Society of Brewing Chemists (ASBC)
  hydrometer-based calculation.
- International Bitterness Units (IBU): Tinseth utilization model
  (Tinseth, G. 1997).
- Standard Reference Method (SRM) color: Morey equation derived from
  Malt Color Units (MCU).
"""

from __future__ import annotations

import math
from typing import Iterable, Mapping, Sequence, Tuple, Union


Number = Union[int, float]

__all__ = [
    "calculate_abv",
    "calculate_ibu_tinseth",
    "calculate_srm_morey",
    "scale_recipe_by_volume",
    "calculate_ingredient_cost",
]


def calculate_abv(original_gravity: Number, final_gravity: Number) -> float:
    """
    Calculate Alcohol by Volume (ABV) from original and final gravity readings.

    The equation implemented is the ASBC hydrometer formula commonly used in
    North American breweries:

        ABV = (OG - FG) * 131.25

    where OG and FG are the specific gravity readings (dimensionless).

    Args:
        original_gravity: Original gravity measurement (e.g., 1.050).
        final_gravity: Final gravity measurement after fermentation (e.g., 1.012).

    Returns:
        The calculated ABV as a percentage (e.g., 5.0 for 5% ABV).

    Raises:
        ValueError: If gravity readings are non-positive or OG <= FG.
    """
    try:
        og = float(original_gravity)
        fg = float(final_gravity)
    except (TypeError, ValueError) as exc:
        raise ValueError("Gravity readings must be numeric.") from exc

    if og <= 0 or fg <= 0:
        raise ValueError("Gravity readings must be positive values.")
    if og <= fg:
        raise ValueError("Original gravity must be greater than final gravity.")

    return (og - fg) * 131.25


def calculate_ibu_tinseth(
    original_gravity: Number,
    boil_volume_liters: Number,
    hop_alpha_acid: Number,
    hop_mass_grams: Number,
    boil_time_minutes: Number,
) -> float:
    """
    Estimate International Bitterness Units (IBU) using the Tinseth formula.

    Tinseth's model (Tinseth, G. 1997) calculates utilization (U) from boil
    time and wort gravity, then determines IBU as the concentration of iso-alpha
    acids:

        U = 1.65 * 0.000125 ** (OG - 1) * (1 - e^{-0.04 * t}) / 4.15
        IBU = (mass_g * alpha_acid_fraction * U * 1000) / volume_l

    Args:
        original_gravity: Pre-boil specific gravity of the wort (dimensionless).
        boil_volume_liters: Volume of wort in the kettle (liters).
        hop_alpha_acid: Alpha acid percentage of the hop addition (e.g., 12.0 for 12% AA).
        hop_mass_grams: Mass of the hop addition (grams).
        boil_time_minutes: Duration the hops are boiled (minutes).

    Returns:
        Estimated IBU contribution from the hop addition.

    Raises:
        ValueError: If any numeric input is invalid or non-positive where forbidden.
    """
    try:
        og = float(original_gravity)
        volume_l = float(boil_volume_liters)
        alpha_acid_percent = float(hop_alpha_acid)
        mass_g = float(hop_mass_grams)
        boil_minutes = float(boil_time_minutes)
    except (TypeError, ValueError) as exc:
        raise ValueError("Inputs must be numeric values.") from exc

    if og <= 0:
        raise ValueError("Original gravity must be positive.")
    if volume_l <= 0:
        raise ValueError("Boil volume must be positive.")
    if alpha_acid_percent < 0:
        raise ValueError("Alpha acid percentage cannot be negative.")
    if mass_g < 0:
        raise ValueError("Hop mass cannot be negative.")
    if boil_minutes < 0:
        raise ValueError("Boil time cannot be negative.")

    if mass_g == 0 or alpha_acid_percent == 0 or boil_minutes == 0:
        return 0.0

    gravity_factor = 1.65 * 0.000125 ** (og - 1)
    time_factor = (1 - math.exp(-0.04 * boil_minutes)) / 4.15
    utilization = gravity_factor * time_factor
    alpha_fraction = alpha_acid_percent / 100.0

    ibu = (mass_g * alpha_fraction * utilization * 1000) / volume_l
    return max(ibu, 0.0)


def calculate_srm_morey(
    grain_bill: Sequence[Tuple[Number, Number]],
    batch_volume_gallons: Number,
) -> float:
    """
    Estimate finished beer color in SRM using the Morey equation.

    The Morey equation refines Malt Color Units (MCU) for richer colors:

        MCU = sum(weight_lb * lovibond) / volume_gal
        SRM = 1.4922 * MCU ** 0.6859

    Args:
        grain_bill: Iterable of (weight_pounds, lovibond) tuples for each grist component.
        batch_volume_gallons: Fermentor batch size in gallons.

    Returns:
        Estimated SRM value. Returns 0.0 when the grain bill is empty.

    Raises:
        ValueError: If batch volume is non-positive or any weight/color is negative.
    """
    try:
        volume_gal = float(batch_volume_gallons)
    except (TypeError, ValueError) as exc:
        raise ValueError("Batch volume must be numeric.") from exc

    if volume_gal <= 0:
        raise ValueError("Batch volume must be greater than zero.")

    if not grain_bill:
        return 0.0

    mcu_total = 0.0
    for weight_lb, lovibond in grain_bill:
        try:
            weight = float(weight_lb)
            color = float(lovibond)
        except (TypeError, ValueError) as exc:
            raise ValueError("Grain bill entries must be numeric.") from exc
        if weight < 0 or color < 0:
            raise ValueError("Grain weight and color must be non-negative.")
        mcu_total += weight * color

    if mcu_total == 0:
        return 0.0

    mcu = mcu_total / volume_gal
    return 1.4922 * (mcu ** 0.6859)


def scale_recipe_by_volume(
    ingredients: Mapping[str, Number],
    original_batch_volume: Number,
    target_batch_volume: Number,
) -> Mapping[str, float]:
    """
    Scale ingredient quantities to match a different batch volume.

    This assumes linear scaling, which is the accepted approach for recipe
    adjustments within normal production ranges.

    Args:
        ingredients: Mapping of ingredient names to their quantities in the original recipe.
        original_batch_volume: Volume the base recipe is formulated for.
        target_batch_volume: Desired output volume.

    Returns:
        A new dict with scaled ingredient quantities.

    Raises:
        ValueError: If batch volumes are non-positive.
    """
    try:
        original_volume = float(original_batch_volume)
        target_volume = float(target_batch_volume)
    except (TypeError, ValueError) as exc:
        raise ValueError("Batch volumes must be numeric.") from exc

    if original_volume <= 0 or target_volume <= 0:
        raise ValueError("Batch volumes must be positive.")

    scale_factor = target_volume / original_volume
    return {
        name: float(amount) * scale_factor
        for name, amount in ingredients.items()
    }


def calculate_ingredient_cost(
    ingredients: Iterable[Tuple[str, Number, Number]]
) -> float:
    """
    Compute total ingredient cost from individual quantity and unit price data.

    Args:
        ingredients: Iterable of tuples containing (ingredient_name, quantity, unit_cost).
            Quantities and unit costs should share compatible units (e.g., pounds and
            cost per pound, liters and cost per liter).

    Returns:
        Total ingredient cost as a float.

    Raises:
        ValueError: If quantity or unit cost values are negative or non-numeric.
    """
    total_cost = 0.0
    for name, quantity, unit_cost in ingredients:
        try:
            qty = float(quantity)
            cost = float(unit_cost)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Ingredient '{name}' must have numeric quantity and unit cost."
            ) from exc
        if qty < 0 or cost < 0:
            raise ValueError(
                f"Ingredient '{name}' cannot have negative quantity or cost."
            )
        total_cost += qty * cost
    return total_cost
