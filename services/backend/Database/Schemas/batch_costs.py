# services/backend/Database/Schemas/batch_costs.py

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class BatchCostBase(BaseModel):
    """Base schema for batch cost tracking."""

    # Ingredient costs
    fermentables_cost: float = Field(default=0.0, ge=0, description="Cost of fermentables")
    hops_cost: float = Field(default=0.0, ge=0, description="Cost of hops")
    yeasts_cost: float = Field(default=0.0, ge=0, description="Cost of yeasts")
    miscs_cost: float = Field(default=0.0, ge=0, description="Cost of miscellaneous ingredients")

    # Utility costs
    electricity_cost: float = Field(default=0.0, ge=0, description="Electricity cost")
    water_cost: float = Field(default=0.0, ge=0, description="Water cost")
    gas_cost: float = Field(default=0.0, ge=0, description="Gas cost")

    # Other costs
    labor_cost: float = Field(default=0.0, ge=0, description="Labor cost")
    packaging_cost: float = Field(default=0.0, ge=0, description="Packaging cost")
    other_cost: float = Field(default=0.0, ge=0, description="Other miscellaneous costs")

    # Sales information
    expected_yield_volume: Optional[float] = Field(None, gt=0, description="Expected yield volume in liters")
    selling_price_per_unit: Optional[float] = Field(None, ge=0, description="Selling price per unit")
    unit_type: str = Field(default="pint", description="Unit type (pint, liter, bottle, etc.)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fermentables_cost": 25.50,
                "hops_cost": 15.00,
                "yeasts_cost": 8.50,
                "miscs_cost": 5.00,
                "electricity_cost": 3.50,
                "water_cost": 2.00,
                "gas_cost": 4.00,
                "labor_cost": 0.0,
                "packaging_cost": 10.00,
                "other_cost": 2.00,
                "expected_yield_volume": 20.0,
                "selling_price_per_unit": 5.00,
                "unit_type": "pint",
            }
        }
    )


class BatchCostCreate(BatchCostBase):
    """Schema for creating a new batch cost record."""

    batch_id: int = Field(..., description="ID of the associated batch")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "batch_id": 1,
                "fermentables_cost": 25.50,
                "hops_cost": 15.00,
                "yeasts_cost": 8.50,
                "miscs_cost": 5.00,
                "electricity_cost": 3.50,
                "water_cost": 2.00,
                "gas_cost": 4.00,
                "labor_cost": 0.0,
                "packaging_cost": 10.00,
                "other_cost": 2.00,
                "expected_yield_volume": 20.0,
                "selling_price_per_unit": 5.00,
                "unit_type": "pint",
            }
        }
    )


class BatchCostUpdate(BaseModel):
    """Schema for updating batch cost record."""

    # Ingredient costs
    fermentables_cost: Optional[float] = Field(None, ge=0)
    hops_cost: Optional[float] = Field(None, ge=0)
    yeasts_cost: Optional[float] = Field(None, ge=0)
    miscs_cost: Optional[float] = Field(None, ge=0)

    # Utility costs
    electricity_cost: Optional[float] = Field(None, ge=0)
    water_cost: Optional[float] = Field(None, ge=0)
    gas_cost: Optional[float] = Field(None, ge=0)

    # Other costs
    labor_cost: Optional[float] = Field(None, ge=0)
    packaging_cost: Optional[float] = Field(None, ge=0)
    other_cost: Optional[float] = Field(None, ge=0)

    # Sales information
    expected_yield_volume: Optional[float] = Field(None, gt=0)
    selling_price_per_unit: Optional[float] = Field(None, ge=0)
    unit_type: Optional[str] = None


class BatchCost(BatchCostBase):
    """Schema for batch cost with all fields."""

    id: int
    batch_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "batch_id": 1,
                "fermentables_cost": 25.50,
                "hops_cost": 15.00,
                "yeasts_cost": 8.50,
                "miscs_cost": 5.00,
                "electricity_cost": 3.50,
                "water_cost": 2.00,
                "gas_cost": 4.00,
                "labor_cost": 0.0,
                "packaging_cost": 10.00,
                "other_cost": 2.00,
                "expected_yield_volume": 20.0,
                "selling_price_per_unit": 5.00,
                "unit_type": "pint",
                "created_at": "2024-03-21T08:00:00Z",
                "updated_at": "2024-03-22T10:30:00Z",
            }
        },
    )


class CostSummary(BaseModel):
    """Summary of all costs for a batch."""

    total_ingredient_cost: float = Field(..., description="Total cost of all ingredients")
    total_utility_cost: float = Field(..., description="Total cost of utilities")
    total_other_cost: float = Field(..., description="Total of other costs")
    total_cost: float = Field(..., description="Grand total of all costs")
    cost_per_unit: Optional[float] = Field(None, description="Cost per unit (pint/liter)")
    profit_margin: Optional[float] = Field(None, description="Profit margin percentage")
    profit_per_unit: Optional[float] = Field(None, description="Profit per unit")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_ingredient_cost": 54.00,
                "total_utility_cost": 9.50,
                "total_other_cost": 12.00,
                "total_cost": 75.50,
                "cost_per_unit": 1.89,
                "profit_margin": 62.2,
                "profit_per_unit": 3.11,
            }
        }
    )
