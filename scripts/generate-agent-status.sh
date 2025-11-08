#!/bin/bash

# Generate agent status JSON for dashboard
# This script reads all agent context files and generates JSON data

OUTPUT_FILE=".agents/status.json"

echo "{"
echo '  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",'
echo '  "agents": ['

first=true

# Read all agent files
for agent_file in .agents/CODEX_AGENT_*.md; do
    if [ -f "$agent_file" ]; then
        agent_name=$(basename "$agent_file" .md | sed 's/CODEX_AGENT_//')
        
        # Extract progress percentage
        progress=$(grep "^\*\*Overall Progress\*\*:" "$agent_file" | head -1 | sed 's/.*: //' | sed 's/%//')
        if [ -z "$progress" ]; then
            progress="0"
        fi
        
        # Extract status
        status=$(grep "^- \*\*Status\*\*:" "$agent_file" | head -1 | sed 's/.*: //')
        if [ -z "$status" ]; then
            status="STANDBY"
        fi
        
        # Extract agent ID
        agent_id=$(grep "^- \*\*Agent ID\*\*:" "$agent_file" | head -1 | sed 's/.*`//' | sed 's/`.*//')
        
        # Extract last update
        last_update=$(grep "^\*\*Last Update\*\*:" "$agent_file" | head -1 | sed 's/.*: //')
        
        # Extract current task
        current_task=$(grep "^\*\*Current Task\*\*:" "$agent_file" | head -1 | sed 's/.*: //')
        
        if [ "$first" = true ]; then
            first=false
        else
            echo ","
        fi
        
        echo "    {"
        echo "      \"name\": \"$agent_name\","
        echo "      \"id\": \"$agent_id\","
        echo "      \"status\": \"$status\","
        echo "      \"progress\": $progress,"
        echo "      \"last_update\": \"$last_update\","
        echo "      \"current_task\": \"$current_task\""
        echo -n "    }"
    fi
done

echo ""
echo "  ]"
echo "}"

