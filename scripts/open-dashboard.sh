#!/bin/bash

# Open AI Agent Dashboard
# Quick launcher for the HoppyBrew AI Agent monitoring dashboard

DASHBOARD_PATH="$(dirname "$0")/../.agents/dashboard.html"

echo "🎭 Opening HoppyBrew AI Agent Dashboard..."
echo "📊 Dashboard: file://$(realpath "$DASHBOARD_PATH")"
echo ""

# Try to open in default browser
if command -v xdg-open &> /dev/null; then
    xdg-open "$DASHBOARD_PATH"
elif command -v open &> /dev/null; then
    open "$DASHBOARD_PATH"
elif command -v start &> /dev/null; then
    start "$DASHBOARD_PATH"
else
    echo "⚠️  Could not detect browser opener command"
    echo "📍 Please open manually: file://$(realpath "$DASHBOARD_PATH")"
fi

echo ""
echo "✨ Dashboard features:"
echo "   • Real-time agent status monitoring"
echo "   • Visual progress tracking"
echo "   • Filter by status (All/Running/Active/Standby)"
echo "   • Auto-refresh every 30 seconds"
echo "   • Phase-based organization"
echo ""
echo "🔄 Other monitoring commands:"
echo "   ./scripts/agent-status.sh       - CLI status check"
echo "   tail -f .agents/logs/*.log      - View agent logs"
echo ""
