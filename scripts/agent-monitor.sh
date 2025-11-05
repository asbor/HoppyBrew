#!/bin/bash
# Agent Orchestration Monitor
# Monitors running Codex agents and detects conflicts

set -euo pipefail

AGENTS_DIR=".agents"
ORCHESTRATOR_FILE="$AGENTS_DIR/orchestrator.json"
LOG_FILE="$AGENTS_DIR/orchestrator.log"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

log() {
    echo "[$(timestamp)] $1" | tee -a "$LOG_FILE"
}

log_color() {
    color=$1
    shift
    echo -e "${color}[$(timestamp)] $@${NC}" | tee -a "$LOG_FILE"
}

# Check for running Codex processes
check_running_agents() {
    log_color "$BLUE" "=== Checking Running Codex Agents ==="
    
    # Get all codex processes (exclude grep and app-server)
    codex_processes=$(ps aux | grep -i "codex exec" | grep -v grep | grep -v app-server || true)
    
    if [ -z "$codex_processes" ]; then
        log_color "$GREEN" "✓ No running Codex agents detected"
        return 0
    fi
    
    # Count agents
    agent_count=$(echo "$codex_processes" | wc -l)
    log_color "$YELLOW" "⚠️  Found $agent_count running Codex agents:"
    echo ""
    
    # Parse and display agents
    echo "$codex_processes" | while IFS= read -r line; do
        pid=$(echo "$line" | awk '{print $2}')
        terminal=$(echo "$line" | awk '{print $7}')
        command=$(echo "$line" | awk '{for(i=11;i<=NF;i++) printf $i" "; print ""}')
        
        # Extract agent name from command
        agent_name="Unknown"
        if [[ "$command" =~ AGENT\ [0-9]+:\ ([^-]+) ]]; then
            agent_name="${BASH_REMATCH[1]}"
        elif [[ "$command" =~ \"([^\"]+)\" ]]; then
            agent_name="${BASH_REMATCH[1]:0:50}..."
        fi
        
        echo -e "  ${BLUE}PID $pid${NC} | ${YELLOW}$terminal${NC} | $agent_name"
    done
    
    echo ""
    return $agent_count
}

# Detect file conflicts
check_file_conflicts() {
    log_color "$BLUE" "=== Checking for File Conflicts ==="
    
    # Get modified files
    modified_files=$(git status --short | awk '{print $2}')
    
    if [ -z "$modified_files" ]; then
        log_color "$GREEN" "✓ No uncommitted file changes"
        return 0
    fi
    
    file_count=$(echo "$modified_files" | wc -l)
    log_color "$YELLOW" "⚠️  Found $file_count modified files:"
    echo ""
    
    echo "$modified_files" | while IFS= read -r file; do
        echo "  - $file"
    done
    
    echo ""
    
    # Check if multiple agents might have modified same files
    # This is a heuristic - we can't know for sure without deeper tracking
    if [ $file_count -gt 10 ]; then
        log_color "$RED" "⚠️  HIGH CONFLICT RISK: Many files modified simultaneously"
        log_color "$RED" "    Recommendation: Review git diff carefully before committing"
    fi
    
    return $file_count
}

# Recommend actions
recommend_actions() {
    agent_count=$1
    file_count=$2
    
    echo ""
    log_color "$BLUE" "=== Recommendations ==="
    
    if [ $agent_count -eq 0 ]; then
        log_color "$GREEN" "✓ All agents have completed. Safe to commit changes."
        return 0
    fi
    
    if [ $agent_count -gt 4 ]; then
        log_color "$RED" "❌ TOO MANY CONCURRENT AGENTS ($agent_count > 4)"
        echo "   Action: Terminate excess agents to prevent conflicts"
        echo "   Command: kill -TERM <PID>"
    elif [ $agent_count -gt 1 ] && [ $file_count -gt 0 ]; then
        log_color "$YELLOW" "⚠️  MODERATE RISK: Multiple agents with file changes"
        echo "   Action: Monitor agents, wait for completion before committing"
        echo "   Command: watch -n 5 './scripts/agent-monitor.sh'"
    else
        log_color "$GREEN" "✓ Agent activity within safe limits"
    fi
    
    echo ""
}

# Detect duplicate agents
check_duplicate_agents() {
    log_color "$BLUE" "=== Checking for Duplicate Agents ==="
    
    # Get all agent commands
    agent_commands=$(ps aux | grep -i "codex exec" | grep -v grep | grep -v app-server | awk '{for(i=11;i<=NF;i++) printf $i" "; print ""}' || true)
    
    if [ -z "$agent_commands" ]; then
        return 0
    fi
    
    # Simple duplicate detection: look for similar task descriptions
    duplicates=$(echo "$agent_commands" | sort | uniq -d)
    
    if [ -z "$duplicates" ]; then
        log_color "$GREEN" "✓ No duplicate agents detected"
        return 0
    fi
    
    log_color "$RED" "❌ DUPLICATE AGENTS DETECTED:"
    echo "$duplicates"
    echo ""
    log_color "$RED" "   Action: Identify and terminate duplicate agents"
    
    return 1
}

# Main execution
main() {
    echo ""
    log_color "$GREEN" "╔═══════════════════════════════════════════════════╗"
    log_color "$GREEN" "║     AI Agent Orchestration Monitor v1.0          ║"
    log_color "$GREEN" "╚═══════════════════════════════════════════════════╝"
    echo ""
    
    # Create logs directory if needed
    mkdir -p "$AGENTS_DIR"
    
    # Run checks
    check_running_agents
    agent_count=$?
    
    check_file_conflicts
    file_count=$?
    
    check_duplicate_agents
    
    recommend_actions $agent_count $file_count
    
    # Summary
    echo ""
    log_color "$BLUE" "=== Summary ==="
    echo "  Active Agents: $agent_count"
    echo "  Modified Files: $file_count"
    echo "  Log File: $LOG_FILE"
    echo ""
    
    if [ $agent_count -gt 0 ]; then
        echo "Run with --watch to monitor continuously:"
        echo "  watch -n 5 './scripts/agent-monitor.sh'"
        echo ""
        echo "To stop all agents:"
        echo "  pkill -f 'codex exec'"
    fi
}

# Handle watch mode
if [ "${1:-}" = "--watch" ]; then
    watch -n 5 "$0"
else
    main
fi
