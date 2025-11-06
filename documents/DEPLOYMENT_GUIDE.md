# HoppyBrew Deployment Guide

## Overview

This guide covers deploying HoppyBrew in various environments, from local development to production self-hosted setups.

## Quick Start (Development)

```bash
# Clone the repository
git clone https://github.com/asbor/HoppyBrew.git
cd HoppyBrew

# Copy environment template
cp .env.example .env

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Environment Variables

### Required Variables

```bash
# Database Configuration
DATABASE_HOST=hoppybrew-db-1        # PostgreSQL host
DATABASE_PORT=5432                   # PostgreSQL port
DATABASE_NAME=hoppybrew_db          # Database name
DATABASE_USER=postgres               # Database user
DATABASE_PASSWORD=postgres           # Database password (CHANGE IN PRODUCTION!)

# Application Mode
TESTING=0                            # Set to 1 for testing mode (SQLite)
```

### Optional Variables

```bash
# Frontend
API_BASE_URL=http://localhost:8000  # Backend API URL

# Alembic
ALEMBIC_DATABASE_URL=postgresql://postgres:postgres@hoppybrew-db-1:5432/hoppybrew_db
```

## Deployment Scenarios

### 1. Local Development (Docker Compose)

**Recommended for**: Development, testing, quick demos

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

**Features**:
- Hot reload for frontend and backend
- Development server with detailed error messages
- Direct volume mounts for code changes
- SQLite option for faster iteration

### 2. Production Docker Compose

**Recommended for**: Self-hosted production on a single server

#### Production docker-compose.yml

Create `docker-compose.prod.yml`:

```yaml
version: "3.8"

services:
  backend:
    container_name: hoppybrew-backend
    build:
      context: ./services/backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    command: sh -c "cd /app && uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"
    depends_on:
      db:
        condition: service_healthy
    env_file:
      - .env.production
    networks:
      - hoppybrew-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    container_name: hoppybrew-db
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=${DATABASE_USER}
      - POSTGRES_PASSWORD=${DATABASE_PASSWORD}
      - POSTGRES_DB=${DATABASE_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - hoppybrew-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DATABASE_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  frontend:
    container_name: hoppybrew-frontend
    build:
      context: ./services/nuxt3-shadcn
      dockerfile: Dockerfile.prod
      args:
        - API_BASE_URL=${API_BASE_URL}
    ports:
      - "3000:3000"
    environment:
      - API_BASE_URL=${API_BASE_URL}
    networks:
      - hoppybrew-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

networks:
  hoppybrew-network:
    driver: bridge

volumes:
  postgres_data:
```

#### Deployment Steps

```bash
# 1. Create production environment file
cp .env.example .env.production
# Edit .env.production with production values

# 2. Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# 3. Run database migrations
docker exec hoppybrew-backend alembic upgrade head

# 4. (Optional) Seed initial data
docker exec hoppybrew-backend python /app/seeds/seed_all.py

# 5. Verify services
docker-compose -f docker-compose.prod.yml ps
```

### 3. Reverse Proxy with Nginx

**Recommended for**: Production with SSL/TLS, domain name

#### Nginx Configuration

```nginx
# /etc/nginx/sites-available/hoppybrew

upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name hoppybrew.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name hoppybrew.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/hoppybrew.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hoppybrew.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API Docs
    location /docs {
        proxy_pass http://backend/docs;
    }

    # Health checks
    location /health {
        proxy_pass http://backend/health;
        access_log off;
    }
}
```

#### Setup Steps

```bash
# 1. Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# 2. Obtain SSL certificate
sudo certbot --nginx -d hoppybrew.yourdomain.com

# 3. Enable site
sudo ln -s /etc/nginx/sites-available/hoppybrew /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 4. Update frontend API URL
# In .env.production:
API_BASE_URL=https://hoppybrew.yourdomain.com/api
```

### 4. Unraid Server

**Recommended for**: Home server enthusiasts using Unraid

#### Using Docker Compose

1. Install "Docker Compose Manager" plugin in Unraid
2. Copy your `docker-compose.yml` to `/mnt/user/appdata/hoppybrew/`
3. Use the Compose Manager UI to start the stack

#### Using Community Applications (Future)

*Note: HoppyBrew template for Unraid Community Applications is planned for Phase 5*

### 5. Kubernetes Deployment (Advanced)

**Recommended for**: Large-scale deployments, high availability

*Full Kubernetes deployment guide is planned for a future release. For now, the Docker Compose setup is recommended.*

## Post-Deployment Setup

### 1. Database Initialization

```bash
# Run migrations
docker exec hoppybrew-backend alembic upgrade head

# Seed initial data
docker exec hoppybrew-backend python seeds/seed_all.py
```

### 2. Create Admin User (When Auth is Implemented)

```bash
# This will be available in a future release
docker exec hoppybrew-backend python scripts/create_admin.py
```

### 3. Configure Backups

See [BACKUP_RESTORE_GUIDE.md](BACKUP_RESTORE_GUIDE.md) for backup setup.

### 4. Set Up Monitoring

```bash
# View application logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Check health endpoints
curl http://localhost:8000/health
```

## Production Checklist

- [ ] **Security**
  - [ ] Change default database password
  - [ ] Use strong passwords (20+ characters)
  - [ ] Enable SSL/TLS with valid certificates
  - [ ] Configure firewall rules
  - [ ] Disable unnecessary ports
  - [ ] Set up fail2ban (optional)

- [ ] **Database**
  - [ ] Configure automatic backups
  - [ ] Test restore procedure
  - [ ] Set up off-site backup storage
  - [ ] Monitor disk space

- [ ] **Application**
  - [ ] Set `TESTING=0` in environment
  - [ ] Remove `--reload` from uvicorn command
  - [ ] Configure proper logging
  - [ ] Set up log rotation
  - [ ] Configure CORS for your domain only

- [ ] **Monitoring**
  - [ ] Set up health check monitoring
  - [ ] Configure log aggregation
  - [ ] Set up alerts for failures
  - [ ] Monitor disk usage
  - [ ] Monitor database performance

- [ ] **Updates**
  - [ ] Document current version
  - [ ] Plan update schedule
  - [ ] Test updates in staging first
  - [ ] Have rollback plan ready

## Updating HoppyBrew

### Standard Update Procedure

```bash
# 1. Backup current installation
./backup_hoppybrew.sh

# 2. Pull latest changes
git pull origin main

# 3. Rebuild containers
docker-compose down
docker-compose up -d --build

# 4. Run migrations
docker exec hoppybrew-backend alembic upgrade head

# 5. Verify services
docker-compose ps
curl http://localhost:8000/health
```

### Rollback Procedure

```bash
# 1. Stop services
docker-compose down

# 2. Checkout previous version
git checkout <previous-tag>

# 3. Restore database
docker-compose up -d db
docker exec -i hoppybrew-db psql -U postgres -d hoppybrew_db < backup_latest.sql

# 4. Restart all services
docker-compose up -d
```

## Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Check disk space
df -h

# Check port conflicts
sudo netstat -tlnp | grep -E '3000|8000|5432'
```

### Database Connection Issues

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker exec hoppybrew-db psql -U postgres -d hoppybrew_db -c "SELECT 1;"
```

### Frontend Can't Connect to Backend

```bash
# Check API_BASE_URL is correct
docker-compose exec frontend env | grep API

# Check backend is accessible
curl http://localhost:8000/health

# Check network connectivity
docker-compose exec frontend ping backend
```

## Performance Tuning

### Database

```bash
# In docker-compose.yml, add to db service:
environment:
  - POSTGRES_SHARED_BUFFERS=256MB
  - POSTGRES_EFFECTIVE_CACHE_SIZE=1GB
  - POSTGRES_MAINTENANCE_WORK_MEM=128MB
  - POSTGRES_CHECKPOINT_COMPLETION_TARGET=0.9
  - POSTGRES_WAL_BUFFERS=16MB
  - POSTGRES_DEFAULT_STATISTICS_TARGET=100
  - POSTGRES_RANDOM_PAGE_COST=1.1
```

### Backend

```bash
# Increase workers for better concurrency
command: sh -c "uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"

# Or use gunicorn
command: sh -c "gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"
```

### Frontend

```bash
# Build for production (reduces size)
docker build -f Dockerfile.prod -t hoppybrew-frontend .
```

## Security Hardening

### 1. Use Docker Secrets (Docker Swarm)

```yaml
services:
  db:
    secrets:
      - db_password
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### 2. Limit Container Resources

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 3. Read-Only Filesystem

```yaml
services:
  backend:
    read_only: true
    tmpfs:
      - /tmp
```

## Support

For deployment issues:
1. Check the [troubleshooting section](#troubleshooting)
2. Review logs: `docker-compose logs`
3. Check [GitHub Issues](https://github.com/asbor/HoppyBrew/issues)
4. Read [ARCHITECTURE.md](../ARCHITECTURE.md) for system understanding

## Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Documentation](https://hub.docker.com/_/postgres)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
