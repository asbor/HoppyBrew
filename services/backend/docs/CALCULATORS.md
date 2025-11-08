# Brewing Calculators API Documentation

This document describes the brewing calculator endpoints available in the HoppyBrew API.

## Available Calculators

### 1. ABV Calculator
**Endpoint:** `POST /calculators/abv`

Calculate Alcohol by Volume from original and final gravity readings.

**Request Body:**
```json
{
  "original_gravity": 1.050,
  "final_gravity": 1.010
}
```

**Response:**
```json
{
  "abv": 5.25
}
```

**Formula:** ABV = (OG - FG) * 131.25

---

### 2. IBU Calculator (Tinseth)
**Endpoint:** `POST /calculators/ibu`

Calculate International Bitterness Units using the Tinseth model.

**Request Body:**
```json
{
  "alpha_acid": 12.0,
  "weight_oz": 2.0,
  "boil_time_min": 60.0,
  "batch_size_gal": 5.0,
  "gravity": 1.050
}
```

**Response:**
```json
{
  "ibu": 35.2
}
```

---

### 3. SRM Color Calculator (Morey)
**Endpoint:** `POST /calculators/srm`

Estimate beer color using the Morey equation.

**Request Body:**
```json
{
  "grain_color": 3.0,
  "grain_weight_lbs": 10.0,
  "batch_size_gal": 5.0
}
```

**Response:**
```json
{
  "srm": 4.5
}
```

---

### 4. Strike Water Calculator
**Endpoint:** `POST /calculators/strike-water`

Calculate strike water temperature and volume for mashing.

**Request Body:**
```json
{
  "grain_weight_lbs": 11.0,
  "mash_temp_f": 152.0,
  "grain_temp_f": 68.0,
  "water_to_grain_ratio": 1.25
}
```

**Response:**
```json
{
  "volume_quarts": 13.75,
  "temperature_f": 164.2
}
```

**Notes:**
- `water_to_grain_ratio` defaults to 1.25 quarts per pound if not specified
- Uses simplified infusion equation for temperature calculation

---

### 5. Priming Sugar Calculator
**Endpoint:** `POST /calculators/priming-sugar`

Calculate priming sugar needed for bottle carbonation.

**Request Body:**
```json
{
  "volume_gal": 5.0,
  "carbonation_level": 2.4,
  "sugar_type": "table"
}
```

**Response:**
```json
{
  "grams": 106.2,
  "oz": 3.75
}
```

**Sugar Types:**
- `table`: Table sugar (sucrose)
- `corn`: Corn sugar (dextrose)
- `dme`: Dry malt extract
- `honey`: Honey

---

### 6. Yeast Starter Calculator
**Endpoint:** `POST /calculators/yeast-starter`

Calculate yeast starter requirements based on beer characteristics and yeast age.

**Request Body:**
```json
{
  "og": 1.050,
  "volume_gal": 5.0,
  "yeast_age_months": 2.0,
  "target_cell_count": null
}
```

**Response:**
```json
{
  "cells_needed_billions": 188.7,
  "packages": 3,
  "starter_size_ml": 1000
}
```

**Notes:**
- `target_cell_count` is optional; if not provided, calculated based on gravity and volume
- Default pitch rate: 0.75M cells/mL/°P for ales
- Assumes 100B viable cells per fresh package, decreasing 20% per month

---

### 7. Dilution Calculator
**Endpoint:** `POST /calculators/dilution`

Calculate water needed to dilute wort to target gravity.

**Request Body:**
```json
{
  "current_og": 1.060,
  "current_volume_gal": 5.0,
  "target_og": 1.050
}
```

**Response:**
```json
{
  "water_to_add_gal": 1.0,
  "final_volume_gal": 6.0
}
```

**Notes:**
- Returns 0 water to add if target gravity is higher than or equal to current gravity

---

### 8. Carbonation Pressure Calculator
**Endpoint:** `POST /calculators/carbonation`

Calculate carbonation pressure for a given temperature and CO2 volumes.

**Request Body:**
```json
{
  "temp_f": 38.0,
  "co2_volumes": 2.5
}
```

**Response:**
```json
{
  "psi": 12.5,
  "bar": 0.86
}
```

**Notes:**
- Higher temperatures require higher pressures to achieve the same CO2 volumes
- Takes into account dissolved CO2 at temperature (Henry's Law)

---

### 9. Water Chemistry Calculator
**Endpoint:** `POST /calculators/water-chemistry`

Estimate water chemistry adjustments for target mash pH.

**Request Body:**
```json
{
  "water_profile": {
    "calcium": 50,
    "magnesium": 10,
    "sodium": 15,
    "chloride": 60,
    "sulfate": 120,
    "bicarbonate": 80
  },
  "grain_bill_lbs": 11.0,
  "target_ph": 5.4
}
```

**Response:**
```json
{
  "residual_alkalinity": 23.5,
  "estimated_ph": 5.47,
  "ph_target": 5.4,
  "ph_difference": 0.07
}
```

**Notes:**
- Uses Kolbach formula for residual alkalinity
- Provides simplified pH estimation
- All ion concentrations in ppm (mg/L)
- Required profile keys: calcium, magnesium, bicarbonate

---

## Testing

All calculators have comprehensive unit and integration tests. To run the tests:

```bash
cd services/backend
python -m pytest tests/test_modules/test_brewing_calculations.py -v
python -m pytest tests/test_endpoints/test_calculators.py -v
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Error Handling

All endpoints validate input parameters and return appropriate HTTP status codes:
- `200`: Successful calculation
- `422`: Validation error (invalid input parameters)
- `500`: Server error (calculation error)

## Formulas and References

- **ABV**: Standard brewing formula
- **IBU**: Tinseth model (most common in homebrewing)
- **SRM**: Morey equation for color estimation
- **Strike Water**: Simplified infusion equation
- **Priming Sugar**: Based on dissolved CO2 and sugar fermentability
- **Yeast Pitching**: Standard pitch rates (0.75M cells/mL/°P for ales)
- **Water Chemistry**: Kolbach residual alkalinity formula
