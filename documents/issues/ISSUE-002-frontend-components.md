# ISSUE-002 Frontend Component Reusability and Performance

- **Branch**: `feature/frontend-components`
- **Owner**: Frontend Component Agent
- **Status**: Open
- **Related TODO**: Frontend section items 1-4
- **Created**: 2025-11-05

## Summary
Modernise core UI building blocks to consume backend APIs consistently and deliver responsive management views for recipes, batches, and style guides.

## Acceptance Criteria
- [ ] Centralise API configuration using Nuxt runtime config/composables.
- [ ] Introduce a typed API client with error/loading state helpers shared across pages.
- [ ] Replace placeholder dashboard data with live endpoints and Pinia-backed state.
- [ ] Refine large tables/forms for responsiveness and validation feedback.

## Dependencies
- Backend fixes for batches and style guideline endpoints (Database Agent).
- Testing Agent support for new frontend unit coverage.

## Notes
- Coordinate with Workspace Agent before reorganising component directories.
- Log any UX decisions in the status journal for review.
