# Equipment Profiles Management

This document describes the equipment profiles management features implemented in HoppyBrew.

## Overview

Equipment profiles allow brewers to track their brewing equipment specifications, efficiency metrics, and associate equipment with batches for accurate brewing calculations.

## Features

### 1. Equipment Profile Management (CRUD)

**List all equipment profiles:**
```http
GET /equipment
```

**Get specific equipment profile:**
```http
GET /equipment/{profile_id}
```

**Create equipment profile:**
```http
POST /equipment
Content-Type: application/json

{
  "name": "10 Gallon Electric Brewery",
  "batch_size": 23,
  "boil_size": 38,
  "brewhouse_efficiency": 75.0,
  "mash_efficiency": 85.0,
  "evap_rate": 12,
  "boil_time": 60,
  "trub_chiller_loss": 2,
  "lauter_deadspace": 1
}
```

**Update equipment profile:**
```http
PUT /equipment/{profile_id}
Content-Type: application/json

{
  "brewhouse_efficiency": 78.0
}
```

**Delete equipment profile:**
```http
DELETE /equipment/{profile_id}
```

### 2. Efficiency Tracking

Equipment profiles now include two efficiency fields:

- **brewhouse_efficiency**: Overall efficiency from grain to fermenter (typically 70-80%)
- **mash_efficiency**: Efficiency of the mash conversion process (typically 80-90%)

These values help predict actual gravity readings and adjust recipes accordingly.

### 3. Batch-Equipment Association

Batches can now be associated with equipment profiles:

```python
# Create a batch with equipment
batch = Batches(
    batch_name="IPA Batch #5",
    recipe_id=recipe_id,
    equipment_id=equipment_id,  # Associate with equipment
    batch_size=20.0,
    # ... other fields
)
```

This association allows:
- Tracking which equipment was used for each batch
- Accessing equipment specifications during brewing
- Historical analysis of equipment performance

### 4. Volume and Loss Calculations

The new `utils/equipment_calculations.py` module provides brewing calculations:

#### Calculate Pre-Boil Volume
```python
from utils.equipment_calculations import calculate_pre_boil_volume

pre_boil = calculate_pre_boil_volume(
    batch_size=20.0,        # Target batch size in liters
    boil_time=60,           # Boil time in minutes
    evap_rate=10.0,         # Evaporation rate in L/hr
    trub_chiller_loss=2.0,  # Loss to trub/chiller in L
)
# Returns: 32.0 liters
```

#### Calculate Strike Water
```python
from utils.equipment_calculations import calculate_strike_water_volume

strike_water = calculate_strike_water_volume(
    grain_weight=5.0,      # Total grain weight in kg
    mash_thickness=3.0,    # Water to grain ratio (L/kg)
)
# Returns: 15.0 liters
```

#### Calculate Total Water Needed
```python
from utils.equipment_calculations import calculate_total_water_needed

water = calculate_total_water_needed(
    batch_size=20.0,
    boil_time=60,
    evap_rate=10.0,
    grain_weight=5.0,
    trub_chiller_loss=2.0,
    lauter_deadspace=1.0,
)
# Returns: {
#   "strike_water": 15.0,
#   "sparge_water": 22.0,
#   "total_water": 37.0,
#   "pre_boil_volume": 32.0,
#   "grain_absorption": 5.0
# }
```

#### Calculate Brewing Efficiency
```python
from utils.equipment_calculations import calculate_efficiency

efficiency = calculate_efficiency(
    actual_og=1.048,       # Measured original gravity
    target_og=1.050,       # Recipe target OG
)
# Returns: 96.0 (%)
```

#### Calculate Volume Losses
```python
from utils.equipment_calculations import calculate_volume_loss

losses = calculate_volume_loss(
    trub_chiller_loss=2.0,
    lauter_deadspace=1.0,
    boil_time=60,
    evap_rate=10.0,
)
# Returns: {
#   "trub_chiller_loss": 2.0,
#   "lauter_deadspace": 1.0,
#   "evaporation_loss": 10.0,
#   "total_loss": 13.0
# }
```

## Database Schema Changes

### Equipment Table
New columns:
- `brewhouse_efficiency` (FLOAT) - Overall brewing efficiency percentage
- `mash_efficiency` (FLOAT) - Mash conversion efficiency percentage

### Batches Table
New column:
- `equipment_id` (INTEGER, FOREIGN KEY) - References equipment.id

## Migration

To apply the database changes:

```bash
cd services/backend
alembic upgrade head
```

This will run migration `0008_add_equipment_enhancements.py`.

## Examples

### Creating a Complete Equipment Profile

```python
equipment = EquipmentProfiles(
    name="3-Vessel Brewery",
    batch_size=20,
    boil_size=30,
    tun_volume=45,
    brewhouse_efficiency=76.0,
    mash_efficiency=86.0,
    evap_rate=12,
    boil_time=60,
    trub_chiller_loss=2.5,
    lauter_deadspace=1.5,
    notes="Standard 3-vessel HERMS system"
)
```

### Batch with Equipment

```python
# Create batch associated with equipment
batch = Batches(
    batch_name="Pale Ale Batch 12",
    recipe_id=recipe.id,
    equipment_id=equipment.id,
    batch_size=20.0,
    brewer="John Brewer",
    brew_date=datetime.now(),
)

# Access equipment from batch
print(f"Using {batch.equipment_profile.name}")
print(f"Expected efficiency: {batch.equipment_profile.brewhouse_efficiency}%")
```

## Best Practices

1. **Set Realistic Efficiency Values**: Track your actual brewhouse efficiency over several batches and use the average.

2. **Update Equipment Profiles**: As you dial in your system, update efficiency values to reflect reality.

3. **Use Calculations for Planning**: Use the calculation utilities when planning brew days to ensure you have enough water and understand expected volumes.

4. **Associate Batches with Equipment**: Always link batches to equipment profiles for better tracking and historical analysis.

## Testing

Comprehensive tests are available:
- Equipment CRUD tests: `tests/test_endpoints/test_equipment_profiles.py`
- Calculation tests: `tests/test_modules/test_equipment_calculations.py`

Run tests:
```bash
cd services/backend
TESTING=1 pytest tests/test_modules/test_equipment_calculations.py -v
```
