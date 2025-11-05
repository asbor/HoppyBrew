#!/bin/bash
# Multi-Agent Parallel Test Fix Deployment
# Spawns multiple Codex CLI agents to fix test failures simultaneously

WORKSPACE="/home/asbo/repo/HoppyBrew"
cd "$WORKSPACE" || exit 1

echo "🤖 Deploying Parallel Codex Agents for HoppyBrew Test Fixes"
echo "============================================================"

# Agent 1: Fix Pydantic Schema Defaults
echo "🟢 Agent 1: Fixing Pydantic schemas (hops, fermentables, yeasts, miscs)..."
npx @openai/codex exec \
  --context-file CODEX_AGENT_TESTING.md \
  "Fix all Pydantic schemas in services/backend/Database/Schemas/ by adding '= None' default values to all Optional fields. Start with hops.py, fermentables.py, yeasts.py, and miscs.py. Each Optional[type] field must become Optional[type] = None. Commit changes with message '🔧 Add default values to Pydantic Optional fields'." \
  > /tmp/agent1_pydantic.log 2>&1 &
AGENT1_PID=$!

# Agent 2: Fix Recipe Schema and Tests
echo "🔵 Agent 2: Fixing recipe schema and test data..."
npx @openai/codex exec \
  --context-file CODEX_AGENT_TESTING.md \
  "Fix services/backend/Database/Schemas/recipes.py by adding '= None' to all Optional fields in RecipeBase. Then review test_recipes.py BASE_RECIPE_PAYLOAD and ensure it matches schema requirements. Commit with message '🧪 Fix recipe schema defaults and test payloads'." \
  > /tmp/agent2_recipes.log 2>&1 &
AGENT2_PID=$!

# Agent 3: Fix References Endpoint Tests
echo "🟡 Agent 3: Investigating References test failures..."
npx @openai/codex exec \
  --context-file CODEX_AGENT_TESTING.md \
  "Analyze and fix test_references.py failures. Check if the favicon_url fix in api/endpoints/references.py is working correctly. Run tests locally and fix any remaining issues. Commit with message '🔧 Fix References endpoint test failures'." \
  > /tmp/agent3_references.log 2>&1 &
AGENT3_PID=$!

# Agent 4: Fix Batch Tests
echo "🟣 Agent 4: Fixing batch endpoint tests..."
npx @openai/codex exec \
  --context-file CODEX_AGENT_TESTING.md \
  "Fix test_batches.py failures. Batches depend on recipes, so ensure recipe creation works first. Update batch test fixtures to use complete recipe payloads. Commit with message '🧪 Fix batch endpoint test data and fixtures'." \
  > /tmp/agent4_batches.log 2>&1 &
AGENT4_PID=$!

echo ""
echo "📊 Agent Status:"
echo "  Agent 1 (Pydantic): PID $AGENT1_PID"
echo "  Agent 2 (Recipes):  PID $AGENT2_PID"
echo "  Agent 3 (References): PID $AGENT3_PID"
echo "  Agent 4 (Batches):  PID $AGENT4_PID"
echo ""
echo "📝 Logs available at:"
echo "  /tmp/agent1_pydantic.log"
echo "  /tmp/agent2_recipes.log"
echo "  /tmp/agent3_references.log"
echo "  /tmp/agent4_batches.log"
echo ""
echo "⏳ Waiting for agents to complete..."

# Wait for all agents to finish
wait $AGENT1_PID
AGENT1_EXIT=$?
wait $AGENT2_PID
AGENT2_EXIT=$?
wait $AGENT3_PID
AGENT3_EXIT=$?
wait $AGENT4_PID
AGENT4_EXIT=$?

echo ""
echo "✅ Agent Completion Status:"
echo "  Agent 1 (Pydantic):   Exit $AGENT1_EXIT"
echo "  Agent 2 (Recipes):    Exit $AGENT2_EXIT"
echo "  Agent 3 (References): Exit $AGENT3_EXIT"
echo "  Agent 4 (Batches):    Exit $AGENT4_EXIT"
echo ""

# Show log summaries
echo "📋 Agent Summaries:"
echo "===================="
echo "🟢 Agent 1 (Pydantic):"
tail -20 /tmp/agent1_pydantic.log
echo ""
echo "🔵 Agent 2 (Recipes):"
tail -20 /tmp/agent2_recipes.log
echo ""
echo "🟡 Agent 3 (References):"
tail -20 /tmp/agent3_references.log
echo ""
echo "🟣 Agent 4 (Batches):"
tail -20 /tmp/agent4_batches.log

echo ""
echo "🎯 Next Steps:"
echo "1. Review git status for all changes"
echo "2. Push changes: git push origin main"
echo "3. Monitor CI/CD: gh run list --limit 5"
echo ""
