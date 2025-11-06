# Water Profile Management System

## Overview

The Water Profile Management System allows brewers to manage brewing water chemistry profiles for recipes. It supports both source water profiles (starting water) and target brewing profiles (desired water chemistry for specific beer styles).

## Features

### Profile Types

1. **Source Water Profiles**
   - Reverse Osmosis (RO) Water
   - Distilled Water
   - Natural Mineral Water
   - Tap Water
   - Custom source waters

2. **Target Brewing Profiles**
   - Style-specific profiles (Amber, Black, Hoppy, Malty)
   - Regional water replicas (Burton, Dublin, Pilsen, Vienna)
   - Custom target profiles

### Water Chemistry Parameters

Each profile tracks six key ions (in ppm):
- **Calcium (Ca²⁺)** - Affects mash pH, yeast health, and beer stability
- **Magnesium (Mg²⁺)** - Yeast nutrient, mash pH
- **Sodium (Na⁺)** - Flavor enhancement (in moderation)
- **Chloride (Cl⁻)** - Enhances malt character and fullness
- **Sulfate (SO₄²⁻)** - Accentuates hop bitterness and dryness
- **Bicarbonate (HCO₃⁻)** - Affects mash pH and alkalinity

Additional parameters:
- pH value
- Total alkalinity
- Residual alkalinity
- Sulfate/Chloride ratio (automatically calculated)

## API Endpoints

### List All Profiles
```
GET /water-profiles
Query Parameters:
  - profile_type: 'source' | 'target' (optional)
  - style_category: string (optional)
  - is_default: boolean (optional)
```

### Get Specific Profile
```
GET /water-profiles/{id}
```

### Create New Profile
```
POST /water-profiles
Body: {
  "name": "My Custom Profile",
  "description": "Profile description",
  "profile_type": "source" | "target",
  "style_category": "IPA",
  "calcium": 100,
  "magnesium": 10,
  "sodium": 15,
  "chloride": 50,
  "sulfate": 150,
  "bicarbonate": 40,
  "ph": 7.0,
  "notes": "Additional notes"
}
```

### Update Profile
```
PUT /water-profiles/{id}
Body: {
  "name": "Updated Name",
  "calcium": 120,
  ...
}
Note: Only custom profiles can be updated. Default profiles are read-only.
```

### Delete Profile
```
DELETE /water-profiles/{id}
Note: Only custom profiles can be deleted. Default profiles are protected.
```

### Duplicate Profile
```
POST /water-profiles/{id}/duplicate?new_name=My Copy
Note: Creates a custom copy of any profile (including defaults)
```

## Default Profiles

### Source Profiles

1. **Reverse Osmosis Water**
   - Nearly pure water ideal for building custom profiles
   - Ca: 1, Mg: 0, Na: 8, Cl: 4, SO₄: 1, HCO₃: 16 ppm

2. **Distilled Water**
   - Pure water with zero mineral content
   - All ions: 0 ppm

3. **JANA Natural Mineral Water**
   - Natural Czech mineral water
   - Ca: 30, Mg: 10, Na: 5, Cl: 6, SO₄: 15, HCO₃: 90 ppm

4. **Typical Tap Water**
   - Average municipal water profile
   - Ca: 50, Mg: 15, Na: 20, Cl: 40, SO₄: 50, HCO₃: 100 ppm

### Target Profiles

**Amber Ales:**
- Amber Balanced - General purpose balanced profile
- Amber Dry - Higher sulfate for crisp finish

**Dark Beers:**
- Black Balanced - Balanced for porters and stouts
- Black Full - Rich profile for imperial stouts

**Hop-Forward:**
- Hoppy - High sulfate for West Coast IPAs
- Hoppy Lite - Moderate sulfate for session IPAs
- Hoppy NEIPA - Chloride-forward for New England IPAs

**Malt-Forward:**
- Malty - Chloride emphasis for malty beers
- Sweet - High chloride for sweet, full-bodied beers

**Regional Waters:**
- Burton-on-Trent - Classic English IPA water
- Dublin - Traditional Irish stout water
- Pilsen - Soft water for Czech Pilsners
- Vienna - Moderate carbonate for lagers

## Usage Examples

### Setting Up Default Profiles

```bash
# Run the seed script to populate default profiles
python seeds/seed_water_profiles.py
```

### Creating a Custom Profile

```python
import requests

profile = {
    "name": "My West Coast IPA Water",
    "description": "Custom water for hop-forward beers",
    "profile_type": "target",
    "style_category": "IPA",
    "calcium": 100,
    "magnesium": 15,
    "sodium": 10,
    "chloride": 50,
    "sulfate": 250,
    "bicarbonate": 0,
    "ph": 6.5
}

response = requests.post(
    'http://localhost:8000/water-profiles',
    json=profile
)
```

### Filtering Profiles

```python
# Get all source profiles
response = requests.get(
    'http://localhost:8000/water-profiles?profile_type=source'
)

# Get all IPA profiles
response = requests.get(
    'http://localhost:8000/water-profiles?style_category=IPA'
)

# Get only default profiles
response = requests.get(
    'http://localhost:8000/water-profiles?is_default=true'
)
```

## Frontend Usage

Navigate to `/profiles/water` in the web interface to:

1. **View All Profiles** - See all available water profiles in a grid layout
2. **Filter Profiles** - Filter by type (source/target) or default status
3. **Create New Profile** - Click "+ New Profile" to create a custom profile
4. **Edit Profile** - Click the edit icon on any custom profile
5. **Duplicate Profile** - Click the copy icon to duplicate any profile
6. **Delete Profile** - Click the trash icon on custom profiles
7. **View Details** - Click the eye icon to view profile details

## Water Chemistry Guidelines

### Sulfate/Chloride Ratio

The SO₄:Cl ratio is crucial for flavor balance:
- **< 0.5** - Malt-forward, sweet, fuller body
- **0.5 - 1.0** - Balanced
- **1.0 - 2.0** - Hop-forward, moderate bitterness
- **> 2.0** - Very hop-forward, dry, bitter

### Typical Ranges (ppm)

- **Calcium**: 50-150 (essential for mash and yeast)
- **Magnesium**: 10-30 (yeast nutrient)
- **Sodium**: 0-150 (flavor enhancement, use sparingly)
- **Chloride**: 0-250 (malt character)
- **Sulfate**: 0-400 (hop character)
- **Bicarbonate**: 0-300 (alkalinity, use more for dark beers)

## Database Schema

```sql
CREATE TABLE water (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    profile_type VARCHAR(50) NOT NULL DEFAULT 'source',
    style_category VARCHAR(100),
    
    -- Ion concentrations (ppm)
    calcium DECIMAL(8,2) NOT NULL DEFAULT 0,
    magnesium DECIMAL(8,2) NOT NULL DEFAULT 0,
    sodium DECIMAL(8,2) NOT NULL DEFAULT 0,
    chloride DECIMAL(8,2) NOT NULL DEFAULT 0,
    sulfate DECIMAL(8,2) NOT NULL DEFAULT 0,
    bicarbonate DECIMAL(8,2) NOT NULL DEFAULT 0,
    
    -- Additional properties
    ph DECIMAL(4,2),
    total_alkalinity DECIMAL(8,2),
    residual_alkalinity DECIMAL(8,2),
    
    -- Metadata
    is_default BOOLEAN NOT NULL DEFAULT false,
    is_custom BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Legacy fields
    version INTEGER,
    amount INTEGER,
    notes TEXT,
    display_amount VARCHAR(255),
    inventory INTEGER,
    recipe_id INTEGER REFERENCES recipes(id)
);
```

## Migration

To apply the water profiles enhancement:

```bash
# Upgrade to latest schema
alembic upgrade head

# Or upgrade to specific revision
alembic upgrade 0002

# To rollback
alembic downgrade 0001
```

## Testing

Run the test suite:

```bash
cd services/backend
python -m pytest tests/test_endpoints/test_water_profiles.py -v
```

Test coverage includes:
- CRUD operations
- Filtering functionality
- Default profile protection
- Input validation
- Error handling
- Edge cases (division by zero, duplicate names)

## Future Enhancements

Potential additions to the water profile system:

1. **Water Treatment Calculator**
   - Calculate salt additions to reach target from source
   - Acid addition recommendations
   - Dilution calculations

2. **Profile Comparison**
   - Side-by-side comparison of profiles
   - Difference highlighting
   - Suitability scoring for styles

3. **Import/Export**
   - BeerXML water profile import
   - CSV export/import
   - JSON backup/restore

4. **Advanced Calculations**
   - Residual alkalinity calculation
   - Mash pH estimation
   - Effective hardness
   - Calcium carbonate precipitation

5. **Integration**
   - Recipe water profile selection
   - Batch brewing water tracking
   - Equipment profile water volume considerations

## Support

For issues or questions about the water profile system:
- Check the test suite for usage examples
- Review the API documentation
- See the seed script for profile examples

## References

- [How to Brew - Water Knowledge](http://www.howtobrew.com/book/section-3/understanding-the-mash-ph/water-knowledge)
- [Bru'n Water Spreadsheet](https://sites.google.com/view/brunwater/)
- [Water: A Comprehensive Guide for Brewers](https://www.brewerspublications.com/products/water-a-comprehensive-guide-for-brewers)
