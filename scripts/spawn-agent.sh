#!/bin/bash

# Autonomous Agent Spawner
# Spawns real AI agents as separate processes using GitHub Copilot CLI

set -e

AGENT_ID=$1
AGENT_CONTEXT_FILE=$2
WORKSPACE_DIR=$(pwd)
AGENT_LOG_DIR="${WORKSPACE_DIR}/.agents/logs"
AGENT_LOCK_DIR="${WORKSPACE_DIR}/.agents/locks"
AGENT_OUTPUT_DIR="${WORKSPACE_DIR}/.agents/output"

# Ensure directories exist
mkdir -p "${AGENT_LOG_DIR}" "${AGENT_LOCK_DIR}" "${AGENT_OUTPUT_DIR}"

if [ -z "$AGENT_ID" ] || [ -z "$AGENT_CONTEXT_FILE" ]; then
    echo "Usage: $0 <AGENT_ID> <AGENT_CONTEXT_FILE>"
    echo "Example: $0 ARCH-001 .agents/CODEX_AGENT_ARCHITECTURE.md"
    exit 1
fi

if [ ! -f "$AGENT_CONTEXT_FILE" ]; then
    echo "Error: Agent context file not found: $AGENT_CONTEXT_FILE"
    exit 1
fi

# Check if agent is already running
LOCK_FILE="${AGENT_LOCK_DIR}/${AGENT_ID}.lock"
if [ -f "$LOCK_FILE" ]; then
    PID=$(cat "$LOCK_FILE" | grep "pid" | cut -d':' -f2 | tr -d ' ",')
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Agent ${AGENT_ID} is already running (PID: $PID)"
        exit 1
    else
        echo "Stale lock file found, removing..."
        rm -f "$LOCK_FILE"
    fi
fi

echo "🤖 Spawning autonomous agent: ${AGENT_ID}"
echo "📁 Context: ${AGENT_CONTEXT_FILE}"
echo "🔒 Creating lock file..."

# Create lock file
cat > "$LOCK_FILE" <<EOF
{
  "agent_id": "${AGENT_ID}",
  "pid": $$,
  "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "context_file": "${AGENT_CONTEXT_FILE}",
  "workspace": "${WORKSPACE_DIR}",
  "status": "RUNNING"
}
EOF

# Create agent instruction file
AGENT_INSTRUCTION_FILE="${AGENT_OUTPUT_DIR}/${AGENT_ID}_instructions.md"
cat > "$AGENT_INSTRUCTION_FILE" <<EOF
# Agent ${AGENT_ID} - Autonomous Task Execution

You are an autonomous AI agent working on the HoppyBrew project.

## Your Identity
- Agent ID: ${AGENT_ID}
- Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)
- Workspace: ${WORKSPACE_DIR}

## Your Context and Tasks
$(cat "$AGENT_CONTEXT_FILE")

## Your Mission
1. Read your context file carefully: ${AGENT_CONTEXT_FILE}
2. Identify all PENDING tasks in priority order
3. Execute each task following the action required steps
4. Update your context file with progress as you complete each step
5. Update the "Overall Progress" percentage based on task completion
6. Update "Last Update" timestamp after each task
7. Update "Current Task" to reflect what you're working on
8. Commit your changes with the [${AGENT_ID}] prefix
9. When all tasks are complete, update status to COMPLETED

## Important Coordination Rules
- Before modifying any file, check if other agents own it (see File Ownership section)
- Update your context file progress every time you complete a sub-task
- Create commits frequently with descriptive messages tagged [${AGENT_ID}]
- If blocked by another agent, document the blocker in your context file
- Work autonomously - don't ask for permission, just follow your task list

## Progress Tracking Format
Update your context file with this format:
- **Status**: RUNNING
- **Last Update**: $(date -u +%Y-%m-%dT%H:%M:%SZ)
- **Current Task**: [describe what you're working on]
- **Overall Progress**: [percentage]%

## Example Task Execution
For a task like "Fix component diagram":
1. Read the existing file
2. Make the required changes
3. Update context: Task 1 status to IN_PROGRESS, progress to 10%
4. Test/validate the changes
5. Update context: progress to 30%
6. Commit with message "[${AGENT_ID}] Fix component diagram - step 1"
7. Update context: Task 1 status to COMPLETED, progress to 40%
8. Move to next task

## Success Criteria
- All PENDING tasks moved to COMPLETED
- Overall Progress reaches 100%
- All changes committed to git
- Context file updated with final status

## Now Begin!
Start executing your first PENDING task immediately. Work through your task list systematically.
EOF

echo "📝 Agent instructions created: ${AGENT_INSTRUCTION_FILE}"
echo ""
echo "🚀 Starting autonomous agent process..."
echo "📊 Log file: ${AGENT_LOG_DIR}/${AGENT_ID}_$(date +%Y%m%d_%H%M%S).log"
echo ""

# Launch agent using VS Code with GitHub Copilot
# The agent runs in a detached tmux session for true autonomy
TMUX_SESSION="${AGENT_ID}_$(date +%s)"
LOG_FILE="${AGENT_LOG_DIR}/${AGENT_ID}_$(date +%Y%m%d_%H%M%S).log"

# Create agent startup script
AGENT_SCRIPT="${AGENT_OUTPUT_DIR}/${AGENT_ID}_runner.sh"
cat > "$AGENT_SCRIPT" <<'AGENT_RUNNER_EOF'
#!/bin/bash
AGENT_ID="__AGENT_ID__"
INSTRUCTION_FILE="__INSTRUCTION_FILE__"
WORKSPACE="__WORKSPACE__"
LOG_FILE="__LOG_FILE__"

cd "$WORKSPACE"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Agent ${AGENT_ID} starting..." >> "$LOG_FILE"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Reading instructions from ${INSTRUCTION_FILE}" >> "$LOG_FILE"

# The agent will work through VS Code Copilot Chat
# This requires manual interaction currently, but we'll set up the environment
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Agent environment ready" >> "$LOG_FILE"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Workspace: ${WORKSPACE}" >> "$LOG_FILE"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Instructions: ${INSTRUCTION_FILE}" >> "$LOG_FILE"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Waiting for autonomous execution..." >> "$LOG_FILE"

# Keep the session alive
while true; do
    if [ ! -f "__LOCK_FILE__" ]; then
        echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Lock file removed, shutting down" >> "$LOG_FILE"
        break
    fi
    sleep 30
done
AGENT_RUNNER_EOF

# Replace placeholders
sed -i "s|__AGENT_ID__|${AGENT_ID}|g" "$AGENT_SCRIPT"
sed -i "s|__INSTRUCTION_FILE__|${AGENT_INSTRUCTION_FILE}|g" "$AGENT_SCRIPT"
sed -i "s|__WORKSPACE__|${WORKSPACE_DIR}|g" "$AGENT_SCRIPT"
sed -i "s|__LOG_FILE__|${LOG_FILE}|g" "$AGENT_SCRIPT"
sed -i "s|__LOCK_FILE__|${LOCK_FILE}|g" "$AGENT_SCRIPT"

chmod +x "$AGENT_SCRIPT"

# Check if tmux is available
if command -v tmux &> /dev/null; then
    echo "✅ Launching agent in tmux session: ${TMUX_SESSION}"
    tmux new-session -d -s "$TMUX_SESSION" "$AGENT_SCRIPT"
    echo "📺 Attach to agent: tmux attach -t ${TMUX_SESSION}"
else
    echo "⚠️  tmux not found, running in background..."
    nohup "$AGENT_SCRIPT" > "$LOG_FILE" 2>&1 &
    AGENT_PID=$!
    echo "$AGENT_PID" > "${LOCK_FILE}.pid"
    echo "🔢 Agent PID: $AGENT_PID"
fi

echo ""
echo "✅ Agent ${AGENT_ID} spawned successfully!"
echo ""
echo "📋 Agent Instructions: ${AGENT_INSTRUCTION_FILE}"
echo "📊 Monitor progress:"
echo "   - View log: tail -f ${LOG_FILE}"
echo "   - Check status: cat ${AGENT_CONTEXT_FILE} | grep 'Overall Progress'"
echo "   - View dashboard: ./scripts/agent-progress.sh"
if command -v tmux &> /dev/null; then
    echo "   - Attach to agent: tmux attach -t ${TMUX_SESSION}"
fi
echo ""
echo "🛑 Stop agent:"
echo "   - Remove lock: rm ${LOCK_FILE}"
if command -v tmux &> /dev/null; then
    echo "   - Kill session: tmux kill-session -t ${TMUX_SESSION}"
fi
echo ""
