# Yeast Management & Harvesting Features

This document describes the comprehensive yeast management and harvesting features implemented for Issue #14.

## Overview

The yeast management system provides brewers with tools to:
- Maintain a database of yeast strains with detailed characteristics
- Track yeast viability based on age, storage conditions, and generation
- Log yeast harvesting operations and propagation history
- Monitor generation tracking for harvested yeast

## Features

### 1. Yeast Strain Database

A master database of yeast strains with detailed characteristics including:
- **Basic Information**: Name, laboratory, product ID
- **Type & Form**: Ale/Lager/Wine, Dry/Liquid/Slant/Culture
- **Temperature Ranges**: Minimum and maximum fermentation temperatures
- **Performance**: Flocculation level, attenuation range, alcohol tolerance
- **Reuse**: Maximum recommended generations
- **Viability**: Default viability days for different forms

**Supported Laboratories:**
- Fermentis (SafAle, SafLager series)
- White Labs (WLP series)
- Wyeast (numbered series)

### 2. Viability Calculator

Advanced viability calculation considering:
- **Age**: Days since manufacture/packaging
- **Storage Temperature**: Adjusted decay rate for temperature
- **Yeast Form**: Different decay rates for dry, liquid, and slant yeasts
- **Generation**: Viability loss per generation (~12% per generation)

**Viability Status Categories:**
- **Excellent** (≥95%): Direct pitching recommended
- **Good** (85-94%): Suitable for most applications, starter recommended for high gravity
- **Fair** (70-84%): Starter strongly recommended
- **Poor** (50-69%): Large starter required, consider fresh yeast
- **Expired** (<50%): Not recommended for use

**Decay Rates:**
- Dry yeast: 0.5% per month (very stable)
- Liquid yeast: 3.0% per month (faster decay)
- Slant yeast: 1.0% per month (moderate decay)

**Temperature Effects:**
Storage at 4°C (refrigeration) is ideal. Each degree above 4°C increases decay rate by 15%.

### 3. Harvesting Logs

Track yeast harvesting operations with:
- **Source**: Batch ID or inventory yeast
- **Harvest Details**: Date, quantity, unit
- **Viability**: Cell count, viability at harvest
- **Storage**: Method and temperature
- **Generation**: Automatic tracking with parent-child relationships
- **Status**: Active, used, or discarded

### 4. Generation Tracking

Comprehensive generation tracking features:
- Automatic generation increment for harvested yeast
- Parent-child harvest relationships
- Genealogy tree visualization
- Viability degradation warnings for high generations

## API Endpoints

### Yeast Strains

#### List Yeast Strains
```http
GET /yeast-strains?skip=0&limit=100&laboratory=Fermentis&yeast_type=Ale
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 100, max: 100)
- `laboratory` (string, optional): Filter by laboratory name
- `yeast_type` (string, optional): Filter by yeast type

**Response:**
```json
[
  {
    "id": 1,
    "name": "SafAle US-05",
    "laboratory": "Fermentis",
    "product_id": "US-05",
    "type": "Ale",
    "form": "Dry",
    "min_temperature": 15.0,
    "max_temperature": 24.0,
    "flocculation": "Medium",
    "attenuation_min": 78.0,
    "attenuation_max": 82.0,
    "alcohol_tolerance": 12.0,
    "best_for": "American ales, especially Pale Ales and IPAs",
    "notes": "Clean fermenting American ale yeast...",
    "max_reuse": 5,
    "viability_days_dry": 1095,
    "created_at": "2024-11-09T12:00:00",
    "updated_at": "2024-11-09T12:00:00"
  }
]
```

#### Get Yeast Strain
```http
GET /yeast-strains/{strain_id}
```

#### Create Yeast Strain
```http
POST /yeast-strains
Content-Type: application/json

{
  "name": "SafAle US-05",
  "laboratory": "Fermentis",
  "product_id": "US-05",
  "type": "Ale",
  "form": "Dry",
  "min_temperature": 15.0,
  "max_temperature": 24.0,
  "flocculation": "Medium",
  "attenuation_min": 78.0,
  "attenuation_max": 82.0,
  "alcohol_tolerance": 12.0,
  "best_for": "American ales",
  "max_reuse": 5
}
```

#### Update Yeast Strain
```http
PUT /yeast-strains/{strain_id}
Content-Type: application/json

{
  "notes": "Updated notes",
  "max_reuse": 10
}
```

#### Delete Yeast Strain
```http
DELETE /yeast-strains/{strain_id}
```

### Yeast Harvests

#### List Yeast Harvests
```http
GET /yeast-harvests?skip=0&limit=100&yeast_strain_id=1&status=active
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip
- `limit` (int, optional): Maximum records to return
- `yeast_strain_id` (int, optional): Filter by yeast strain
- `status` (string, optional): Filter by status (active, used, discarded)

#### Create Yeast Harvest
```http
POST /yeast-harvests
Content-Type: application/json

{
  "yeast_strain_id": 1,
  "source_batch_id": 5,
  "generation": 1,
  "quantity_harvested": 200.0,
  "unit": "ml",
  "viability_at_harvest": 95.0,
  "cell_count": 250.0,
  "storage_method": "refrigerated",
  "storage_temperature": 4.0,
  "status": "active",
  "notes": "Harvested from top cropping"
}
```

**Response:**
```json
{
  "id": 1,
  "yeast_strain_id": 1,
  "source_batch_id": 5,
  "generation": 1,
  "parent_harvest_id": null,
  "quantity_harvested": 200.0,
  "unit": "ml",
  "viability_at_harvest": 95.0,
  "cell_count": 250.0,
  "storage_method": "refrigerated",
  "storage_temperature": 4.0,
  "status": "active",
  "harvest_date": "2024-11-09T12:00:00",
  "used_date": null,
  "notes": "Harvested from top cropping",
  "created_at": "2024-11-09T12:00:00",
  "updated_at": "2024-11-09T12:00:00"
}
```

#### Get Harvest Genealogy
```http
GET /yeast-harvests/{harvest_id}/genealogy
```

Returns the complete family tree including ancestors and descendants.

**Response:**
```json
{
  "current": { /* harvest object */ },
  "ancestors": [ /* array of parent harvests */ ],
  "descendants": [
    {
      "harvest": { /* child harvest object */ },
      "children": [ /* recursive structure */ ]
    }
  ]
}
```

### Viability Calculator

#### Calculate Viability
```http
POST /yeasts/calculate-viability
Content-Type: application/json

{
  "yeast_form": "Liquid",
  "manufacture_date": "2024-01-01T00:00:00",
  "initial_viability": 100.0,
  "storage_temperature": 4.0,
  "generation": 0
}
```

**Response:**
```json
{
  "current_viability": 85.2,
  "days_since_manufacture": 90,
  "days_until_expiry": 90,
  "viability_status": "good",
  "recommendation": "Good for direct pitching, starter recommended for high gravity",
  "estimated_cell_loss_percent": 14.8
}
```

#### Get Inventory Yeast Viability
```http
GET /yeasts/inventory/{inventory_id}/viability
```

Automatically calculates and updates viability for an inventory yeast item.

## Database Schema

### yeast_strains Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String | Strain name |
| laboratory | String | Laboratory/manufacturer |
| product_id | String | Product ID or catalog number |
| type | String | Yeast type (Ale, Lager, Wine, etc.) |
| form | String | Form (Dry, Liquid, Slant, Culture) |
| min_temperature | Float | Minimum fermentation temperature (°C) |
| max_temperature | Float | Maximum fermentation temperature (°C) |
| flocculation | String | Flocculation level |
| attenuation_min | Float | Minimum attenuation (%) |
| attenuation_max | Float | Maximum attenuation (%) |
| alcohol_tolerance | Float | Alcohol tolerance (ABV %) |
| best_for | Text | Best uses for this strain |
| notes | Text | Additional notes |
| max_reuse | Integer | Maximum recommended generations |
| viability_days_dry | Integer | Viability days for dry form |
| viability_days_liquid | Integer | Viability days for liquid form |
| viability_days_slant | Integer | Viability days for slant form |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### yeast_harvests Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| source_batch_id | Integer | Source batch (FK to batches) |
| source_inventory_id | Integer | Source inventory yeast |
| yeast_strain_id | Integer | Yeast strain (FK to yeast_strains) |
| harvest_date | DateTime | Date of harvest |
| generation | Integer | Generation number |
| parent_harvest_id | Integer | Parent harvest (FK to yeast_harvests) |
| quantity_harvested | Float | Quantity harvested |
| unit | String | Unit of measurement |
| viability_at_harvest | Float | Viability percentage at harvest |
| cell_count | Float | Cell count (billions) |
| storage_method | String | Storage method |
| storage_temperature | Float | Storage temperature (°C) |
| status | String | Status (active, used, discarded) |
| used_date | DateTime | Date when used |
| notes | Text | Additional notes |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### inventory_yeasts Enhancements

New fields added:
- `yeast_strain_id`: Link to master yeast strain
- `manufacture_date`: Manufacture/packaging date
- `expiry_date`: Expiry date
- `generation`: Generation number (0 for commercial)
- `harvest_id`: Link to harvest record
- `current_viability`: Current viability percentage
- `last_viability_check`: Last viability check timestamp

## Usage Examples

### Example 1: Track a New Yeast Harvest

```python
# 1. Create or get the yeast strain
strain = {
    "name": "SafAle US-05",
    "laboratory": "Fermentis",
    "product_id": "US-05",
    "type": "Ale",
    "form": "Dry"
}
response = requests.post("/yeast-strains", json=strain)
strain_id = response.json()["id"]

# 2. Log the harvest
harvest = {
    "yeast_strain_id": strain_id,
    "source_batch_id": 5,
    "generation": 1,
    "quantity_harvested": 200.0,
    "unit": "ml",
    "viability_at_harvest": 95.0,
    "storage_method": "refrigerated",
    "storage_temperature": 4.0
}
response = requests.post("/yeast-harvests", json=harvest)
harvest_id = response.json()["id"]
```

### Example 2: Calculate Yeast Viability

```python
# Calculate viability for a 3-month-old liquid yeast
viability_request = {
    "yeast_form": "Liquid",
    "manufacture_date": "2024-08-01T00:00:00",
    "initial_viability": 100.0,
    "storage_temperature": 4.0,
    "generation": 0
}
response = requests.post("/yeasts/calculate-viability", json=viability_request)
print(response.json())
# {
#   "current_viability": 91.0,
#   "days_since_manufacture": 90,
#   "viability_status": "good",
#   "recommendation": "Good for direct pitching, starter recommended for high gravity"
# }
```

### Example 3: Create a Yeast Propagation Chain

```python
# First harvest (Generation 1)
parent_harvest = {
    "yeast_strain_id": 1,
    "source_batch_id": 10,
    "generation": 1,
    "quantity_harvested": 200.0,
    "unit": "ml"
}
parent_response = requests.post("/yeast-harvests", json=parent_harvest)
parent_id = parent_response.json()["id"]

# Second harvest from first (Generation 2 - automatic)
child_harvest = {
    "yeast_strain_id": 1,
    "parent_harvest_id": parent_id,
    "generation": 2,  # Will be auto-incremented if lower than parent
    "quantity_harvested": 150.0,
    "unit": "ml"
}
child_response = requests.post("/yeast-harvests", json=child_harvest)

# Get the genealogy
genealogy_response = requests.get(f"/yeast-harvests/{child_response.json()['id']}/genealogy")
```

## Seed Data

The system includes seed data for 12 common yeast strains:

**Fermentis:**
- SafAle US-05 (American Ale)
- SafAle S-04 (English Ale)
- SafLager W-34/70 (German Lager)
- SafAle K-97 (German Ale)

**White Labs:**
- WLP001 California Ale
- WLP002 English Ale
- WLP830 German Lager
- WLP400 Belgian Wit

**Wyeast:**
- 1056 American Ale
- 1968 London ESB Ale
- 2565 German Ale/Kölsch
- 3944 Belgian Witbier

To seed the database:
```bash
cd services/backend
python seeds/seed_yeast_strains.py
```

## Migration

To apply the database migration:

```bash
cd /path/to/HoppyBrew
alembic upgrade head
```

This will:
1. Create the `yeast_strains` table
2. Create the `yeast_harvests` table
3. Add viability tracking fields to `inventory_yeasts`
4. Create necessary indexes and foreign keys

To rollback:
```bash
alembic downgrade -1
```

## Testing

### Unit Tests

Run viability calculator tests:
```bash
cd services/backend
python -c "from tests.test_yeast_viability import *; test = TestYeastViabilityCalculator(); test.test_fresh_dry_yeast()"
```

Or run all tests with pytest (requires database):
```bash
pytest tests/test_yeast_viability.py -v
pytest tests/test_endpoints/test_yeast_management.py -v
```

### Manual Testing

Use the viability calculator standalone:
```python
from utils.yeast_viability import YeastViabilityCalculator
from datetime import datetime, timedelta

# Test viability calculation
result = YeastViabilityCalculator.calculate_viability(
    yeast_form="Liquid",
    manufacture_date=datetime.now() - timedelta(days=90),
    initial_viability=100.0,
    storage_temperature=4.0,
    generation=0
)
print(f"Current viability: {result['current_viability']}%")
print(f"Status: {result['viability_status']}")
print(f"Recommendation: {result['recommendation']}")
```

## Best Practices

1. **Always log harvests**: Track every yeast harvest for better management
2. **Check viability regularly**: Use the calculator before pitching
3. **Monitor generations**: Limit reuse to recommended generations (typically 5-10)
4. **Proper storage**: Store at 4°C for best longevity
5. **Use starters**: When viability is below 85%, make a starter
6. **Document everything**: Add notes to harvests about fermentation performance

## Future Enhancements

Potential future features:
- Yeast banking system
- Plate count integration
- Automatic starter size calculator
- Performance tracking (actual attenuation vs. expected)
- Yeast health scoring based on multiple factors
- Integration with fermentation readings
- Alerts for low viability or expiring yeast
- Bulk operations for yeast management

## Support

For issues or questions:
- Check the API documentation at `/docs` (FastAPI Swagger UI)
- Review the inline code documentation
- Submit issues on GitHub

## License

This feature is part of the HoppyBrew project and follows the same MIT license.
