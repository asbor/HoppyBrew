#!/bin/bash
# Script to close resolved and duplicate GitHub issues
# Requires: GitHub CLI (gh) installed and authenticated

set -e  # Exit on error

REPO="asbor/HoppyBrew"

echo "========================================="
echo "GitHub Issues Closure Script"
echo "Repository: $REPO"
echo "========================================="
echo ""

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) is not installed."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Error: Not authenticated with GitHub CLI."
    echo "Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is installed and authenticated"
echo ""

# Function to close an issue with a comment
close_issue() {
    local issue_number=$1
    local comment=$2
    local reason=$3
    
    echo "Closing issue #$issue_number as $reason..."
    if gh issue close "$issue_number" --repo "$REPO" --comment "$comment"; then
        echo "  ✅ Issue #$issue_number closed successfully"
    else
        echo "  ❌ Failed to close issue #$issue_number"
        return 1
    fi
}

# Confirm before proceeding
echo "This script will close the following issues:"
echo "  - Issue #139 (RESOLVED)"
echo "  - Issues #111-118 (DUPLICATES)"
echo ""
read -p "Do you want to proceed? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted by user."
    exit 0
fi

echo ""
echo "========================================="
echo "Closing Issues..."
echo "========================================="
echo ""

# Close issue #139 as resolved
echo "1. Closing issue #139 as RESOLVED..."
close_issue 139 \
"✅ **RESOLVED - Emergency Infrastructure Stabilization Complete**

All Phase 1 objectives have been successfully completed as documented in previous comments:

**Completed Work:**
- ✅ Docker infrastructure stabilized - all containers building and running
- ✅ Frontend build issues resolved - TypeScript errors fixed, dependencies cleaned
- ✅ API connectivity working - backend health endpoint responding
- ✅ Comprehensive AI agent analysis completed

**New Focused Issues Created:**
The findings from this comprehensive analysis have been broken down into specific, actionable issues:
- #144 - 🐳 DockerHub Publishing (P0-Critical)
- #145 - 🧪 Missing Test Coverage (P1-High)
- #146 - ⚛️ Frontend Architecture Issues (P1-High)
- #147 - 🗄️ Backend API Incomplete (P1-High)
- #148 - 🚀 CI/CD Pipeline Enhancements (P2-Medium)

The emergency infrastructure work is complete. The application is now operational. 
Future improvements will be tracked in the focused issues listed above.

**Closing as resolved.** ✅" \
"RESOLVED"

echo ""

# Close duplicates
echo "2. Closing duplicate issues #111-118..."
echo ""

close_issue 111 "Duplicate of #120. Closing to consolidate discussion." "DUPLICATE"
close_issue 112 "Duplicate of #121. Closing to consolidate discussion." "DUPLICATE"
close_issue 113 "Duplicate of #122. Closing to consolidate discussion." "DUPLICATE"
close_issue 114 "Duplicate of #123. Closing to consolidate discussion." "DUPLICATE"
close_issue 115 "Duplicate of #124. Closing to consolidate discussion." "DUPLICATE"
close_issue 116 "Duplicate of #125. Closing to consolidate discussion." "DUPLICATE"
close_issue 117 "Duplicate of #126. Closing to consolidate discussion." "DUPLICATE"
close_issue 118 "Duplicate of #127. Closing to consolidate discussion." "DUPLICATE"

echo ""
echo "========================================="
echo "Summary"
echo "========================================="
echo "✅ Successfully closed 9 issues:"
echo "   - 1 RESOLVED issue: #139"
echo "   - 8 DUPLICATE issues: #111-118"
echo ""
echo "Remaining open issues: $(gh issue list --repo "$REPO" --state open --json number --jq '. | length')"
echo ""
echo "🎉 Done!"
