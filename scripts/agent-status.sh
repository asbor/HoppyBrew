#!/bin/bash

# 🎭 Puppet Master Agent Status Monitor
# Real-time monitoring and control of the Codex AI Agent Army

set -euo pipefail

AGENT_DIR=".agents"
REPO_OWNER="asbor"
REPO_NAME="HoppyBrew"

echo "🎭 PUPPET MASTER CONTROL CENTER"
echo "============================="
echo "📅 Status Check: $(date)"
echo ""

# Function to get agent status
get_agent_status() {
    local agent_file="$1"
    local agent_name=$(basename "$agent_file" .md | sed 's/CODEX_AGENT_//')
    
    echo "🤖 Agent: $agent_name"
    
    # Extract current status from agent file
    if grep -q "🟢.*ACTIVE" "$agent_file"; then
        echo "   📊 Status: 🟢 ACTIVE"
    elif grep -q "🟡.*WORKING" "$agent_file"; then
        echo "   📊 Status: 🟡 WORKING"
    elif grep -q "🔴.*OFFLINE" "$agent_file"; then
        echo "   📊 Status: 🔴 OFFLINE"
    else
        echo "   📊 Status: 🔵 STANDBY"
    fi
    
    # Extract progress if available
    local progress=$(grep "Progress" "$agent_file" | head -1 | grep -o '[0-9]\+%' || echo "0%")
    echo "   📈 Progress: $progress"
    
    # Extract current focus
    local focus=$(grep "Current Focus" "$agent_file" | cut -d':' -f2 | sed 's/^[[:space:]]*//' || echo "Initializing")
    echo "   🎯 Focus: $focus"
    
    echo ""
}

# Function to analyze GitHub issues assigned to agents
analyze_agent_targets() {
    echo "🎯 AGENT TARGET ANALYSIS"
    echo "========================"
    
    # Security alerts
    local security_count=$(gh issue list --label "security-alert" --state open --json number --jq length 2>/dev/null || echo "0")
    echo "🛡️  Security Alerts: $security_count open issues"
    
    # Enhancement requests  
    local enhancement_count=$(gh issue list --label "enhancement" --state open --json number --jq length 2>/dev/null || echo "0")
    echo "🚀 Enhancements: $enhancement_count open issues"
    
    # CI failures
    local ci_count=$(gh issue list --label "ci-failure" --state open --json number --jq length 2>/dev/null || echo "0")
    echo "🔄 CI Issues: $ci_count open issues"
    
    echo ""
}

# Function to show agent task progress
show_agent_progress() {
    echo "📊 AGENT PROGRESS SUMMARY"
    echo "========================="
    
    local total_agents=0
    local active_agents=0
    local completed_tasks=0
    
    if [[ -d "$AGENT_DIR" ]]; then
        for agent_file in "$AGENT_DIR"/CODEX_AGENT_*.md; do
            if [[ -f "$agent_file" ]]; then
                total_agents=$((total_agents + 1))
                
                if grep -q "🟢.*ACTIVE\|🟡.*WORKING" "$agent_file"; then
                    active_agents=$((active_agents + 1))
                fi
                
                # Count completed tasks (✅ markers)
                local agent_completed=0
                if [[ -f "$agent_file" ]]; then
                    agent_completed=$(grep -c "✅" "$agent_file" 2>/dev/null) || agent_completed=0
                fi
                completed_tasks=$((completed_tasks + agent_completed))
            fi
        done
    fi
    
    echo "🤖 Total Agents: $total_agents"
    echo "⚡ Active Agents: $active_agents"
    echo "✅ Completed Tasks: $completed_tasks"
    if [[ $total_agents -gt 0 ]]; then
        local efficiency=$(( active_agents * 100 / total_agents ))
        echo "🎯 Agent Efficiency: ${efficiency}%"
    else
        echo "🎯 Agent Efficiency: 0%"
    fi
    echo ""
}

# Function to suggest next puppet master actions
suggest_actions() {
    echo "🎮 PUPPET MASTER RECOMMENDATIONS"
    echo "================================="
    
    local security_count=$(gh issue list --label "security-alert" --state open --json number --jq length 2>/dev/null || echo "0")
    
    if [[ $security_count -gt 5 ]]; then
        echo "🚨 HIGH PRIORITY: Deploy additional security agents"
        echo "   Command: ./scripts/deploy-security-specialist.sh"
    fi
    
    echo "📚 Wiki Enhancement: Check agent progress on wiki optimization"
    echo "   Command: ./scripts/check-wiki-metrics.sh"
    
    echo "🧪 Test Coverage: Monitor test generation progress"
    echo "   Command: ./scripts/test-coverage-report.sh"
    
    echo "🔄 CI/CD Pipeline: Review automation implementation"
    echo "   Command: ./scripts/ci-pipeline-status.sh"
    
    echo ""
}

# Main execution
echo "🔍 Scanning agent deployment directory..."

if [[ ! -d "$AGENT_DIR" ]]; then
    echo "❌ No agents deployed yet!"
    echo "   Run: ./scripts/deploy-agent-army.sh"
    exit 1
fi

echo "📂 Agent Directory: $AGENT_DIR"
echo ""

# Show status of all deployed agents
echo "🤖 ACTIVE AGENT STATUS"
echo "======================"

agent_count=0
for agent_file in "$AGENT_DIR"/CODEX_AGENT_*.md; do
    if [[ -f "$agent_file" ]]; then
        get_agent_status "$agent_file"
        agent_count=$((agent_count + 1))
    fi
done

if [[ $agent_count -eq 0 ]]; then
    echo "⚠️  No agent configuration files found"
    echo "   Deploy agents with: ./scripts/deploy-agent-army.sh"
else
    analyze_agent_targets
    show_agent_progress
    suggest_actions
fi

echo "🎭 PUPPET MASTER STATUS: MONITORING ACTIVE"
echo "🌐 Repository: https://github.com/$REPO_OWNER/$REPO_NAME"
echo "📊 Live Issues: https://github.com/$REPO_OWNER/$REPO_NAME/issues"
echo "📚 Wiki Status: https://github.com/$REPO_OWNER/$REPO_NAME/wiki"
echo ""
echo "✨ Autonomous AI Enhancement System: OPERATIONAL ✨"