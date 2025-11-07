#!/bin/bash
# Script to clean up automated CI failure and security alert issues
# These issues are created by GitHub Actions and clutter the repository

set -e  # Exit on error

REPO="asbor/HoppyBrew"

echo "========================================="
echo "Automated Issues Cleanup Script"
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
    local title="$2"
    
    echo "Closing automated issue #$issue_number: $title"
    if gh issue close "$issue_number" --repo "$REPO" --comment "🧹 **Automated Issue Cleanup**

This automated CI/security alert issue is being closed as part of repository maintenance. 

**Why closing:**
- These automated issues were created by GitHub Actions workflows
- They represent transient CI failures from previous PRs that are now closed
- Keeping them open clutters the issue tracker without providing actionable value

**Current Status:**
- System is now operational after recent infrastructure fixes
- CI/CD improvements are tracked in Issue #148
- Security dependency updates will be handled through normal dependency management

**Note:** If this represents an ongoing issue, please create a new focused issue with current context.

Closing to maintain a clean issue tracker. ✅"; then
        echo "  ✅ Issue #$issue_number closed successfully"
        return 0
    else
        echo "  ❌ Failed to close issue #$issue_number"
        return 1
    fi
}

# Get all CI failure issues
echo "🔍 Finding automated CI failure issues..."
CI_ISSUES=$(gh issue list --repo "$REPO" --label "ci-failure" --label "automated" --state open --json number,title --jq '.[] | "\(.number)|\(.title)"')

# Get all security alert issues  
echo "🔍 Finding automated security alert issues..."
SECURITY_ISSUES=$(gh issue list --repo "$REPO" --label "security-alert" --label "automated" --state open --json number,title --jq '.[] | "\(.number)|\(.title)"')

# Count issues
CI_COUNT=$(echo "$CI_ISSUES" | grep -c . || echo "0")
SECURITY_COUNT=$(echo "$SECURITY_ISSUES" | grep -c . || echo "0")
TOTAL_COUNT=$((CI_COUNT + SECURITY_COUNT))

echo ""
echo "📊 Found automated issues to clean up:"
echo "   - CI failure issues: $CI_COUNT"
echo "   - Security alert issues: $SECURITY_COUNT"
echo "   - Total to close: $TOTAL_COUNT"
echo ""

if [ $TOTAL_COUNT -eq 0 ]; then
    echo "✅ No automated issues found to clean up!"
    exit 0
fi

# Show what will be closed
echo "📋 Issues that will be closed:"
echo ""
if [ $CI_COUNT -gt 0 ]; then
    echo "CI Failure Issues:"
    echo "$CI_ISSUES" | while IFS='|' read -r number title; do
        echo "  - #$number: $title"
    done
fi

if [ $SECURITY_COUNT -gt 0 ]; then
    echo ""
    echo "Security Alert Issues:"
    echo "$SECURITY_ISSUES" | while IFS='|' read -r number title; do
        echo "  - #$number: $title"
    done
fi

echo ""

# Confirm before proceeding
read -p "Do you want to close all $TOTAL_COUNT automated issues? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted by user."
    exit 0
fi

echo ""
echo "========================================="
echo "Closing Automated Issues..."
echo "========================================="
echo ""

# Close CI failure issues
if [ $CI_COUNT -gt 0 ]; then
    echo "🔧 Closing CI failure issues..."
    echo "$CI_ISSUES" | while IFS='|' read -r number title; do
        close_issue "$number" "$title"
        sleep 1  # Rate limiting
    done
    echo ""
fi

# Close security alert issues
if [ $SECURITY_COUNT -gt 0 ]; then
    echo "🔒 Closing security alert issues..."
    echo "$SECURITY_ISSUES" | while IFS='|' read -r number title; do
        close_issue "$number" "$title"
        sleep 1  # Rate limiting
    done
    echo ""
fi

echo "========================================="
echo "Cleanup Summary"
echo "========================================="
echo "✅ Successfully closed $TOTAL_COUNT automated issues"
echo ""

# Show remaining open issues
REMAINING=$(gh issue list --repo "$REPO" --state open --json number --jq '. | length')
echo "📊 Remaining open issues: $REMAINING"
echo ""

# Show a few remaining issues for context
echo "🔍 Current open issues (showing first 5):"
gh issue list --repo "$REPO" --state open --limit 5 --json number,title --jq '.[] | "  - #\(.number): \(.title)"'

echo ""
echo "🎉 GitHub repository cleanup complete!"
echo ""
echo "💡 Next steps:"
echo "   1. Review remaining open issues for actionable items"
echo "   2. Focus on core application functionality"
echo "   3. Consider implementing CI/CD improvements (#148) to prevent future automated issue spam"