# Hop Schedule Optimizer

The Hop Schedule Optimizer is an advanced tool for designing and analyzing hop additions in beer recipes. It provides visual IBU contribution analysis, hop utilization calculations, and intelligent hop substitution suggestions.

## Features

### 1. Visual Hop Schedule Builder
- Add multiple hop additions with detailed parameters
- Configure hop variety, alpha acid percentage, amount, and boil time
- Specify hop type (Bittering, Aroma, Dual Purpose)
- Specify hop form (Pellet, Whole, Plug)
- Easy addition and removal of hop entries

### 2. IBU Contribution Visualization
- Graphical bar chart showing relative IBU contributions
- Detailed table view with all hop parameters
- Total IBU calculation for the recipe
- Sorted by boil time (traditional brewing order)

### 3. Utilization Calculator
- Automatic calculation of hop utilization percentage
- Based on Tinseth formula
- Factors in boil gravity and time
- Displayed for each hop addition

### 4. Substitution Suggestions
- Intelligent hop substitution recommendations
- Similarity scores based on characteristics
- Alpha acid range information
- Flavor and aroma characteristics
- Origin information for each substitute

## Usage

### Accessing the Tool
1. Navigate to the **Tools** page in HoppyBrew
2. Click on the **Hop Schedule** tab

### Creating a Hop Schedule

#### Step 1: Set Batch Parameters
- **Batch Size**: Enter your batch size in gallons (default: 5.0)
- **Boil Gravity**: Enter your pre-boil gravity (default: 1.050)

#### Step 2: Add Hop Additions
1. Click the **"Add Hop"** button
2. Fill in the hop details:
   - **Hop Variety**: Name of the hop (e.g., Cascade, Citra)
   - **Alpha Acid %**: Alpha acid percentage (typically 4-15%)
   - **Amount (oz)**: Weight of hops in ounces
   - **Boil Time (min)**: Duration of boil (60 for bittering, 0-15 for aroma)
   - **Type**: Select Bittering, Aroma, or Dual Purpose
   - **Form**: Select Pellet, Whole, or Plug

3. Repeat for all hop additions in your recipe

#### Step 3: Calculate Schedule
Click the **"Calculate Hop Schedule"** button to analyze your hop additions.

### Understanding Results

#### Total IBU
The total International Bitterness Units (IBU) for your recipe, displayed prominently at the top of results.

#### IBU Contribution Chart
- Visual bar chart showing each hop's contribution
- Bars scaled relative to total IBU
- Percentage utilization shown on the right
- Color-coded for easy identification

#### Detailed Table
- **Hop**: Variety name
- **Time**: Boil time in minutes
- **Amount**: Weight in ounces
- **IBU**: Individual IBU contribution
- **Utilization**: Hop utilization percentage
- **Type**: Color-coded hop type badge

### Finding Hop Substitutions

1. After adding a hop, click the **"Find Substitutions"** button
2. View a list of similar hop varieties
3. Each substitute shows:
   - Similarity match score (0-100)
   - Alpha acid range
   - Flavor/aroma characteristics
   - Origin region

## API Endpoints

### Calculate Hop Schedule
```
POST /api/calculators/hop-schedule
```

**Request Body:**
```json
{
  "hops": [
    {
      "name": "Magnum",
      "alpha_acid": 12.0,
      "amount_oz": 1.0,
      "time_min": 60.0,
      "type": "Bittering",
      "form": "Pellet"
    },
    {
      "name": "Cascade",
      "alpha_acid": 5.5,
      "amount_oz": 1.0,
      "time_min": 15.0,
      "type": "Aroma",
      "form": "Pellet"
    }
  ],
  "batch_size_gal": 5.0,
  "boil_gravity": 1.050
}
```

**Response:**
```json
{
  "total_ibu": 50.9,
  "hop_contributions": [
    {
      "name": "Magnum",
      "time_min": 60.0,
      "amount_oz": 1.0,
      "ibu": 41.5,
      "utilization": 23.1,
      "type": "Bittering",
      "form": "Pellet"
    },
    {
      "name": "Cascade",
      "time_min": 15.0,
      "amount_oz": 1.0,
      "ibu": 9.4,
      "utilization": 11.4,
      "type": "Aroma",
      "form": "Pellet"
    }
  ]
}
```

### Get Hop Substitutions
```
POST /api/calculators/hop-substitutions
```

**Request Body:**
```json
{
  "hop_name": "Cascade",
  "alpha_acid": 5.5
}
```

**Response:**
```json
{
  "original_hop": "Cascade",
  "substitutes": [
    {
      "name": "Centennial",
      "alpha_acid_range": "9-12%",
      "similarity_score": 85.0,
      "characteristics": "Citrus, floral, pine notes",
      "origin": "USA"
    },
    {
      "name": "Amarillo",
      "alpha_acid_range": "8-11%",
      "similarity_score": 78.0,
      "characteristics": "Orange, grapefruit, floral",
      "origin": "USA"
    }
  ]
}
```

## Calculations

### IBU Calculation (Tinseth Formula)
The tool uses the Tinseth formula for calculating IBU:

```
IBU = (AA% × Weight_oz × 7490 × Utilization) / Volume_gal

Where:
- AA% = Alpha acid percentage / 100
- Weight = Hop weight in ounces
- 7490 = Conversion factor
- Utilization = Gravity Factor × Time Factor
```

### Utilization Calculation
```
Utilization = Gravity Factor × Time Factor

Gravity Factor = 1.65 × 0.000125^(Gravity - 1.0)
Time Factor = (1 - e^(-0.04 × Time)) / 4.15
```

## Hop Substitution Database

The tool includes a comprehensive database of 16+ hop varieties with substitution recommendations:

### American Hops
- Cascade, Centennial, Citra, Mosaic, Simcoe
- Amarillo, Columbus, Chinook, Magnum

### European Hops
- Saaz, Hallertau, Tettnanger
- Fuggle, East Kent Golding

### Southern Hemisphere
- Galaxy (Australia)
- Nelson Sauvin (New Zealand)

Each hop includes:
- Typical alpha acid range
- Flavor/aroma characteristics
- Origin information
- Ranked substitutes with similarity scores

## Tips for Best Results

1. **Bittering Hops**: Use high alpha acid hops (10-15%) with long boil times (60 min)
2. **Flavor Hops**: Add hops at 15-30 minutes for balanced flavor and bitterness
3. **Aroma Hops**: Add hops at 0-15 minutes or whirlpool for maximum aroma
4. **Flameout**: Use 0 minutes for flameout additions (minimal IBU contribution)

## Technical Details

### Frontend Component
- Location: `services/nuxt3-shadcn/components/tools/HopScheduleOptimizer.vue`
- Built with Vue 3 Composition API
- Uses shadcn-vue UI components
- Responsive design for mobile and desktop

### Backend Implementation
- Location: `services/backend/api/endpoints/calculators.py`
- Uses existing brewing calculation utilities
- RESTful API design
- Comprehensive input validation

### Testing
- Unit tests: `services/backend/tests/test_endpoints/test_hop_schedule.py`
- Calculation verification
- Substitution database validation
