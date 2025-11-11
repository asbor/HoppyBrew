# Development Guide

Complete guide for setting up a local development environment and contributing to HoppyBrew.

## Table of Contents

- [Quick Start](#quick-start)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Database Management](#database-management)
- [Debugging](#debugging)
- [Troubleshooting](#troubleshooting)
- [Contributing Guidelines](#contributing-guidelines)

---

## Quick Start

Get a development environment running in under 10 minutes:

```bash
# 1. Clone repository
git clone https://github.com/asbor/HoppyBrew.git
cd HoppyBrew

# 2. Start services with Docker Compose
docker-compose up -d

# 3. Install frontend dependencies
cd services/nuxt3-shadcn
yarn install

# 4. Start frontend development server
yarn dev
```

Access the applications:
- 🌐 Frontend: http://localhost:3000
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

---

## Development Environment Setup

### Prerequisites

**Required:**
- Docker & Docker Compose 20.10+
- Node.js 20.x or higher
- Yarn 1.22+ or higher
- Git 2.30+

**Recommended:**
- Python 3.11+ (for backend development)
- PostgreSQL 16+ (for local database)
- VS Code with recommended extensions

**VS Code Extensions:**
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Vue - Official (vue.volar)
- ESLint (dbaeumer.vscode-eslint)
- Prettier (esbenp.prettier-vscode)
- Docker (ms-azuretools.vscode-docker)

### Backend Setup (Local Development)

#### 1. Install Python Dependencies

```bash
cd services/backend

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# For local development with SQLite:
TESTING=1
TEST_DATABASE_URL=sqlite:///./hoppybrew_dev.db

# For local PostgreSQL:
TESTING=0
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=hoppybrew_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
```

#### 3. Initialize Database

```bash
# Run migrations
alembic upgrade head

# Optional: Load sample data
python seeds/seed_sample_dataset.py
```

#### 4. Start Development Server

```bash
# With auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# With specific log level
uvicorn main:app --reload --log-level debug
```

### Frontend Setup (Local Development)

#### 1. Install Node Dependencies

```bash
cd services/nuxt3-shadcn

# Install dependencies
yarn install
```

#### 2. Configure API Endpoint

Edit `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000'
    }
  }
})
```

#### 3. Start Development Server

```bash
# Start with hot module replacement
yarn dev

# Start on specific port
yarn dev --port 3001

# Start and open browser
yarn dev --open
```

### Docker Development Setup

For full stack development with Docker:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend

# Stop all services
docker-compose down
```

**Development with Live Reload:**

The `docker-compose.yml` already has volume mounts for live code reloading:

```yaml
services:
  backend:
    volumes:
      - ./services/backend:/app
    command: uvicorn main:app --reload --host 0.0.0.0
```

---

## Project Structure

```
HoppyBrew/
├── services/
│   ├── backend/                    # FastAPI backend
│   │   ├── api/                   # API endpoints
│   │   │   ├── endpoints/         # Route handlers
│   │   │   └── router.py          # Main router
│   │   ├── Database/              # Database layer
│   │   │   ├── Models/            # SQLAlchemy models
│   │   │   └── Schemas/           # Pydantic schemas
│   │   ├── modules/               # Business logic
│   │   ├── tests/                 # Backend tests
│   │   ├── main.py                # FastAPI application
│   │   ├── database.py            # Database configuration
│   │   └── requirements.txt       # Python dependencies
│   │
│   └── nuxt3-shadcn/              # Nuxt 3 frontend
│       ├── components/            # Vue components
│       ├── composables/           # Composable functions
│       ├── pages/                 # Application pages
│       ├── layouts/               # Layout components
│       ├── assets/                # Static assets
│       ├── public/                # Public files
│       ├── tests/                 # Frontend tests
│       └── nuxt.config.ts         # Nuxt configuration
│
├── alembic/                       # Database migrations
├── seeds/                         # Database seed scripts
├── documents/                     # Project documentation
│   ├── docs/                      # Technical docs
│   └── images/                    # Images and diagrams
├── wiki/                          # Wiki pages
├── .github/                       # GitHub workflows
├── docker-compose.yml             # Docker orchestration
├── .env.example                   # Environment template
├── makefile                       # Build commands
└── README.md                      # Project overview
```

---

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Backend: Edit files in `services/backend/`
   - Frontend: Edit files in `services/nuxt3-shadcn/`

3. **Test your changes**
   ```bash
   # Backend tests
   cd services/backend
   pytest -v
   
   # Frontend tests
   cd services/nuxt3-shadcn
   yarn test
   ```

4. **Lint and format**
   ```bash
   # Backend
   make backend-format
   make backend-lint
   
   # Frontend
   yarn lint
   yarn format
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Format

Follow conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(api): add batch cloning endpoint
fix(ui): correct recipe form validation
docs: update API documentation
test(backend): add tests for calculator endpoints
```

---

## Testing

### Backend Testing

**Run all tests:**
```bash
cd services/backend
pytest
```

**Run specific test file:**
```bash
pytest tests/test_endpoints/test_recipes.py
```

**Run with coverage:**
```bash
pytest --cov=. --cov-report=html
```

**Run with verbose output:**
```bash
pytest -v -s
```

**Test Structure:**
```
services/backend/tests/
├── conftest.py                 # Test configuration
├── test_endpoints/             # API endpoint tests
│   ├── test_recipes.py
│   ├── test_batches.py
│   └── ...
├── test_modules/               # Module tests
│   ├── test_calculators.py
│   └── ...
└── test_database/              # Database tests
    └── test_models.py
```

**Writing Tests:**

```python
def test_create_recipe(client, db_session):
    """Test recipe creation endpoint."""
    # Arrange
    recipe_data = {
        "name": "Test IPA",
        "batch_size_l": 20,
        "efficiency": 72
    }
    
    # Act
    response = client.post("/recipes", json=recipe_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["name"] == "Test IPA"
```

### Frontend Testing

**Run all tests:**
```bash
cd services/nuxt3-shadcn
yarn test
```

**Run in watch mode:**
```bash
yarn test:watch
```

**Run E2E tests:**
```bash
yarn test:e2e
```

**Test Structure:**
```
services/nuxt3-shadcn/tests/
├── unit/                      # Component tests
│   └── components/
├── integration/               # Integration tests
└── e2e/                       # End-to-end tests
    └── recipes.spec.ts
```

**Writing Component Tests:**

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import RecipeCard from '@/components/RecipeCard.vue'

describe('RecipeCard', () => {
  it('renders recipe name', () => {
    const wrapper = mount(RecipeCard, {
      props: {
        recipe: {
          name: 'Test IPA',
          og: 1.052,
          fg: 1.012
        }
      }
    })
    
    expect(wrapper.text()).toContain('Test IPA')
  })
})
```

---

## Code Quality

### Backend Code Quality

**Linting (Flake8):**
```bash
cd services/backend
flake8 .
```

**Formatting (Black):**
```bash
# Check formatting
black --check .

# Apply formatting
black .
```

**Type Checking (mypy):**
```bash
mypy .
```

**Code Quality Configuration:**

`.flake8`:
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,.venv,__pycache__,alembic
```

`pyproject.toml`:
```toml
[tool.black]
line-length = 88
target-version = ['py311']
```

### Frontend Code Quality

**Linting (ESLint):**
```bash
yarn lint
```

**Formatting (Prettier):**
```bash
# Check formatting
yarn format:check

# Apply formatting
yarn format
```

**Type Checking:**
```bash
yarn type-check
```

---

## Database Management

### Migrations

**Create a new migration:**
```bash
cd services/backend
alembic revision --autogenerate -m "Add new field to recipes"
```

**Apply migrations:**
```bash
# Upgrade to latest
alembic upgrade head

# Upgrade by one version
alembic upgrade +1

# Downgrade by one version
alembic downgrade -1
```

**View migration history:**
```bash
alembic history
alembic current
```

### Seeding Data

**Seed sample dataset:**
```bash
python seeds/seed_sample_dataset.py
```

**Seed specific data:**
```bash
python seeds/seed_beer_styles.py
python seeds/seed_equipment_profiles.py
```

**Reset database:**
```bash
# Drop all tables
alembic downgrade base

# Recreate tables
alembic upgrade head

# Reseed data
python seeds/seed_sample_dataset.py
```

### Database CLI

**Connect to PostgreSQL:**
```bash
# Local
psql -h localhost -U postgres -d hoppybrew_db

# Docker
docker exec -it hoppybrew-db-1 psql -U postgres -d hoppybrew_db
```

**Useful SQL queries:**
```sql
-- List all tables
\dt

-- Describe table
\d recipes

-- Count records
SELECT COUNT(*) FROM recipes;

-- View recent batches
SELECT * FROM batches ORDER BY created_at DESC LIMIT 10;
```

---

## Debugging

### Backend Debugging

**Python Debugger (pdb):**
```python
import pdb; pdb.set_trace()
```

**VS Code Launch Configuration:**

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "jinja": true,
      "justMyCode": false,
      "cwd": "${workspaceFolder}/services/backend"
    }
  ]
}
```

**View Logs:**
```bash
# Backend logs
docker-compose logs -f backend

# Filter logs
docker-compose logs backend | grep ERROR
```

### Frontend Debugging

**Vue DevTools:**
- Install Vue DevTools browser extension
- Access at http://localhost:3000

**Browser Console:**
```javascript
// In any component
console.log('Debug:', this.recipeData)
```

**Nuxt DevTools:**
- Automatically enabled in development
- Press Shift+Option+D to toggle

---

## Troubleshooting

### Common Issues

#### Port Already in Use

**Error:** `Address already in use: 8000 or 3000`

**Solution:**
```bash
# Find process using port
lsof -i :8000
lsof -i :3000

# Kill process
kill -9 <PID>

# Or change port
uvicorn main:app --port 8001
yarn dev --port 3001
```

#### Database Connection Failed

**Error:** `Could not connect to database`

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart db

# Check logs
docker-compose logs db

# Verify connection
psql -h localhost -U postgres -d hoppybrew_db
```

#### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
```bash
# Backend
cd services/backend
pip install -r requirements.txt

# Frontend
cd services/nuxt3-shadcn
yarn install
```

#### Alembic Migration Failed

**Error:** `Target database is not up to date`

**Solution:**
```bash
# Check current version
alembic current

# Force to specific version
alembic stamp head

# Or reset and reapply
alembic downgrade base
alembic upgrade head
```

#### Frontend Build Fails

**Error:** `Error: Cannot find module '@/components/X'`

**Solution:**
```bash
# Clear Nuxt cache
rm -rf .nuxt
yarn dev

# Reinstall dependencies
rm -rf node_modules yarn.lock
yarn install
```

### Docker Issues

**Container won't start:**
```bash
# View container logs
docker logs hoppybrew-backend-1

# Check container status
docker ps -a

# Remove and recreate
docker-compose down
docker-compose up -d --build
```

**Volume permission issues:**
```bash
# Fix permissions
sudo chown -R $USER:$USER services/backend
```

---

## Contributing Guidelines

### Before You Start

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Check [open issues](https://github.com/asbor/HoppyBrew/issues)
3. Review [ROADMAP.md](ROADMAP.md) for project direction

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts with main
- [ ] PR description explains changes

### Code Review Process

1. Automated checks run (linting, tests)
2. Maintainer reviews code
3. Address feedback
4. Approval and merge

---

## Additional Resources

- 📚 [Wiki](wiki/Home.md) - Comprehensive documentation
- 🏗️ [Architecture](wiki/Architecture.md) - System design
- 📖 [API Docs](API_DOCUMENTATION.md) - API reference
- 🐛 [Issue Tracker](https://github.com/asbor/HoppyBrew/issues)
- 💬 [Discussions](https://github.com/asbor/HoppyBrew/discussions)

---

## Getting Help

**Stuck? Need help?**

1. Check this guide first
2. Search [existing issues](https://github.com/asbor/HoppyBrew/issues)
3. Ask in [Discussions](https://github.com/asbor/HoppyBrew/discussions)
4. Open a [new issue](https://github.com/asbor/HoppyBrew/issues/new)

**Response Times:**
- Critical bugs: 1-2 days
- Feature requests: 1-2 weeks
- Questions: 2-3 days

---

**Last Updated:** 2025-01-15  
**Guide Version:** 1.0.0
