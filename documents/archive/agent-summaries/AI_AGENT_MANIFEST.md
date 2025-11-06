# HoppyBrew Multi-Agent Manifest

This manifest codifies how AI (and human) contributors collaborate on HoppyBrew. Keep the scope for each agent tight to avoid inflated context, and rely on the coordinator for cross-domain decisions.

## Shared Ground Rules
- **Source of truth**: `ROADMAP.md` (strategy) + `TODO.md` (execution backlog). Update these before or immediately after substantial work.
- **Status logging**: The coordinator maintains rolling notes in `documents/status/` (create as needed). Every session ends with a short delta summary and next-step pointers.
- **Branching**: One task/branch per change-set; avoid mixing frontend/backend workstreams. Reference TODO items or GitHub issues in branch names/PRs.
- **Quality gates**: Tests must pass locally. Run formatters/linting when available; record missing tooling in TODO if gaps exist.

## Roles & Responsibilities

### 1. Coordinator (Orchestrator)
- Curate roadmap priorities and convert them into task briefs.
- Assign briefs to specialised agents, ensuring overlapping context is minimised.
- Review delivered changes, reconcile conflicts, and update TODO/Roadmap/status logs.
- Surface risks, open questions, or dependency blockers to human stakeholders.
- Deliver weekly executive summary (links to PRs, metrics, blockers).

### 2. Backend/API Agent
- Implement FastAPI endpoints, domain services, and SQLAlchemy models/migrations.
- Ensure environment configuration (`.env`, Docker) remains consistent.
- Extend backend test coverage; add fixtures and factories when needed.
- Produce concise change notes (routes touched, migrations added).

### 3. Frontend/UX Agent
- Develop Nuxt 3 components/pages and shared composables.
- Wire UI to backend via typed API client; handle loading/error states gracefully.
- Maintain visual consistency (Shadcn/Tailwind conventions) and update Storybook/examples if added.
- Capture screenshots or describe UX changes for review.

### 4. Data/Automation Agent
- Manage BeerXML import/export pipelines and BJCP style ingestion jobs.
- Own data validation, deduplication, and provenance tracking.
- Coordinate schema changes with backend agent; provide sample files/tests.

### 5. DevOps/SRE Agent
- Maintain Dockerfiles, Compose stack, CI workflows, and deployment docs.
- Implement observability (structured logging, health checks).
- Guard secrets handling and produce runbooks for ops tasks (backup/restore).

### 6. QA & Tooling Agent
- Expand automated testing (backend pytest, frontend Vitest/cypress when ready).
- Introduce linting, type-checking, and coverage reporting.
- Monitor CI health and create follow-up tasks when new flakes/bugs appear.

### 7. Documentation Agent
- Keep README, setup guides, ADRs, and user/operator docs current.
- Generate release notes and cross-link tutorials/screenshots.
- Standardise terminology via the existing glossary and update as new concepts emerge.

## Collaboration Lifecycle
1. **Planning**: Coordinator reviews roadmap/TODO, selects sprint goals, and drafts briefs (context, files, acceptance criteria).
2. **Execution**: Specialised agent claims a brief, works within its scope, and records interim notes in `documents/status/YYYY-MM-DD.md`.
3. **Integration**: Agent opens PR (or provides diff) + summary. Coordinator verifies alignment, resolves conflicts, merges, and updates backlog/docs.
4. **Retrospective**: Coordinator produces weekly summary (wins, blockers, metrics) and flags any structural changes needed in process/tooling.

## Brief Template (for Coordinator)
```
### Task
<short title>

### Context
- Repository areas/files:
- Related TODO/Roadmap items:
- Known constraints:

### Acceptance Criteria
- [ ]
- [ ]

### Deliverables
- Code/docs/tests + status log update.
- Review notes or follow-up tickets if scope exceeds brief.
```

Store issued briefs in `documents/status/` alongside status updates so future agents can audit decision history.

## Getting Started Checklist for New Agents
1. Read `ROADMAP.md`, `TODO.md`, `Project Setup Guide.md`, and this manifest.
2. Run local setup (Docker Compose or manual) and confirm backend/frontend health.
3. Sync with coordinator via latest status log to avoid duplicate work.
4. Before finishing, update relevant docs and leave a short note for the next agent about remaining risks or follow-ups.

Maintaining discipline around this manifest keeps the project manageable even with many contributors and limited context windows.
