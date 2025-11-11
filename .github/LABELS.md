# Label Taxonomy & Usage Guidelines

This document defines the label system used in the HoppyBrew issue tracker to maintain consistency and clarity.

## Label Categories

### 1. Type Labels
Define what kind of issue/PR this is:

| Label | Description | Color | Use When |
|-------|-------------|-------|----------|
| `bug` | Something isn't working | `#d73a4a` | Reporting broken functionality |
| `feature` | New feature or request | `#a2eeef` | Proposing new capabilities |
| `enhancement` | Improvement to existing feature | `#84b6eb` | Suggesting improvements |
| `documentation` | Documentation improvements | `#0075ca` | Docs need updating |
| `performance` | Performance optimization | `#ff9800` | Speed or efficiency issues |
| `refactoring` | Code refactoring | `#fbca04` | Code quality improvements |
| `security` | Security-related issue | `#ee0701` | Security vulnerabilities |
| `dependencies` | Dependency updates | `#0366d6` | Package updates |
| `infrastructure` | DevOps, CI/CD, deployment | `#0e8a16` | Infrastructure changes |

### 2. Priority Labels
Indicate urgency and importance:

| Label | Description | Color | SLA | Use When |
|-------|-------------|-------|-----|----------|
| `P0-critical` | Critical - Fix ASAP | `#b60205` | 24h | Blocking bugs, security issues, data loss |
| `P1-high` | High priority | `#d93f0b` | 1 week | Major features, user-reported bugs |
| `P2-medium` | Medium priority | `#fbca04` | 1 month | Enhancements, technical debt |
| `P3-low` | Low priority | `#0e8a16` | Backlog | Nice-to-have, future features |

### 3. Area Labels
Identify which part of the codebase is affected:

| Label | Description | Color |
|-------|-------------|-------|
| `area: backend` | Backend/API related | `#5319e7` |
| `area: frontend` | Frontend/UI related | `#1d76db` |
| `area: database` | Database schema/migrations | `#006b75` |
| `area: docker` | Docker/containerization | `#0db7ed` |
| `area: ci-cd` | CI/CD pipelines | `#28a745` |
| `area: testing` | Testing infrastructure | `#d4c5f9` |
| `area: security` | Security components | `#ff0000` |
| `area: docs` | Documentation | `#0075ca` |

### 4. Status Labels
Track issue lifecycle:

| Label | Description | Color | Use When |
|-------|-------------|-------|----------|
| `status: blocked` | Blocked by another issue/PR | `#d93f0b` | Cannot proceed |
| `status: in-progress` | Currently being worked on | `#fbca04` | Active development |
| `status: needs-discussion` | Requires team discussion | `#d4c5f9` | Design decisions needed |
| `status: needs-review` | Waiting for code review | `#0e8a16` | PR ready for review |
| `status: needs-testing` | Needs manual testing | `#fef2c0` | Testing required |
| `status: on-hold` | Temporarily paused | `#cccccc` | Waiting for decision |
| `status: duplicate` | Duplicate issue | `#cfd3d7` | Already reported |
| `status: wontfix` | Will not be fixed | `#ffffff` | Out of scope |
| `status: stale` | No activity for 6+ months | `#eeeeee` | Inactive issues |

### 5. Difficulty Labels
Help contributors find appropriate issues:

| Label | Description | Color | Use When |
|-------|-------------|-------|----------|
| `good first issue` | Easy for newcomers | `#7057ff` | Simple, well-defined tasks |
| `intermediate` | Moderate complexity | `#008672` | Requires some knowledge |
| `advanced` | Complex implementation | `#d93f0b` | Deep codebase understanding |

### 6. Special Labels

| Label | Description | Color |
|-------|-------------|-------|
| `help wanted` | Seeking contributors | `#008672` |
| `question` | Further information requested | `#d876e3` |
| `breaking change` | Introduces breaking changes | `#ff0000` |
| `needs-reproduction` | Cannot reproduce | `#fef2c0` |
| `hacktoberfest` | Hacktoberfest eligible | `#ff6b6b` |
| `automated` | Created by automation | `#ededed` |

## Labeling Guidelines

### Issue Labeling Process

1. **New Issue Triage**
   - Add at least one **Type** label
   - Add a **Priority** label (P0-P3)
   - Add relevant **Area** labels
   - Add **Difficulty** if suitable for contributors

2. **Active Development**
   - Add `status: in-progress` when work starts
   - Add `status: needs-review` when PR is ready
   - Add `status: blocked` if dependencies exist

3. **Resolution**
   - Add `status: duplicate` if duplicate found
   - Add `status: wontfix` if out of scope
   - Close with explanation

### Pull Request Labeling

1. **Match Issue Labels**: Copy Type and Area labels from related issue
2. **Add Status**: Use `status: needs-review` or `status: needs-testing`
3. **Flag Impact**: Add `breaking change` if applicable
4. **Automation**: `automated` label for bot PRs

## Label Usage Examples

### Example 1: Critical Bug
```
Labels: bug, P0-critical, area: backend, area: security
```
A security vulnerability in the authentication system.

### Example 2: Feature Request
```
Labels: feature, P2-medium, area: frontend, good first issue
```
Add a new chart type to the dashboard.

### Example 3: Technical Debt
```
Labels: refactoring, P2-medium, area: backend, intermediate
```
Refactor recipe calculation logic for better maintainability.

### Example 4: Documentation
```
Labels: documentation, P3-low, area: docs, good first issue
```
Update installation instructions in README.

### Example 5: Performance Issue
```
Labels: performance, bug, P1-high, area: database
```
Slow query when loading recipe list with 1000+ recipes.

## Milestone Integration

Labels work together with milestones:

- **P0-critical**: Usually in current sprint milestone
- **P1-high**: Next sprint or current release milestone
- **P2-medium**: Upcoming release milestones
- **P3-low**: Future milestones or backlog

## Automated Labeling

Some labels are automatically applied:

- `dependencies`: Added by Dependabot
- `automated`: Added by GitHub Actions
- `ci-cd`, `python`, `javascript`: Added based on file changes

## Maintenance

### Quarterly Label Review
- Review stale labels
- Merge similar labels
- Update this documentation
- Clean up unused labels

### Label Consistency
- Use this guide when creating issues
- Update labels as issues evolve
- Remove outdated labels promptly

## Creating New Labels

Before creating a new label, consider:

1. **Is it needed?** Can existing labels work?
2. **Is it clear?** Name should be self-explanatory
3. **Does it fit?** Should belong to a category
4. **Is it consistent?** Follow naming conventions

### Naming Conventions
- Use lowercase with hyphens: `good-first-issue`
- Use prefixes for categories: `area:`, `status:`, `P0-`
- Be concise but descriptive
- Avoid ambiguity

## GitHub Label Sync

To apply these labels to the repository, use GitHub's label management or a tool like [github-label-sync](https://github.com/Financial-Times/github-label-sync).

Example label configuration for automation tools is available in `.github/labels.yml`.

## Questions?

- Check [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- Open a discussion for clarification
- Propose changes via pull request to this document

---

**Last Updated**: 2025-11-11
**Maintained By**: HoppyBrew Core Team
