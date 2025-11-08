#!/bin/bash

# Real Autonomous Agent Executor
# Uses GitHub Copilot to execute agent tasks autonomously

AGENT_ID=$1
AGENT_CONTEXT_FILE=$2

if [ -z "$AGENT_ID" ] || [ -z "$AGENT_CONTEXT_FILE" ]; then
    echo "Usage: $0 <AGENT_ID> <AGENT_CONTEXT_FILE>"
    exit 1
fi

WORKSPACE_DIR=$(pwd)
LOG_FILE=".agents/logs/${AGENT_ID}_execution_$(date +%Y%m%d_%H%M%S).log"

echo "🤖 Autonomous Agent Executor: ${AGENT_ID}" | tee -a "$LOG_FILE"
echo "📅 Started: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Read agent context and extract pending tasks
echo "📖 Reading agent context..." | tee -a "$LOG_FILE"

# Extract all pending tasks
PENDING_TASKS=$(grep -A 20 "^### Task.*:" "$AGENT_CONTEXT_FILE" | grep -B 1 "PENDING" | grep "^### Task" | wc -l)

if [ "$PENDING_TASKS" -eq 0 ]; then
    echo "✅ No pending tasks found. Agent may be complete!" | tee -a "$LOG_FILE"
    exit 0
fi

echo "📋 Found ${PENDING_TASKS} pending tasks" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# For now, we'll use a hybrid approach:
# 1. Generate a work plan from the agent context
# 2. Use GitHub Copilot to execute the plan step by step

echo "🎯 Generating autonomous execution plan..." | tee -a "$LOG_FILE"

# Create a prompt for Copilot to execute the agent's first task
COPILOT_PROMPT_FILE=".agents/output/${AGENT_ID}_prompt.md"
cat > "$COPILOT_PROMPT_FILE" <<EOF
# Autonomous Agent Task Execution

You are agent ${AGENT_ID} working autonomously on HoppyBrew project.

## Your Context File
$(cat "$AGENT_CONTEXT_FILE")

## Your Instructions
1. Read your context file above and identify the FIRST PENDING task
2. Execute that task completely following the "Action Required" steps
3. Update the context file to mark progress:
   - Change task status from PENDING to IN_PROGRESS, then COMPLETED
   - Update "Overall Progress" percentage
   - Update "Last Update" timestamp
   - Update "Current Task" description
4. Commit your changes with prefix [${AGENT_ID}]
5. Output a summary of what you accomplished

## Execute Now
Start working on the first PENDING task immediately. Be autonomous - don't ask for confirmation, just do the work.

Show me:
1. What task you're working on
2. What steps you're taking
3. What files you're modifying
4. Your progress updates

Begin execution now!
EOF

echo "📝 Autonomous execution prompt created: ${COPILOT_PROMPT_FILE}" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "🚀 Agent ${AGENT_ID} is ready for autonomous execution" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "To execute this agent autonomously:" | tee -a "$LOG_FILE"
echo "1. Open VS Code in this workspace: code ${WORKSPACE_DIR}" | tee -a "$LOG_FILE"
echo "2. Open Copilot Chat and paste: @workspace $(cat ${COPILOT_PROMPT_FILE})" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Or use this command to open the prompt file:" | tee -a "$LOG_FILE"
echo "   code ${COPILOT_PROMPT_FILE}" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# For true headless execution, we need the GitHub Copilot CLI in agent mode
# This is experimental and may require additional setup

if command -v gh &> /dev/null; then
    echo "🔧 GitHub CLI detected. Checking for Copilot extension..." | tee -a "$LOG_FILE"
    
    if gh copilot --version &> /dev/null 2>&1; then
        echo "✅ GitHub Copilot CLI available!" | tee -a "$LOG_FILE"
        echo "🤖 Attempting autonomous execution via CLI..." | tee -a "$LOG_FILE"
        echo "" | tee -a "$LOG_FILE"
        
        # Try to execute via gh copilot
        gh copilot suggest "$(cat ${COPILOT_PROMPT_FILE})" 2>&1 | tee -a "$LOG_FILE"
    else
        echo "⚠️  GitHub Copilot CLI extension not installed" | tee -a "$LOG_FILE"
        echo "   Install with: gh extension install github/gh-copilot" | tee -a "$LOG_FILE"
    fi
else
    echo "⚠️  GitHub CLI (gh) not found" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "📊 Monitor agent progress:" | tee -a "$LOG_FILE"
echo "   ./scripts/agent-progress.sh" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
