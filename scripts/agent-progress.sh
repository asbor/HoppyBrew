#!/bin/bash

# Quick Agent Progress Viewer
# Shows a compact view of all agents with progress bars

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🎭 HoppyBrew AI Agent Progress Report         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo -e "${CYAN}📅 $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo ""

# Function to draw progress bar
draw_progress_bar() {
    local progress=$1
    local width=30
    local filled=$((progress * width / 100))
    local empty=$((width - filled))
    
    printf "["
    printf "%${filled}s" | tr ' ' '█'
    printf "%${empty}s" | tr ' ' '░'
    printf "] %3d%%" "$progress"
}

# Function to get status color
get_status_color() {
    case "$1" in
        "RUNNING") echo "$GREEN" ;;
        "ACTIVE") echo "$BLUE" ;;
        "COMPLETED") echo "$GREEN" ;;
        *) echo "$NC" ;;
    esac
}

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Phase 1: Critical Foundation Agents${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Architecture Agent
if [ -f ".agents/CODEX_AGENT_ARCHITECTURE.md" ]; then
    progress=$(grep "^\*\*Overall Progress\*\*:" .agents/CODEX_AGENT_ARCHITECTURE.md | head -1 | sed 's/.*: //' | sed 's/%//')
    status=$(grep "^- \*\*Status\*\*:" .agents/CODEX_AGENT_ARCHITECTURE.md | head -1 | sed 's/.*: //')
    task=$(grep "^\*\*Current Task\*\*:" .agents/CODEX_AGENT_ARCHITECTURE.md | head -1 | sed 's/.*: //' | cut -c1-50)
    
    color=$(get_status_color "$status")
    echo -e "\n🏗️  ${color}ARCH-001${NC} - Architecture & Diagram Agent"
    echo -e "   Status: ${color}${status}${NC}"
    echo -e "   $(draw_progress_bar ${progress:-0})"
    echo -e "   Task: $task"
fi

# Data Model Agent
if [ -f ".agents/CODEX_AGENT_DATA_MODEL.md" ]; then
    progress=$(grep "^\*\*Overall Progress\*\*:" .agents/CODEX_AGENT_DATA_MODEL.md | head -1 | sed 's/.*: //' | sed 's/%//')
    status=$(grep "^- \*\*Status\*\*:" .agents/CODEX_AGENT_DATA_MODEL.md | head -1 | sed 's/.*: //')
    task=$(grep "^\*\*Current Task\*\*:" .agents/CODEX_AGENT_DATA_MODEL.md | head -1 | sed 's/.*: //' | cut -c1-50)
    
    color=$(get_status_color "$status")
    echo -e "\n📊 ${color}DATA-001${NC} - Data Model & Schema Agent"
    echo -e "   Status: ${color}${status}${NC}"
    echo -e "   $(draw_progress_bar ${progress:-0})"
    echo -e "   Task: $task"
fi

# API Docs Agent
if [ -f ".agents/CODEX_AGENT_API_DOCS.md" ]; then
    progress=$(grep "^\*\*Overall Progress\*\*:" .agents/CODEX_AGENT_API_DOCS.md | head -1 | sed 's/.*: //' | sed 's/%//')
    status=$(grep "^- \*\*Status\*\*:" .agents/CODEX_AGENT_API_DOCS.md | head -1 | sed 's/.*: //')
    task=$(grep "^\*\*Current Task\*\*:" .agents/CODEX_AGENT_API_DOCS.md | head -1 | sed 's/.*: //' | cut -c1-50)
    
    color=$(get_status_color "$status")
    echo -e "\n🔌 ${color}API-001${NC} - API Documentation Agent"
    echo -e "   Status: ${color}${status}${NC}"
    echo -e "   $(draw_progress_bar ${progress:-0})"
    echo -e "   Task: $task"
fi

echo -e "\n${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}Other Active Agents${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Count other active agents
active_count=0
for agent in WIKI_ENHANCER TEST_COVERAGE SECURITY_RESOLVER DEVOPS_CI FRONTEND_UX DOCUMENTATION; do
    if [ -f ".agents/CODEX_AGENT_${agent}.md" ]; then
        status=$(grep "^- \*\*Status\*\*:" .agents/CODEX_AGENT_${agent}.md | head -1 | sed 's/.*: //')
        if [ "$status" = "ACTIVE" ] || [ "$status" = "RUNNING" ]; then
            ((active_count++))
        fi
    fi
done

echo -e "\n📊 ${active_count} additional agents active (monitoring mode)"

echo -e "\n${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Key Achievements${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Check for completed tasks
if grep -q "Task 1.*COMPLETED" .agents/CODEX_AGENT_ARCHITECTURE.md 2>/dev/null; then
    echo -e "✅ ${GREEN}Architecture Agent:${NC} Fixed ComponentDiagram (Issue #348)"
fi

echo ""
echo -e "${CYAN}🔄 Auto-refresh: watch -n 5 '$0'${NC}"
echo -e "${CYAN}📊 Full dashboard: ./scripts/open-dashboard.sh${NC}"
echo ""
