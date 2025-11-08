# Deployment Guide

This guide consolidates the instructions from `documents/DEPLOYMENT_GUIDE.md`, the Docker assets, and the PlantUML deployment diagrams.

## Supported Targets

1. **Local development** – `docker-compose.yml`
2. **Single-node production** – custom `docker-compose.prod.yml`
3. **Unraid + Cloudflare Tunnel** – matches the PlantUML deployment diagram
4. **HomeAssistant integration** – consumes the public API via Cloudflare Access or VPN

![Deployment](diagrams/misc/d.png)

## Environment Variables

Minimal configuration (`.env` / `.env.production`):

```ini
DATABASE_HOST=hoppybrew-db-1
DATABASE_PORT=5432
DATABASE_NAME=hoppybrew_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres   # change in prod!
TESTING=0
API_BASE_URL=http://localhost:8000  # injected into Nuxt build
ALEMBIC_DATABASE_URL=postgresql://postgres:postgres@hoppybrew-db-1:5432/hoppybrew_db
```

Use distinct secrets per environment and store them in your secret manager (1Password, Vault, Docker/Compose env files).

## Local Development (Compose)

```bash
docker-compose up -d --build
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API docs: http://localhost:8000/docs
```

Common tasks:

| Task | Command |
| --- | --- |
| Tail logs | `docker-compose logs -f backend` |
| Recreate services | `docker-compose down && docker-compose up -d --build` |
| Reset volumes | `docker-compose down -v` |
| Run migrations | `docker exec hoppybrew-backend alembic upgrade head` |
| Seed data | `docker exec hoppybrew-backend python /app/seeds/seed_all.py` |

## Production Compose

Create `docker-compose.prod.yml` (see `documents/DEPLOYMENT_GUIDE.md` for full example):

```yaml
services:
  backend:
    build: ./services/backend
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
    env_file: .env.production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  frontend:
    build:
      context: ./services/nuxt3-shadcn
      dockerfile: Dockerfile.prod
      args: ["API_BASE_URL=${API_BASE_URL}"]
    ports: ["3000:3000"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      retries: 3
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${DATABASE_USER}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
      POSTGRES_DB: ${DATABASE_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

Deployment steps:

```bash
cp .env.example .env.production
# Update secrets, API base URL, and allowed origins

docker-compose -f docker-compose.prod.yml up -d --build

docker exec hoppybrew-backend alembic upgrade head
# Optional seed
# docker exec hoppybrew-backend python /app/seeds/seed_all.py
```

## Reverse Proxy & TLS

Use Nginx or Caddy in front of the compose stack or rely on Cloudflare Tunnel:

```nginx
server {
  listen 80;
  server_name hoppybrew.domain.com;
  location / {
    proxy_pass http://localhost:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
  location /api/ {
    proxy_pass http://localhost:8000/;
  }
}
```

Cloudflare Zero Trust can terminate TLS, enforce device posture, and publish only `/homeassistant/*` endpoints externally.

## Operations Checklist

| Concern | Checks |
| --- | --- |
| Health | `/health` endpoint, docker health checks, HomeAssistant summary sensor |
| Logs | `/logs` endpoint + `docker logs hoppybrew-backend` |
| Backups | Regular `pg_dump` of `postgres_data` volume; schedule in Unraid or cron |
| Updates | `git pull && docker-compose build --pull` or CI-published Docker tags |
| Monitoring | Expose Prometheus-friendly metrics (future). Today use HomeAssistant sensors and Compose health.

## Disaster Recovery

1. Snapshot `postgres_data` volume.
2. Export `.env.production` and compose files.
3. Restore by running `docker-compose -f docker-compose.prod.yml up -d` on a new host and copying the volume contents back.

## HomeAssistant Publishing

- Ensure the API is reachable from your HomeAssistant instance (via Cloudflare Access, VPN, or LAN).
- Copy the snippets from `homeassistant_config_example.yaml` into your `configuration.yaml`.
- Restart HomeAssistant and confirm sensors appear (`/homeassistant/summary`, `/homeassistant/batches`).

## Maintenance Windows

- Put the frontend into “maintenance mode” via Cloudflare Access or Nginx 503 responses while running migrations that break contracts.
- Communicate schema-impacting changes via this wiki and `CHANGELOG.md`.
