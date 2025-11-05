# Testing Strategy Agent Context

## Agent Mission
Analyze current test coverage and create comprehensive testing strategy for both backend and frontend.

## Current Status
- ACTIVE: Analyzing test coverage and identifying gaps
- PHASE: Test strategy development and gap analysis

## Test Infrastructure Analyzed
- ✅ Backend pytest configuration (pytest.ini)
- ✅ Test structure in services/backend/tests/
- ✅ Existing test endpoints coverage
- 🔄 Frontend testing setup (in progress)

## Current Test Coverage
### Backend Tests (services/backend/tests/)
- ✅ conftest.py - SQLite test database + FastAPI dependency overrides
- ✅ test_endpoints/test_batches.py - Batch cloning and inventory cleanup
- ✅ test_endpoints/test_fermentables.py - Fermentable inventory CRUD
- ✅ test_endpoints/test_hops.py - Hop inventory CRUD
- ✅ test_endpoints/test_miscs.py - Misc inventory CRUD
- ✅ test_endpoints/test_questions.py - FAQ lifecycle coverage
- ✅ test_endpoints/test_health.py - Service health probe
- ✅ test_endpoints/test_logs.py - Log retrieval and error handling
- ✅ test_endpoints/test_references.py - CRUD + XML import/export validation
- ✅ test_endpoints/test_style_guidelines.py - Full guideline CRUD
- ✅ test_endpoints/test_trigger_beer_styles.py - Background task registration
- ✅ test_endpoints/test_yeasts.py - Yeast inventory CRUD

### Missing Test Coverage
#### Backend Endpoints (NOT TESTED)
- ❌ recipes.py - No CRUD or relationship tests for core recipe workflow
- ❌ styles.py - Endpoint unreachable (not included in router) and untested
- ❌ users.py - Endpoint stub only; requires implementation + tests
- ❌ equipment_profiles.py - Endpoint stub only; requires implementation + tests
- ❌ mash_profiles.py - Endpoint stub only; requires implementation + tests
- ❌ water_profiles.py - Endpoint stub only; requires implementation + tests

#### Backend Modules (NOT TESTED)
- ❌ scraper.py - Script-style Selenium scraper lacks injectable dependencies
- ❌ modules/export_references.py - Hard-coded session prevents unit tests
- ❌ modules/import_references.py - Hard-coded session prevents unit tests
- ❌ api/scripts/ - Network-heavy background scripts without mocks

#### Frontend (NO TESTS FOUND)
- ❌ No Vitest/Jest configuration detected
- ❌ Component logic (e.g., BeerXML import dialogs, StyleCard search) untested
- ❌ No integration tests for Nuxt pages or composables
- ❌ No e2e coverage for core user journeys

## Latest Findings
- Confirmed additional backend endpoint tests for health, logs, references, style guidelines, yeasts, and background triggers.
- Discovered `/styles` endpoint is defined but never registered in `api/router.py`, leaving the route inaccessible to both clients and tests.
- Identified recipe endpoints as the highest-risk gap (no tests exercising nested ingredient persistence or duplicate detection).
- Frontend relies on direct `fetch` calls without abstraction, increasing the need for mockable utilities before testing.

## High-Priority Test Implementation Recommendations
### Backend
- Add pytest suite for `/recipes` covering happy path CRUD, duplicate name rejection, relationship persistence (RecipeHop/Fermentable/Misc/Yeast), and cascading deletes.
- Register `styles.router` in `api/router.py`, seed sample data in fixtures, and add tests for list retrieval and empty-dataset handling.
- Replace API stubs (`users`, `equipment_profiles`, `mash_profiles`, `water_profiles`) with minimal CRUD endpoints or explicitly disable them; once implemented, add contract tests similar to existing inventory suites.
- Refactor `scraper.py` and `api/scripts` to expose pure functions (HTML fetcher, parser, DB writer) so they can be unit-tested with mocked `requests`/`BeautifulSoup` and SQLAlchemy sessions.
- Parameterize `modules/import_references.py` and `modules/export_references.py` to accept a session/engine fixture, enabling round-trip tests using the SQLite test database.

### Frontend
- Introduce Vitest + Vue Testing Library inside `services/nuxt3-shadcn` with Nuxt test utils configuration.
- Create component tests for `components/BeerXML/ImportRecipeDialog.vue` validating BeerXML parsing, missing node handling, and UI feedback toggles from `useHelpers`.
- Exercise `pages/recipes/index.vue` via component tests: verify loading state, table render with mocked fetch response, delete flow optimism, and error toast handling once added.
- Test `pages/styles.vue` search behaviour: suggestion list trimming, keyboard navigation, and fallback when API returns empty data.
- Add snapshot/interaction tests for `components/Sidebar` or navigation-critical components to ensure routing links render as expected.

### Integration & E2E
- Add pytest integration test chaining `/recipes` creation followed by `/batches` cloning to ensure batch creation uses origin recipe data correctly.
- Plan Playwright (or Cypress) smoke tests for recipe import/export flows once backend coverage is solid, starting with BeerXML recipe upload and references XML round-trip.

## TODO Tasks
- [ ] Add backend pytest suite for `/recipes` (CRUD, duplicate protection, nested ingredient sync)
- [ ] Include `styles.router` in the FastAPI router and cover `/styles` with tests
- [ ] Flesh out and test `users`, `equipment_profiles`, `mash_profiles`, `water_profiles` endpoints or document their exclusion
- [ ] Refactor scraper/modules for dependency injection and add unit tests with mocked IO
- [ ] Set up frontend testing framework (Vitest + Testing Library)
- [ ] Write frontend component tests for Recipes index, Styles search, and BeerXML import dialogs
- [ ] Implement integration tests for API workflows (e.g., recipe -> batch lifecycle)
- [ ] Add e2e tests for critical user journeys (BeerXML import, reference export)
- [ ] Set up test coverage reporting
- [ ] Create performance/load tests
- [ ] Implement database migration tests

## Testing Strategy Recommendations
1. **Backend**: Achieve 90%+ test coverage for API endpoints
2. **Frontend**: Component testing with Vue Testing Library
3. **Integration**: Full API workflow testing
4. **E2E**: Critical user journey automation
5. **Performance**: Load testing for database operations

## Agent Log
- Analyzed existing test infrastructure
- Identified significant coverage gaps
- Currently developing comprehensive testing strategy
- Logged newly validated endpoint tests (health, logs, references, style guidelines, yeasts, trigger)
- Flagged missing `/styles` router registration and high-risk `/recipes` coverage gap
- Outlined backend/frontend test case priorities for next execution cycle
