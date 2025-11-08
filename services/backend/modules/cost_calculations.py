"""
Cost calculation utilities for brewing batches.
"""

from typing import Optional, Dict, Any


def calculate_ingredient_costs(
    fermentables: list,
    hops: list,
    yeasts: list,
    miscs: list,
) -> Dict[str, float]:
    """
    Calculate total ingredient costs from batch ingredients.

    Args:
        fermentables: List of fermentable ingredients with amount and cost_per_unit
        hops: List of hop ingredients with amount and cost_per_unit
        yeasts: List of yeast ingredients with amount and cost_per_unit
        miscs: List of miscellaneous ingredients with amount and cost_per_unit

    Returns:
        Dictionary with individual and total ingredient costs
    """
    fermentables_cost = sum(
        (item.get("amount", 0) or 0) * (item.get("cost_per_unit", 0) or 0)
        for item in fermentables
    )
    hops_cost = sum(
        (item.get("amount", 0) or 0) * (item.get("cost_per_unit", 0) or 0)
        for item in hops
    )
    yeasts_cost = sum(
        (item.get("amount", 0) or 0) * (item.get("cost_per_unit", 0) or 0)
        for item in yeasts
    )
    miscs_cost = sum(
        (item.get("amount", 0) or 0) * (item.get("cost_per_unit", 0) or 0)
        for item in miscs
    )

    return {
        "fermentables_cost": round(fermentables_cost, 2),
        "hops_cost": round(hops_cost, 2),
        "yeasts_cost": round(yeasts_cost, 2),
        "miscs_cost": round(miscs_cost, 2),
        "total_ingredient_cost": round(
            fermentables_cost + hops_cost + yeasts_cost + miscs_cost, 2
        ),
    }


def calculate_utility_costs(
    brew_time_hours: float = 5.0,
    electricity_rate_per_kwh: float = 0.12,
    water_volume_liters: float = 30.0,
    water_rate_per_liter: float = 0.001,
    gas_usage_cubic_meters: float = 0.0,
    gas_rate_per_cubic_meter: float = 0.50,
    heating_power_kw: float = 3.5,
) -> Dict[str, float]:
    """
    Calculate utility costs for a brewing session.

    Args:
        brew_time_hours: Total brewing time in hours (default: 5.0)
        electricity_rate_per_kwh: Cost per kilowatt-hour (default: 0.12 USD)
        water_volume_liters: Total water used in liters (default: 30.0)
        water_rate_per_liter: Cost per liter of water (default: 0.001 USD)
        gas_usage_cubic_meters: Gas usage in cubic meters (default: 0.0)
        gas_rate_per_cubic_meter: Cost per cubic meter of gas (default: 0.50 USD)
        heating_power_kw: Power consumption of heating element in kW (default: 3.5)

    Returns:
        Dictionary with utility costs breakdown
    """
    # Calculate electricity cost (heating element + other equipment)
    # Heating element runs ~70% of brew time
    heating_cost = brew_time_hours * 0.7 * heating_power_kw * electricity_rate_per_kwh
    # Other equipment (pumps, controllers) ~0.2 kW continuous
    equipment_cost = brew_time_hours * 0.2 * electricity_rate_per_kwh
    electricity_cost = heating_cost + equipment_cost

    # Calculate water cost
    water_cost = water_volume_liters * water_rate_per_liter

    # Calculate gas cost
    gas_cost = gas_usage_cubic_meters * gas_rate_per_cubic_meter

    return {
        "electricity_cost": round(electricity_cost, 2),
        "water_cost": round(water_cost, 2),
        "gas_cost": round(gas_cost, 2),
        "total_utility_cost": round(electricity_cost + water_cost + gas_cost, 2),
    }


def calculate_cost_per_unit(
    total_cost: float,
    yield_volume_liters: float,
    unit_type: str = "pint",
) -> float:
    """
    Calculate cost per serving unit.

    Args:
        total_cost: Total cost of the batch
        yield_volume_liters: Expected yield volume in liters
        unit_type: Type of unit ('pint', 'liter', 'bottle', 'can')

    Returns:
        Cost per unit
    """
    if yield_volume_liters <= 0:
        return 0.0

    # Conversion factors to liters
    unit_conversions = {
        "pint": 0.568,  # UK pint
        "us_pint": 0.473,  # US pint
        "liter": 1.0,
        "bottle": 0.33,  # Standard 330ml bottle
        "can": 0.355,  # Standard 355ml can (12 oz)
        "half_liter": 0.5,
    }

    unit_volume = unit_conversions.get(unit_type.lower(), 0.568)  # Default to UK pint
    units_per_batch = yield_volume_liters / unit_volume

    if units_per_batch <= 0:
        return 0.0

    return round(total_cost / units_per_batch, 2)


def calculate_profit_margin(
    cost_per_unit: float,
    selling_price_per_unit: float,
) -> Dict[str, float]:
    """
    Calculate profit margin and profit per unit.

    Args:
        cost_per_unit: Cost per unit
        selling_price_per_unit: Selling price per unit

    Returns:
        Dictionary with profit margin percentage and profit per unit
    """
    if selling_price_per_unit <= 0:
        return {
            "profit_per_unit": 0.0,
            "profit_margin_percentage": 0.0,
        }

    profit_per_unit = selling_price_per_unit - cost_per_unit
    profit_margin_percentage = (profit_per_unit / selling_price_per_unit) * 100

    return {
        "profit_per_unit": round(profit_per_unit, 2),
        "profit_margin_percentage": round(profit_margin_percentage, 2),
    }


def calculate_batch_cost_summary(
    ingredient_costs: Dict[str, float],
    utility_costs: Dict[str, float],
    labor_cost: float = 0.0,
    packaging_cost: float = 0.0,
    other_cost: float = 0.0,
    yield_volume_liters: Optional[float] = None,
    selling_price_per_unit: Optional[float] = None,
    unit_type: str = "pint",
) -> Dict[str, Any]:
    """
    Calculate comprehensive cost summary for a batch.

    Args:
        ingredient_costs: Dictionary with ingredient cost breakdown
        utility_costs: Dictionary with utility cost breakdown
        labor_cost: Cost of labor (default: 0.0)
        packaging_cost: Cost of packaging materials (default: 0.0)
        other_cost: Other miscellaneous costs (default: 0.0)
        yield_volume_liters: Expected yield volume in liters (optional)
        selling_price_per_unit: Selling price per unit (optional)
        unit_type: Type of unit for calculations (default: 'pint')

    Returns:
        Comprehensive cost summary dictionary
    """
    total_ingredient_cost = ingredient_costs.get("total_ingredient_cost", 0.0)
    total_utility_cost = utility_costs.get("total_utility_cost", 0.0)
    total_other_cost = labor_cost + packaging_cost + other_cost

    total_cost = total_ingredient_cost + total_utility_cost + total_other_cost

    summary = {
        "total_ingredient_cost": round(total_ingredient_cost, 2),
        "total_utility_cost": round(total_utility_cost, 2),
        "total_other_cost": round(total_other_cost, 2),
        "total_cost": round(total_cost, 2),
        "cost_per_unit": None,
        "profit_margin": None,
        "profit_per_unit": None,
    }

    # Calculate cost per unit if yield is provided
    if yield_volume_liters and yield_volume_liters > 0:
        cost_per_unit = calculate_cost_per_unit(
            total_cost, yield_volume_liters, unit_type
        )
        summary["cost_per_unit"] = cost_per_unit

        # Calculate profit margin if selling price is provided
        if selling_price_per_unit and selling_price_per_unit > 0:
            profit_info = calculate_profit_margin(cost_per_unit, selling_price_per_unit)
            summary["profit_margin"] = profit_info["profit_margin_percentage"]
            summary["profit_per_unit"] = profit_info["profit_per_unit"]

    return summary
