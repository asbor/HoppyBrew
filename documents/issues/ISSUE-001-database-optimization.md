# ISSUE-001 Database Optimization and Performance Improvements

- **Branch**: `feature/database-optimization`
- **Owner**: Database Optimization Agent
- **Status**: Open
- **Related TODO**: Backend section top priority items
- **Created**: 2025-11-05

## Summary
Stabilise the backend data layer by fixing database connectivity, aligning ORM relationships with the domain model, and preparing for reliable migrations.

## Acceptance Criteria
- [ ] Replace the brittle PostgreSQL connection polling with a resilient health-check loop (`services/backend/database.py`).
- [ ] Update batch relationships and fixtures to match the new ORM models (`services/backend/api/endpoints/batches.py`, `services/backend/tests/test_endpoints/test_batches.py`).
- [ ] Make primary keys non-nullable and verify cascade rules to protect referential integrity.
- [ ] Produce at least one Alembic migration covering the relationship/index changes.

## Dependencies
- Coordinates with the Testing Agent for updated backend tests.
- Aligns with the Data/Automation Agent for beer style ingestion schema assumptions.

## Notes
- Ensure new migrations are idempotent for local development.
- Capture any follow-up cleanup in TODO.md once the branch is merged.
