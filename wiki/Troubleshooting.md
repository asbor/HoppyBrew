# Troubleshooting Guide

Common issues and their solutions when working with HoppyBrew.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Docker Issues](#docker-issues)
- [Database Issues](#database-issues)
- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [Integration Issues](#integration-issues)
- [Performance Issues](#performance-issues)

---

## Installation Issues

### Docker Not Found

**Symptom:** `docker: command not found` or `docker-compose: command not found`

**Solution:**
```bash
# Check if Docker is installed
docker --version
docker-compose --version

# If not installed, install Docker Desktop (includes Compose)
# Visit: https://docs.docker.com/get-docker/

# Or install Docker Engine + Compose plugin on Linux
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Log out and back in for group membership to take effect
```

### Permission Denied (Docker)

**Symptom:** `permission denied while trying to connect to the Docker daemon socket`

**Solution:**
```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker

# Verify
docker ps
```

### Git Clone Fails

**Symptom:** `fatal: could not read Username` or authentication errors

**Solution:**
```bash
# Use HTTPS with token
git clone https://github.com/asbor/HoppyBrew.git

# Or use SSH (requires SSH key setup)
git clone git@github.com:asbor/HoppyBrew.git

# If repository is private, ensure you have access
# Generate GitHub personal access token: Settings > Developer settings > Tokens
```

---

## Docker Issues

### Port Already in Use

**Symptom:** `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution:**
```bash
# Find process using the port
lsof -i :8000
# Or on Linux without lsof
netstat -tulpn | grep 8000

# Kill the process
kill -9 <PID>

# Or change the port in docker-compose.yml
services:
  backend:
    ports:
      - "8001:8000"  # Host:Container
```

### Container Keeps Restarting

**Symptom:** Container status shows `Restarting` or exits immediately

**Solution:**
```bash
# Check container logs
docker-compose logs backend
docker logs hoppybrew-backend-1

# Common causes:
# 1. Database not ready - Add depends_on with health check
# 2. Missing environment variables - Check .env file
# 3. Port conflict - Change port mapping
# 4. Code error - Check logs for Python/Node errors

# View last 100 log lines
docker-compose logs --tail=100 backend

# Follow logs in real-time
docker-compose logs -f backend
```

### Cannot Connect to Database from Container

**Symptom:** `could not connect to server: Connection refused`

**Solution:**
```bash
# Check if database container is running
docker-compose ps

# Check database health
docker-compose logs db

# Verify network connectivity
docker exec hoppybrew-backend-1 ping db

# Check environment variables
docker exec hoppybrew-backend-1 env | grep DATABASE

# Ensure DATABASE_HOST uses service name, not localhost
DATABASE_HOST=db  # Not 'localhost' or '127.0.0.1'
```

### Disk Space Issues

**Symptom:** `no space left on device`

**Solution:**
```bash
# Check Docker disk usage
docker system df

# Remove unused images, containers, volumes
docker system prune -a --volumes

# Remove specific components
docker image prune
docker container prune
docker volume prune

# Check host disk space
df -h
```

### Image Build Fails

**Symptom:** `failed to solve` or build errors

**Solution:**
```bash
# Clear build cache
docker-compose build --no-cache

# Pull base images first
docker pull python:3.11-slim
docker pull node:20-alpine
docker pull postgres:latest

# Check Dockerfile syntax
# Verify requirements.txt and package.json exist

# Build with verbose output
docker-compose build --progress=plain
```

---

## Database Issues

### Connection Refused

**Symptom:** `psycopg2.OperationalError: could not connect to server`

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps db
# Should show "Up" with healthy status

# Test direct connection
psql -h localhost -U postgres -d hoppybrew_db
# Password: postgres (from .env)

# If using Docker, connect from backend container
docker exec -it hoppybrew-backend-1 bash
psql -h db -U postgres -d hoppybrew_db

# Check network
docker network ls
docker network inspect hoppybrew_my-network
```

### Migration Fails

**Symptom:** `alembic.util.exc.CommandError` or SQL errors during migration

**Solution:**
```bash
# Check current migration version
cd services/backend
alembic current

# View migration history
alembic history

# Rollback to previous version
alembic downgrade -1

# Or reset to base
alembic downgrade base

# Re-apply migrations
alembic upgrade head

# If migration file is corrupted, delete and recreate
rm alembic/versions/xxxxx_bad_migration.py
alembic revision --autogenerate -m "New migration"
```

### Database Locked (SQLite)

**Symptom:** `sqlite3.OperationalError: database is locked`

**Solution:**
```bash
# Only occurs in test mode with SQLite
# Ensure only one process accesses database

# Check for stale lock files
rm -f *.db-journal

# Use PostgreSQL for development instead
TESTING=0
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hoppybrew_db

# Or use WAL mode for SQLite (in config.py)
engine = create_engine('sqlite:///./hoppybrew.db', 
                      connect_args={"check_same_thread": False,
                                   "timeout": 30})
```

### Lost Database Data

**Symptom:** All data disappeared after restart

**Solution:**
```bash
# Check if volume was deleted
docker volume ls | grep hoppybrew

# Recreate volume if missing
docker-compose up -d db

# Always use named volumes in docker-compose.yml
volumes:
  postgres_data:  # Named volume persists data

# Backup database regularly
docker exec hoppybrew-db-1 pg_dump -U postgres hoppybrew_db > backup.sql

# Restore from backup
docker exec -i hoppybrew-db-1 psql -U postgres hoppybrew_db < backup.sql
```

---

## Backend Issues

### Import Errors

**Symptom:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
```bash
cd services/backend

# Ensure virtual environment is activated
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# If in Docker, rebuild container
docker-compose build backend

# Check Python path
python -c "import sys; print(sys.path)"

# Verify package is installed
pip list | grep <package-name>
```

### Uvicorn Won't Start

**Symptom:** `Error loading ASGI app` or `ModuleNotFoundError: No module named 'main'`

**Solution:**
```bash
# Ensure you're in the correct directory
cd services/backend

# Check main.py exists
ls -la main.py

# Try running directly
python -m uvicorn main:app

# Check for syntax errors
python -m py_compile main.py

# View full error
uvicorn main:app --reload --log-level debug
```

### API Returns 500 Errors

**Symptom:** All endpoints return `Internal Server Error`

**Solution:**
```bash
# Check backend logs
docker-compose logs backend

# Enable debug mode
# In main.py or config
DEBUG=True

# Check database connection
docker exec hoppybrew-backend-1 python -c "from database import engine; print(engine)"

# Verify environment variables
docker exec hoppybrew-backend-1 env

# Test endpoint directly
curl -v http://localhost:8000/health
```

### Alembic Can't Find Database

**Symptom:** `Can't locate revision identified by 'xxxxx'`

**Solution:**
```bash
# Check alembic.ini database URL
cat alembic.ini | grep sqlalchemy.url

# Override with environment variable
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/hoppybrew_db"

# Or edit alembic/env.py to use config.settings

# Stamp database with current version
alembic stamp head

# Or start fresh
alembic downgrade base
alembic upgrade head
```

---

## Frontend Issues

### Yarn Install Fails

**Symptom:** `error An unexpected error occurred`

**Solution:**
```bash
cd services/nuxt3-shadcn

# Clear cache
yarn cache clean

# Remove node_modules and lockfile
rm -rf node_modules yarn.lock

# Reinstall
yarn install

# If still fails, check Node version
node --version  # Should be 20+

# Install with verbose output
yarn install --verbose
```

### Dev Server Won't Start

**Symptom:** `Cannot find module '@nuxt/kit'` or similar

**Solution:**
```bash
# Clear Nuxt cache
rm -rf .nuxt .output

# Reinstall dependencies
rm -rf node_modules
yarn install

# Start with clean cache
yarn dev --clear

# Check port availability
lsof -i :3000

# Try different port
yarn dev --port 3001
```

### Hot Reload Not Working

**Symptom:** Changes don't appear without manual refresh

**Solution:**
```bash
# Check file watchers limit (Linux)
cat /proc/sys/fs/inotify/max_user_watches

# Increase limit
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Or set in nuxt.config.ts
export default defineNuxtConfig({
  vite: {
    server: {
      watch: {
        usePolling: true
      }
    }
  }
})

# Restart dev server
yarn dev
```

### API Calls Fail (CORS)

**Symptom:** `blocked by CORS policy` in browser console

**Solution:**
```bash
# Check frontend API configuration
# In nuxt.config.ts
runtimeConfig: {
  public: {
    apiBase: 'http://localhost:8000'  # Must match backend
  }
}

# Check backend CORS settings
# In services/backend/config.py
CORS_ORIGINS = ["http://localhost:3000"]

# Or allow all for development (not production!)
CORS_ORIGINS = ["*"]

# Restart both services
docker-compose restart backend frontend
```

### Build Fails

**Symptom:** `ERROR Cannot start nuxt: Failed to parse source` 

**Solution:**
```bash
# Clear caches
rm -rf .nuxt .output node_modules/.cache

# Check for TypeScript errors
yarn type-check

# Fix linting issues
yarn lint --fix

# Build with verbose output
yarn build --verbose

# Check for circular dependencies
npx madge --circular components/
```

---

## Integration Issues

### HomeAssistant Can't Connect

**Symptom:** REST sensor shows `unavailable` or `unknown`

**Solution:**
```yaml
# Verify URL in configuration.yaml
sensor:
  - platform: rest
    name: "Brewery Status"
    resource: http://192.168.1.100:8000/homeassistant/summary  # Use IP, not localhost
    scan_interval: 300
    
# Test endpoint manually
curl http://192.168.1.100:8000/homeassistant/summary

# Check HomeAssistant logs
# Settings > System > Logs

# Verify network connectivity
# HA must be able to reach HoppyBrew host

# Check firewall
sudo ufw allow 8000
```

### ISpindel Data Not Appearing

**Symptom:** Device connected but no readings

**Solution:**
```bash
# Check device endpoint configuration
# In ISpindel: http://your-ip:9501/ispindel

# Verify port is exposed in docker-compose.yml
services:
  backend:
    ports:
      - "9501:9501"

# Check device logs in HoppyBrew
curl http://localhost:8000/devices

# Test webhook manually
curl -X POST http://localhost:8000/ispindel \
  -H "Content-Type: application/json" \
  -d '{"name":"test","ID":123456,"token":"xxx","angle":25.5,"temperature":20.1,"battery":4.1,"gravity":1.050}'
```

---

## Performance Issues

### Slow API Response

**Symptom:** Requests take several seconds

**Solution:**
```bash
# Enable SQL query logging
# In database.py
engine = create_engine(url, echo=True)

# Check for N+1 queries
# Add eager loading in SQLAlchemy models
.options(joinedload(Recipe.hops))

# Add database indexes
alembic revision -m "Add indexes"
# In migration file:
op.create_index('idx_recipes_name', 'recipes', ['name'])

# Use connection pooling
# In database.py
engine = create_engine(url, pool_size=20, max_overflow=40)

# Monitor with pgAdmin or pg_stat_statements
```

### High Memory Usage

**Symptom:** Container uses excessive RAM

**Solution:**
```bash
# Limit container memory in docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M

# Check for memory leaks
docker stats

# Profile Python code
pip install memory-profiler
python -m memory_profiler main.py

# Reduce SQLAlchemy session scope
# Use scoped_session with proper cleanup
```

### Database Slow Queries

**Symptom:** Specific queries take long time

**Solution:**
```sql
-- Enable query statistics
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Analyze query plans
EXPLAIN ANALYZE SELECT * FROM recipes WHERE ...;

-- Add missing indexes
CREATE INDEX idx_batches_status ON batches(status);
CREATE INDEX idx_recipes_style_id ON recipes(style_id);

-- Update table statistics
ANALYZE recipes;
VACUUM ANALYZE;
```

---

## Still Stuck?

If your issue isn't covered here:

1. **Check Logs:**
   ```bash
   docker-compose logs -f --tail=100
   ```

2. **Search Issues:**
   - [Existing Issues](https://github.com/asbor/HoppyBrew/issues)
   - [Closed Issues](https://github.com/asbor/HoppyBrew/issues?q=is%3Aissue+is%3Aclosed)

3. **Ask for Help:**
   - [Discussions](https://github.com/asbor/HoppyBrew/discussions)
   - [Open New Issue](https://github.com/asbor/HoppyBrew/issues/new)

4. **Provide Information:**
   - OS and version
   - Docker version
   - Error messages and logs
   - Steps to reproduce
   - What you've tried already

---

**Last Updated:** 2025-01-15  
**Version:** 1.0.0
