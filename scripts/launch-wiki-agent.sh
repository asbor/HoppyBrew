#!/bin/bash
# HoppyBrew Wiki Generator - Headless Codex Agent Launcher
# Generates comprehensive GitHub wiki with PlantUML integration

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

log_color() {
    color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Configuration
PROJECT_ROOT="/home/asbo/repo/HoppyBrew"
AGENT_CONTEXT=".agents/CODEX_AGENT_WIKI_GENERATOR.md"
LOG_FILE="/tmp/wiki_generator_agent.log"
MCP_ACCESS=${1:-false}  # true/false for MCP server access

main() {
    log_color "$BLUE" "╔══════════════════════════════════════════════════════════╗"
    log_color "$BLUE" "║          HoppyBrew Wiki Generator Agent                  ║"
    log_color "$BLUE" "║               Headless Execution Mode                    ║"
    log_color "$BLUE" "╚══════════════════════════════════════════════════════════╝"
    echo ""
    
    # Validate environment
    validate_environment
    
    # Prepare agent task
    if [[ "$MCP_ACCESS" == "true" ]]; then
        prepare_full_publishing_task
    else
        prepare_export_task
    fi
    
    # Execute agent
    execute_wiki_agent
    
    # Monitor and report
    monitor_progress
    
    log_color "$GREEN" "🎉 Wiki generator agent deployment complete!"
}

validate_environment() {
    log_color "$YELLOW" "🔍 Validating environment..."
    
    # Check if we're in the right directory
    if [[ ! -f "$PROJECT_ROOT/README.md" ]]; then
        log_color "$RED" "❌ Error: Not in HoppyBrew project root"
        exit 1
    fi
    
    # Check for PlantUML files
    puml_count=$(find "$PROJECT_ROOT/documents/docs/plantuml" -name "*.puml" 2>/dev/null | wc -l)
    log_color "$GREEN" "✓ Found $puml_count PlantUML files to process"
    
    # Check for Codex CLI
    if ! command -v codex &> /dev/null; then
        log_color "$RED" "❌ Error: Codex CLI not found"
        exit 1
    fi
    
    # Check for PlantUML renderer
    if command -v plantuml &> /dev/null; then
        log_color "$GREEN" "✓ PlantUML renderer available"
    elif [[ -f "/usr/share/plantuml/plantuml.jar" ]]; then
        log_color "$GREEN" "✓ PlantUML jar file available"
    else
        log_color "$YELLOW" "⚠️  PlantUML not found - will attempt installation"
    fi
    
    log_color "$GREEN" "✓ Environment validation complete"
    echo ""
}

prepare_full_publishing_task() {
    log_color "$PURPLE" "🚀 Preparing FULL PUBLISHING task (with MCP access)..."
    
    TASK_DESCRIPTION="Generate comprehensive GitHub wiki for HoppyBrew project with PlantUML integration and direct publishing.

OBJECTIVES:
1. Process 220+ existing PlantUML files from documents/docs/plantuml/
2. Render all diagrams to PNG and SVG formats
3. Create comprehensive wiki structure with technical documentation
4. Generate architecture, API, database, and component documentation
5. Embed rendered diagrams in appropriate wiki pages
6. Publish directly to GitHub wiki repository using MCP server access

DELIVERABLES:
- Complete GitHub wiki with navigation
- Rendered diagram catalog (PNG/SVG)
- Technical architecture documentation
- API reference with interaction diagrams
- Database schema documentation with ERD
- Development and deployment guides
- User onboarding documentation

ACCESS LEVEL: Full GitHub repository and wiki publishing access via MCP server"
}

prepare_export_task() {
    log_color "$PURPLE" "📁 Preparing EXPORT task (local generation)..."
    
    TASK_DESCRIPTION="Create comprehensive wiki documentation structure for HoppyBrew project with PlantUML processing.

OBJECTIVES:
1. Process all PlantUML files from documents/docs/plantuml/ directory
2. Render diagrams to PNG and SVG formats in local structure
3. Generate complete wiki documentation with embedded diagrams
4. Create technical documentation for architecture, API, database schemas
5. Prepare export-ready wiki structure in documents/wiki-exports/
6. Provide complete setup instructions for manual GitHub wiki publishing

DELIVERABLES:
- Local wiki structure ready for upload
- Rendered diagram collection organized by category
- Complete technical documentation with embedded diagrams
- Navigation structure and cross-references
- Manual publishing instructions and scripts
- Quality assurance checklist

ACCESS LEVEL: Local file system only, export for manual publishing"
}

execute_wiki_agent() {
    log_color "$YELLOW" "🤖 Launching Codex wiki generator agent..."
    echo ""
    
    cd "$PROJECT_ROOT"
    
    # Launch agent in background with output logging
    (
        log_color "$BLUE" "Agent Task Description:"
        echo "$TASK_DESCRIPTION"
        echo ""
        
        # Execute the agent
        codex exec -s workspace-write "$TASK_DESCRIPTION"
        
    ) 2>&1 | tee "$LOG_FILE" &
    
    AGENT_PID=$!
    
    log_color "$GREEN" "✓ Wiki generator agent launched (PID: $AGENT_PID)"
    log_color "$BLUE" "📝 Logs: tail -f $LOG_FILE"
    echo ""
}

monitor_progress() {
    log_color "$YELLOW" "📊 Monitoring agent progress..."
    
    # Monitor for key milestones
    local start_time=$(date +%s)
    local timeout=3600  # 1 hour timeout
    
    while true; do
        current_time=$(date +%s)
        elapsed=$((current_time - start_time))
        
        # Check if agent is still running
        if ! kill -0 "$AGENT_PID" 2>/dev/null; then
            log_color "$GREEN" "✓ Agent completed execution"
            break
        fi
        
        # Check for timeout
        if [[ $elapsed -gt $timeout ]]; then
            log_color "$RED" "⏰ Agent timeout after 1 hour"
            kill "$AGENT_PID" 2>/dev/null || true
            break
        fi
        
        # Show progress indicators
        local minutes=$((elapsed / 60))
        echo -ne "\r⏱️  Agent running: ${minutes}m elapsed"
        
        sleep 30
    done
    
    echo ""
}

show_results() {
    log_color "$BLUE" "📋 Agent Execution Summary:"
    echo "=================================="
    
    if [[ "$MCP_ACCESS" == "true" ]]; then
        log_color "$GREEN" "📚 Wiki published to: https://github.com/asbor/HoppyBrew/wiki"
        log_color "$GREEN" "🖼️  Diagrams rendered and embedded"
    else
        log_color "$GREEN" "📁 Wiki structure created in: documents/wiki-exports/"
        log_color "$GREEN" "🖼️  Diagrams rendered in: documents/wiki-exports/diagrams/"
        echo ""
        log_color "$YELLOW" "📤 Next steps for manual publishing:"
        echo "   1. Review generated content in documents/wiki-exports/"
        echo "   2. Clone wiki repository: git clone https://github.com/asbor/HoppyBrew.wiki.git"
        echo "   3. Copy content from wiki-exports/ to cloned repository"
        echo "   4. Commit and push to publish"
    fi
    
    echo ""
    log_color "$BLUE" "📈 Statistics:"
    if [[ -d "documents/wiki-exports" ]]; then
        local wiki_files=$(find documents/wiki-exports -name "*.md" 2>/dev/null | wc -l)
        local diagram_files=$(find documents/wiki-exports/diagrams -name "*.png" 2>/dev/null | wc -l)
        echo "   - Wiki pages created: $wiki_files"
        echo "   - Diagrams rendered: $diagram_files"
    fi
    
    echo ""
    log_color "$GREEN" "📝 Full logs available at: $LOG_FILE"
}

# Handle script arguments
case "${1:-help}" in
    "true"|"full"|"publish")
        MCP_ACCESS=true
        main
        show_results
        ;;
    "false"|"export"|"local")
        MCP_ACCESS=false
        main
        show_results
        ;;
    "help"|"--help"|"-h")
        log_color "$BLUE" "HoppyBrew Wiki Generator - Headless Agent"
        echo ""
        echo "Usage:"
        echo "  $0 [true|false]   # MCP server access"
        echo "  $0 full           # Full publishing with MCP access"
        echo "  $0 export         # Local generation only"
        echo ""
        echo "Examples:"
        echo "  $0 true           # Generate and publish to GitHub wiki"
        echo "  $0 false          # Generate locally for manual upload"
        echo ""
        exit 0
        ;;
    *)
        log_color "$RED" "❌ Invalid argument. Use 'help' for usage information."
        exit 1
        ;;
esac