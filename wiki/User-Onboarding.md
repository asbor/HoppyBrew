# User Onboarding

This playbook gets new contributors and brewers productive quickly, from local setup to brewing workflows and automation integrations.

## Personas

| Persona | Goals | Primary Surfaces |
| --- | --- | --- |
| **Contributor** | Extend backend/front-end features, add diagrams, update docs | GitHub repo, wiki, PlantUML assets |
| **Brewer** | Manage recipes, track batches, monitor fermentation remotely | Nuxt UI, HomeAssistant dashboard |
| **Operator** | Deploy/upgrade stack, monitor health, enforce backups | Docker/Unraid, Cloudflare tunnel, PostgreSQL |

## First Day Checklist

1. **Clone & bootstrap**
   ```bash
   git clone https://github.com/asbor/HoppyBrew.git
   cd HoppyBrew
   cp .env.example .env
   docker-compose up -d --build
   ```
2. **Smoke test**
   - Visit http://localhost:3000 and confirm dashboard loads.
   - Open http://localhost:8000/docs and run `GET /health`.
3. **Load reference data**
   ```bash
   docker exec hoppybrew-backend alembic upgrade head
   docker exec hoppybrew-backend python /app/seeds/seed_all.py
   ```
4. **Explore seed content**
   - Recipes tab: review sample recipes and mash schedules.
   - Batches tab: walk through workflow states (Planning → Completed).
   - Inventory tab: adjust stock to see low-inventory warnings.

## Feature Walkthrough

1. **Recipe → Batch Flow**
   - Duplicate an existing recipe, tweak fermentable percentages, and press “Start Batch”.
   - Watch the batch appear in Planning; move it through each status to understand lifecycle hooks.
2. **Inventory Auto-linking**
   - When editing a recipe, use “Check Inventory” to ensure enough hops/fermentables exist.
   - Consume ingredients and verify the inventory quantities update.
3. **Calculators & Tools**
   - Visit `/tools` and run ABV/IBU/SRM calculators. Compare numbers against backend calculations via API.
4. **HomeAssistant Integration (optional)**
   - Copy the `sensor:` snippets from `homeassistant_config_example.yaml`.
   - Point `resource:` URLs to your running backend (Cloudflare tunnel or LAN IP).
   - Restart HomeAssistant and confirm sensors: `sensor.hoppybrew_active_batches`, `sensor.hoppybrew_last_brew_date`, etc.

## Developer Ramp-up

- Read `FRONTEND_ARCHITECTURE.md` and `services/backend/main.py` to grok design decisions.
- Update PlantUML diagrams when touching architecture—render via `scripts/render_plantuml_diagrams.py` and reference them in relevant wiki pages.
- Before opening a PR, run `make backend-test`, `yarn lint`, and the applicable Playwright suite.

## Troubleshooting FAQ

| Symptom | Fix |
| --- | --- |
| `docker-compose` stuck waiting for Postgres | `docker-compose logs db`; ensure volume permissions allow Postgres to initialize. |
| API returns 422 on recipe creation | Validate payload matches `Database/Schemas/recipes.py` (all nested ingredients need IDs). |
| PlantUML script fails on ERD aggregator files | Known limitation; edit the nested `.puml` files to remove extra `@startuml` if you need composite diagrams. |
| HomeAssistant sensors missing | Confirm backend reachable from HomeAssistant, inspect HA logs, and verify `/homeassistant/summary` returns JSON. |

## Beyond Day 1

- Join discussions in GitHub Issues/Projects for roadmap items.
- Record major sessions (design spikes, production incidents) in `documents/archive/sessions`.
- Keep this onboarding page updated with new workflows (e.g., Brew Day wizard, IoT ingestion).
