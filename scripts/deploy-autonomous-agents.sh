#!/bin/bash

# Deploy Autonomous Agents - Phase 1
# Spawns real AI agents that work independently

set -e

WORKSPACE_DIR=$(pwd)

echo "🎭 HoppyBrew Autonomous Agent Deployment System"
echo "=================================================="
echo ""
echo "This will spawn 3 autonomous AI agents that work independently:"
echo "  🏗️  ARCH-001  - Architecture & Diagram Agent"
echo "  📊 DATA-001  - Data Model & Schema Agent"
echo "  🔌 API-001   - API Documentation Agent"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."
echo ""

# Check for tmux
if ! command -v tmux &> /dev/null; then
    echo "⚠️  tmux not found (optional but recommended)"
    echo "   Install: sudo dnf install tmux"
else
    echo "✅ tmux available"
fi

# Check for GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI not found"
    echo "   Install: sudo dnf install gh"
else
    echo "✅ GitHub CLI available"
    
    # Check for Copilot extension
    if gh copilot --version &> /dev/null 2>&1; then
        echo "✅ GitHub Copilot CLI extension available"
    else
        echo "⚠️  GitHub Copilot CLI extension not installed"
        echo "   Install: gh extension install github/gh-copilot"
    fi
fi

echo ""
echo "📋 Deployment Strategy:"
echo "   Each agent will run in its own process with full autonomy"
echo "   Agents coordinate via file locks and shared context files"
echo "   Agents commit their own changes to git"
echo ""

read -p "🚀 Ready to deploy Phase 1 agents? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo "🚀 Deploying Phase 1 agents..."
echo ""

# Make scripts executable
chmod +x scripts/spawn-agent.sh
chmod +x scripts/execute-agent.sh

# Deploy Architecture Agent
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏗️  Deploying ARCH-001 - Architecture Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
./scripts/spawn-agent.sh ARCH-001 .agents/CODEX_AGENT_ARCHITECTURE.md
sleep 2

# Deploy Data Model Agent
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Deploying DATA-001 - Data Model Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
./scripts/spawn-agent.sh DATA-001 .agents/CODEX_AGENT_DATA_MODEL.md
sleep 2

# Deploy API Documentation Agent
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔌 Deploying API-001 - API Documentation Agent"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
./scripts/spawn-agent.sh API-001 .agents/CODEX_AGENT_API_DOCS.md
sleep 2

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Phase 1 agents deployed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Active agent sessions:"
if command -v tmux &> /dev/null; then
    tmux list-sessions 2>/dev/null | grep -E "ARCH-001|DATA-001|API-001" || echo "   (no tmux sessions found)"
fi
echo ""
echo "📋 Monitor agents:"
echo "   ./scripts/agent-progress.sh          # View progress"
echo "   watch -n 5 ./scripts/agent-progress.sh  # Auto-refresh"
echo "   tail -f .agents/logs/*.log           # View all logs"
echo ""

if command -v tmux &> /dev/null; then
    echo "🔗 Attach to agents:"
    tmux list-sessions 2>/dev/null | grep -E "ARCH-001|DATA-001|API-001" | while read session; do
        session_name=$(echo "$session" | cut -d: -f1)
        echo "   tmux attach -t ${session_name}"
    done
    echo ""
fi

echo "🛑 Stop all agents:"
echo "   rm .agents/locks/*.lock"
if command -v tmux &> /dev/null; then
    echo "   tmux kill-session -t ARCH-001*"
    echo "   tmux kill-session -t DATA-001*"
    echo "   tmux kill-session -t API-001*"
fi
echo ""

echo "🎯 Next steps:"
echo "   1. Agents are now working autonomously in the background"
echo "   2. Each agent reads its context file and executes tasks"
echo "   3. Agents update their progress and commit changes"
echo "   4. Monitor progress with ./scripts/agent-progress.sh"
echo ""
echo "✨ Autonomous AI Enhancement System: OPERATIONAL ✨"
echo ""
