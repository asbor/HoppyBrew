# Cost Tracking & Analysis Feature

## Overview

The Cost Tracking & Analysis feature provides comprehensive cost management for brewing batches, including ingredient costs, utility expenses, and profit margin analysis. This feature addresses Issue #19 and provides brewers with detailed financial insights into their brewing operations.

## Features

### 1. Ingredient Cost Tracking

Track costs for all brewing ingredients:
- **Fermentables**: Grains, malts, extracts
- **Hops**: All varieties and forms
- **Yeasts**: Dry and liquid yeasts
- **Miscellaneous**: Irish moss, clarifiers, water treatments, etc.

Costs are calculated from the `cost_per_unit` field in ingredient inventory items.

### 2. Utility Cost Management

Create reusable utility cost configurations with rates for:
- **Electricity**: Cost per kilowatt-hour (kWh)
- **Water**: Cost per liter
- **Gas**: Cost per unit (cubic meter, etc.)

Store average consumption values per batch for quick cost estimation.

### 3. Additional Cost Categories

Track other brewing expenses:
- **Labor**: Time and effort costs
- **Packaging**: Bottles, caps, labels, kegs
- **Other**: Any miscellaneous expenses

### 4. Cost Analysis

Automatic calculation of:
- **Total Cost**: Sum of all cost categories
- **Cost per Liter**: Total cost divided by batch size
- **Cost per Pint**: Cost for a US pint (473ml)
- **Profit Margin**: Percentage profit when target price is set

### 5. Batch Cost Summary

Get a comprehensive breakdown of costs:
- Total ingredients cost
- Total utilities cost
- Total other costs
- Per-unit costs (liter and pint)
- Profit analysis

## API Endpoints

### Batch Costs

#### Create Batch Cost
```http
POST /batch-costs
Content-Type: application/json

{
  "batch_id": 42,
  "fermentables_cost": 45.50,
  "hops_cost": 12.30,
  "yeasts_cost": 7.99,
  "miscs_cost": 3.50,
  "electricity_cost": 1.02,
  "water_cost": 0.12,
  "packaging_cost": 15.00,
  "target_price_per_pint": 5.50,
  "notes": "First batch with new equipment"
}
```

#### Get Batch Cost
```http
GET /batch-costs/{batch_id}
```

#### Update Batch Cost
```http
PUT /batch-costs/{batch_id}
Content-Type: application/json

{
  "labor_cost": 50.00,
  "notes": "Added labor cost"
}
```

#### Delete Batch Cost
```http
DELETE /batch-costs/{batch_id}
```

#### Get Cost Summary
```http
GET /batch-costs/{batch_id}/summary
```

Returns:
```json
{
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
  "profit_margin": 63.27
}
```

#### Calculate from Ingredients
```http
POST /batch-costs/{batch_id}/calculate-from-ingredients
```

Automatically calculates ingredient costs from batch inventory items based on their `cost_per_unit` values.

### Utility Cost Configurations

#### Create Utility Config
```http
POST /utility-cost-configs
Content-Type: application/json

{
  "name": "Home Brewery - Summer 2024",
  "electricity_rate_per_kwh": 0.12,
  "water_rate_per_liter": 0.002,
  "gas_rate_per_unit": 0.85,
  "avg_electricity_kwh_per_batch": 8.5,
  "avg_water_liters_per_batch": 60.0,
  "avg_gas_units_per_batch": 0.0,
  "currency": "USD",
  "notes": "Summer rates with solar offset"
}
```

#### List All Configs
```http
GET /utility-cost-configs?active_only=true
```

#### Get Specific Config
```http
GET /utility-cost-configs/{config_id}
```

#### Update Config
```http
PUT /utility-cost-configs/{config_id}
Content-Type: application/json

{
  "electricity_rate_per_kwh": 0.15,
  "notes": "Winter rate increase"
}
```

#### Delete Config
```http
DELETE /utility-cost-configs/{config_id}
```

#### Apply Config to Batch
```http
POST /batch-costs/{batch_id}/apply-utility-config/{config_id}
```

Calculates and applies utility costs to a batch based on the configuration's rates and average consumption values.

## Database Schema

### batch_costs Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| batch_id | Integer | Foreign key to batches |
| fermentables_cost | Float | Cost of fermentables |
| hops_cost | Float | Cost of hops |
| yeasts_cost | Float | Cost of yeasts |
| miscs_cost | Float | Cost of misc ingredients |
| electricity_cost | Float | Cost of electricity |
| water_cost | Float | Cost of water |
| gas_cost | Float | Cost of gas |
| other_utility_cost | Float | Other utility costs |
| labor_cost | Float | Labor costs |
| packaging_cost | Float | Packaging costs |
| other_cost | Float | Other miscellaneous costs |
| total_cost | Float | Total cost (calculated) |
| cost_per_liter | Float | Cost per liter (calculated) |
| cost_per_pint | Float | Cost per pint (calculated) |
| target_price_per_pint | Float | Target selling price |
| profit_margin | Float | Profit margin % (calculated) |
| notes | String | Additional notes |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### utility_cost_configs Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Configuration name (unique) |
| electricity_rate_per_kwh | Float | Cost per kWh |
| water_rate_per_liter | Float | Cost per liter |
| gas_rate_per_unit | Float | Cost per gas unit |
| avg_electricity_kwh_per_batch | Float | Average kWh per batch |
| avg_water_liters_per_batch | Float | Average liters per batch |
| avg_gas_units_per_batch | Float | Average gas units per batch |
| currency | String | Currency code (default: USD) |
| is_active | Integer | Active flag (1=active, 0=inactive) |
| notes | String | Additional notes |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## Usage Examples

### Example 1: Track Complete Batch Costs

```python
# 1. Create a batch cost record with all ingredients
POST /batch-costs
{
  "batch_id": 1,
  "fermentables_cost": 45.50,
  "hops_cost": 12.30,
  "yeasts_cost": 7.99,
  "miscs_cost": 3.50,
  "target_price_per_pint": 5.50
}

# Response shows calculated values:
{
  "id": 1,
  "batch_id": 1,
  "total_cost": 69.29,
  "cost_per_liter": 3.46,
  "cost_per_pint": 1.64,
  "profit_margin": 70.2,
  ...
}
```

### Example 2: Auto-Calculate from Inventory

```python
# Calculate ingredient costs from batch inventory
POST /batch-costs/1/calculate-from-ingredients

# This reads cost_per_unit from all inventory items
# and calculates fermentables, hops, yeasts, and miscs costs
```

### Example 3: Add Utility Costs

```python
# 1. Create a utility configuration
POST /utility-cost-configs
{
  "name": "My Brewery",
  "electricity_rate_per_kwh": 0.12,
  "water_rate_per_liter": 0.002,
  "avg_electricity_kwh_per_batch": 8.5,
  "avg_water_liters_per_batch": 60.0
}

# 2. Apply it to a batch
POST /batch-costs/1/apply-utility-config/1

# Electricity cost: 8.5 kWh × $0.12 = $1.02
# Water cost: 60 liters × $0.002 = $0.12
```

### Example 4: Get Profit Analysis

```python
# Set a target price and get profit margin
PUT /batch-costs/1
{
  "target_price_per_pint": 6.00
}

# Response shows profit analysis:
{
  "cost_per_pint": 2.02,
  "target_price_per_pint": 6.00,
  "profit_margin": 66.3
}

# Calculation: (6.00 - 2.02) / 6.00 × 100 = 66.3%
```

## Migration

To add the cost tracking tables to your database, run the Alembic migration:

```bash
alembic upgrade head
```

This will execute migration `0007_add_batch_cost_tracking.py`.

## Best Practices

1. **Set ingredient costs**: Add `cost_per_unit` to your ingredient inventory items for automatic cost calculation

2. **Create utility configs**: Set up one or more utility cost configurations for different scenarios (e.g., summer/winter rates)

3. **Use auto-calculation**: Use the `/calculate-from-ingredients` endpoint to automatically pull costs from inventory

4. **Track all costs**: Don't forget to add packaging, labor, and other costs for accurate total cost

5. **Set target prices**: Add target selling prices to calculate profit margins

6. **Review regularly**: Use the summary endpoint to review cost breakdowns and identify areas to optimize

## Profit Margin Calculation

The profit margin is calculated as:

```
profit_margin = ((target_price - cost_per_pint) / target_price) × 100
```

Example:
- Cost per pint: $2.00
- Target price: $6.00
- Profit: $6.00 - $2.00 = $4.00
- Margin: ($4.00 / $6.00) × 100 = 66.7%

## Notes

- All costs default to 0.0 if not provided
- Batch size must be greater than 0 for per-unit calculations
- Profit margin is only calculated when `target_price_per_pint` is set
- Deleting a batch automatically deletes associated cost records (cascade)
- US pint (473ml) is used for per-pint calculations
- Currency is configurable but not enforced in calculations

## Future Enhancements

Potential future improvements:
- Multi-currency support with conversion
- Cost comparison between batches
- Historical cost trends and analytics
- Budget alerts and warnings
- Export cost reports (CSV, PDF)
- Integration with accounting software
