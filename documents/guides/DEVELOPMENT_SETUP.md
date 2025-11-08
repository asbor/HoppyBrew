# Development Setup Guide

Complete guide for setting up HoppyBrew for development.

## 📋 Prerequisites

### Required Software

- **Python 3.11+**: Backend runtime
- **Node.js 20+**: Frontend runtime  
- **Git**: Version control
- **Docker** (optional): Containerized development
- **PostgreSQL** or **SQLite**: Database

### Recommended Tools

- **VS Code**: IDE with Python and Vue extensions
- **Postman/Thunder Client**: API testing
- **pgAdmin/DBeaver**: Database management
- **GitHub CLI**: For PR management

## 🚀 Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/asbor/HoppyBrew.git
cd HoppyBrew
```

### 2. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip nodejs npm postgresql
```

**macOS (Homebrew):**
```bash
brew install python@3.11 node postgresql
```

**Windows:**
- Install Python from [python.org](https://www.python.org/)
- Install Node.js from [nodejs.org](https://nodejs.org/)
- Install PostgreSQL from [postgresql.org](https://www.postgresql.org/)

## 🐍 Backend Setup

### 1. Create Virtual Environment

```bash
cd services/backend
python3.11 -m venv .venv
```

### 2. Activate Virtual Environment

```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file in `services/backend/`:

```bash
# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=hoppybrew_dev
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres

# Or use SQLite for development
TESTING=1
TEST_DATABASE_URL=sqlite:///./hoppybrew_dev.db

# Application
DEBUG=True
LOG_LEVEL=DEBUG
ENVIRONMENT=development

# CORS (for frontend)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. Set Up Database

**PostgreSQL:**
```bash
# Create database
sudo -u postgres createdb hoppybrew_dev

# Or using psql
sudo -u postgres psql
CREATE DATABASE hoppybrew_dev;
\q
```

**SQLite (for quick development):**
- No setup needed, database file created automatically

### 6. Run Migrations

```bash
cd services/backend

# Run Alembic migrations
alembic upgrade head

# Verify migrations
alembic current
```

### 7. Load Sample Data

```bash
# Using SQLite
TESTING=1 TEST_DATABASE_URL=sqlite:///./hoppybrew_dev.db \
  python seeds/seed_sample_dataset.py

# Using PostgreSQL
python seeds/seed_sample_dataset.py
```

### 8. Start Backend Server

```bash
# Development server with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or with custom host/port
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

### 9. Verify Backend

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs  # or /redoc
```

## 🎨 Frontend Setup

### 1. Navigate to Frontend

```bash
cd services/nuxt3-shadcn
```

### 2. Install Dependencies

```bash
# Using Yarn (recommended)
yarn install

# Or using npm
npm install
```

### 3. Configure Environment

Create `.env` file in `services/nuxt3-shadcn/`:

```bash
# API Configuration
API_BASE_URL=http://localhost:8000

# Nuxt Configuration
NODE_ENV=development
NITRO_HOST=0.0.0.0
NITRO_PORT=3000
```

### 4. Start Development Server

```bash
# Development mode with hot reload
yarn dev

# Or with custom port
yarn dev --port 3001
```

### 5. Verify Frontend

Open browser to:
- Frontend: http://localhost:3000
- Should see HoppyBrew dashboard

## 🐳 Docker Development

### Option 1: Full Docker Setup

```bash
# Build and start all services
export HOST_UID=$(id -u) && export HOST_GID=$(id -g)
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Database Only in Docker

Run only the database in Docker, develop backend/frontend locally:

```bash
# Start only database
docker-compose up db -d

# Backend and frontend run locally as above
```

### Docker Commands

```bash
# Rebuild specific service
docker-compose build backend

# Access container shell
docker exec -it hoppybrew-backend bash

# View logs
docker-compose logs -f backend

# Run migrations in container
docker exec hoppybrew-backend alembic upgrade head

# Load sample data in container
docker exec hoppybrew-backend python seeds/seed_sample_dataset.py
```

## 🧪 Running Tests

### Backend Tests

```bash
cd services/backend

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_recipes.py

# Run with verbose output
pytest -v

# Run only fast tests
pytest -m "not slow"
```

### Frontend Tests

```bash
cd services/nuxt3-shadcn

# Run tests (when available)
yarn test

# Run with coverage
yarn test:coverage

# Run in watch mode
yarn test:watch
```

## 🔧 Development Tools

### Code Formatting

**Backend (Python):**
```bash
cd services/backend

# Format with Black
black .

# Sort imports
isort .

# Lint with flake8
flake8 .

# Type checking
mypy .
```

**Frontend (TypeScript/Vue):**
```bash
cd services/nuxt3-shadcn

# Format with Prettier
yarn format

# Lint with ESLint
yarn lint

# Type check
yarn type-check
```

### Database Management

**View Database:**
```bash
# Using psql
psql hoppybrew_dev

# List tables
\dt

# Describe table
\d recipes

# Query
SELECT * FROM recipes LIMIT 5;
```

**Database Migrations:**
```bash
cd services/backend

# Create new migration
alembic revision --autogenerate -m "Add new column"

# Upgrade to latest
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

### API Testing

**Using cURL:**
```bash
# Get all recipes
curl http://localhost:8000/api/recipes

# Create recipe (POST)
curl -X POST http://localhost:8000/api/recipes \
  -H "Content-Type: application/json" \
  -d '{"name":"Test IPA","style_id":1}'

# Get specific recipe
curl http://localhost:8000/api/recipes/1
```

**Using Python Requests:**
```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Get recipes
response = requests.get("http://localhost:8000/api/recipes")
print(response.json())
```

## 📝 Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/my-new-feature
```

### 2. Make Changes

- Edit code
- Add tests
- Update documentation

### 3. Test Changes

```bash
# Backend tests
cd services/backend
pytest

# Frontend tests
cd services/nuxt3-shadcn
yarn test
```

### 4. Format Code

```bash
# Backend
black services/backend
isort services/backend

# Frontend
cd services/nuxt3-shadcn && yarn format
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add new feature"
```

### 6. Push and Create PR

```bash
git push origin feature/my-new-feature

# Create PR on GitHub
gh pr create --title "Add new feature" --body "Description"
```

## 🐛 Debugging

### Backend Debugging

**VS Code launch.json:**
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

**Python Debugger:**
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use debugpy for VS Code
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()
```

### Frontend Debugging

- Use Vue DevTools browser extension
- Use browser developer tools
- Check console for errors
- Inspect network requests

### Docker Debugging

```bash
# View container logs
docker-compose logs -f backend

# Access container shell
docker exec -it hoppybrew-backend bash

# Check container status
docker-compose ps

# View container resource usage
docker stats
```

## 📚 Documentation

### Generate API Documentation

FastAPI auto-generates documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

### Add Docstrings

**Python:**
```python
def calculate_abv(og: float, fg: float) -> float:
    """
    Calculate alcohol by volume from original and final gravity.
    
    Args:
        og: Original gravity (e.g., 1.050)
        fg: Final gravity (e.g., 1.010)
        
    Returns:
        Alcohol by volume as percentage
        
    Examples:
        >>> calculate_abv(1.050, 1.010)
        5.25
    """
    return (og - fg) * 131.25
```

**TypeScript:**
```typescript
/**
 * Fetch recipes from API
 * @param filters - Optional filter parameters
 * @returns Promise resolving to recipe array
 */
async function fetchRecipes(filters?: RecipeFilters): Promise<Recipe[]> {
  // Implementation
}
```

## 🔍 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn main:app --reload --port 8001
```

**Database Connection Failed:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql

# Check connection
psql hoppybrew_dev
```

**Module Not Found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check virtual environment is activated
which python  # Should show .venv path
```

**Frontend Build Errors:**
```bash
# Clear node modules and reinstall
rm -rf node_modules
yarn install

# Clear Nuxt cache
rm -rf .nuxt
yarn dev
```

## 📖 Additional Resources

- [Contributing Guide](../../CONTRIBUTING.md)
- [Architecture Documentation](../features/ARCHITECTURE.md)
- [API Reference](../../api_endpoint_catalog.md)
- [Testing Strategy](../../TESTING_STRATEGY.md)
- [Frontend Architecture](../../services/nuxt3-shadcn/FRONTEND_ARCHITECTURE.md)

## 🆘 Getting Help

- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Documentation: Search wiki
- Code Comments: Read inline documentation

---

**Last Updated**: November 8, 2025
