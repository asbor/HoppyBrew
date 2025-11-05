# AI Agent Orchestration System

## Overview

This directory contains the orchestration system for managing multiple AI agents working concurrently on the HoppyBrew codebase.

## Problem Statement

When deploying multiple Codex agents simultaneously:
- Agents can modify the same files, creating conflicts
- No visibility into which agents are running
- No coordination between agents
- Risk of infinite loops or race conditions
- Difficult to track which agent made which changes

## Solution: Agent Orchestration System

### Components

1. **orchestrator.json** - Central coordination manifest
   - Active agent registry
   - File lock tracking
   - Conflict detection
   - Dependency management

2. **Agent Lifecycle Management**
   - Start: Register agent with file locks
   - Run: Monitor progress and file changes
   - Complete: Release locks and commit changes
   - Terminate: Handle timeouts or conflicts

3. **File Locking System**
   - Exclusive locks: Only one agent can modify a file
   - Shared locks: Multiple agents can read
   - Lock timeout: Auto-release after inactivity

4. **Conflict Resolution**
   - Detect overlapping file locks
   - Identify duplicate agents
   - Recommend termination or merge strategies
   - Manual review for complex conflicts

## Usage

### Starting an Agent

```bash
# 1. Register agent first
./scripts/agent-register.sh \
  --name "Backend API Agent" \
  --files "services/backend/api/endpoints/*.py" \
  --priority 1

# 2. Launch Codex agent with registered ID
codex exec -s workspace-write "task description"
```

### Monitoring Agents

```bash
# List all active agents
./scripts/agent-list.sh

# Check for conflicts
./scripts/agent-check-conflicts.sh

# View agent timeline
./scripts/agent-timeline.sh
```

### Stopping an Agent

```bash
# Graceful stop (wait for completion)
./scripts/agent-stop.sh --id agent-1 --graceful

# Force stop (terminate immediately)
./scripts/agent-stop.sh --id agent-1 --force
```

## Orchestration Rules

### Priority System
- **Priority 1**: Foundation agents (database, core API)
- **Priority 2**: Business logic agents
- **Priority 3**: Documentation agents
- **Priority 4**: Testing agents
- **Priority 5**: Enhancement agents

Higher priority agents get exclusive access to contested files.

### Concurrency Limits
- **Max concurrent agents**: 4 (configurable)
- **Max agents per file**: 1 (exclusive lock)
- **Max runtime per agent**: 10 minutes (timeout)

### Dependency Management
Agents can declare dependencies:
```json
{
  "dependencies": ["agent-1-database"],
  "wait_for_completion": true
}
```

### File Lock Rules
1. Agent must declare files before modification
2. Locks are exclusive by default
3. Lock timeout: 10 minutes of inactivity
4. Lock release: Automatic on agent completion

## Agent States

```
REGISTERED → WAITING → RUNNING → COMPLETING → COMPLETED
                ↓         ↓          ↓
              BLOCKED  TIMEOUT   CONFLICT → TERMINATED
```

- **REGISTERED**: Agent declared but not started
- **WAITING**: Waiting for dependencies or file locks
- **BLOCKED**: Waiting for another agent to release lock
- **RUNNING**: Actively making changes
- **TIMEOUT**: Exceeded max runtime, auto-terminated
- **CONFLICT**: Detected file lock conflict
- **COMPLETING**: Finalizing changes, about to release locks
- **COMPLETED**: Successfully finished, locks released
- **TERMINATED**: Stopped due to conflict, timeout, or manual intervention

## Integration with Git

Each agent's changes should be committed separately:

```bash
# Agent 1 completes
git add services/backend/api/endpoints/hops.py
git commit -m "feat(agent-1): Add POST/PUT endpoints for hops inventory"

# Agent 2 completes
git add alembic.ini alembic/
git commit -m "feat(agent-2): Initialize Alembic migrations"
```

This creates a clear audit trail of which agent made which changes.

## Conflict Resolution Workflow

1. **Detection**: Orchestrator detects file lock conflict
2. **Analysis**: Compare agent priorities and start times
3. **Recommendation**: 
   - Terminate lower-priority agent
   - OR wait for higher-priority agent to complete
   - OR merge changes manually
4. **Resolution**: Execute recommended action
5. **Verification**: Check git diff for conflicts

## Future Enhancements

- [ ] Real-time agent communication via message queue
- [ ] Automatic conflict resolution with LLM
- [ ] Agent performance metrics and analytics
- [ ] Distributed agent coordination across machines
- [ ] Agent learning from previous conflicts
- [ ] Integration with CI/CD for automatic validation

## Example Session

```bash
# Session: Phase 1 - Backend Foundation

# Register and start 4 agents
./scripts/agent-start-session.sh --phase phase-1-backend

# Monitor progress
watch -n 5 './scripts/agent-status.sh'

# Detect conflict
# Output: ⚠️  CONFLICT: agent-1 and agent-5 both modifying hops.py

# Resolve conflict
./scripts/agent-resolve-conflict.sh --keep agent-1 --terminate agent-5

# Complete session
./scripts/agent-complete-session.sh --phase phase-1-backend
```

## Troubleshooting

### Agent Stuck
```bash
# Check agent logs
./scripts/agent-logs.sh --id agent-1

# Force terminate
./scripts/agent-stop.sh --id agent-1 --force
```

### File Lock Deadlock
```bash
# Release all locks for agent
./scripts/agent-release-locks.sh --id agent-1

# Reset orchestrator state
./scripts/agent-reset.sh
```

### Changes Not Appearing
```bash
# Check git status
git status

# Verify agent completed
./scripts/agent-status.sh --id agent-1

# Manual checkpoint
git add -A && git commit -m "checkpoint: agent-1 progress"
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  Orchestrator                           │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Agent     │  │     File     │  │   Conflict   │  │
│  │  Registry   │  │     Lock     │  │   Resolver   │  │
│  │             │  │   Manager    │  │              │  │
│  └─────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
         │                 │                 │
         ├─────────────────┼─────────────────┤
         ▼                 ▼                 ▼
   ┌──────────┐      ┌──────────┐     ┌──────────┐
   │ Agent 1  │      │ Agent 2  │     │ Agent N  │
   │ (Backend)│      │(Database)│     │  (Docs)  │
   └──────────┘      └──────────┘     └──────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           ▼
                    ┌──────────────┐
                    │  Workspace   │
                    │   (Files)    │
                    └──────────────┘
```

---

**Status**: 🚧 System Deployed  
**Version**: 1.0.0  
**Last Updated**: 2025-11-05
