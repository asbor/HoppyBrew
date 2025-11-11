# HoppyBrew Wiki

Welcome to the living documentation for the HoppyBrew platform. This wiki captures the current architecture, APIs, database schema, development workflow, deployment practices, and onboarding material for contributors and operators.

## Quick Links

- [Architecture](Architecture.md)
- [API Reference](API-Reference.md)
- [Database Schema](Database-Schema.md)
- [Frontend Component Guide](Frontend-Guide.md)
- [Development Guide](Development-Guide.md)
- [Deployment Guide](Deployment-Guide.md)
- [Troubleshooting](Troubleshooting.md)
- [User Onboarding](User-Onboarding.md)
- [Diagram Catalog](Diagram-Catalog.md)

## Platform Snapshot

| Layer | Technology | Notes |
| --- | --- | --- |
| UI | Nuxt 3 + shadcn-vue | SPA served from `services/nuxt3-shadcn` with composable-based data layer |
| API | FastAPI + Uvicorn | `services/backend` exposes resource-focused routers with OpenAPI tags |
| Data | PostgreSQL + SQLAlchemy | Migration-managed schema with seeders under `services/backend/seeds` |
| Messaging & Integrations | REST, HomeAssistant REST sensors, future MQTT tunnel | ISpindel telemetry, HomeAssistant dashboards, Cloudflare tunnel |
| Packaging | Docker / docker-compose | `docker-compose.yml` for local dev, `docker-compose.prod.yml` pattern for prod |
| Automation | Makefile, Alembic, pytest, Playwright | Shared CLI entry points for backend/frontend workflows |

## Getting Started

1. **Clone & configure**
   ```bash
   git clone https://github.com/asbor/HoppyBrew.git
   cd HoppyBrew
   cp .env.example .env
   ```
2. **Launch the stack**
   ```bash
   docker-compose up -d --build
   ```
3. **Open the apps**
   - Frontend: http://localhost:3000
   - API + docs: http://localhost:8000 / http://localhost:8000/docs
4. **Load demo data (optional)**
   ```bash
   docker exec hoppybrew-backend python /app/seeds/seed_all.py
   ```

## Documentation Map

| Page | What you will find |
| --- | --- |
| `Architecture.md` | System context, service boundaries, runtime/deployment diagrams, integration touch points |
| `API-Reference.md` | REST surface area grouped by tags, payload contracts, HomeAssistant integration patterns |
| `Database-Schema.md` | ERDs for ingredients, profiles, inventory plus normalization rules and migration strategy |
| `Frontend-Guide.md` | Nuxt 3 architecture, composable patterns, UI conventions, and quality gates |
| `Development-Guide.md` | Local environments, tooling, coding standards, and validation checklist |
| `Deployment-Guide.md` | Docker Compose scenarios, environment variables, secrets, and observability hooks |
| `User-Onboarding.md` | Role-specific onboarding, data seeding, HomeAssistant walkthrough, and troubleshooting |
| `Diagram-Catalog.md` | Direct PNG/SVG embeds for every rendered PlantUML asset categorized by domain |

## Diagram Workflows

All original `.puml` sources live in `documents/docs/plantuml`. Rendered PNG/SVG variants are generated with:

```bash
scripts/render_plantuml_diagrams.py
```

Outputs are written to `wiki/diagrams` (and mirrored under `documents/wiki-exports/diagrams`). See [Diagram Catalog](Diagram-Catalog.md) for the full gallery and regeneration instructions.

## Maintainers & Contributions

- Use `ROADMAP.md`, `TODO.md`, and GitHub Projects for prioritization.
- Follow the coding standards captured in `CONTRIBUTING.md` and `TESTING_STRATEGY.md`.
- Prefer documentation pull requests that update both the textual guidance and the relevant PlantUML diagram.
- When touching the database schema, add or update Alembic migrations plus ERD exports.

Please keep this wiki up to date when introducing structural changes—diagram updates, new endpoints, and deployment adjustments should all land here first.
