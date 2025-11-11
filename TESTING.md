# HoppyBrew Testing Guide

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Testing Infrastructure](#testing-infrastructure)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Code Coverage](#code-coverage)
- [Testing Best Practices](#testing-best-practices)
- [Pre-commit Hooks](#pre-commit-hooks)
- [CI/CD Integration](#cicd-integration)

## Overview

HoppyBrew uses a comprehensive testing strategy to ensure code quality and reliability:

- **Backend**: pytest with coverage reporting (target: 80%+)
- **Frontend**: Vitest for unit tests, Playwright for E2E tests (target: 70%+)
- **Pre-commit hooks**: Automated code quality checks before commits
- **CI/CD**: Automated testing on every push and pull request

### Current Coverage
- Backend: ~57% (target: 80%)
- Frontend: Variable (target: 70%)

## Quick Start

### Backend Testing

```bash
# Navigate to backend directory
cd services/backend

# Install dependencies
pip install -r requirements.txt

# Run all tests
TESTING=1 pytest

# Run with coverage report
TESTING=1 pytest --cov=. --cov-report=html

# Run specific test file
TESTING=1 pytest tests/test_endpoints/test_health.py

# Run specific test function
TESTING=1 pytest tests/test_endpoints/test_health.py::test_health_check
```

### Frontend Testing

```bash
# Navigate to frontend directory
cd services/nuxt3-shadcn

# Install dependencies
yarn install

# Run unit tests
yarn test:unit

# Run unit tests with coverage
yarn test:unit --coverage

# Run E2E tests
yarn test:e2e

# Run E2E tests in UI mode
yarn test:e2e:ui
```

## Testing Infrastructure

### Backend Stack
- **Framework**: [pytest](https://docs.pytest.org/)
- **Coverage**: [pytest-cov](https://pytest-cov.readthedocs.io/)
- **HTTP Testing**: [httpx](https://www.python-httpx.org/) with FastAPI TestClient
- **Database**: SQLite in-memory for tests
- **Fixtures**: Defined in `tests/conftest.py`

### Frontend Stack
- **Unit Testing**: [Vitest](https://vitest.dev/)
- **E2E Testing**: [Playwright](https://playwright.dev/)
- **Vue Testing**: [@vue/test-utils](https://test-utils.vuejs.org/)
- **Coverage**: [@vitest/coverage-v8](https://vitest.dev/guide/coverage)

### Configuration Files
- Backend: `services/backend/pytest.ini`, `services/backend/pyproject.toml`
- Frontend: `services/nuxt3-shadcn/vitest.config.ts`, `services/nuxt3-shadcn/playwright.config.ts`

## Running Tests

### Backend Test Commands

```bash
# Run all tests with minimal output
TESTING=1 pytest -q

# Run tests in verbose mode
TESTING=1 pytest -v

# Run tests in parallel (faster)
TESTING=1 pytest -n auto

# Run only failed tests from last run
TESTING=1 pytest --lf

# Run tests that match a keyword
TESTING=1 pytest -k "batch"

# Run specific test markers
TESTING=1 pytest -m "unit"
TESTING=1 pytest -m "not slow"

# Show coverage summary
TESTING=1 pytest --cov=. --cov-report=term

# Generate HTML coverage report
TESTING=1 pytest --cov=. --cov-report=html
# Then open: reports/htmlcov/index.html
```

### Frontend Test Commands

```bash
# Run unit tests in watch mode
yarn test

# Run unit tests once
yarn test:unit

# Run with UI (visual test runner)
yarn test --ui

# Run E2E tests
yarn test:e2e

# Debug E2E tests
yarn test:e2e:debug

# View E2E test report
yarn test:e2e:report
```

### Docker Testing

```bash
# Run backend tests in Docker
docker compose -f docker-compose.test.yml up --abort-on-container-exit

# Clean up after tests
docker compose -f docker-compose.test.yml down -v
```

## Writing Tests

### Backend Test Structure

```python
# tests/test_endpoints/test_example.py
import pytest
from fastapi.testclient import TestClient

def test_get_endpoint(client):
    """Test GET endpoint returns expected data."""
    # Arrange
    expected_status = 200
    
    # Act
    response = client.get("/api/endpoint")
    
    # Assert
    assert response.status_code == expected_status
    assert "data" in response.json()

def test_post_endpoint_with_db(client, db_session):
    """Test POST endpoint with database interaction."""
    # Arrange
    test_data = {
        "name": "Test Item",
        "value": 42
    }
    
    # Act
    response = client.post("/api/endpoint", json=test_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["name"] == test_data["name"]
    
    # Verify database state
    from Database.Models.example import ExampleModel
    item = db_session.query(ExampleModel).filter_by(name="Test Item").first()
    assert item is not None
    assert item.value == 42

@pytest.mark.slow
def test_expensive_operation(client):
    """Test that takes a long time."""
    # This test can be skipped with: pytest -m "not slow"
    pass
```

### Frontend Test Structure

```typescript
// test/components/Example.spec.ts
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ExampleComponent from '@/components/ExampleComponent.vue'

describe('ExampleComponent', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(ExampleComponent, {
      props: {
        title: 'Test Title'
      }
    })
  })

  it('renders with correct title', () => {
    expect(wrapper.find('h1').text()).toBe('Test Title')
  })

  it('emits event when button clicked', async () => {
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('clicked')).toBeTruthy()
  })

  it('calls API when loading data', async () => {
    const mockFetch = vi.fn().mockResolvedValue({ data: [] })
    global.fetch = mockFetch

    await wrapper.vm.loadData()
    expect(mockFetch).toHaveBeenCalledWith('/api/data')
  })
})
```

### Test Organization

#### Backend Tests Location
```
services/backend/tests/
├── conftest.py              # Shared fixtures
├── test_auth.py             # Authentication tests
├── test_cors.py             # CORS tests
├── test_endpoints/          # API endpoint tests
│   ├── test_batches.py
│   ├── test_recipes.py
│   └── ...
├── test_modules/            # Module/utility tests
│   └── test_brewing_calculations.py
└── test_seeds/              # Seed data tests
    └── test_seed_american_ipa.py
```

#### Frontend Tests Location
```
services/nuxt3-shadcn/
├── test/                    # Unit tests
│   └── components/
│       ├── Card.spec.ts
│       └── ...
├── e2e/                     # E2E tests
│   ├── equipment.spec.ts
│   └── ...
└── tests/e2e/specs/        # Alternative E2E location
    └── ...
```

## Code Coverage

### Viewing Coverage Reports

#### Backend Coverage

After running tests with coverage:
```bash
TESTING=1 pytest --cov=. --cov-report=html
```

Open `services/backend/reports/htmlcov/index.html` in a browser.

#### Frontend Coverage

After running tests with coverage:
```bash
yarn test:unit --coverage
```

Open `services/nuxt3-shadcn/coverage/index.html` in a browser.

### Coverage Thresholds

The project enforces minimum coverage thresholds:
- Backend: 80% (configured in `pyproject.toml`)
- Frontend: 70% (recommended)

Tests will fail in CI if coverage drops below these thresholds.

### Coverage Configuration

#### Backend (`pyproject.toml`)
```toml
[tool.coverage.run]
source = ["."]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/alembic/*",
]
branch = true

[tool.coverage.report]
precision = 2
show_missing = true
fail_under = 80
```

#### Frontend (`vitest.config.ts`)
```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      lines: 70,
      functions: 70,
      branches: 70,
      statements: 70
    }
  }
})
```

## Testing Best Practices

### General Principles

1. **Follow AAA Pattern**: Arrange, Act, Assert
   ```python
   def test_example():
       # Arrange - Set up test data
       data = {"key": "value"}
       
       # Act - Execute the code under test
       result = function_under_test(data)
       
       # Assert - Verify the result
       assert result == expected_value
   ```

2. **One Assertion Per Test**: Each test should verify one specific behavior
   - Good: `test_user_creation_sets_username()`
   - Bad: `test_user_operations()` (tests multiple things)

3. **Test Isolation**: Tests should not depend on each other
   - Use fixtures for setup/teardown
   - Don't rely on test execution order

4. **Descriptive Names**: Test names should describe what they test
   - Good: `test_recipe_creation_requires_name()`
   - Bad: `test_recipe_1()`

5. **Test Edge Cases**: Don't just test the happy path
   - Empty inputs
   - Null/None values
   - Maximum/minimum values
   - Invalid data types
   - Error conditions

### Backend-Specific Best Practices

1. **Use Fixtures for Common Setup**
   ```python
   @pytest.fixture
   def sample_recipe(db_session):
       recipe = Recipe(name="Test IPA", batch_size=20.0)
       db_session.add(recipe)
       db_session.commit()
       return recipe
   ```

2. **Mock External Dependencies**
   ```python
   from unittest.mock import patch
   
   @patch('requests.get')
   def test_external_api_call(mock_get, client):
       mock_get.return_value.json.return_value = {"data": "mocked"}
       response = client.get("/api/external-data")
       assert response.json()["data"] == "mocked"
   ```

3. **Test Database Transactions**
   ```python
   def test_rollback_on_error(db_session):
       try:
           # Operation that should fail
           invalid_operation()
       except Exception:
           db_session.rollback()
       
       # Verify database state is clean
       assert db_session.query(Model).count() == 0
   ```

4. **Test Authorization**
   ```python
   def test_endpoint_requires_auth(client):
       response = client.get("/api/protected")
       assert response.status_code == 401
       
   def test_endpoint_with_valid_token(client, auth_token):
       headers = {"Authorization": f"Bearer {auth_token}"}
       response = client.get("/api/protected", headers=headers)
       assert response.status_code == 200
   ```

### Frontend-Specific Best Practices

1. **Mock Composables**
   ```typescript
   vi.mock('@/composables/useApi', () => ({
     useApi: () => ({
       get: vi.fn().mockResolvedValue({ data: [] })
     })
   }))
   ```

2. **Test User Interactions**
   ```typescript
   it('submits form when valid', async () => {
     await wrapper.find('input[name="email"]').setValue('test@example.com')
     await wrapper.find('form').trigger('submit')
     expect(wrapper.emitted('submit')).toBeTruthy()
   })
   ```

3. **Test Async Operations**
   ```typescript
   it('displays data after loading', async () => {
     await wrapper.vm.loadData()
     await wrapper.vm.$nextTick()
     expect(wrapper.find('.data-item').exists()).toBe(true)
   })
   ```

### What to Test

#### High Priority
- ✅ API endpoints (all CRUD operations)
- ✅ Business logic and calculations
- ✅ Authentication and authorization
- ✅ Data validation
- ✅ Error handling
- ✅ Database models and queries

#### Medium Priority
- ⚠️ UI components with logic
- ⚠️ Composables and utilities
- ⚠️ Form validation
- ⚠️ State management

#### Low Priority
- 🔵 Simple getter/setter methods
- 🔵 Pure presentation components
- 🔵 Configuration files

## Pre-commit Hooks

Pre-commit hooks automatically check code quality before each commit.

### Setup

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### Configured Hooks

The following checks run automatically before each commit:

**General:**
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON syntax validation
- Large file detection
- Merge conflict detection

**Python (Backend):**
- Black: Code formatting
- isort: Import sorting
- Flake8: Linting
- mypy: Type checking
- Bandit: Security checks

**JavaScript/TypeScript (Frontend):**
- Prettier: Code formatting
- ESLint: Linting

### Bypassing Hooks

In rare cases, you may need to bypass hooks:
```bash
git commit --no-verify -m "Emergency fix"
```

⚠️ **Warning**: Only use `--no-verify` for urgent fixes. CI will still run all checks.

## CI/CD Integration

### GitHub Actions Workflows

#### Test Suite (`test-suite.yml`)
Runs on: push, pull_request, schedule
- Backend unit tests with coverage
- Backend integration tests (Docker)
- Frontend build and unit tests
- Uploads coverage reports

#### Python Quality (`python-quality.yml`)
Runs on: push to backend files
- Black formatting check
- Ruff linting
- Pylint analysis

#### Frontend Quality (`frontend-quality.yml`)
Runs on: push to frontend files
- ESLint checks
- Prettier formatting
- TypeScript type checking

#### PR Validation (`pr-validation.yml`)
Runs on: pull_request
- All quality checks
- Coverage threshold enforcement
- Test execution

### Coverage Reporting

Coverage reports are uploaded as artifacts in CI:
- Backend: `backend-coverage-report`
- Frontend: `frontend-coverage-report`

View reports in GitHub Actions under "Artifacts" section.

### Quality Gates

PRs must pass these checks to merge:
- ✅ All tests passing
- ✅ Coverage above thresholds (80% backend, 70% frontend)
- ✅ No linting errors
- ✅ No type checking errors
- ✅ No security vulnerabilities

## Test Templates

### Backend API Endpoint Test Template

```python
# tests/test_endpoints/test_example.py
import pytest

def test_get_all_items(client):
    """Test GET /api/items returns all items."""
    response = client.get("/api/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_item_by_id(client, sample_item):
    """Test GET /api/items/{id} returns specific item."""
    response = client.get(f"/api/items/{sample_item.id}")
    assert response.status_code == 200
    assert response.json()["id"] == sample_item.id

def test_get_item_not_found(client):
    """Test GET /api/items/{id} with invalid id returns 404."""
    response = client.get("/api/items/99999")
    assert response.status_code == 404

def test_create_item(client):
    """Test POST /api/items creates new item."""
    data = {"name": "Test Item", "value": 42}
    response = client.post("/api/items", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]

def test_create_item_invalid_data(client):
    """Test POST /api/items with invalid data returns 422."""
    data = {"invalid_field": "value"}
    response = client.post("/api/items", json=data)
    assert response.status_code == 422

def test_update_item(client, sample_item):
    """Test PUT /api/items/{id} updates item."""
    data = {"name": "Updated Name"}
    response = client.put(f"/api/items/{sample_item.id}", json=data)
    assert response.status_code == 200
    assert response.json()["name"] == data["name"]

def test_delete_item(client, sample_item):
    """Test DELETE /api/items/{id} deletes item."""
    response = client.delete(f"/api/items/{sample_item.id}")
    assert response.status_code == 204
    
    # Verify deletion
    get_response = client.get(f"/api/items/{sample_item.id}")
    assert get_response.status_code == 404
```

### Frontend Component Test Template

```typescript
// test/components/Example.spec.ts
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, VueWrapper } from '@vue/test-utils'
import ExampleComponent from '@/components/ExampleComponent.vue'

describe('ExampleComponent', () => {
  let wrapper: VueWrapper

  beforeEach(() => {
    wrapper = mount(ExampleComponent, {
      props: {
        title: 'Test Title',
        items: []
      }
    })
  })

  describe('Rendering', () => {
    it('renders with correct title', () => {
      expect(wrapper.find('h1').text()).toBe('Test Title')
    })

    it('renders list of items', async () => {
      await wrapper.setProps({ items: [{ id: 1, name: 'Item 1' }] })
      expect(wrapper.findAll('.item')).toHaveLength(1)
    })

    it('displays empty state when no items', () => {
      expect(wrapper.find('.empty-state').exists()).toBe(true)
    })
  })

  describe('User Interactions', () => {
    it('emits event when item clicked', async () => {
      await wrapper.setProps({ items: [{ id: 1, name: 'Item 1' }] })
      await wrapper.find('.item').trigger('click')
      expect(wrapper.emitted('itemClicked')).toBeTruthy()
      expect(wrapper.emitted('itemClicked')[0]).toEqual([{ id: 1, name: 'Item 1' }])
    })

    it('disables button when loading', async () => {
      await wrapper.setProps({ loading: true })
      expect(wrapper.find('button').attributes('disabled')).toBeDefined()
    })
  })

  describe('Data Loading', () => {
    it('calls API when mounted', async () => {
      const mockFetch = vi.fn().mockResolvedValue({ data: [] })
      global.fetch = mockFetch

      const wrapper = mount(ExampleComponent)
      await wrapper.vm.$nextTick()

      expect(mockFetch).toHaveBeenCalled()
    })

    it('handles API errors gracefully', async () => {
      const mockFetch = vi.fn().mockRejectedValue(new Error('API Error'))
      global.fetch = mockFetch

      const wrapper = mount(ExampleComponent)
      await wrapper.vm.$nextTick()

      expect(wrapper.find('.error-message').exists()).toBe(true)
    })
  })
})
```

## Troubleshooting

### Common Issues

#### Backend Tests

**Issue**: `Exception: Could not connect to PostgreSQL`
**Solution**: Set `TESTING=1` environment variable:
```bash
TESTING=1 pytest
```

**Issue**: `ImportError: cannot import name 'X'`
**Solution**: Ensure `PYTHONPATH` is set correctly:
```bash
export PYTHONPATH=/home/runner/work/HoppyBrew/HoppyBrew/services/backend
```

**Issue**: Database tables not created
**Solution**: Check that all models are imported in `Database/Models/__init__.py`

#### Frontend Tests

**Issue**: `Cannot find module '@/components/X'`
**Solution**: Check path aliases in `nuxt.config.ts` and `vitest.config.ts`

**Issue**: `window is not defined`
**Solution**: Use `happy-dom` or `jsdom` environment in vitest config

**Issue**: Component doesn't mount
**Solution**: Ensure all required props are provided in `mount()` call

### Getting Help

- Check existing tests for examples
- Review framework documentation:
  - [pytest docs](https://docs.pytest.org/)
  - [Vitest docs](https://vitest.dev/)
  - [Playwright docs](https://playwright.dev/)
- Ask in project discussions or issues

## Contributing

When contributing tests:
1. Follow the test templates and best practices
2. Ensure tests are isolated and repeatable
3. Add descriptive docstrings
4. Run pre-commit hooks before committing
5. Verify coverage doesn't decrease

For more details, see [CONTRIBUTING.md](CONTRIBUTING.md).
