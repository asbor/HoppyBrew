#!/bin/bash
# PlantUML Processing Utilities for Wiki Generator
# Handles rendering, categorization, and integration of PlantUML diagrams

set -euo pipefail

# Configuration
PROJECT_ROOT="${1:-/home/asbo/repo/HoppyBrew}"
PLANTUML_SOURCE="$PROJECT_ROOT/documents/docs/plantuml"
WIKI_OUTPUT="${2:-$PROJECT_ROOT/documents/wiki-exports}"
DIAGRAM_OUTPUT="$WIKI_OUTPUT/diagrams"

# Color codes
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

# Ensure PlantUML is available
setup_plantuml() {
    log_color "$BLUE" "🔧 Setting up PlantUML renderer..."
    
    if command -v plantuml &> /dev/null; then
        log_color "$GREEN" "✓ PlantUML command available"
        return 0
    elif [[ -f "/usr/share/plantuml/plantuml.jar" ]]; then
        log_color "$GREEN" "✓ PlantUML jar available"
        alias plantuml="java -jar \"/usr/share/plantuml/plantuml.jar\""
        return 0
    elif [[ -f "$PROJECT_ROOT/tools/plantuml-1.2024.3.jar" ]]; then
        log_color "$GREEN" "✓ Using bundled PlantUML jar"
        alias plantuml="java -jar \"$PROJECT_ROOT/tools/plantuml-1.2024.3.jar\""
        return 0
    else
        log_color "$YELLOW" "⚠️  Installing PlantUML..."
        
        # Try package manager installation
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y plantuml
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y plantuml
        else
            # Download jar directly
            log_color "$YELLOW" "📥 Downloading PlantUML jar..."
            mkdir -p /tmp/plantuml
            wget -O /tmp/plantuml/plantuml.jar "http://plantuml.com/plantuml.jar"
            alias plantuml="java -jar \"/tmp/plantuml/plantuml.jar\""
        fi
        
        log_color "$GREEN" "✓ PlantUML installed"
    fi
}

# Create output directory structure
create_output_structure() {
    log_color "$BLUE" "📁 Creating output directory structure..."
    
    mkdir -p "$DIAGRAM_OUTPUT"/{architecture,database,workflows,components,api,misc}
    
    log_color "$GREEN" "✓ Output directories created"
}

# Categorize PlantUML files
categorize_files() {
    local puml_file="$1"
    local filename=$(basename "$puml_file" .puml)
    local dirname=$(dirname "$puml_file")
    
    # Determine category based on file path and name
    case "$dirname" in
        *ERD*|*Database*)
            echo "database"
            ;;
        *Component*|*component*)
            echo "components"
            ;;
        *API*|*api*)
            echo "api"
            ;;
        *Workflow*|*workflow*|*Process*)
            echo "workflows"
            ;;
        *)
            case "$filename" in
                *ERD*|*erd*|*Database*|*database*|*Schema*)
                    echo "database"
                    ;;
                *Component*|*component*|*Architecture*)
                    echo "architecture"
                    ;;
                *API*|*api*|*endpoint*)
                    echo "api"
                    ;;
                *workflow*|*process*|*flow*)
                    echo "workflows"
                    ;;
                *)
                    echo "misc"
                    ;;
            esac
            ;;
    esac
}

# Render single PlantUML file
render_puml_file() {
    local puml_file="$1"
    local category="$2"
    local filename=$(basename "$puml_file" .puml)
    local target_dir="$DIAGRAM_OUTPUT/$category"
    
    log_color "$YELLOW" "🖼️  Rendering: $filename"
    
    # Render to PNG
    if plantuml -tpng "$puml_file" -o "$target_dir" 2>/dev/null; then
        log_color "$GREEN" "  ✓ PNG: $target_dir/${filename}.png"
    else
        log_color "$RED" "  ❌ Failed to render PNG"
        return 1
    fi
    
    # Render to SVG
    if plantuml -tsvg "$puml_file" -o "$target_dir" 2>/dev/null; then
        log_color "$GREEN" "  ✓ SVG: $target_dir/${filename}.svg"
    else
        log_color "$YELLOW" "  ⚠️  SVG render failed (non-critical)"
    fi
    
    return 0
}

# Process all PlantUML files
process_all_puml() {
    log_color "$BLUE" "🔄 Processing all PlantUML files..."
    
    local total_files=0
    local rendered_files=0
    local failed_files=0
    
    # Find all .puml files
    while IFS= read -r -d '' puml_file; do
        ((total_files++))
        
        # Categorize file
        category=$(categorize_files "$puml_file")
        
        # Render file
        if render_puml_file "$puml_file" "$category"; then
            ((rendered_files++))
        else
            ((failed_files++))
        fi
        
    done < <(find "$PLANTUML_SOURCE" -name "*.puml" -type f -print0)
    
    log_color "$BLUE" "📊 Processing Summary:"
    echo "   Total files: $total_files"
    echo "   Rendered: $rendered_files"
    echo "   Failed: $failed_files"
    
    return 0
}

# Generate diagram index
generate_diagram_index() {
    log_color "$BLUE" "📋 Generating diagram index..."
    
    local index_file="$WIKI_OUTPUT/Diagram-Index.md"
    
    cat > "$index_file" << 'EOF'
# PlantUML Diagram Index

This page provides a comprehensive catalog of all PlantUML diagrams in the HoppyBrew project.

## Architecture Diagrams
High-level system architecture and component relationships.

EOF
    
    # Add architecture diagrams
    for png_file in "$DIAGRAM_OUTPUT/architecture"/*.png; do
        if [[ -f "$png_file" ]]; then
            local filename=$(basename "$png_file" .png)
            echo "### $filename" >> "$index_file"
            echo "![${filename}](diagrams/architecture/${filename}.png)" >> "$index_file"
            echo "" >> "$index_file"
        fi
    done
    
    cat >> "$index_file" << 'EOF'

## Database Schema Diagrams
Entity Relationship Diagrams (ERD) and database structure.

EOF
    
    # Add database diagrams
    for png_file in "$DIAGRAM_OUTPUT/database"/*.png; do
        if [[ -f "$png_file" ]]; then
            local filename=$(basename "$png_file" .png)
            echo "### $filename" >> "$index_file"
            echo "![${filename}](diagrams/database/${filename}.png)" >> "$index_file"
            echo "" >> "$index_file"
        fi
    done
    
    cat >> "$index_file" << 'EOF'

## Component Diagrams
Detailed component structure and interactions.

EOF
    
    # Add component diagrams
    for png_file in "$DIAGRAM_OUTPUT/components"/*.png; do
        if [[ -f "$png_file" ]]; then
            local filename=$(basename "$png_file" .png)
            echo "### $filename" >> "$index_file"
            echo "![${filename}](diagrams/components/${filename}.png)" >> "$index_file"
            echo "" >> "$index_file"
        fi
    done
    
    cat >> "$index_file" << 'EOF'

## Workflow Diagrams
Process flows and business logic diagrams.

EOF
    
    # Add workflow diagrams
    for png_file in "$DIAGRAM_OUTPUT/workflows"/*.png; do
        if [[ -f "$png_file" ]]; then
            local filename=$(basename "$png_file" .png)
            echo "### $filename" >> "$index_file"
            echo "![${filename}](diagrams/workflows/${filename}.png)" >> "$index_file"
            echo "" >> "$index_file"
        fi
    done
    
    cat >> "$index_file" << 'EOF'

## API Diagrams
API interaction patterns and endpoint relationships.

EOF
    
    # Add API diagrams
    for png_file in "$DIAGRAM_OUTPUT/api"/*.png; do
        if [[ -f "$png_file" ]]; then
            local filename=$(basename "$png_file" .png)
            echo "### $filename" >> "$index_file"
            echo "![${filename}](diagrams/api/${filename}.png)" >> "$index_file"
            echo "" >> "$index_file"
        fi
    done
    
    log_color "$GREEN" "✓ Diagram index generated: $index_file"
}

# Main execution
main() {
    log_color "$BLUE" "╔════════════════════════════════════════╗"
    log_color "$BLUE" "║     PlantUML Processing Utilities      ║"
    log_color "$BLUE" "╚════════════════════════════════════════╝"
    echo ""
    
    # Validate inputs
    if [[ ! -d "$PLANTUML_SOURCE" ]]; then
        log_color "$RED" "❌ PlantUML source directory not found: $PLANTUML_SOURCE"
        exit 1
    fi
    
    # Setup environment
    setup_plantuml
    create_output_structure
    
    # Process files
    process_all_puml
    
    # Generate index
    generate_diagram_index
    
    log_color "$GREEN" "🎉 PlantUML processing complete!"
    echo ""
    log_color "$BLUE" "📁 Output location: $DIAGRAM_OUTPUT"
    log_color "$BLUE" "📋 Index file: $WIKI_OUTPUT/Diagram-Index.md"
}

# Handle command line arguments
case "${1:-help}" in
    "help"|"--help"|"-h")
        echo "PlantUML Processing Utilities"
        echo ""
        echo "Usage:"
        echo "  $0 [project_root] [output_directory]"
        echo ""
        echo "Examples:"
        echo "  $0 /home/asbo/repo/HoppyBrew /path/to/wiki"
        echo "  $0  # Uses default paths"
        exit 0
        ;;
    *)
        main
        ;;
esac
