# Multi-Agent Coordination Context

## Coordination Mission
Oversee and coordinate multiple Codex agents working on the HoppyBrew project to ensure efficient collaboration and avoid conflicts.

## Active Agents
1. **Workspace Organization Agent** (CODEX_AGENT_WORKSPACE.md) ⭐ HIGHEST PRIORITY
   - Status: ACTIVE
   - Focus: Clean workspace, file organization, clutter removal
   - Terminal ID: TBD

2. **GitHub Repository Agent** (CODEX_AGENT_GITHUB.md) ⭐ CRITICAL
   - Status: ACTIVE  
   - Focus: Git workflow, branches, PRs, issues, releases
   - Terminal ID: TBD

3. **Database Optimization Agent** (CODEX_AGENT_DATABASE.md)
   - Status: ACTIVE
   - Focus: SQLAlchemy models, relationships, indexing
   - Terminal ID: TBD

4. **Frontend Component Agent** (CODEX_AGENT_FRONTEND.md)  
   - Status: ACTIVE
   - Focus: Vue.js components, reusability, performance
   - Terminal ID: TBD

5. **Testing Strategy Agent** (CODEX_AGENT_TESTING.md)
   - Status: ACTIVE
   - Focus: Test coverage analysis, strategy development
   - Terminal ID: TBD

## Coordination Rules
- Each agent maintains its own context file
- Agents must update their context files with progress
- No two agents should modify the same files simultaneously
- Cross-agent dependencies should be noted in context files
- Regular status updates should be posted to this coordination file

## File Ownership
### Workspace Agent (HIGHEST PRIORITY)
- All root directory files (cleanup authority)
- Documentation organization across all directories
- Agent context file maintenance
- Code formatting and cleanup authority

### GitHub Agent (CRITICAL)
- .git/ directory and all git operations
- Branch management and PR coordination
- Issue tracking and labels
- Release management and tagging

### Database Agent
- services/backend/Database/Models/**
- database.py
- Any migration files

### Frontend Agent  
- services/nuxt3-shadcn/components/**
- services/nuxt3-shadcn/composables/**
- nuxt.config.ts (component-related configs)

### Testing Agent
- services/backend/tests/**
- pytest.ini
- Any new test configurations

## Shared Resources (Coordination Required)
- README.md updates
- requirements.txt changes
- package.json modifications
- Docker configurations
- Documentation files

## Agent Communication Protocol
1. Before modifying shared files, agents should note intent in their context
2. Agents should check other context files for conflicts
3. Major architectural changes require coordination
4. Each agent should log completion of major tasks

## Progress Tracking
- Database Agent: 25% complete (relationship analysis in progress)
- Frontend Agent: 30% complete (component structure analyzed)  
- Testing Agent: 15% complete (coverage analysis started)

## Coordination Log
- [TIME] Multi-agent system initialized with context files
- [TIME] All agents started with individual contexts
- [TIME] Coordination protocol established
- [2025-11-05 14:14 UTC] Coordinator reviewed all agent context files; no conflicting file ownership noted; awaiting progress updates
