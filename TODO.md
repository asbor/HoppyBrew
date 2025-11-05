# HoppyBrew TODO

This checklist captures the immediate, high-impact work needed to stabilise the project after the repository move. Group items by area so specialised contributors (human or AI) can pick up focused tasks quickly.

## Backend
- [ ] Fix the PostgreSQL connection string construction in `services/backend/database.py` and replace the busy-wait loop with a resilient health-check strategy.
- [ ] Remove the module-level `SessionLocal()` in `services/backend/api/endpoints/users.py`; design real user/account endpoints (authentication, authorisation, profile) or stub them cleanly until ready.
- [ ] Audit the `services/backend/api/endpoints/batches.py` relationships so the schema matches the ORM models (e.g. use the `inventory_*` relationships instead of non-existent `fermentables/hops/miscs/yeasts`).
- [ ] Make primary keys non-nullable (e.g. `StyleGuidelines.id`) and review cascades/constraints to avoid orphaned inventory rows.
- [ ] Decide whether to keep the Selenium-based scraper; if so, wrap it in a callable module with configuration, error handling, and tests.
- [ ] Replace placeholder modules in `services/backend/modules` that still reference `your_models` with production-ready services or remove them.
- [ ] Introduce a service/repository layer (or at minimum helper functions) to reduce duplication across CRUD endpoints.
- [ ] Add Alembic migrations and seed scripts so new environments can be bootstrapped consistently.

## Frontend
- [ ] Centralise API base URLs using Nuxt runtime config/composables instead of hard-coded `http://localhost:8000` strings.
- [ ] Create a typed API client (e.g. leveraging `useFetch`/`$fetch` with Zod validation) and surface loading/error states consistently.
- [ ] Replace placeholder dashboard data with real endpoints once backend stabilises; adopt Pinia (or alternative) for shared state (recipes, inventory, batches).
- [ ] Refine large tables/forms (recipes, batches) for usability: pagination, column selection, responsive layouts, and validation feedback.
- [ ] Build pages/components for style guidelines, references, and batch logs using shared UI primitives.

## Data & Integrations
- [ ] Map BeerXML import/export end-to-end with validation and conflict handling.
- [ ] Finalise the beer style ingestion flow: choose between the Selenium scraper and the requests/BeautifulSoup pipeline, add retry/backoff, and persist provenance.
- [ ] Document data ownership for reference material (sources, licensing, update cadence).

## DevOps & Infrastructure
- [ ] Align Docker Compose with container entrypoints (avoid `yarn && yarn dev` in Compose while Dockerfile runs `yarn start`); add `.env.example`.
- [ ] Remove `--reload` from the production backend image and expose configurable Gunicorn/Uvicorn settings.
- [ ] Harden database configuration (secrets management, health checks, backup/restore instructions).
- [ ] Extend the Makefile to cover linting, tests, formatters, and container lifecycle.

## Testing & QA
- [ ] Finish and clean up backend endpoint tests (complete `test_create_batch`, avoid duplicate SQLite files, share fixtures).
- [ ] Add unit/integration tests for recipes, references import/export, and beer style ingestion.
- [ ] Introduce frontend unit tests (Vitest) for critical components and composables.
- [ ] Configure CI (GitHub Actions) to run linting, type checks, and tests on every push/PR.

## Documentation & Project Management
- [ ] Update `README.md` to remove template placeholders, describe the new repository location, and link to roadmap/TODO.
- [ ] Refresh setup instructions (Docker, local, testing) and add a concise architecture overview.
- [ ] Create contribution guidelines (coding standards, branching strategy, review expectations).
- [ ] Maintain a changelog/decision log to support multi-agent and multi-contributor coordination.

## AI Workflow Enablement
- [ ] Stand up a shared context log (e.g. `documents/status/weekly.md`) that the AI coordinator updates after each work session.
- [ ] Define per-agent prompt templates referencing this TODO list and the roadmap.
- [ ] Automate status roll-ups (daily/weekly summary) so human stakeholders can track AI progress without manual digging.

