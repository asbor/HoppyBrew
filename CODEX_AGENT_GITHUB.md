# GitHub Repository Management Agent Context

## Agent Mission
Manage all GitHub repository operations, including commits, branches, pull requests, issues, and release management for the HoppyBrew project.

## Current Status
- ACTIVE: Repository management and coordination
- PHASE: Initial repository assessment and workflow setup

## Core Responsibilities
1. **Commit Management**: Organize and coordinate commits from all agents
2. **Branch Strategy**: Manage feature branches and merging workflow
3. **Pull Request Coordination**: Create and manage PRs for agent work
4. **Issue Tracking**: Create and track issues for agent tasks
5. **Release Management**: Coordinate versioning and releases
6. **Repository Maintenance**: Keep repo clean and well-organized

## Repository Information
- **Repository**: HoppyBrew (github.com/asbor/HoppyBrew.git)
- **Current Branch**: main
- **Default Branch**: main
- **Owner**: asbor

## Agent Work Coordination
### Active Agent Branches
- [x] `feature/database-optimization` - Database Agent work (created 2025-11-05)
- [x] `feature/frontend-components` - Frontend Agent work (created 2025-11-05)  
- [x] `feature/testing-strategy` - Testing Agent work (created 2025-11-05)
- [x] `feature/workspace-cleanup` - Workspace Agent work (created 2025-11-05)

### Commit Strategy
1. **Agent Commits**: Each agent commits to their feature branch
2. **Coordinated Merging**: GitHub agent manages merges to main
3. **Clean History**: Squash commits for clean history
4. **Descriptive Messages**: Standardized commit message format

## GitHub Workflow Management
### Issues to Create
- [x] Database Optimization and Performance Improvements
- [x] Frontend Component Reusability and Performance  
- [x] Comprehensive Testing Strategy Implementation
- [x] Workspace Organization and Cleanup
- [x] Multi-Agent Development Coordination

### Pull Request Strategy
1. Create feature branches for each agent
2. Regular commits to feature branches
3. PR creation when agent work is ready
4. Code review and testing before merge
5. Clean merge to main branch

### Branch Protection
- Require PR reviews for main branch
- Run tests before merging
- Ensure clean merge history

## Repository Organization Tasks
### ✅ Immediate Actions
- [x] Create feature branches for each agent
- [ ] Set up branch protection rules
- [x] Create tracking issues for agent work
- [x] Establish commit message standards

### ✅ Ongoing Management
- [ ] Monitor agent progress through commits
- [ ] Coordinate merge conflicts
- [ ] Manage release versioning
- [ ] Update repository documentation

## Commit Message Standards
```
<type>(<scope>): <description>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore
Scopes: database, frontend, testing, workspace, agents

Commit template stored at `.github/COMMIT_TEMPLATE.txt` (apply locally with `git config commit.template .github/COMMIT_TEMPLATE.txt`).

## Release Management
- **Current Version**: v1.0.2-alpha (tagged)
- **Next Release**: v1.1.0 (post-agent improvements)
- **Release Strategy**: Semantic versioning

## Repository Health Metrics
- **Open Issues**: TBD (will create tracking issues)
- **Active Branches**: main + 4 feature branches (to create)
- **Last Release**: v1.0.2-alpha
- **Commit Frequency**: Active development

## Integration with Other Agents
- **Workspace Agent**: Coordinates file cleanup before commits
- **Database Agent**: Manages database schema commits
- **Frontend Agent**: Manages component and UI commits
- **Testing Agent**: Manages test file commits
- **Coordinator**: Reports to coordination system

## GitHub Tasks Queue
1. Create feature branches for all agents
2. Set up issue templates and labels
3. Create tracking issues for agent work
4. Establish automated workflows (CI/CD)
5. Configure branch protection rules

## Agent Log
- Repository management agent initialized
- Assessed current repository state
- Ready to establish multi-agent GitHub workflow
- 2025-11-05: Created feature branches for all active agents.
- 2025-11-05: Published tracking issues in `documents/issues/` and documented commit template usage.
