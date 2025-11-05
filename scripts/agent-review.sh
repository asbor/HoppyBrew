#!/bin/bash
# Agent Changes Review & Commit Script
# Safely reviews and commits changes from completed agents

set -euo pipefail

AGENTS_DIR=".agents"
LOG_FILE="$AGENTS_DIR/review.log"

# Colors
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

# Group files by agent responsibility
categorize_files() {
    log_color "$BLUE" "╔═══════════════════════════════════════════════════╗"
    log_color "$BLUE" "║   Categorizing Files by Agent Responsibility     ║"
    log_color "$BLUE" "╚═══════════════════════════════════════════════════╝"
    echo ""
    
    # Agent 1: Backend API / Inventory Endpoints
    echo -e "${GREEN}Agent 1: Backend API - Inventory Endpoints${NC}"
    git status --short | grep -E "inventory_(hops|fermentables|yeasts|miscs|inventory_fermentables)\.py" || echo "  (none)"
    echo ""
    
    # Agent 2: Database / Schemas / Alembic
    echo -e "${GREEN}Agent 2: Database - Schemas & Models${NC}"
    git status --short | grep -E "Database/(Schemas|Models)|alembic|seed" || echo "  (none)"
    echo ""
    
    # Agent 3: Business Logic / Calculations
    echo -e "${GREEN}Agent 3: Business Logic - Brewing Calculations${NC}"
    git status --short | grep -E "modules/brewing_calculations|test_modules" || echo "  (none)"
    echo ""
    
    # Agent 4: Documentation
    echo -e "${GREEN}Agent 4: API Documentation${NC}"
    git status --short | grep -E "README_API|main\.py|__init__|endpoints/__init__" || echo "  (none)"
    echo ""
    
    # Orchestration System
    echo -e "${YELLOW}Orchestration System (New)${NC}"
    git status --short | grep -E "\.agents/|scripts/agent" || echo "  (none)"
    echo ""
    
    # Unclassified
    echo -e "${YELLOW}Other Changes${NC}"
    git status --short | grep -vE "inventory_|Database/|modules/brewing|test_modules|README_API|main\.py|__init__|\.agents/|scripts/agent|alembic|seed" || echo "  (none)"
    echo ""
}

# Check for potential conflicts
check_conflicts() {
    log_color "$BLUE" "╔═══════════════════════════════════════════════════╗"
    log_color "$BLUE" "║        Checking for Potential Conflicts          ║"
    log_color "$BLUE" "╚═══════════════════════════════════════════════════╝"
    echo ""
    
    conflicts=0
    
    # Check Pydantic schema changes
    schema_changes=$(git diff --name-only | grep "Database/Schemas/" || true)
    if [ ! -z "$schema_changes" ]; then
        log_color "$YELLOW" "⚠️  Multiple schema files modified - potential for import conflicts"
        echo "   Files: $schema_changes"
        echo ""
        ((conflicts++))
    fi
    
    # Check endpoint changes
    endpoint_changes=$(git diff --name-only | grep "api/endpoints/" || true)
    if [ ! -z "$endpoint_changes" ]; then
        endpoint_count=$(echo "$endpoint_changes" | wc -l)
        if [ $endpoint_count -gt 5 ]; then
            log_color "$YELLOW" "⚠️  $endpoint_count endpoint files modified - review for consistency"
            echo ""
            ((conflicts++))
        fi
    fi
    
    # Check for circular imports
    log_color "$BLUE" "Checking for circular import risks..."
    if grep -r "from Database.Schemas import" services/backend/Database/Schemas/ 2>/dev/null | grep -v ".pyc" > /dev/null; then
        log_color "$RED" "❌ Potential circular import detected in Schemas!"
        echo ""
        ((conflicts++))
    else
        log_color "$GREEN" "✓ No obvious circular imports"
        echo ""
    fi
    
    if [ $conflicts -eq 0 ]; then
        log_color "$GREEN" "✓ No major conflicts detected"
    else
        log_color "$YELLOW" "⚠️  Found $conflicts potential issues - review recommended"
    fi
    echo ""
}

# Show key changes summary
show_key_changes() {
    log_color "$BLUE" "╔═══════════════════════════════════════════════════╗"
    log_color "$BLUE" "║            Key Changes Summary                    ║"
    log_color "$BLUE" "╚═══════════════════════════════════════════════════╝"
    echo ""
    
    # New files
    new_files=$(git status --short | grep "^??" | wc -l)
    modified_files=$(git status --short | grep "^ M" | wc -l)
    added_files=$(git status --short | grep "^A " | wc -l)
    
    echo "  New files: $new_files"
    echo "  Modified files: $modified_files"
    echo "  Staged files: $added_files"
    echo ""
    
    # Lines changed
    if [ $modified_files -gt 0 ] || [ $added_files -gt 0 ]; then
        log_color "$BLUE" "Lines changed (approx):"
        git diff --stat 2>/dev/null | tail -1 || echo "  (run git add first to see stats)"
    fi
    echo ""
}

# Offer commit strategy
offer_commit_strategy() {
    log_color "$BLUE" "╔═══════════════════════════════════════════════════╗"
    log_color "$BLUE" "║          Recommended Commit Strategy             ║"
    log_color "$BLUE" "╚═══════════════════════════════════════════════════╝"
    echo ""
    
    echo "Option 1: Single comprehensive commit (Fast)"
    echo "  $ git add -A"
    echo "  $ git commit -m 'feat: Multi-agent Phase 1 completion'"
    echo ""
    
    echo "Option 2: Separate commits per agent (Clean history)"
    echo "  $ git add services/backend/api/endpoints/inventory_*.py"
    echo "  $ git commit -m 'feat(agent-1): Add inventory CRUD endpoints'"
    echo ""
    echo "  $ git add **/Database/Schemas/* alembic* seeds/"
    echo "  $ git commit -m 'feat(agent-2): Database schemas and migrations'"
    echo ""
    echo "  $ git add services/backend/modules/brewing_calculations.py tests/test_modules/"
    echo "  $ git commit -m 'feat(agent-3): Brewing calculation functions'"
    echo ""
    echo "  $ git add README_API.md services/backend/main.py"
    echo "  $ git commit -m 'feat(agent-4): API documentation'"
    echo ""
    echo "  $ git add .agents/ scripts/agent-*"
    echo "  $ git commit -m 'feat: Agent orchestration system'"
    echo ""
    
    echo "Option 3: Review and commit interactively"
    echo "  $ git add -p  # Interactive staging"
    echo "  $ git commit  # Write detailed message"
    echo ""
}

# Main
main() {
    echo ""
    categorize_files
    check_conflicts
    show_key_changes
    offer_commit_strategy
    
    log_color "$GREEN" "Ready to commit? Choose your strategy above."
    echo ""
}

main
