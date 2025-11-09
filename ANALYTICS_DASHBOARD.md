# Batch Analytics Dashboard

## Overview

The Batch Analytics Dashboard provides comprehensive insights into batch performance, costs, fermentation trends, and brewing patterns. This feature helps brewers make data-driven decisions and track their brewing success over time.

## Features

### Key Metrics

The dashboard displays six primary metrics:

1. **Total Batches** - Total number of batches in the selected period with completion count
2. **Success Rate** - Percentage of batches that reached completion status
3. **Average Cost per Batch** - Mean cost across all batches with cost per pint
4. **Average Fermentation Days** - Mean fermentation duration
5. **OG Accuracy** - Average accuracy of original gravity measurements vs estimates
6. **FG Accuracy** - Average accuracy of final gravity measurements vs estimates

### Analytics Categories

#### Success Rate Analysis
- **Success Rate by Recipe** - Bar chart showing completion rates for each recipe
- **Success Rate by Style** - Bar chart showing completion rates by beer style

#### Cost Analysis
- **Cost Breakdown** - Multi-series chart displaying:
  - Total cost per batch
  - Cost per liter
  - Identifies most expensive batches

#### Fermentation Trends
- **Fermentation Times** - Line chart showing duration of fermentation for each batch
- Helps identify patterns and optimize fermentation schedules

#### Seasonal Patterns
- **Seasonal Brewing Patterns** - Column chart showing batch counts by season (Winter, Spring, Summer, Fall)
- Reveals brewing seasonality and planning opportunities

### Filters

The dashboard supports filtering by:
- **Date Range** - Start and end dates to focus on specific time periods
- **Recipe** - Filter by specific recipe
- **Beer Style** - Filter by beer style category

### Export

- **CSV Export** - Download complete analytics data in CSV format
- Includes all metrics, breakdowns, and detailed batch information
- File naming convention: `batch_analytics_YYYYMMDD.csv`

## Usage

### Access

Navigate to the Analytics page from the sidebar menu or visit `/analytics/batches`.

### Applying Filters

1. Select desired start and end dates
2. Optionally select a specific recipe or style
3. Click "Apply Filters" to update the dashboard
4. Click "Clear" to reset all filters

### Viewing Charts

Use the tabbed interface to switch between different analytics views:
- Success Rate
- Costs
- Fermentation
- Seasonal

### Exporting Data

Click the "Export CSV" button in the top-right corner to download analytics data.

## API Endpoints

### Get Analytics Summary

```
GET /analytics/batches/summary
```

**Query Parameters:**
- `start_date` (optional) - ISO 8601 date string
- `end_date` (optional) - ISO 8601 date string
- `recipe_id` (optional) - Filter by recipe ID
- `style` (optional) - Filter by beer style name

**Response:**
```json
{
  "summary": {
    "total_batches": 10,
    "completed_batches": 8,
    "success_rate": 80.0,
    "avg_cost_per_batch": 45.50,
    "avg_cost_per_liter": 2.28,
    "avg_cost_per_pint": 4.81,
    "avg_fermentation_days": 14.2,
    "avg_og_accuracy": 95.5,
    "avg_fg_accuracy": 93.2
  },
  "cost_breakdown": [...],
  "fermentation_times": [...],
  "og_fg_accuracy": [...],
  "seasonal_patterns": [...],
  "success_by_recipe": [...],
  "success_by_style": [...]
}
```

### Export Analytics as CSV

```
GET /analytics/batches/export/csv
```

**Query Parameters:** Same as summary endpoint

**Response:** CSV file download

## Technical Details

### Backend Implementation

- **File:** `services/backend/api/endpoints/analytics.py`
- **Framework:** FastAPI
- **Database:** PostgreSQL via SQLAlchemy
- **Key Functions:**
  - `get_batch_analytics_summary()` - Main analytics computation
  - `export_batch_analytics_csv()` - CSV export generation
  - `calculate_batch_cost()` - Batch cost calculation helper
  - `get_season()` - Season determination helper

### Frontend Implementation

- **Page:** `services/nuxt3-shadcn/pages/analytics/batches.vue`
- **Composable:** `services/nuxt3-shadcn/composables/useBatchAnalytics.ts`
- **Framework:** Nuxt 3 with Vue 3
- **UI Components:** shadcn-vue
- **Charts:** Highcharts (via nuxt-highcharts)

### Data Sources

Analytics calculations draw from:
- `batches` table - Batch information, status, dates
- `recipes` table - Recipe details, target OG/FG, styles
- `fermentation_readings` table - Actual OG/FG measurements
- `inventory_fermentables` table - Ingredient costs

### Cost Calculation

Currently, batch costs are calculated from:
- Fermentables with `cost_per_unit` * `amount`

**Note:** Cost tracking for hops, yeasts, and miscellaneous ingredients requires adding `cost_per_unit` fields to their respective models for complete cost analysis.

## Future Enhancements

Potential improvements to consider:

1. **PDF Export** - Generate PDF reports with charts
2. **More Cost Tracking** - Add cost fields to all ingredient types
3. **Trend Analysis** - Show trends over time with sparklines
4. **Comparison Mode** - Compare multiple recipes or time periods
5. **Equipment Efficiency** - Track equipment-specific metrics
6. **Water Chemistry** - Analyze water profile impacts
7. **Predictive Analytics** - Forecast costs and trends
8. **Email Reports** - Schedule automated reports
9. **Custom Date Ranges** - Quick filters (Last 30 days, Last year, etc.)
10. **Export Charts** - Download charts as images

## Testing

### Backend Tests

Run backend tests:
```bash
cd services/backend
pytest tests/test_endpoints/test_analytics.py -v
```

### Frontend Tests

Run frontend tests:
```bash
cd services/nuxt3-shadcn
npm run test
```

## Troubleshooting

### No Data Displayed

- Verify batches exist in the database
- Check that fermentation readings have been recorded
- Ensure cost data is available in inventory items
- Verify date range includes existing batches

### Inaccurate Costs

- Confirm `cost_per_unit` is set for fermentables
- Check that ingredient amounts are correct
- Note: Hops, yeasts, and miscs currently don't contribute to costs

### Charts Not Rendering

- Ensure Highcharts is properly installed
- Check browser console for JavaScript errors
- Verify data format matches expected structure

## Support

For issues or feature requests, please create an issue in the repository or contact the development team.
