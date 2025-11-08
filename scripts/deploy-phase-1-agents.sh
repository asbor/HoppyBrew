#!/bin/bash

# Phase 1 Agent Deployment Script
# Deploys: Architecture, Data Model, and API Documentation agents
# Priority: CRITICAL (1) - Foundation agents that unblock other work

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
AGENTS_DIR=".agents"
LOCKS_DIR="${AGENTS_DIR}/locks"
LOGS_DIR="${AGENTS_DIR}/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create necessary directories
mkdir -p "${LOCKS_DIR}"
mkdir -p "${LOGS_DIR}"

# Agent definitions for Phase 1
PHASE1_AGENTS=(
    "ARCH-001:ARCHITECTURE:Fix component diagram issue #348"
    "DATA-001:DATA_MODEL:Audit database models and create ERDs"
    "API-001:API_DOCS:Document all REST endpoints"
)

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   HoppyBrew Phase 1 Agent Deployment              ║${NC}"
echo -e "${BLUE}║   Deploying 3 Critical Foundation Agents          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check if agent is already running
check_agent_running() {
    local agent_id=$1
    if [ -f "${LOCKS_DIR}/${agent_id}.lock" ]; then
        return 0  # Running
    else
        return 1  # Not running
    fi
}

# Function to create agent lock
create_agent_lock() {
    local agent_id=$1
    local agent_name=$2
    echo "{
  \"agent_id\": \"${agent_id}\",
  \"agent_name\": \"${agent_name}\",
  \"status\": \"RUNNING\",
  \"started_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
  \"pid\": $$,
  \"priority\": 1
}" > "${LOCKS_DIR}/${agent_id}.lock"
}

# Function to deploy single agent
deploy_agent() {
    local agent_id=$1
    local agent_name=$2
    local mission=$3
    
    echo -e "${YELLOW}[${agent_id}]${NC} Deploying ${agent_name}..."
    
    # Check if already running
    if check_agent_running "${agent_id}"; then
        echo -e "${RED}[${agent_id}]${NC} Already running! Skipping..."
        return 1
    fi
    
    # Create lock file
    create_agent_lock "${agent_id}" "${agent_name}"
    
    # Update agent context file
    local context_file="${AGENTS_DIR}/CODEX_AGENT_${agent_name}.md"
    if [ ! -f "${context_file}" ]; then
        echo -e "${RED}[${agent_id}]${NC} Context file not found: ${context_file}"
        rm -f "${LOCKS_DIR}/${agent_id}.lock"
        return 1
    fi
    
    # Update status in context file (using sed)
    sed -i 's/\*\*Status\*\*: REGISTERED/**Status**: RUNNING/' "${context_file}" || true
    
    # Log deployment
    local log_file="${LOGS_DIR}/${agent_id}_${TIMESTAMP}.log"
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Agent ${agent_id} deployed" > "${log_file}"
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Mission: ${mission}" >> "${log_file}"
    
    echo -e "${GREEN}[${agent_id}]${NC} Deployed successfully!"
    echo -e "${GREEN}[${agent_id}]${NC} Mission: ${mission}"
    echo -e "${GREEN}[${agent_id}]${NC} Log: ${log_file}"
    echo ""
    
    return 0
}

# Deploy Phase 1 agents
echo -e "${BLUE}Starting Phase 1 deployment...${NC}"
echo ""

deployed_count=0
failed_count=0

for agent_def in "${PHASE1_AGENTS[@]}"; do
    IFS=':' read -r agent_id agent_name mission <<< "$agent_def"
    
    if deploy_agent "${agent_id}" "${agent_name}" "${mission}"; then
        ((deployed_count++))
    else
        ((failed_count++))
    fi
done

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Phase 1 Deployment Summary${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo -e "Deployed: ${GREEN}${deployed_count}${NC}"
echo -e "Failed:   ${RED}${failed_count}${NC}"
echo -e "Total:    ${deployed_count} / ${#PHASE1_AGENTS[@]}"
echo ""

# Show active agents
echo -e "${BLUE}Active Agents:${NC}"
for lock_file in "${LOCKS_DIR}"/*.lock; do
    if [ -f "${lock_file}" ]; then
        agent_id=$(basename "${lock_file}" .lock)
        echo -e "  ${GREEN}✓${NC} ${agent_id}"
    fi
done
echo ""

# Instructions for monitoring
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "1. Monitor agents: ${BLUE}./scripts/agent-status.sh${NC}"
echo -e "2. View logs:      ${BLUE}tail -f ${LOGS_DIR}/*.log${NC}"
echo -e "3. Check progress: ${BLUE}cat ${AGENTS_DIR}/CODEX_AGENT_*.md | grep 'Overall Progress'${NC}"
echo ""

# Git commit deployment
echo -e "${YELLOW}Committing Phase 1 deployment...${NC}"
git add "${AGENTS_DIR}"
git commit -m "[DEPLOY] Phase 1 agents deployed: Architecture, Data Model, API Docs

- ARCH-001: Fix component diagram issue #348
- DATA-001: Audit database models and create ERDs
- API-001: Document all REST endpoints

Priority: CRITICAL (1)
Status: RUNNING
Deployed: $(date -u +%Y-%m-%dT%H:%M:%SZ)
" || echo -e "${YELLOW}Nothing to commit (already up to date)${NC}"

echo ""
echo -e "${GREEN}Phase 1 deployment complete! 🚀${NC}"
echo -e "${BLUE}Agents are now running and will coordinate automatically.${NC}"
echo ""
