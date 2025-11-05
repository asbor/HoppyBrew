# ISSUE-004 Workspace Organization and Cleanup

- **Branch**: `feature/workspace-cleanup`
- **Owner**: Workspace Organization Agent
- **Status**: Open
- **Related TODO**: Documentation & Project Management + AI Workflow Enablement sections
- **Created**: 2025-11-05

## Summary
Streamline the repository structure, remove redundant artefacts, and ensure docs/sandbox files are easy to navigate for all agents.

## Acceptance Criteria
- [ ] Audit root-level clutter and archive outdated artefacts appropriately.
- [ ] Refresh README/setup guides to match the new repo layout alongside the Documentation Agent.
- [ ] Establish contribution guidelines referencing branch/commit standards.
- [ ] Confirm status logs and archival docs follow the manifest conventions.

## Dependencies
- Collaborates with Documentation Agent for shared files (README, setup guides).
- Coordinates with GitHub Agent before moving files that impact workflows.

## Notes
- Record any mass file moves in the status journal and notify other agents via their context files.
- Keep `.gitignore` aligned with workspace cleanup outcomes.
