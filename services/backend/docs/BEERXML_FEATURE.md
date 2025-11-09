# BeerXML Import/Export Feature

This feature provides full support for importing and exporting brewing recipes in BeerXML format (version 1.0 standard).

## Overview

BeerXML is an XML-based standard for exchanging brewing recipe data between different brewing software applications. This implementation allows HoppyBrew to:

- Import recipes from other brewing software (BeerSmith, Beerfather, etc.)
- Export recipes for sharing or backup
- Maintain compatibility with the brewing community standard

## Supported BeerXML Elements

### Recipe Fields
- Basic recipe information (name, type, brewer, version)
- Batch and boil sizes
- Efficiency and timing
- Original/Final Gravity (OG/FG)
- IBU calculations and method
- Fermentation stages and temperatures
- Carbonation and aging information
- Display values for UI rendering

### Ingredient Categories
- **Hops**: All standard hop fields including alpha acids, form, use, timing, and oil composition
- **Fermentables**: Grains, extracts, and sugars with yield, color, and mashing properties
- **Yeasts**: Lab strains with attenuation, temperature ranges, and flocculation
- **Miscs**: Adjuncts, finings, spices, and other additives

## API Endpoints

### Import Recipes

```
POST /api/recipes/import/beerxml
```

Import one or more recipes from a BeerXML file.

**Request:**
- Content-Type: `multipart/form-data`
- Body: File upload with field name `file`

**Response:**
```json
{
  "message": "Import completed: 1 recipes imported, 0 skipped",
  "imported_count": 1,
  "skipped_count": 0,
  "errors": [],
  "recipe_ids": [42]
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/recipes/import/beerxml" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@my_recipe.xml"
```

### Export Single Recipe

```
GET /api/recipes/{recipe_id}/export/beerxml
```

Export a single recipe to BeerXML format.

**Response:**
- Content-Type: `application/xml`
- Content-Disposition: `attachment; filename=Recipe_Name_42.xml`
- Body: BeerXML formatted recipe

**Example:**
```bash
curl -X GET "http://localhost:8000/api/recipes/42/export/beerxml" \
  -o recipe_export.xml
```

### Export Multiple Recipes

```
POST /api/recipes/export/beerxml
```

Export multiple recipes to a single BeerXML file.

**Request:**
```json
[42, 43, 44]
```

**Response:**
- Content-Type: `application/xml`
- Content-Disposition: `attachment; filename=recipes_export.xml`
- Body: BeerXML formatted recipes

**Example:**
```bash
curl -X POST "http://localhost:8000/api/recipes/export/beerxml" \
  -H "Content-Type: application/json" \
  -d '[42, 43, 44]' \
  -o recipes_export.xml
```

## Usage Examples

### Import from BeerSmith

1. Export your recipe from BeerSmith as BeerXML
2. Use the import endpoint to upload the file
3. The recipe will be created with all ingredients and settings

### Export for Sharing

1. Create or modify recipes in HoppyBrew
2. Export individual recipes or collections
3. Share the XML file with other brewers or applications

### Backup and Restore

1. Export all recipes periodically for backup
2. Store the XML files safely
3. Re-import if needed to restore recipes

## Technical Details

### BeerXML Standard Compliance

This implementation follows the BeerXML 1.0 specification with the following considerations:

- **Required Fields**: NAME and VERSION are required for all recipes
- **Optional Fields**: All other fields are optional and handled gracefully
- **Data Types**: Proper conversion between XML strings and database types
- **Boolean Values**: Supports TRUE/FALSE, YES/NO, and 1/0 formats
- **Units**: Preserves both numeric values and display strings for units

### Validation

Import validation checks:
- XML well-formedness
- Root element must be RECIPES or RECIPE
- At least one valid recipe must be present
- Required fields (NAME, VERSION) must exist

### Error Handling

- Malformed XML returns 400 Bad Request with parse error details
- Invalid BeerXML structure returns 400 Bad Request with validation errors
- Non-existent recipe IDs for export return 404 Not Found
- Partial imports succeed with error reporting for failed recipes

### Data Mapping

The implementation maps BeerXML fields to HoppyBrew database models:

- Recipe → Recipes table
- Hop → RecipeHop table (linked to recipe)
- Fermentable → RecipeFermentable table (linked to recipe)
- Yeast → RecipeYeast table (linked to recipe)
- Misc → RecipeMisc table (linked to recipe)

### Database Schema

New fields added to support BeerXML:

**recipe_hops:**
- version, substitutes, humulene, caryophyllene, cohumulone, myrcene

**recipe_fermentables:**
- version, add_after_boil, coarse_fine_diff, moisture, diastatic_power, protein, max_in_batch, recommend_mash, ibu_gal_per_lb, display_amount, inventory, display_color

**recipe_yeasts:**
- version, display_amount, disp_min_temp, disp_max_temp, inventory, culture_date

**recipe_miscs:**
- version (plus type changes from Integer to Float for amount, time, batch_size)

## Migration

To add the new BeerXML fields to your database:

```bash
cd services/backend
alembic upgrade head
```

This will run the migration: `add_beerxml_fields`

## Testing

Comprehensive test coverage includes:

### Parser Tests (`test_beerxml_parser.py`)
- Valid BeerXML parsing
- Invalid XML handling
- Empty recipe handling
- Multiple recipe parsing
- Optional field handling
- Boolean field parsing
- Special character handling

### Endpoint Tests (`test_endpoints/test_beerxml_endpoints.py`)
- Successful import
- Invalid XML rejection
- Multiple recipe import
- Single recipe export
- Multiple recipe export
- Round-trip import/export integrity
- Error handling for missing recipes
- Special character handling

Run tests with:
```bash
cd services/backend
python -m pytest tests/test_beerxml_parser.py -v
python -m pytest tests/test_endpoints/test_beerxml_endpoints.py -v
```

## Limitations

- Water profiles are not currently imported/exported
- Mash profiles are not currently imported/exported
- Style guidelines are not currently imported/exported
- Equipment profiles are not currently imported/exported

These features may be added in future versions.

## Compatibility

Tested with BeerXML files from:
- BeerSmith
- Standard BeerXML 1.0 format

Should be compatible with any software that produces valid BeerXML 1.0 format files.

## Future Enhancements

Potential improvements:
- BeerXML 2.0 support
- Import preview/wizard functionality
- Conflict resolution for duplicate recipes
- Ingredient mapping/substitution during import
- Batch import with folder scanning
- Export filters and customization
- Validation report generation

## References

- BeerXML Standard: http://www.beerxml.com/
- BeerXML 1.0 Specification: http://www.beerxml.com/beerxml.htm
