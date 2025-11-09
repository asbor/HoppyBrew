# Batch Analytics Dashboard

## Overview

The Batch Analytics Dashboard provides comprehensive insights into brewing performance, costs, and trends. This feature helps brewers analyze their batch data to improve efficiency, quality, and cost management.

## Features

### 1. Analytics Summary
- **Total Batches**: Count of all batches in the selected date range
- **Completion Rate**: Percentage of batches that reached completion status
- **Active Batches**: Number of batches currently in progress
- **Average Batch Size**: Mean volume across all batches
- **Most Brewed Recipe**: The recipe with the highest batch count
- **Most Brewed Style**: The beer style brewed most frequently

### 2. Success Rate by Recipe
Tracks completion rates for each recipe, helping identify:
- Which recipes are most reliable
- Which recipes have higher failure rates
- Style-specific completion trends

**Metrics:**
- Total batches brewed
- Completed batches
- Success rate (percentage)
- Associated beer style

### 3. Cost Analysis
Analyzes the financial aspects of brewing:
- **Total Cost**: Sum of ingredient costs per batch
- **Cost per Liter**: Total cost divided by batch volume
- **Cost per Pint**: Cost per 0.473176 liters (US pint)

**Note:** Currently tracks fermentable costs. Future enhancements will include hops, yeasts, and miscellaneous ingredients when cost data is added to those models.

### 4. Fermentation Time Trends
Monitors fermentation duration to:
- Identify typical fermentation periods
- Compare different recipes
- Track seasonal variations

**Statistics:**
- Average fermentation time
- Minimum fermentation time
- Maximum fermentation time

### 5. OG/FG Accuracy Tracking
Compares target gravity readings with actual measurements:
- **OG Accuracy**: How close the original gravity matches the recipe target
- **FG Accuracy**: How close the final gravity matches the recipe target

This helps brewers:
- Improve process consistency
- Identify equipment or technique issues
- Validate recipe calculations

### 6. Seasonal Brewing Patterns
Shows brewing activity over time:
- Batch counts by month and year
- Identifies seasonal trends
- Helps with capacity planning

## Using the Dashboard

### Accessing Analytics
Navigate to the Analytics page via the sidebar menu (icon: bar chart).

### Date Range Filtering

The dashboard supports flexible date filtering:

**Presets:**
- **All Time**: Shows all historical data
- **Last 30 Days**: Recent month's activity
- **Last 90 Days**: Quarter-year view
- **This Year**: Current calendar year

**Custom Range:**
1. Select a start date
2. Select an end date
3. Click "Apply Filter"

All analytics data will update to reflect the selected date range.

### Exporting Data

Each analytics section includes an "Export CSV" button to download data for:
- Further analysis in spreadsheet applications
- Sharing with brewing partners
- Archival purposes

The exported CSV files include:
- All visible columns from the table
- Timestamp in filename for versioning
- Proper CSV formatting with comma escaping

## API Endpoints

### Backend API

All analytics endpoints are available at `/analytics/*`:

#### GET `/analytics/summary`
Returns overall metrics summary.

**Query Parameters:**
- `start_date` (optional): ISO format date (YYYY-MM-DD)
- `end_date` (optional): ISO format date (YYYY-MM-DD)

**Response:**
```json
{
  "total_batches": 45,
  "completed_batches": 38,
  "active_batches": 7,
  "total_recipes_used": 12,
  "average_batch_size": 20.5,
  "most_brewed_recipe": {
    "id": 5,
    "name": "West Coast IPA",
    "count": 8
  },
  "most_brewed_style": {
    "name": "American IPA",
    "count": 15
  }
}
```

#### GET `/analytics/success-rate`
Returns success rate data by recipe.

**Query Parameters:**
- `start_date` (optional): ISO format date (YYYY-MM-DD)
- `end_date` (optional): ISO format date (YYYY-MM-DD)

**Response:** Array of objects with recipe success metrics.

#### GET `/analytics/cost-analysis`
Returns cost breakdown per batch.

**Query Parameters:**
- `start_date` (optional): ISO format date (YYYY-MM-DD)
- `end_date` (optional): ISO format date (YYYY-MM-DD)

**Response:** Array of objects with batch cost data.

#### GET `/analytics/fermentation-time`
Returns fermentation duration data.

**Query Parameters:**
- `start_date` (optional): ISO format date (YYYY-MM-DD)
- `end_date` (optional): ISO format date (YYYY-MM-DD)

**Response:** Array of objects with fermentation time data.

#### GET `/analytics/og-fg-accuracy`
Returns gravity accuracy measurements.

**Query Parameters:**
- `start_date` (optional): ISO format date (YYYY-MM-DD)
- `end_date` (optional): ISO format date (YYYY-MM-DD)

**Response:** Array of objects with OG/FG comparison data.

#### GET `/analytics/seasonal-patterns`
Returns batch counts by month.

**Query Parameters:**
- `start_date` (optional): ISO format date (YYYY-MM-DD)
- `end_date` (optional): ISO format date (YYYY-MM-DD)

**Response:** Array of objects with monthly batch counts.

## Technical Implementation

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: PostgreSQL (with SQLite support for testing)
- **ORM**: SQLAlchemy

**File Locations:**
- Endpoint: `services/backend/api/endpoints/analytics.py`
- Router registration: `services/backend/api/router.py`
- Tests: `services/backend/tests/test_endpoints/test_analytics.py`

### Frontend
- **Framework**: Nuxt 3
- **UI Library**: shadcn-vue
- **Language**: TypeScript

**File Locations:**
- Page component: `services/nuxt3-shadcn/pages/analytics.vue`
- Composable: `services/nuxt3-shadcn/composables/useAnalytics.ts`
- Navigation: `services/nuxt3-shadcn/components/Sidebar/Menu.vue`

## Future Enhancements

Potential improvements for the analytics dashboard:

1. **Visual Charts**: Add interactive charts using Highcharts or Chart.js
   - Bar charts for success rates
   - Line charts for seasonal trends
   - Scatter plots for OG/FG accuracy

2. **PDF Export**: Generate formatted PDF reports

3. **Comparison Views**: Compare performance between:
   - Different recipes
   - Different time periods
   - Different brewing equipment

4. **Cost Tracking Improvements**:
   - Add cost fields to hops, yeasts, and misc models
   - Track utility costs (water, electricity, gas)
   - Calculate profit margins for commercial brewers

5. **Predictive Analytics**:
   - Forecast seasonal demand
   - Predict fermentation times based on recipe
   - Suggest optimal brewing schedules

6. **Advanced Filters**:
   - Filter by brewer
   - Filter by equipment profile
   - Filter by specific ingredients

7. **Alerts and Notifications**:
   - Alert when success rates drop below threshold
   - Notify of cost increases
   - Warn about inventory shortages

## Troubleshooting

### No Data Displayed
- Ensure batches exist in the database
- Check that the selected date range includes batch brew dates
- Verify the backend API is accessible

### CSV Export Not Working
- Check browser permissions for file downloads
- Ensure data is loaded before attempting export
- Verify JavaScript is enabled in the browser

### Inaccurate Cost Data
- Verify that `cost_per_unit` is set on fermentables
- Note that hops, yeasts, and misc ingredients currently don't have cost tracking
- Check that `amount` fields are populated correctly

### Missing OG/FG Data
- Ensure fermentation readings are recorded for batches
- Verify that gravity values are entered in the fermentation tracker
- Check that recipe has `est_og` and `est_fg` values set

## Support

For issues or feature requests related to the Analytics Dashboard, please:
1. Check existing GitHub issues
2. Create a new issue with:
   - Description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

## Contributing

Contributions to improve the analytics dashboard are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

Follow the existing code style and patterns in the repository.
