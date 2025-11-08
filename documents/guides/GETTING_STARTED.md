# Getting Started with HoppyBrew

Welcome to HoppyBrew! This guide will help you get up and running quickly.

## 📋 Overview

HoppyBrew is a self-hosted brewing management application that helps homebrewers:
- Manage brewing recipes
- Track batches through fermentation
- Monitor inventory of ingredients
- Calculate brewing parameters
- Integrate with HomeAssistant

## 🚀 Quick Start

Choose your deployment method:

### Option 1: Docker (Recommended)
The easiest way to get started. See [Docker Deployment Guide](#docker-deployment).

### Option 2: Local Development
For development and testing. See [Local Development Setup](#local-development).

### Option 3: Unraid
For Unraid server users. See [Unraid Deployment](#unraid-deployment).

## 🐳 Docker Deployment

### Prerequisites
- Docker and Docker Compose installed
- 2GB RAM minimum
- PostgreSQL (included in compose file)

### Quick Deploy

1. **Clone the repository**
   ```bash
   git clone https://github.com/asbor/HoppyBrew.git
   cd HoppyBrew
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Using Pre-built Images

HoppyBrew provides pre-built images on DockerHub:

```yaml
version: '3.8'

services:
  db:
    image: postgres:latest
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: hoppybrew_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    image: <dockerhub_username>/hoppybrew-backend:latest
    ports:
      - "8000:8000"
    environment:
      DATABASE_HOST: db
      DATABASE_PORT: 5432
      DATABASE_NAME: hoppybrew_db
      DATABASE_USER: postgres
      DATABASE_PASSWORD: postgres
    depends_on:
      - db

  frontend:
    image: <dockerhub_username>/hoppybrew-frontend:latest
    ports:
      - "3000:3000"
    environment:
      API_BASE_URL: http://backend:8000
    depends_on:
      - backend

volumes:
  postgres_data:
```

See [DockerHub Setup Guide](../DOCKERHUB_SETUP.md) for details.

## 💻 Local Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL or SQLite
- Git

### Backend Setup

1. **Navigate to backend**
   ```bash
   cd services/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database**
   ```bash
   # PostgreSQL
   sudo apt install postgresql postgresql-contrib
   sudo -u postgres createdb hoppybrew_db
   
   # Or use SQLite (development only)
   export TESTING=1
   export TEST_DATABASE_URL=sqlite:///./hoppybrew.db
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Load sample data (optional)**
   ```bash
   python seeds/seed_sample_dataset.py
   ```

7. **Start backend**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd services/nuxt3-shadcn
   ```

2. **Install dependencies**
   ```bash
   yarn install
   ```

3. **Set up environment**
   ```bash
   # Create .env file
   echo "API_BASE_URL=http://localhost:8000" > .env
   ```

4. **Start development server**
   ```bash
   yarn dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000

## 🖥️ Unraid Deployment

### Installation

1. **Add Community Application**
   - Open Unraid's Community Applications
   - Search for "HoppyBrew"
   - Click Install

2. **Configure Container**
   - Set database credentials
   - Map ports (default: 3000 for frontend, 8000 for backend)
   - Configure volumes for persistent data

3. **Start Container**
   - Click Start to launch HoppyBrew
   - Access via http://[UNRAID-IP]:3000

For detailed Unraid setup, see the [Unraid Template](#) (coming soon).

## 📊 Sample Data

To explore HoppyBrew with sample data:

```bash
# Using SQLite (quick demo)
TESTING=1 TEST_DATABASE_URL=sqlite:///./hoppybrew_demo.db \
  python seeds/seed_sample_dataset.py

# Or with running Docker container
docker exec hoppybrew-backend python /app/seeds/seed_sample_dataset.py
```

This loads:
- 10 sample recipes (various beer styles)
- 4 sample batches (different stages)
- Ingredient inventory
- Equipment profiles
- Water profiles

## 🔧 Configuration

### Environment Variables

Key environment variables (see `.env.example`):

```bash
# Database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=hoppybrew_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres

# Frontend
API_BASE_URL=http://localhost:8000

# Application
DEBUG=false
LOG_LEVEL=info
```

### Customization

- **Theme**: Edit `services/nuxt3-shadcn/app.vue` for theme settings
- **Features**: See [ROADMAP.md](../ROADMAP.md) for upcoming features
- **Integration**: Configure HomeAssistant in settings (see [HomeAssistant Integration](../features/HOMEASSISTANT_INTEGRATION.md))

## 🧪 Verify Installation

1. **Check backend health**
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status":"healthy"}
   ```

2. **Check frontend**
   - Visit http://localhost:3000
   - You should see the HoppyBrew dashboard

3. **Test API**
   - Visit http://localhost:8000/docs
   - Try the "Try it out" feature on any endpoint

## 📚 Next Steps

Now that you're up and running:

1. **Explore the Interface**
   - Browse recipes
   - Check inventory
   - View brewing tools

2. **Create Your First Recipe**
   - Go to Recipes → New Recipe
   - Follow the recipe wizard

3. **Start a Batch**
   - Select a recipe
   - Click "Start Batch"
   - Track fermentation progress

4. **Read the Documentation**
   - [User Guide](USER_GUIDE.md) - Detailed usage instructions
   - [API Reference](../../api_endpoint_catalog.md) - For developers
   - [Architecture](../features/ARCHITECTURE.md) - System design

## ❓ Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Change ports in docker-compose.yml or .env
# Frontend: 3000 → 3001
# Backend: 8000 → 8001
```

**Database Connection Failed**
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify credentials in `.env`
- Check DATABASE_HOST (use `host.docker.internal` for Docker on Mac/Windows)

**Frontend Can't Reach Backend**
- Verify API_BASE_URL in frontend `.env`
- Check backend is running: `curl http://localhost:8000/health`
- Check CORS settings in backend

### Getting Help

- **Documentation**: Search this wiki
- **Issues**: [GitHub Issues](https://github.com/asbor/HoppyBrew/issues)
- **Discussions**: [GitHub Discussions](https://github.com/asbor/HoppyBrew/discussions)

## 🤝 Contributing

Want to contribute? Great!

1. Read [CONTRIBUTING.md](../../CONTRIBUTING.md)
2. Check [TODO.md](../../TODO.md) for tasks
3. Submit a Pull Request

---

**Last Updated**: November 8, 2025  
**Version**: 1.0.0
