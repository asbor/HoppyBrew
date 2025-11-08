# services/backend/Database/Schemas/batch_costs.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class UtilityCostConfigBase(BaseModel):
    """Base schema for utility cost configuration"""

    name: str = Field(..., description="Name for this cost configuration (e.g., 'Home Brewery', 'Winter Rates')")
    electricity_rate_per_kwh: Optional[float] = Field(None, description="Cost per kilowatt-hour")
    water_rate_per_liter: Optional[float] = Field(None, description="Cost per liter of water")
    gas_rate_per_unit: Optional[float] = Field(None, description="Cost per gas unit")
    avg_electricity_kwh_per_batch: Optional[float] = Field(None, description="Average kWh consumed per batch")
    avg_water_liters_per_batch: Optional[float] = Field(None, description="Average liters of water per batch")
    avg_gas_units_per_batch: Optional[float] = Field(None, description="Average gas units per batch")
    currency: str = Field(default="USD", description="Currency code")
    notes: Optional[str] = Field(None, description="Additional notes")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Home Brewery - Summer 2024",
                "electricity_rate_per_kwh": 0.12,
                "water_rate_per_liter": 0.002,
                "gas_rate_per_unit": 0.85,
                "avg_electricity_kwh_per_batch": 8.5,
                "avg_water_liters_per_batch": 60.0,
                "avg_gas_units_per_batch": 0.0,
                "currency": "USD",
                "notes": "Summer rates with solar offset",
            }
        }
    )


class UtilityCostConfigCreate(UtilityCostConfigBase):
    """Schema for creating a utility cost configuration"""

    is_active: int = Field(default=1, description="1 for active, 0 for inactive")


class UtilityCostConfigUpdate(BaseModel):
    """Schema for updating a utility cost configuration"""

    name: Optional[str] = None
    electricity_rate_per_kwh: Optional[float] = None
    water_rate_per_liter: Optional[float] = None
    gas_rate_per_unit: Optional[float] = None
    avg_electricity_kwh_per_batch: Optional[float] = None
    avg_water_liters_per_batch: Optional[float] = None
    avg_gas_units_per_batch: Optional[float] = None
    currency: Optional[str] = None
    is_active: Optional[int] = None
    notes: Optional[str] = None


class UtilityCostConfig(UtilityCostConfigBase):
    """Schema for utility cost configuration response"""

    id: int
    is_active: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BatchCostBase(BaseModel):
    """Base schema for batch cost tracking"""

    # Ingredient costs
    fermentables_cost: float = Field(default=0.0, description="Total cost of fermentables")
    hops_cost: float = Field(default=0.0, description="Total cost of hops")
    yeasts_cost: float = Field(default=0.0, description="Total cost of yeasts")
    miscs_cost: float = Field(default=0.0, description="Total cost of miscellaneous ingredients")
    
    # Utility costs
    electricity_cost: float = Field(default=0.0, description="Cost of electricity used")
    water_cost: float = Field(default=0.0, description="Cost of water used")
    gas_cost: float = Field(default=0.0, description="Cost of gas used")
    other_utility_cost: float = Field(default=0.0, description="Other utility costs")
    
    # Other costs
    labor_cost: float = Field(default=0.0, description="Labor cost")
    packaging_cost: float = Field(default=0.0, description="Packaging cost")
    other_cost: float = Field(default=0.0, description="Other miscellaneous costs")
    
    # Profit analysis
    target_price_per_pint: Optional[float] = Field(None, description="Target selling price per pint")
    
    # Metadata
    notes: Optional[str] = Field(None, description="Additional cost notes")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fermentables_cost": 45.50,
                "hops_cost": 12.30,
                "yeasts_cost": 7.99,
                "miscs_cost": 3.50,
                "electricity_cost": 1.02,
                "water_cost": 0.12,
                "gas_cost": 0.0,
                "other_utility_cost": 0.0,
                "labor_cost": 0.0,
                "packaging_cost": 15.00,
                "other_cost": 0.0,
                "target_price_per_pint": 5.50,
                "notes": "First batch with new equipment",
            }
        }
    )


class BatchCostCreate(BatchCostBase):
    """Schema for creating a batch cost record"""

    batch_id: int = Field(..., description="ID of the batch")


class BatchCostUpdate(BaseModel):
    """Schema for updating a batch cost record"""

    fermentables_cost: Optional[float] = None
    hops_cost: Optional[float] = None
    yeasts_cost: Optional[float] = None
    miscs_cost: Optional[float] = None
    electricity_cost: Optional[float] = None
    water_cost: Optional[float] = None
    gas_cost: Optional[float] = None
    other_utility_cost: Optional[float] = None
    labor_cost: Optional[float] = None
    packaging_cost: Optional[float] = None
    other_cost: Optional[float] = None
    target_price_per_pint: Optional[float] = None
    notes: Optional[str] = None


class BatchCost(BatchCostBase):
    """Schema for batch cost response with calculated fields"""

    id: int
    batch_id: int
    total_cost: float = Field(..., description="Total cost of the batch")
    cost_per_liter: float = Field(..., description="Cost per liter")
    cost_per_pint: float = Field(..., description="Cost per pint (473ml)")
    profit_margin: Optional[float] = Field(None, description="Profit margin percentage if target price is set")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "batch_id": 42,
                "fermentables_cost": 45.50,
                "hops_cost": 12.30,
                "yeasts_cost": 7.99,
                "miscs_cost": 3.50,
                "electricity_cost": 1.02,
                "water_cost": 0.12,
                "gas_cost": 0.0,
                "other_utility_cost": 0.0,
                "labor_cost": 0.0,
                "packaging_cost": 15.00,
                "other_cost": 0.0,
                "total_cost": 85.43,
                "cost_per_liter": 4.27,
                "cost_per_pint": 2.02,
                "target_price_per_pint": 5.50,
                "profit_margin": 63.27,
                "notes": "First batch with new equipment",
                "created_at": "2024-03-21T08:00:00Z",
                "updated_at": "2024-03-21T08:00:00Z",
            }
        },
    )


class BatchCostSummary(BaseModel):
    """Summary of costs for a batch"""

    batch_id: int
    batch_name: str
    batch_size: float
    total_ingredients_cost: float
    total_utilities_cost: float
    total_other_costs: float
    total_cost: float
    cost_per_liter: float
    cost_per_pint: float
    target_price_per_pint: Optional[float] = None
    profit_margin: Optional[float] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "batch_id": 42,
                "batch_name": "Citrus IPA - March Run",
                "batch_size": 20.0,
                "total_ingredients_cost": 69.29,
                "total_utilities_cost": 1.14,
                "total_other_costs": 15.00,
                "total_cost": 85.43,
                "cost_per_liter": 4.27,
                "cost_per_pint": 2.02,
                "target_price_per_pint": 5.50,
                "profit_margin": 63.27,
            }
        }
    )
