# End-to-End Testing Guide

This directory contains comprehensive end-to-end (E2E) tests for HoppyBrew using Playwright.

## Overview

- **Test Framework**: Playwright
- **Total Tests**: 62 unique tests (186 total with 3 browsers)
- **Browsers**: Chromium, Firefox, WebKit
- **Pattern**: Page Object Model (POM)

## Directory Structure

```
tests/e2e/
├── fixtures/           # Mock API responses and test data
│   ├── mockApi.ts     # API mocking utilities
│   └── testData.ts    # Static test fixtures
├── pages/             # Page Object Models
│   ├── BasePage.ts    # Base class with common functionality
│   ├── RecipePage.ts  # Recipe management operations
│   ├── BatchPage.ts   # Batch workflow operations
│   ├── InventoryPage.ts  # Inventory CRUD operations
│   └── ProfilePage.ts    # Profile configuration (water, mash, equipment)
├── specs/             # Test specifications
│   ├── recipe-management.spec.ts     # 10 tests
│   ├── beerxml-import.spec.ts        # 6 tests
│   ├── batch-workflow.spec.ts        # 10 tests
│   ├── inventory-management.spec.ts  # 12 tests
│   ├── profile-configuration.spec.ts # 14 tests
│   ├── recipes.spec.ts               # 3 tests (existing)
│   ├── equipment.spec.ts             # 3 tests (existing)
│   └── library.spec.ts               # 3 tests (existing)
└── utils/             # Utility functions
    ├── helpers.ts            # General test helpers
    ├── apiHelpers.ts         # API mocking and interception
    └── testDataGenerator.ts  # Test data generators
```

## Test Categories

### 1. Recipe Management (10 tests)
Tests complete recipe lifecycle from creation to deletion.

**Key Flows**:
- Create new recipe with ingredients
- Clone and modify recipes
- Search and filter recipes
- Switch between views (card/table)
- Form validation

**File**: `specs/recipe-management.spec.ts`

### 2. BeerXML Import (6 tests)
Tests BeerXML file import and validation.

**Key Flows**:
- Import BeerXML file
- Validate imported data
- Handle invalid XML
- Import recipes with ingredients
- Handle large files

**File**: `specs/beerxml-import.spec.ts`

### 3. Batch Workflow (10 tests)
Tests batch creation and fermentation tracking.

**Key Flows**:
- Start batch from recipe
- Log fermentation readings
- Update batch status
- Complete batch workflow
- Archive batches
- Display fermentation charts

**File**: `specs/batch-workflow.spec.ts`

### 4. Inventory Management (12 tests)
Tests inventory CRUD operations across all ingredient types.

**Key Flows**:
- Add/update/delete ingredients (hops, fermentables, yeasts, miscs)
- Search and filter inventory
- Low stock alerts
- Track usage
- Navigate between categories

**File**: `specs/inventory-management.spec.ts`

### 5. Profile Configuration (14 tests)
Tests profile management for water, mash, and equipment.

**Key Flows**:
- Create water/mash/equipment profiles
- Apply profiles to recipes
- Validate chemistry calculations
- Add mash steps
- Duplicate and delete profiles
- Navigate between profile types

**File**: `specs/profile-configuration.spec.ts`

## Running Tests

### Run all tests
```bash
yarn test:e2e
```

### Run specific browser
```bash
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

### Run specific test file
```bash
npx playwright test specs/recipe-management.spec.ts
```

### Run specific test
```bash
npx playwright test specs/recipe-management.spec.ts -g "should create a new recipe"
```

### Debug mode
```bash
yarn test:e2e:debug
```

### UI mode
```bash
yarn test:e2e:ui
```

### View test report
```bash
yarn test:e2e:report
```

## Page Object Model (POM)

Page Objects encapsulate page interactions and provide reusable methods.

### Example: RecipePage

```typescript
import { RecipePage } from '../pages/RecipePage'

test('create recipe', async ({ page }) => {
  const recipePage = new RecipePage(page)
  
  await recipePage.navigateToList()
  await recipePage.clickNewRecipe()
  await recipePage.fillRecipeBasicInfo({
    name: 'My IPA',
    type: 'All Grain',
    batchSize: '20'
  })
  await recipePage.saveRecipe()
})
```

## Test Utilities

### API Mocking

```typescript
import { mockApiSuccess, mockApiError } from '../utils/apiHelpers'

// Mock successful API response
await mockApiSuccess(page, /\/recipes/, [recipe1, recipe2])

// Mock error response
await mockApiError(page, /\/recipes/, 500, 'Internal Server Error')
```

### Test Data Generation

```typescript
import { generateRecipeData, generateBatchData } from '../utils/testDataGenerator'

const recipe = generateRecipeData({
  name: 'Custom Recipe',
  batchSize: 20
})

const batch = generateBatchData({
  recipeId: recipe.id,
  status: 'fermenting'
})
```

### Helper Functions

```typescript
import { waitForCondition, retry, generateTestName } from '../utils/helpers'

// Wait for a condition
await waitForCondition(
  async () => await page.locator('.success').isVisible(),
  { timeout: 10000 }
)

// Retry operation
await retry(
  async () => await page.click('.unstable-button'),
  { maxAttempts: 3 }
)

// Generate unique test name
const recipeName = generateTestName('Test Recipe')
```

## Writing New Tests

### 1. Choose the right test file
- Add to existing spec if testing same feature
- Create new spec for new feature area

### 2. Use Page Objects
```typescript
import { RecipePage } from '../pages/RecipePage'

test('my test', async ({ page }) => {
  const recipePage = new RecipePage(page)
  await recipePage.navigateToList()
  // ... test logic
})
```

### 3. Mock APIs
```typescript
import { mockMultipleApis } from '../utils/apiHelpers'

await mockMultipleApis(page, [
  { pattern: /\/recipes$/, response: [], method: 'GET' },
  { pattern: /\/recipes$/, response: newRecipe, status: 201, method: 'POST' }
])
```

### 4. Use test data generators
```typescript
import { generateRecipeData } from '../utils/testDataGenerator'

const recipe = generateRecipeData({
  name: 'Test Recipe',
  type: 'All Grain'
})
```

### 5. Add assertions
```typescript
await expect(page.getByRole('heading', { name: 'Recipes' })).toBeVisible()
await expect(page).toHaveURL(/\/recipes/)
```

## Best Practices

### ✅ DO

- Use Page Objects for page interactions
- Mock APIs for fast, reliable tests
- Use test data generators for dynamic data
- Test user workflows, not implementation details
- Use meaningful test names that describe the scenario
- Clean up test data after tests
- Use proper waits (waitForLoadState, waitForSelector)

### ❌ DON'T

- Don't rely on real backend (use mocks)
- Don't hardcode test data (use generators)
- Don't test implementation details
- Don't use arbitrary timeouts
- Don't duplicate test logic (use Page Objects)
- Don't leave tests dependent on execution order

## CI/CD Integration

Tests run automatically on:
- Pull requests
- Pushes to main branch
- Manual workflow dispatch

**Workflow**: `.github/workflows/e2e-tests.yml`

### CI Configuration
- 3 browser matrix (chromium, firefox, webkit)
- Backend API started with test database
- Frontend served locally
- Test artifacts uploaded on failure
- Backend logs uploaded on failure

## Debugging Failed Tests

### 1. View test report
```bash
yarn test:e2e:report
```

### 2. Run in debug mode
```bash
yarn test:e2e:debug
```

### 3. Run in headed mode
```bash
npx playwright test --headed
```

### 4. Check screenshots
Failed tests automatically capture screenshots in `playwright-report/`

### 5. Check traces
Traces are captured on failure and available in the HTML report

### 6. Run single test
```bash
npx playwright test specs/recipe-management.spec.ts -g "should create"
```

## Test Coverage

| Category | Tests | Coverage |
|----------|-------|----------|
| Recipe Management | 10 | Create, Read, Update, Delete, Clone, Search, Validate |
| BeerXML Import | 6 | Import, Validate, Error handling, Large files |
| Batch Workflow | 10 | Create, Track, Update status, Archive, Charts |
| Inventory | 12 | CRUD all types, Search, Alerts, Navigation |
| Profiles | 14 | Water, Mash, Equipment CRUD, Apply, Calculate |
| Existing | 10 | Recipes, Equipment, Library basic tests |
| **Total** | **62** | **Comprehensive coverage of critical user journeys** |

## Maintenance

### Adding new Page Object
1. Create file in `pages/`
2. Extend `BasePage`
3. Add methods for page interactions
4. Export class

### Adding new test spec
1. Create file in `specs/`
2. Import necessary Page Objects
3. Import utilities
4. Write tests using POM pattern

### Adding new test data
1. Add to `fixtures/testData.ts` for static data
2. Add generator to `utils/testDataGenerator.ts` for dynamic data

## Resources

- [Playwright Documentation](https://playwright.dev/)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Page Object Model Pattern](https://playwright.dev/docs/pom)
- [GitHub Actions Integration](https://playwright.dev/docs/ci-intro)

## Support

For issues or questions:
1. Check test output and error messages
2. Review test report with screenshots/traces
3. Consult this README
4. Check Playwright documentation
5. Open an issue in the repository
