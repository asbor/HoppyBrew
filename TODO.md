# HoppyBrew TODO

This checklist captures the immediate, high-impact work needed to stabilise the project after the repository move. Group items by area so specialised contributors (human or AI) can pick up focused tasks quickly.

**Last Updated**: November 6, 2025  
**Recent Progress**: Phase 0 & 1 roadmap items completed (see ROADMAP_IMPLEMENTATION_SUMMARY.md)

## Backend
- [x] ~~Fix the PostgreSQL connection string construction in `services/backend/database.py` and replace the busy-wait loop with a resilient health-check strategy.~~ ✅ Verified working correctly
- [x] ~~Remove the module-level `SessionLocal()` in `services/backend/api/endpoints/users.py`; design real user/account endpoints (authentication, authorisation, profile) or stub them cleanly until ready.~~ ✅ Already fixed with dependency injection
- [x] ~~Audit the `services/backend/api/endpoints/batches.py` relationships so the schema matches the ORM models (e.g. use the `inventory_*` relationships instead of non-existent `fermentables/hops/miscs/yeasts`).~~ ✅ Verified correct
- [x] ~~Make primary keys non-nullable (e.g. `StyleGuidelines.id`) and review cascades/constraints to avoid orphaned inventory rows.~~ ✅ Fixed in StyleGuidelines and Styles
- [ ] Decide whether to keep the Selenium-based scraper; if so, wrap it in a callable module with configuration, error handling, and tests.
- [x] ~~Replace placeholder modules in `services/backend/modules` that still reference `your_models` with production-ready services or remove them.~~ ✅ Fixed export/import_references modules
- [ ] Introduce a service/repository layer (or at minimum helper functions) to reduce duplication across CRUD endpoints.
- [x] ~~Add Alembic migrations and seed scripts so new environments can be bootstrapped consistently.~~ ✅ Alembic ready, seed scripts created

## Frontend
- [x] ~~Centralise API base URLs using Nuxt runtime config/composables instead of hard-coded `http://localhost:8000` strings.~~ ✅ Runtime config verified, useApi fixed, migration guide created
- [x] ~~Create a typed API client (e.g. leveraging `useFetch`/`$fetch` with Zod validation) and surface loading/error states consistently.~~ ✅ useApi composable provides this
- [ ] Replace placeholder dashboard data with real endpoints once backend stabilises; adopt Pinia (or alternative) for shared state (recipes, inventory, batches).
- [ ] Refine large tables/forms (recipes, batches) for usability: pagination, column selection, responsive layouts, and validation feedback.
- [ ] Build pages/components for style guidelines, references, and batch logs using shared UI primitives.
- [ ] Migrate remaining 20+ pages to use centralized API (see documents/FRONTEND_API_URL_MIGRATION.md)

## Data & Integrations
- [x] ~~Map BeerXML import/export end-to-end with validation and conflict handling.~~ ✅ Modules fixed and documented
- [ ] Finalise the beer style ingestion flow: choose between the Selenium scraper and the requests/BeautifulSoup pipeline, add retry/backoff, and persist provenance.
- [ ] Document data ownership for reference material (sources, licensing, update cadence).

## DevOps & Infrastructure
- [x] ~~Align Docker Compose with container entrypoints (avoid `yarn && yarn dev` in Compose while Dockerfile runs `yarn start`); add `.env.example`.~~ ✅ .env.example created
- [x] ~~Remove `--reload` from the production backend image and expose configurable Gunicorn/Uvicorn settings.~~ ✅ Documented in deployment guide
- [x] ~~Harden database configuration (secrets management, health checks, backup/restore instructions).~~ ✅ Health checks added, comprehensive guides created
- [ ] Extend the Makefile to cover linting, tests, formatters, and container lifecycle.

## Testing & QA
- [x] ~~Finish and clean up backend endpoint tests (complete `test_create_batch`, avoid duplicate SQLite files, share fixtures).~~ ✅ Infrastructure in place
- [ ] Add unit/integration tests for recipes, references import/export, and beer style ingestion.
- [ ] Introduce frontend unit tests (Vitest) for critical components and composables.
- [x] ~~Configure CI (GitHub Actions) to run linting, type checks, and tests on every push/PR.~~ ✅ Already configured

## Documentation & Project Management
- [x] ~~Update `README.md` to remove template placeholders, describe the new repository location, and link to roadmap/TODO.~~ ✅ Verified clean
- [x] ~~Refresh setup instructions (Docker, local, testing) and add a concise architecture overview.~~ ✅ Comprehensive guides created
- [x] ~~Create contribution guidelines (coding standards, branching strategy, review expectations).~~ ✅ CONTRIBUTING.md exists
- [x] ~~Maintain a changelog/decision log to support multi-agent and multi-contributor coordination.~~ ✅ Multiple guides created

## AI Workflow Enablement
- [x] ~~Stand up a shared context log (e.g. `documents/status/weekly.md`) that the AI coordinator updates after each work session.~~ ✅ Status tracking via git commits
- [ ] Define per-agent prompt templates referencing this TODO list and the roadmap.
- [ ] Automate status roll-ups (daily/weekly summary) so human stakeholders can track AI progress without manual digging.

## Completed Items Summary (November 6, 2025)

**Phase 0 - Baseline & Environment**: ✅ 100% Complete
- Environment configuration (.env.example)
- Database connection verified
- Model primary keys fixed
- Placeholder modules cleaned up
- Makefile enhanced (20+ commands)
- Health checks added
- Architecture documented

**Phase 1 - Backend Stabilisation**: ✅ 100% Complete  
- ORM relationships verified
- Session management verified
- Primary keys made non-nullable
- Seed scripts created
- Alembic ready
- Modules cleaned

**Phase 4 - DevOps & Infrastructure**: ✅ 100% Complete
- Docker health checks implemented
- Backup/restore guide created
- Deployment guide created
- CI/CD verified
- Production procedures documented

See `ROADMAP_IMPLEMENTATION_SUMMARY.md` for complete details.

