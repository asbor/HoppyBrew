# Cost Tracking & Analysis Feature

## Overview

The cost tracking feature provides comprehensive cost analysis for brewing batches, including ingredient costs, utility costs, and profit margin calculations.

## Features

### 1. Ingredient Cost Database
Track costs for all ingredient types:
- Fermentables (grains, extracts, sugars)
- Hops
- Yeasts
- Miscellaneous ingredients

Each ingredient can have a `cost_per_unit` field that stores the cost per kilogram, ounce, or package.

### 2. Utility Cost Calculator
Calculate brewing utility costs based on:
- **Electricity**: Based on brew time, heating element power (kW), and electricity rate
- **Water**: Based on water volume and water rate per liter
- **Gas**: Based on gas usage and gas rate per cubic meter

### 3. Cost Per Unit Analysis
Calculate the cost per serving unit:
- Pint (UK: 568ml)
- US Pint (473ml)
- Liter
- Bottle (330ml)
- Can (355ml)
- Half Liter

### 4. Profit Margin Calculator
Track profitability:
- Cost per unit
- Selling price per unit
- Profit per unit
- Profit margin percentage

## API Endpoints

### Batch Cost CRUD Operations

#### Create Cost Tracking for a Batch
```http
POST /batches/{batch_id}/costs
Content-Type: application/json

{
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
  "unit_type": "pint"
}
```

#### Get Cost Tracking for a Batch
```http
GET /batches/{batch_id}/costs
```

#### Update Cost Tracking
```http
PUT /batches/{batch_id}/costs
Content-Type: application/json

{
  "electricity_cost": 4.00,
  "packaging_cost": 12.00
}
```

#### Delete Cost Tracking
```http
DELETE /batches/{batch_id}/costs
```

#### Get Cost Summary
```http
GET /batches/{batch_id}/costs/summary
```

Response:
```json
{
  "total_ingredient_cost": 54.00,
  "total_utility_cost": 9.50,
  "total_other_cost": 12.00,
  "total_cost": 75.50,
  "cost_per_unit": 2.14,
  "profit_margin": 57.2,
  "profit_per_unit": 2.86
}
```

### Cost Calculators

#### Calculate Utility Costs
```http
POST /costs/calculate-utilities
Content-Type: application/json

{
  "brew_time_hours": 5.0,
  "electricity_rate_per_kwh": 0.12,
  "water_volume_liters": 30.0,
  "water_rate_per_liter": 0.001,
  "gas_usage_cubic_meters": 0.0,
  "gas_rate_per_cubic_meter": 0.50,
  "heating_power_kw": 3.5
}
```

Response:
```json
{
  "electricity_cost": 2.52,
  "water_cost": 0.03,
  "gas_cost": 0.00,
  "total_utility_cost": 2.55
}
```

#### Calculate Cost Per Unit
```http
POST /costs/calculate-cost-per-unit
Content-Type: application/json

{
  "total_cost": 75.50,
  "yield_volume_liters": 20.0,
  "unit_type": "pint"
}
```

Response:
```json
{
  "cost_per_unit": 2.14,
  "unit_type": "pint"
}
```

#### Calculate Profit Margin
```http
POST /costs/calculate-profit-margin
Content-Type: application/json

{
  "cost_per_unit": 2.14,
  "selling_price_per_unit": 5.00
}
```

Response:
```json
{
  "profit_per_unit": 2.86,
  "profit_margin_percentage": 57.2
}
```

## Database Schema

### batch_costs Table
```sql
CREATE TABLE batch_costs (
    id INTEGER PRIMARY KEY,
    batch_id INTEGER UNIQUE NOT NULL,
    
    -- Ingredient costs
    fermentables_cost FLOAT DEFAULT 0.0,
    hops_cost FLOAT DEFAULT 0.0,
    yeasts_cost FLOAT DEFAULT 0.0,
    miscs_cost FLOAT DEFAULT 0.0,
    
    -- Utility costs
    electricity_cost FLOAT DEFAULT 0.0,
    water_cost FLOAT DEFAULT 0.0,
    gas_cost FLOAT DEFAULT 0.0,
    
    -- Other costs
    labor_cost FLOAT DEFAULT 0.0,
    packaging_cost FLOAT DEFAULT 0.0,
    other_cost FLOAT DEFAULT 0.0,
    
    -- Sales information
    expected_yield_volume FLOAT,
    selling_price_per_unit FLOAT,
    unit_type VARCHAR DEFAULT 'pint',
    
    -- Timestamps
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    FOREIGN KEY (batch_id) REFERENCES batches(id)
);
```

### Ingredient Tables
All ingredient tables now have a `cost_per_unit` field:
- `recipe_hops.cost_per_unit`
- `inventory_hops.cost_per_unit`
- `recipe_yeasts.cost_per_unit`
- `inventory_yeasts.cost_per_unit`
- `recipe_miscs.cost_per_unit`
- `inventory_miscs.cost_per_unit`
- `recipe_fermentables.cost_per_unit` (already existed)

## Usage Examples

### Example 1: Track Full Batch Costs

```python
import requests

# Create cost tracking for a batch
batch_cost = {
    "batch_id": 1,
    "fermentables_cost": 25.50,
    "hops_cost": 15.00,
    "yeasts_cost": 8.50,
    "miscs_cost": 5.00,
    "electricity_cost": 3.50,
    "water_cost": 2.00,
    "gas_cost": 4.00,
    "packaging_cost": 10.00,
    "expected_yield_volume": 20.0,
    "selling_price_per_unit": 5.00,
    "unit_type": "pint"
}

response = requests.post(
    "http://localhost:8000/batches/1/costs",
    json=batch_cost
)

print(f"Cost tracking created: {response.json()}")

# Get cost summary
summary = requests.get("http://localhost:8000/batches/1/costs/summary")
print(f"Cost summary: {summary.json()}")
```

### Example 2: Calculate Utility Costs

```python
# Calculate utility costs for your brewing setup
utility_request = {
    "brew_time_hours": 6.0,
    "electricity_rate_per_kwh": 0.15,  # Your local rate
    "water_volume_liters": 35.0,
    "water_rate_per_liter": 0.002,
    "heating_power_kw": 4.5  # Your element power
}

response = requests.post(
    "http://localhost:8000/costs/calculate-utilities",
    json=utility_request
)

utilities = response.json()
print(f"Electricity: ${utilities['electricity_cost']:.2f}")
print(f"Water: ${utilities['water_cost']:.2f}")
print(f"Total utilities: ${utilities['total_utility_cost']:.2f}")
```

### Example 3: Analyze Profitability

```python
# Calculate if your beer is profitable
cost_analysis = {
    "cost_per_unit": 2.14,
    "selling_price_per_unit": 5.00
}

response = requests.post(
    "http://localhost:8000/costs/calculate-profit-margin",
    json=cost_analysis
)

profit = response.json()
print(f"Profit per pint: ${profit['profit_per_unit']:.2f}")
print(f"Profit margin: {profit['profit_margin_percentage']:.1f}%")
```

## Migration

To add cost tracking to an existing database:

```bash
# Run the migration
alembic upgrade head

# The migration will:
# 1. Add cost_per_unit column to ingredient tables
# 2. Create the batch_costs table
# 3. Set up proper indexes
```

## Testing

The feature includes comprehensive test coverage:
- 18 unit tests for calculation functions
- 12 API endpoint tests
- Edge case testing (zero values, negative margins, etc.)
- Input validation testing

Run tests:
```bash
cd services/backend
TESTING=1 TEST_DATABASE_URL=sqlite:///:memory: pytest tests/test_cost_calculations.py tests/test_endpoints/test_batch_costs.py -v
```

## Best Practices

1. **Track ingredient costs regularly**: Update cost_per_unit values when you purchase ingredients
2. **Measure utility costs**: Use your actual electricity and water rates for accurate calculations
3. **Account for all costs**: Include labor, packaging, and other overhead costs
4. **Update batch costs after brewing**: Adjust estimates with actual costs incurred
5. **Monitor profit margins**: Regularly review profitability to optimize recipes and pricing

## Future Enhancements

Potential future additions:
- Historical cost tracking and trends
- Cost comparison between batches
- Automatic ingredient cost tracking from inventory
- Integration with purchasing/ordering systems
- Recipe cost estimation before brewing
- Multi-currency support
