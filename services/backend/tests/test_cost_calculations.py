"""
Tests for cost calculation utilities.
"""

import pytest
from modules.cost_calculations import (
    calculate_ingredient_costs,
    calculate_utility_costs,
    calculate_cost_per_unit,
    calculate_profit_margin,
    calculate_batch_cost_summary,
)


class TestIngredientCostCalculation:
    """Tests for ingredient cost calculations."""

    def test_calculate_ingredient_costs_all_types(self):
        """Test calculating costs with all ingredient types."""
        fermentables = [
            {"amount": 5.0, "cost_per_unit": 2.5},
            {"amount": 2.0, "cost_per_unit": 3.0},
        ]
        hops = [
            {"amount": 0.1, "cost_per_unit": 50.0},
            {"amount": 0.05, "cost_per_unit": 60.0},
        ]
        yeasts = [{"amount": 1.0, "cost_per_unit": 8.5}]
        miscs = [{"amount": 0.5, "cost_per_unit": 10.0}]

        result = calculate_ingredient_costs(fermentables, hops, yeasts, miscs)

        assert result["fermentables_cost"] == 18.5  # (5*2.5 + 2*3.0)
        assert result["hops_cost"] == 8.0  # (0.1*50 + 0.05*60)
        assert result["yeasts_cost"] == 8.5  # (1*8.5)
        assert result["miscs_cost"] == 5.0  # (0.5*10)
        assert result["total_ingredient_cost"] == 40.0

    def test_calculate_ingredient_costs_with_none_values(self):
        """Test calculating costs when some values are None."""
        fermentables = [
            {"amount": 5.0, "cost_per_unit": None},
            {"amount": None, "cost_per_unit": 3.0},
        ]
        hops = []
        yeasts = []
        miscs = []

        result = calculate_ingredient_costs(fermentables, hops, yeasts, miscs)

        assert result["fermentables_cost"] == 0.0
        assert result["hops_cost"] == 0.0
        assert result["yeasts_cost"] == 0.0
        assert result["miscs_cost"] == 0.0
        assert result["total_ingredient_cost"] == 0.0

    def test_calculate_ingredient_costs_empty_lists(self):
        """Test calculating costs with empty ingredient lists."""
        result = calculate_ingredient_costs([], [], [], [])

        assert result["fermentables_cost"] == 0.0
        assert result["hops_cost"] == 0.0
        assert result["yeasts_cost"] == 0.0
        assert result["miscs_cost"] == 0.0
        assert result["total_ingredient_cost"] == 0.0


class TestUtilityCostCalculation:
    """Tests for utility cost calculations."""

    def test_calculate_utility_costs_defaults(self):
        """Test utility cost calculation with default values."""
        result = calculate_utility_costs()

        assert result["electricity_cost"] > 0
        assert result["water_cost"] > 0
        assert result["gas_cost"] == 0.0  # Default gas usage is 0
        assert result["total_utility_cost"] > 0

    def test_calculate_utility_costs_custom_values(self):
        """Test utility cost calculation with custom values."""
        result = calculate_utility_costs(
            brew_time_hours=6.0,
            electricity_rate_per_kwh=0.15,
            water_volume_liters=40.0,
            water_rate_per_liter=0.002,
            gas_usage_cubic_meters=2.0,
            gas_rate_per_cubic_meter=0.60,
            heating_power_kw=4.0,
        )

        # Electricity: (6 * 0.7 * 4.0 * 0.15) + (6 * 0.2 * 0.15) = 2.52 + 0.18 = 2.7
        assert result["electricity_cost"] == 2.7
        # Water: 40.0 * 0.002 = 0.08
        assert result["water_cost"] == 0.08
        # Gas: 2.0 * 0.60 = 1.2
        assert result["gas_cost"] == 1.2
        assert result["total_utility_cost"] == 3.98

    def test_calculate_utility_costs_no_gas(self):
        """Test utility cost calculation with no gas usage."""
        result = calculate_utility_costs(
            brew_time_hours=5.0,
            electricity_rate_per_kwh=0.12,
            water_volume_liters=30.0,
            water_rate_per_liter=0.001,
            gas_usage_cubic_meters=0.0,
            gas_rate_per_cubic_meter=0.50,
        )

        assert result["gas_cost"] == 0.0
        assert result["total_utility_cost"] > 0


class TestCostPerUnit:
    """Tests for cost per unit calculations."""

    def test_calculate_cost_per_pint(self):
        """Test cost per pint calculation."""
        cost = calculate_cost_per_unit(
            total_cost=75.50, yield_volume_liters=20.0, unit_type="pint"
        )
        # 20 liters / 0.568 (pint size) = 35.21 pints
        # 75.50 / 35.21 = 2.14 per pint
        assert cost == pytest.approx(2.14, rel=0.01)

    def test_calculate_cost_per_liter(self):
        """Test cost per liter calculation."""
        cost = calculate_cost_per_unit(
            total_cost=75.50, yield_volume_liters=20.0, unit_type="liter"
        )
        # 75.50 / 20 = 3.775 rounds to 3.77
        assert cost == 3.77

    def test_calculate_cost_per_bottle(self):
        """Test cost per bottle (330ml) calculation."""
        cost = calculate_cost_per_unit(
            total_cost=75.50, yield_volume_liters=20.0, unit_type="bottle"
        )
        # 20 liters / 0.33 = 60.61 bottles
        # 75.50 / 60.61 = 1.25 per bottle
        assert cost == pytest.approx(1.25, rel=0.01)

    def test_calculate_cost_per_unit_zero_volume(self):
        """Test cost per unit with zero volume."""
        cost = calculate_cost_per_unit(
            total_cost=75.50, yield_volume_liters=0.0, unit_type="pint"
        )
        assert cost == 0.0

    def test_calculate_cost_per_unit_invalid_type(self):
        """Test cost per unit with invalid unit type defaults to pint."""
        cost = calculate_cost_per_unit(
            total_cost=75.50, yield_volume_liters=20.0, unit_type="invalid"
        )
        # Should default to pint
        assert cost == pytest.approx(2.14, rel=0.01)


class TestProfitMargin:
    """Tests for profit margin calculations."""

    def test_calculate_profit_margin_positive(self):
        """Test profit margin with positive profit."""
        result = calculate_profit_margin(
            cost_per_unit=2.14, selling_price_per_unit=5.00
        )
        # Profit per unit: 5.00 - 2.14 = 2.86
        # Margin: (2.86 / 5.00) * 100 = 57.2%
        assert result["profit_per_unit"] == 2.86
        assert result["profit_margin_percentage"] == 57.2

    def test_calculate_profit_margin_break_even(self):
        """Test profit margin at break even."""
        result = calculate_profit_margin(cost_per_unit=5.00, selling_price_per_unit=5.00)
        assert result["profit_per_unit"] == 0.0
        assert result["profit_margin_percentage"] == 0.0

    def test_calculate_profit_margin_loss(self):
        """Test profit margin with a loss."""
        result = calculate_profit_margin(cost_per_unit=6.00, selling_price_per_unit=5.00)
        # Profit per unit: 5.00 - 6.00 = -1.00
        # Margin: (-1.00 / 5.00) * 100 = -20%
        assert result["profit_per_unit"] == -1.00
        assert result["profit_margin_percentage"] == -20.0

    def test_calculate_profit_margin_zero_selling_price(self):
        """Test profit margin with zero selling price."""
        result = calculate_profit_margin(cost_per_unit=5.00, selling_price_per_unit=0.0)
        assert result["profit_per_unit"] == 0.0
        assert result["profit_margin_percentage"] == 0.0


class TestBatchCostSummary:
    """Tests for batch cost summary calculations."""

    def test_batch_cost_summary_complete(self):
        """Test complete batch cost summary with all parameters."""
        ingredient_costs = {"total_ingredient_cost": 54.0}
        utility_costs = {"total_utility_cost": 9.5}

        result = calculate_batch_cost_summary(
            ingredient_costs=ingredient_costs,
            utility_costs=utility_costs,
            labor_cost=0.0,
            packaging_cost=10.0,
            other_cost=2.0,
            yield_volume_liters=20.0,
            selling_price_per_unit=5.00,
            unit_type="pint",
        )

        assert result["total_ingredient_cost"] == 54.0
        assert result["total_utility_cost"] == 9.5
        assert result["total_other_cost"] == 12.0
        assert result["total_cost"] == 75.5
        assert result["cost_per_unit"] == pytest.approx(2.14, rel=0.01)
        assert result["profit_per_unit"] == pytest.approx(2.86, rel=0.01)
        assert result["profit_margin"] == pytest.approx(57.2, rel=0.1)

    def test_batch_cost_summary_without_yield(self):
        """Test batch cost summary without yield volume."""
        ingredient_costs = {"total_ingredient_cost": 54.0}
        utility_costs = {"total_utility_cost": 9.5}

        result = calculate_batch_cost_summary(
            ingredient_costs=ingredient_costs,
            utility_costs=utility_costs,
            labor_cost=0.0,
            packaging_cost=10.0,
            other_cost=2.0,
        )

        assert result["total_cost"] == 75.5
        assert result["cost_per_unit"] is None
        assert result["profit_per_unit"] is None
        assert result["profit_margin"] is None

    def test_batch_cost_summary_without_selling_price(self):
        """Test batch cost summary without selling price."""
        ingredient_costs = {"total_ingredient_cost": 54.0}
        utility_costs = {"total_utility_cost": 9.5}

        result = calculate_batch_cost_summary(
            ingredient_costs=ingredient_costs,
            utility_costs=utility_costs,
            labor_cost=0.0,
            packaging_cost=10.0,
            other_cost=2.0,
            yield_volume_liters=20.0,
            unit_type="pint",
        )

        assert result["total_cost"] == 75.5
        assert result["cost_per_unit"] == pytest.approx(2.14, rel=0.01)
        assert result["profit_per_unit"] is None
        assert result["profit_margin"] is None
