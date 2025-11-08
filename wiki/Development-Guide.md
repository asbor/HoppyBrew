# Development Guide

This guide documents the repeatable workflow for contributing to HoppyBrew across backend and frontend codebases.

## Prerequisites

| Tool | Version | Notes |
| --- | --- | --- |
| Python | 3.11+ | Backend (FastAPI, Alembic, pytest) |
| Node.js | 18+ & npm/yarn | Nuxt 3 frontend |
| Docker / docker-compose | latest | Local orchestration, production parity |
| Java | 11+ | PlantUML rendering via `tools/plantuml-1.2024.3.jar` |

Clone the repository and copy the environment template:

```bash
git clone https://github.com/asbor/HoppyBrew.git
cd HoppyBrew
cp .env.example .env
```

## Backend Workflow (`services/backend`)

```bash
cd services/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Key commands:

| Action | Command |
| --- | --- |
| Run API locally | `uvicorn main:app --reload --port 8000` |
| Run unit tests | `pytest` or `make backend-test` |
| Format/lint | `black .`, `flake8 .`, or `make backend-format` |
| Generate migration | `alembic revision --autogenerate -m "describe change"` |
| Apply migrations | `alembic upgrade head` or `make db-upgrade` |
| Seed data | `python seeds/seed_all.py` |

Keep schemas (`Database/Schemas`) and models (`Database/Models`) aligned whenever fields change.

## Frontend Workflow (`services/nuxt3-shadcn`)

```bash
cd services/nuxt3-shadcn
yarn install
yarn dev --open
```

Commands:

| Action | Command |
| --- | --- |
| Development server | `yarn dev` (http://localhost:3000) |
| Unit tests | `yarn test:unit` |
| E2E tests | `yarn test:e2e` (Playwright) |
| Build | `yarn build && yarn preview` |
| Lint | `yarn lint` |

Composables (`composables/`) are the only place that should make HTTP calls. Ensure new routes have matching composables and Vitest coverage.

## Full-stack via Docker Compose

```bash
docker-compose up -d --build
```

- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Database: `postgres://postgres:postgres@hoppybrew-db-1:5432/hoppybrew_db`

Use `docker-compose logs -f backend` during debugging and `docker-compose down -v` for a clean slate.

## Data Seeding

1. Run migrations (`alembic upgrade head`).
2. Populate lookup/reference data:
   ```bash
   python modules/import_references.py
   python seeds/seed_all.py
   ```
3. Optional: load demo batches/recipes via `data/` exports.

## PlantUML Pipeline

All diagrams live in `documents/docs/plantuml`. Render the PNG/SVG catalog whenever diagrams change:

```bash
scripts/render_plantuml_diagrams.py
```

- Outputs land in `documents/wiki-exports/diagrams` and are mirrored into `wiki/diagrams` for GitHub publishing.
- Four aggregate ERDs (`ERD.puml`, `Inventory.puml`, `Recipie.puml`, `Fermentable.puml`) currently require manual cleanup due to nested `@startuml` blocks.

## Quality Gates

1. **Static analysis** – `make backend-lint`, `yarn lint`, Tailwind conventions.
2. **Unit tests** – `pytest`, `vitest`.
3. **E2E** – `yarn test:e2e` (Playwright) plus optional API smoke tests via `scripts/ci_smoke.sh` (coming soon).
4. **Formatting** – `black`, `isort`, Prettier, ESLint autofix.
5. **Docs** – Update this wiki + diagrams for any architecture/API change. Include reproduction steps when fixing production bugs.

## Useful Shortcuts

| Goal | Command |
| --- | --- |
| Rebuild everything | `make reinstall` |
| Generate PDF docs | `make pdf` |
| Run backend + frontend dev servers concurrently | `tmux`/`zellij` or `npm-run-all` (scripts coming in `tools/`). |
| Tail logs | `docker-compose logs -f backend` or hit `/logs` endpoint |

## Troubleshooting

- **Port conflicts** – free ports 3000/8000/5432 or change them via `.env` + compose overrides.
- **Migrations failing** – ensure Postgres is healthy (`docker ps`, `pg_isready`). Delete volumes (`docker-compose down -v`) only if you can afford data loss.
- **Node dependencies** – remove `node_modules` + `.nuxt`, then re-run `yarn install`.
- **Playwright** – run `npx playwright install --with-deps` inside `services/nuxt3-shadcn` if browsers are missing.

Document any additional edge cases directly in this page or link to dedicated runbooks in `documents/archive/sessions`.
