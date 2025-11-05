#!/bin/bash
# Agent Cleanup & Safe Shutdown
# Terminates running agents and prepares workspace for commit

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_color() {
    color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Kill all running Codex agents
kill_agents() {
    log_color "$BLUE" "╔═══════════════════════════════════════════════════╗"
    log_color "$BLUE" "║        Terminating Running Codex Agents           ║"
    log_color "$BLUE" "╚═══════════════════════════════════════════════════╝"
    echo ""
    
    # Find codex processes
    codex_pids=$(ps aux | grep -E "codex exec" | grep -v grep | grep -v app-server | awk '{print $2}' || true)
    
    if [ -z "$codex_pids" ]; then
        log_color "$GREEN" "✓ No running Codex agents found"
        return 0
    fi
    
    # Count agents
    agent_count=$(echo "$codex_pids" | wc -l)
    log_color "$YELLOW" "Found $agent_count running agents"
    echo ""
    
    # Show agents before killing
    ps aux | grep -E "codex exec" | grep -v grep | grep -v app-server | while read line; do
        pid=$(echo "$line" | awk '{print $2}')
        terminal=$(echo "$line" | awk '{print $7}')
        echo "  PID $pid on $terminal"
    done
    echo ""
    
    # Ask for confirmation
    if [ "${1:-}" != "--force" ]; then
        read -p "Kill all $agent_count agents? (y/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_color "$YELLOW" "Aborted. Use --force to skip confirmation."
            exit 1
        fi
    fi
    
    # Kill agents
    echo "$codex_pids" | while read pid; do
        if kill -0 $pid 2>/dev/null; then
            log_color "$YELLOW" "Terminating PID $pid..."
            kill -TERM $pid 2>/dev/null || true
            sleep 0.5
            
            # Force kill if still running
            if kill -0 $pid 2>/dev/null; then
                log_color "$RED" "Force killing PID $pid..."
                kill -KILL $pid 2>/dev/null || true
            fi
        fi
    done
    
    echo ""
    log_color "$GREEN" "✓ All agents terminated"
}

# Verify no agents running
verify_clean() {
    log_color "$BLUE" "╔═══════════════════════════════════════════════════╗"
    log_color "$BLUE" "║           Verifying Clean State                   ║"
    log_color "$BLUE" "╚═══════════════════════════════════════════════════╝"
    echo ""
    
    remaining=$(ps aux | grep -E "codex exec" | grep -v grep | grep -v app-server | wc -l)
    
    if [ $remaining -eq 0 ]; then
        log_color "$GREEN" "✓ No running agents"
    else
        log_color "$RED" "❌ $remaining agents still running!"
        ps aux | grep -E "codex exec" | grep -v grep | grep -v app-server
        exit 1
    fi
    
    # Check file state
    modified=$(git status --short | wc -l)
    if [ $modified -gt 0 ]; then
        log_color "$YELLOW" "⚠️  $modified files with uncommitted changes"
        echo "   Run ./scripts/agent-review.sh to review changes"
    else
        log_color "$GREEN" "✓ Working directory clean"
    fi
    
    echo ""
}

# Show next steps
show_next_steps() {
    log_color "$BLUE" "╔═══════════════════════════════════════════════════╗"
    log_color "$BLUE" "║              Next Steps                           ║"
    log_color "$BLUE" "╚═══════════════════════════════════════════════════╝"
    echo ""
    
    echo "1. Review changes:"
    echo "   $ ./scripts/agent-review.sh"
    echo ""
    
    echo "2. Test changes:"
    echo "   $ docker compose exec backend pytest -v"
    echo ""
    
    echo "3. Commit changes:"
    echo "   $ git add -A"
    echo "   $ git commit -m 'feat: Multi-agent deployment phase complete'"
    echo ""
    
    echo "4. Push to remote:"
    echo "   $ git push origin main"
    echo ""
}

# Main
main() {
    echo ""
    kill_agents "$@"
    verify_clean
    show_next_steps
    log_color "$GREEN" "✓ Agent cleanup complete. Workspace ready for commit."
    echo ""
}

main "$@"
