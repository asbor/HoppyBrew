# Quality Control & Tasting Notes Feature

## Overview

The Quality Control (QC) and Tasting Notes feature allows brewers to record and track quality control test results for their batches, including BJCP score calculations, appearance photos, and detailed tasting notes.

## Features

### 1. Quality Control Test Recording
- **Test Date**: Record when the quality control test was performed
- **Final Gravity**: Measure and record the final specific gravity
- **ABV (Actual)**: Record the actual alcohol by volume percentage
- **Color**: Select from standard brewing color descriptions (Pale Straw to Black)
- **Clarity**: Select from clarity options (Brilliant, Clear, Hazy, Cloudy, Opaque)
- **Tasting Notes**: Detailed text notes about the beer's characteristics
- **BJCP Score**: Overall score (0-50) or calculated from component scores
- **Photo Upload**: Upload photos of the beer's appearance

### 2. BJCP Score Calculator
The feature includes an integrated BJCP (Beer Judge Certification Program) score sheet calculator with the following categories:

- **Aroma** (0-12 points): Evaluates the beer's aroma characteristics
- **Appearance** (0-3 points): Visual assessment including color and clarity
- **Flavor** (0-20 points): Taste profile and flavor balance
- **Mouthfeel** (0-5 points): Body, carbonation, and texture
- **Overall Impression** (0-10 points): Overall quality and drinkability

**Total Score Range**: 0-50 points

**Rating Categories**:
- **Outstanding** (45-50): Exceptional beer
- **Excellent** (38-44): Very high quality
- **Very Good** (30-37): Well-crafted beer
- **Good** (21-29): Solid beer with minor flaws
- **Fair** (14-20): Acceptable but notable flaws
- **Problematic** (6-13): Significant issues
- **Flawed** (0-5): Major problems

### 3. Tasting Note Templates
Pre-built templates for common beer styles to help guide tasting notes:

- **Clean Lager**: Crisp, balanced malt-hop profile
- **Hoppy IPA**: Bold hop flavor with citrus/pine notes
- **Rich Stout**: Roasted malt with coffee/chocolate notes
- **Fruity Wheat**: Banana and clove esters with wheat character

### 4. Photo Management
- Upload photos of your beer's appearance
- Stored securely with batch association
- Displayed in QC test history

### 5. PDF Export
Export complete QC test reports as PDF including:
- Batch information
- All measurements (gravity, ABV, color, clarity)
- BJCP score (if recorded)
- Complete tasting notes

## Usage

### Backend API Endpoints

#### Create QC Test
```http
POST /api/quality-control-tests
Content-Type: application/json

{
  "batch_id": 1,
  "test_date": "2024-02-01T10:00:00",
  "final_gravity": 1.012,
  "abv_actual": 5.2,
  "color": "Golden",
  "clarity": "Clear",
  "taste_notes": "Crisp and refreshing...",
  "score": 42.5
}
```

#### Get QC Tests for a Batch
```http
GET /api/batches/{batch_id}/quality-control-tests
```

#### Calculate BJCP Score
```http
POST /api/bjcp-score
Content-Type: application/json

{
  "aroma": 10.0,
  "appearance": 2.5,
  "flavor": 18.0,
  "mouthfeel": 4.0,
  "overall_impression": 8.0
}
```

#### Upload Photo
```http
POST /api/quality-control-tests/{qc_test_id}/upload-photo
Content-Type: multipart/form-data

file: [image file]
```

#### Export PDF
```http
GET /api/quality-control-tests/{qc_test_id}/export-pdf
```

### Frontend Components

#### QualityControlDialog
Dialog component for creating and editing QC tests.

**Props**:
- `open`: boolean - Dialog open state
- `batchId`: number - The batch ID
- `existingTest`: object - Optional existing test to edit

**Events**:
- `@update:open`: Dialog state changed
- `@save`: Test saved successfully

#### QualityControlPanel
Panel component for displaying and managing QC tests for a batch.

**Props**:
- `batchId`: number - The batch ID

**Features**:
- Lists all QC tests for the batch
- Edit existing tests
- Delete tests
- Export tests as PDF
- Add new tests

### Integration

The QC feature is integrated into the batch detail page:

1. **Quick Actions Sidebar**: "Add QC Test" button appears for batches in packaged, completed, or archived status
2. **Completed Phase**: Full QC panel is displayed in the completed batch phase
3. **Batch Details**: QC tests are shown with measurements, scores, and photos

## Database Schema

### quality_control_tests Table

```sql
CREATE TABLE quality_control_tests (
    id INTEGER PRIMARY KEY,
    batch_id INTEGER NOT NULL REFERENCES batches(id) ON DELETE CASCADE,
    test_date DATETIME NOT NULL,
    final_gravity FLOAT,
    abv_actual FLOAT,
    color VARCHAR(100),
    clarity VARCHAR(100),
    taste_notes TEXT,
    score FLOAT,  -- 0-50 BJCP scale
    photo_url VARCHAR(500),
    created_at DATETIME,
    updated_at DATETIME
);
```

## Testing

### Backend Tests
Comprehensive test suite covering:
- BJCP score calculation
- QC test CRUD operations
- Photo upload
- PDF export
- Input validation

Run tests:
```bash
cd services/backend
pytest tests/test_endpoints/test_quality_control.py -v
```

### Manual Testing Checklist

1. **Create QC Test**:
   - Navigate to a completed batch
   - Click "Add QC Test"
   - Fill in measurements
   - Use BJCP calculator
   - Apply a tasting note template
   - Upload a photo
   - Save test

2. **View QC Tests**:
   - Verify test appears in the list
   - Check all fields are displayed correctly
   - Verify photo is visible

3. **Edit QC Test**:
   - Click edit icon
   - Modify values
   - Save changes
   - Verify updates appear

4. **Export PDF**:
   - Click PDF export icon
   - Verify PDF downloads
   - Check PDF contains all data

5. **Delete QC Test**:
   - Click delete icon
   - Confirm deletion
   - Verify test is removed

## Dependencies

### Backend
- `reportlab==4.0.7` - PDF generation

### Frontend
- Vue 3
- Nuxt 3
- shadcn-vue UI components

## File Structure

```
HoppyBrew/
├── services/
│   ├── backend/
│   │   ├── Database/
│   │   │   ├── Models/
│   │   │   │   └── quality_control_tests.py
│   │   │   └── Schemas/
│   │   │       └── quality_control_tests.py
│   │   ├── api/
│   │   │   └── endpoints/
│   │   │       └── quality_control_tests.py
│   │   └── tests/
│   │       └── test_endpoints/
│   │           └── test_quality_control.py
│   └── nuxt3-shadcn/
│       └── components/
│           └── batch/
│               ├── QualityControlDialog.vue
│               ├── QualityControlPanel.vue
│               └── BatchCompletedPhase.vue
└── alembic/
    └── versions/
        └── 0007_add_quality_control_tests.py
```

## Future Enhancements

Potential improvements for future releases:

1. **Batch Comparison**: Compare QC results across multiple batches
2. **Score Trends**: Track BJCP scores over time for recipe refinement
3. **Photo Gallery**: Dedicated photo gallery view for appearance comparison
4. **Custom Templates**: Allow users to create custom tasting note templates
5. **Mobile App**: Dedicated mobile app for on-the-go QC testing
6. **Score Statistics**: Analytics dashboard for QC metrics
7. **Blind Tasting**: Support for blind tasting sessions with multiple judges
8. **Competition Mode**: BJCP competition score sheet format

## Troubleshooting

### Photo Upload Issues
- Ensure file is a valid image format (JPG, PNG, GIF, WebP)
- Check file size is reasonable (< 10MB recommended)
- Verify `/app/data/qc_photos` directory exists and is writable

### PDF Export Issues
- Verify reportlab is installed: `pip list | grep reportlab`
- Check server logs for PDF generation errors
- Ensure sufficient disk space for temporary files

### BJCP Calculator Not Working
- Verify API endpoint `/api/bjcp-score` is accessible
- Check browser console for JavaScript errors
- Ensure all score inputs are within valid ranges

## Support

For issues or questions:
1. Check the [GitHub Issues](https://github.com/asbor/HoppyBrew/issues)
2. Review the [Contributing Guide](../../CONTRIBUTING.md)
3. Consult the [Roadmap](../../ROADMAP.md) for planned features

## License

This feature is part of HoppyBrew and is distributed under the MIT License. See LICENSE.txt for details.
