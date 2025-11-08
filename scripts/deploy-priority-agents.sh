#!/bin/bash

echo "🎯 Deploying Priority Agents for Critical Issues"
echo "================================================"

cd /home/asbo/repo/HoppyBrew

# Deploy CI/CD specialist for Issue #148
echo "🚀 Deploying CI/CD_SPECIALIST for Issue #148..."
gh issue comment 148 --body "🤖 **CODEX AI Agent Deployed**

**Agent Type:** CI/CD_SPECIALIST
**Mission:** Complete missing CI/CD automation pipeline
**Priority:** P1-High 
**ETA:** 6-8 hours

**Immediate Actions:**
✅ Analyzing incomplete test-suite.yml workflow  
✅ Designing automated quality gates (80% coverage minimum)  
✅ Planning staging environment deployment  
✅ Setting up security scanning automation  

**Next Updates:** Every 2 hours until completion
**Agent Status:** 🟢 ACTIVE - Commencing deployment sequence"

# Deploy Testing specialist for Issue #145  
echo "🧪 Deploying TESTING_SPECIALIST for Issue #145..."
gh issue comment 145 --body "🤖 **CODEX AI Agent Deployed**

**Agent Type:** TESTING_SPECIALIST
**Mission:** Implement comprehensive test coverage across backend & frontend
**Priority:** P1-High
**ETA:** 8-10 hours

**Immediate Actions:**
✅ Analyzing current pytest configuration  
✅ Setting up Vitest for Nuxt 3 frontend  
✅ Planning API endpoint test suite  
✅ Designing integration test strategy  

**Coverage Target:** >80% code coverage
**Agent Status:** 🟢 ACTIVE - Initializing test infrastructure"

# Deploy Production Readiness specialist for Issue #226
echo "🔥 Deploying PRODUCTION_SPECIALIST for Issue #226..."
gh issue comment 226 --body "🤖 **CODEX AI Agent Deployed**

**Agent Type:** PRODUCTION_SPECIALIST
**Mission:** Resolve 11 critical production blockers
**Priority:** P0-Critical
**ETA:** 12-16 hours

**Critical Blockers Assigned:**
🔴 Testing infrastructure (SQLite readonly issue)  
🔒 Authentication/Authorization implementation  
🔐 Secrets management overhaul  
💥 Frontend runtime errors (Dialog components)  
🐳 Production Docker optimization  

**Quick Wins Target:** 3 hours for 8 immediate fixes
**Agent Status:** 🟢 ACTIVE - Triaging critical blockers"

echo ""
echo "✅ Priority Agents Deployed Successfully!"
echo "📊 Active Agents: 9 total (6 existing + 3 priority specialists)"
echo ""
echo "🎮 Puppet Master Control: Monitor via ./scripts/agent-status.sh"