# HoppyBrew Roadmap (Post-Migration)

This roadmap outlines how to evolve HoppyBrew from its semester-project baseline into a production-ready, self-hosted brewing management platform. Timelines are indicative (assuming part-time focus across mixed human/AI contributors); adjust once team capacity is firm.

## Current State Snapshot
- FastAPI backend provides broad CRUD coverage but needs refactoring: environment config is brittle, some routes reference non-existent relationships, and several modules remain placeholders.
- Nuxt 3 frontend renders rich UI components yet still consumes mock/local data, lacks centralised API access, and needs state management.
- Data ingestion (BeerXML import, BJCP style scraping) exists as scripts but is not integrated or tested.
- Docker Compose works for local dev, though frontend/backend commands drift and secrets handling is manual.
- Automated testing, linting, and CI are minimal; documentation still references the original course repository.

## Guiding Principles
- Stabilise foundations before adding features; prefer incremental refactors backed by tests.
- Treat the API schema as the contract between backend and frontend—document and enforce it.
- Optimise for self-hosted deploys: deterministic setup, observable services, graceful degradation without external SaaS.
- Use the AI agent network to parallelise work but keep a single source of truth (this roadmap, TODO list, status logs).

## Phase 0 – Baseline & Environment (Week 1)
**Goals**
- Fix critical bugs preventing reliable local/dev deployments.
- Establish observability into the current code so subsequent work is measurable.

**Key actions**
- Repair PostgreSQL connection string handling, confirm migrations/migrations strategy, and eliminate blocking database polling loops.
- Remove template/config placeholders in README and setup docs; publish `.env.example`.
- Audit and prune dead code (placeholder modules, scripts that run on import).
- Capture a “current architecture” snapshot (system diagram, API inventory) for the coordinator.

## Phase 1 – Backend Stabilisation (Weeks 2–4)
**Goals**
- Harden domain models, services, and data integrity.
- Provide reliable APIs for core entities (recipes, batches, inventory, references, style guides, users).

**Key actions**
- Align ORM relationships with schemas; add missing relationships or adjust queries (e.g. batch inventory loaders).
- Introduce application services/helpers to reduce endpoint duplication and centralise validation.
- Implement proper user/account flows (auth skeleton, RBAC hooks) or explicitly defer them with clean stubs.
- Establish Alembic migrations and seed data covering demo users, sample recipes, BJCP styles.
- Expand backend test coverage (unit + API) and prepare contract tests for frontend use.

## Phase 2 – Frontend Integration & UX (Weeks 3–6)
**Goals**
- Connect UI to live APIs with robust error/loading handling.
- Improve usability for large datasets (recipes, inventory) and support batch operations.

**Key actions**
- Create a typed API client wrapping Nuxt runtime config; migrate pages away from ad-hoc `fetch` calls.
- Adopt Pinia (or equivalent) for shared state and caching; add optimistic updates and pagination components.
- Replace placeholder dashboards with meaningful metrics sourced from backend endpoints.
- Iterate on critical flows: recipe creation/editing, batch management, inventory tracking, reference browsing.
- Add component/unit tests (Vitest) and visual regression (if feasible).

## Phase 3 – Data Automation & Integrations (Weeks 5–8)
**Goals**
- Support import/export workflows and automated data refreshes.
- Ensure data provenance and licensing compliance.

**Key actions**
- Finalise BeerXML import/export pipeline with validation, deduplication, and user feedback.
- Refactor beer style ingestion into an idempotent job (requests/BeautifulSoup preferred, Selenium optional) with retry/backoff.
- Persist scrape metadata (source URL, timestamp, checksum) for auditability.
- Explore optional integrations (e.g. Tilt hydrometers, fermentation controllers) and design API hooks for future hardware support.

## Phase 4 – DevOps, Security & Observability (Weeks 6–9)
**Goals**
- Make deployments reproducible and monitorable.
- Protect user data and ensure recoverability.

**Key actions**
- Harmonise Docker images/Compose (production-ready commands, health checks, volumes, backups).
- Introduce logging/metrics stack (OpenTelemetry exporter, structured logs, basic dashboards).
- Configure CI/CD (GitHub Actions) with gated merges (lint, tests, type checks, container build).
- Document backup/restore, update, and roll-back procedures for self-hosted operators.
- Conduct a lightweight security review (dependency scanning, auth model, rate limits).

## Phase 5 – Productisation & Stretch Targets (Week 8+)
**Goals**
- Deliver polished features for long-term operation and community adoption.

**Key actions**
- Implement advanced analytics (brew session insights, inventory forecasting).
- Add collaboration features (multi-user support, activity feeds, permissions).
- Package the application for alternative deployments (Helm chart, Unraid template, Docker Hub images).
- Launch public documentation site (e.g. Docusaurus/GitBook) fed from project docs.

## Cross-Cutting Streams
- **Documentation & Knowledge Sharing**: Keep `SUMMARY.md`, roadmap, and TODO current; maintain ADRs for significant decisions.
- **Quality & Compliance**: Enforce formatting/linting, run security scans, review licensing for imported data/branding.
- **Community & Feedback**: Collect structured feedback (issues, discussions), publish release notes, and plan increments accordingly.

## AI Agent Collaboration Plan
Leverage multiple specialised AI agents orchestrated by a coordinator to manage scope without overwhelming context windows.

| Role | Core Responsibilities | Preferred Inputs | Expected Outputs |
| --- | --- | --- | --- |
| **AI Coordinator (Architect/PM)** | Maintain roadmap/TODO, prioritise work, summarise progress, assign tasks to sub-agents, ensure consistency. | Latest roadmap/TODO, status log, open issues, PR summaries. | Updated plan, delegation briefs, integration notes, weekly summaries. |
| **Backend/API Agent** | Implement FastAPI services, ORM models, migrations, backend tests. | Specific endpoint specs, DB schema, failing tests, backend portion of TODO. | PR-ready diffs, migration scripts, API docs changelog. |
| **Frontend/UX Agent** | Build Nuxt components, integrate API client, enforce design system. | Component specs, API contracts, UX feedback. | Component implementations, stories/tests, UI integration notes. |
| **Data/Automation Agent** | Manage BeerXML handling, scraping, data quality checks. | Data source definitions, import/export requirements, sample files. | ETL scripts/services, validation reports, ingestion schedules. |
| **DevOps/SRE Agent** | Docker images, CI/CD, monitoring, secrets management. | Deployment requirements, infra constraints, build logs. | Updated Docker/compose files, CI workflows, runbooks. |
| **QA & Tooling Agent** | Expand automated tests, set up linting/static analysis, measure coverage. | Test plans, failure cases, coverage reports. | Test suites, CI hooks, quality dashboards. |
| **Documentation Agent** | Keep README, guides, and change logs current; produce user/admin docs. | Feature changes, screenshots, release notes. | Markdown updates, diagrams, knowledge base sync. |

**Collaboration Protocol**
1. Coordinator reviews roadmap/TODO, selects priority items, and drafts briefs referencing relevant files and acceptance criteria.
2. Coordinator hands briefs to specialised agents; each agent limits context to their domain plus the brief.
3. Agents deliver diffs or documentation plus a short summary; coordinator performs integration review, resolves conflicts, and updates roadmap/TODO/status logs.
4. Coordinator publishes a daily/weekly summary for human stakeholders and archives context excerpts for future sessions.

**Tooling Suggestions**
- Maintain `documents/status/` with dated logs authored by the coordinator.
- Use a shared glossary/ADR folder (existing architecture docs can seed this).
- Automate notifications (GitHub issues/PRs tagged by agent role) so progress remains transparent.

By following this roadmap and collaboration model, HoppyBrew can transition from a course project into a sustainable, extensible platform for the homebrewing community.
