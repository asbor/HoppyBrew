# Manual PR Resolution Guide

Since OAuth token lacks workflow scope, use GitHub web interface

echo "🎯 PR Resolution - Manual Steps"
echo "================================"
echo
echo "📋 Open PRs requiring manual merge via GitHub web interface:"
echo

echo "1. 🔧 Setup Python v5→v6 (Safe to merge)"
echo "   URL: https://github.com/asbor/HoppyBrew/pull/233"
echo "   Action: Click 'Merge pull request' → 'Squash and merge'"
echo

echo "2. 📦 Download Artifact v4→v6 (Safe to merge)"  
echo "   URL: https://github.com/asbor/HoppyBrew/pull/235"
echo "   Action: Click 'Merge pull request' → 'Squash and merge'"
echo

echo "3. 🐋 Docker Build-Push v5→v6 (Safe to merge)"
echo "   URL: https://github.com/asbor/HoppyBrew/pull/237" 
echo "   Action: Click 'Merge pull request' → 'Squash and merge'"
echo

echo "4. ⚠️  Vue Use Core v10→v12 (REVIEW FIRST)"
echo "   URL: https://github.com/asbor/HoppyBrew/pull/247"
echo "   Action: Review breaking changes, then merge if safe"
echo

echo "🔍 Alternative: Re-authenticate with workflow scope"
echo "   Command: gh auth login --scopes 'repo,workflow' --web"
echo

echo "📊 Current token scopes: repo (missing: workflow)"
echo "✅ Infrastructure: Docker fixes working perfectly"
echo "🎯 Next: Wiki generation agent ready to launch"