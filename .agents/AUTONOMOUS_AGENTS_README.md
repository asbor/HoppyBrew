# 🤖 Autonomous Agent System - Setup Guide

## Overview

The HoppyBrew project now has **real autonomous AI agents** that work independently using GitHub Copilot CLI.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│ Main Copilot Session (You)                          │
│ - Coordinates high-level strategy                    │
│ - Deploys autonomous agents                         │
│ - Monitors overall progress                         │
└──────────────┬──────────────────────────────────────┘
               │
               │ Spawns via tmux sessions
               │
     ┌─────────┴──────────┬──────────────────────┐
     │                     │                       │
┌────▼────┐          ┌────▼────┐            ┌────▼────┐
│ ARCH-001│          │ DATA-001│            │ API-001 │
│ tmux    │          │ tmux    │            │ tmux    │
│ session │          │ session │            │ session │
└────┬────┘          └────┬────┘            └────┬────┘
     │                     │                       │
     │ Each agent:         │                       │
     │ - Reads context file                       │
     │ - Executes tasks autonomously              │
     │ - Updates progress                         │
     │ - Commits changes                          │
     │ - Coordinates via locks                    │
     └─────────────────────┴───────────────────────┘
```

## Prerequisites

### Required
- ✅ VS Code with GitHub Copilot extension
- ✅ GitHub CLI (`gh`) - already installed
- ✅ GitHub Copilot CLI extension - already installed

### Optional but Recommended
- ✅ tmux (for managing agent sessions) - already installed
- ⚪ Multiple terminal windows

## Deployment

### Method 1: Automated Deployment (Recommended)

Deploy all Phase 1 agents at once:

```bash
./scripts/deploy-autonomous-agents.sh
```

This spawns 3 autonomous agents:
- 🏗️ ARCH-001 - Architecture & Diagram Agent
- 📊 DATA-001 - Data Model & Schema Agent
- 🔌 API-001 - API Documentation Agent

### Method 2: Manual Individual Agent Deployment

Spawn agents one at a time:

```bash
# Architecture Agent
./scripts/spawn-agent.sh ARCH-001 .agents/CODEX_AGENT_ARCHITECTURE.md

# Data Model Agent
./scripts/spawn-agent.sh DATA-001 .agents/CODEX_AGENT_DATA_MODEL.md

# API Documentation Agent
./scripts/spawn-agent.sh API-001 .agents/CODEX_AGENT_API_DOCS.md
```

## Monitoring Agents

### View Progress Dashboard

```bash
./scripts/agent-progress.sh
```

### Auto-Refresh Dashboard

```bash
watch -n 5 './scripts/agent-progress.sh'
```

### View Agent Logs

```bash
# All agents
tail -f .agents/logs/*.log

# Specific agent
tail -f .agents/logs/ARCH-001*.log
```

### Attach to Agent Session

```bash
# List running sessions
tmux list-sessions

# Attach to specific agent
tmux attach -t ARCH-001_<timestamp>
```

Press `Ctrl+B` then `D` to detach without killing the session.

## How Agents Work

### 1. Agent Context Files

Each agent has a context file (`.agents/CODEX_AGENT_*.md`) containing:
- Agent identity and mission
- List of tasks with priorities
- Current progress percentage
- File ownership rules
- Coordination protocol

### 2. Agent Instructions

When spawned, each agent receives:
- Its full context file
- Step-by-step execution instructions
- Progress tracking format
- Coordination rules
- Success criteria

### 3. Autonomous Execution

Each agent:
1. Reads its context file
2. Identifies PENDING tasks
3. Executes tasks following "Action Required" steps
4. Updates progress in context file
5. Commits changes with `[AGENT-ID]` prefix
6. Moves to next task

### 4. Coordination

Agents coordinate via:
- **Lock files** (`.agents/locks/*.lock`) - Prevent concurrent file access
- **File ownership** - Each agent owns specific files
- **Context updates** - Agents update their status every 2 hours
- **Git commits** - All changes are version controlled

## Agent Management

### Check Agent Status

```bash
# Quick check
cat .agents/CODEX_AGENT_*.md | grep "Overall Progress"

# Detailed status
./scripts/agent-status.sh
```

### Stop Specific Agent

```bash
# Remove lock file (agent will shut down)
rm .agents/locks/ARCH-001.lock

# Kill tmux session
tmux kill-session -t ARCH-001_<timestamp>
```

### Stop All Agents

```bash
# Remove all locks
rm .agents/locks/*.lock

# Kill all agent sessions
tmux kill-session -t ARCH-001*
tmux kill-session -t DATA-001*
tmux kill-session -t API-001*
```

### Restart Agent

```bash
# If agent crashed or stuck
rm .agents/locks/ARCH-001.lock
./scripts/spawn-agent.sh ARCH-001 .agents/CODEX_AGENT_ARCHITECTURE.md
```

## Troubleshooting

### Agent Not Starting

```bash
# Check for stale lock file
ls -la .agents/locks/

# Remove stale locks
rm .agents/locks/ARCH-001.lock

# Check tmux sessions
tmux list-sessions
```

### Agent Not Making Progress

```bash
# Attach to agent session to see what's happening
tmux attach -t ARCH-001_<timestamp>

# Check agent log
tail -f .agents/logs/ARCH-001*.log

# Verify agent has pending tasks
grep "PENDING" .agents/CODEX_AGENT_ARCHITECTURE.md
```

### Multiple Agents Conflicting

Agents use file ownership to prevent conflicts. Check:

```bash
# View file ownership rules
grep -A 20 "File Ownership" .agents/CODEX_AGENT_ARCHITECTURE.md
```

If conflict occurs:
1. Agents should wait for locks to clear
2. Higher priority agents (CRITICAL) get access first
3. Lower priority agents queue behind

## File Structure

```
.agents/
├── CODEX_AGENT_*.md        # Agent context files
├── locks/
│   ├── ARCH-001.lock       # Agent lock files
│   ├── DATA-001.lock
│   └── API-001.lock
├── logs/
│   ├── ARCH-001_*.log      # Agent execution logs
│   ├── DATA-001_*.log
│   └── API-001_*.log
├── output/
│   ├── ARCH-001_instructions.md  # Generated agent instructions
│   ├── ARCH-001_runner.sh        # Agent runner script
│   └── ARCH-001_prompt.md        # Copilot execution prompt
└── status.json             # Live agent status (for dashboard)
```

## Advanced Usage

### Execute Agent Task Manually

If you want to manually execute an agent's current task:

```bash
./scripts/execute-agent.sh ARCH-001 .agents/CODEX_AGENT_ARCHITECTURE.md
```

This generates a Copilot prompt that you can use to execute the task.

### Add Custom Agent

1. Create context file: `.agents/CODEX_AGENT_CUSTOM.md`
2. Define agent identity, tasks, and ownership rules
3. Spawn agent: `./scripts/spawn-agent.sh CUSTOM-001 .agents/CODEX_AGENT_CUSTOM.md`

### Modify Agent Tasks

Edit the agent's context file while it's running:

```bash
vim .agents/CODEX_AGENT_ARCHITECTURE.md
```

Agent will pick up changes on next task iteration.

## Current Deployment Status

### Phase 1 (Week 1) - Foundation Agents
- 🏗️ **ARCH-001**: Architecture & Diagram Agent (40% complete)
  - ✅ Task 1: Fixed component diagram (Issue #348)
  - ⏳ Task 2: Audit all PlantUML diagrams
  - ⏳ Task 3: Generate missing diagrams
  - ⏳ Task 4: Establish diagram maintenance process

- 📊 **DATA-001**: Data Model & Schema Agent (0% complete)
  - ⏳ Task 1: Database model audit
  - ⏳ Task 2: Generate ERD diagrams
  - ⏳ Task 3: Index optimization analysis
  - ⏳ Task 4: Migration strategy documentation

- 🔌 **API-001**: API Documentation Agent (0% complete)
  - ⏳ Task 1: Endpoint discovery & inventory
  - ⏳ Task 2: Generate OpenAPI specification
  - ⏳ Task 3: Create API reference documentation
  - ⏳ Task 4: Interactive API documentation

### Phase 2 (Week 2) - Enhancement Agents
Not yet deployed

### Phase 3 (Week 3) - Workflow Agents
Not yet deployed

### Phase 4 (Week 4) - Operations Agents
Not yet deployed

## Success Metrics

Track overall system progress:

```bash
# Total agents deployed
ls .agents/locks/ | wc -l

# Total completed tasks
grep -r "COMPLETED" .agents/CODEX_AGENT_*.md | wc -l

# Average progress
cat .agents/CODEX_AGENT_*.md | grep "Overall Progress" | \
  awk -F':' '{sum+=$2} END {print sum/NR "%"}'
```

## Next Steps

1. ✅ Deploy Phase 1 agents
2. ⏳ Monitor agent progress
3. ⏳ Let agents complete their tasks autonomously
4. ⏳ Review agent work and merge changes
5. ⏳ Deploy Phase 2 agents when Phase 1 reaches 80%
6. ⏳ Iterate through all phases

## Support

- View deployment plan: `.agents/AGENT_DEPLOYMENT_PLAN_2025.md`
- View dashboard guide: `.agents/DASHBOARD_GUIDE.md`
- Check agent status: `./scripts/agent-status.sh`
- View progress: `./scripts/agent-progress.sh`

---

**Status**: 🟢 System Operational  
**Active Agents**: 3 / 20  
**Phase**: 1 (Foundation)  
**Overall Progress**: 13% (40% + 0% + 0%) / 3  

**🎭 Autonomous AI Enhancement System: OPERATIONAL ✨**
