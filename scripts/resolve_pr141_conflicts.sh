#!/bin/bash
# Script to resolve conflicts in PR #141 (copilot/vscode1762383680631)
# This script creates a clean version of the branch based on main with only the valuable fixes

set -e  # Exit on error

echo "=== Branch Conflict Resolution Script ==="
echo ""

# Get current branch to return to later
ORIGINAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $ORIGINAL_BRANCH"

# Ensure we're in a git repository
if [ ! -d ".git" ]; then
    echo "ERROR: Not in a git repository"
    exit 1
fi

# Fetch latest changes
echo ""
echo "Fetching latest changes from origin..."
git fetch origin

# Create a new branch from latest main
BRANCH_NAME="copilot/vscode1762383680631"
TEMP_BRANCH="resolved-${BRANCH_NAME}"

echo ""
echo "Creating clean branch from origin/main..."
git checkout origin/main -b "$TEMP_BRANCH"

echo ""
echo "Applying fixes..."

# Fix 1: Remove package-lock.json (package manager conflict)
if [ -f "services/nuxt3-shadcn/package-lock.json" ]; then
    echo "  - Removing package-lock.json to fix npm/yarn conflict..."
    git rm services/nuxt3-shadcn/package-lock.json
else
    echo "  - package-lock.json already removed"
fi

# Fix 2: Remove deprecated docker-compose version
if grep -q '^version:' docker-compose.yml 2>/dev/null; then
    echo "  - Removing deprecated 'version' from docker-compose.yml..."
    sed -i '/^version:/d' docker-compose.yml
    # Remove any blank line at the start of the file
    sed -i '1{/^$/d}' docker-compose.yml
    git add docker-compose.yml
else
    echo "  - docker-compose version already removed"
fi

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo ""
    echo "No changes to commit - fixes already applied in main"
    echo "Cleaning up..."
    git checkout "$ORIGINAL_BRANCH"
    git branch -D "$TEMP_BRANCH"
    exit 0
fi

# Commit the changes
echo ""
echo "Committing fixes..."
git commit -m "Fix package manager conflict and remove deprecated docker-compose version" \
          -m "- Remove package-lock.json to resolve npm/yarn conflict (project uses yarn)" \
          -m "- Remove deprecated 'version' declaration from docker-compose.yml" \
          -m "" \
          -m "Resolves conflicts in PR #141" \
          -m "Related to #139"

echo ""
echo "=== Resolution Complete ==="
echo ""
echo "The resolved branch '$TEMP_BRANCH' has been created with the following changes:"
git --no-pager log --oneline -1
echo ""
echo "To apply this resolution:"
echo ""
echo "Option 1: Force push to replace the conflicting branch (requires write access)"
echo "  git push --force origin $TEMP_BRANCH:$BRANCH_NAME"
echo ""
echo "Option 2: Create a new PR from this branch"
echo "  git push origin $TEMP_BRANCH"
echo ""
echo "Current branch: $TEMP_BRANCH"
echo "Original branch: $ORIGINAL_BRANCH"
echo ""
echo "To return to your original branch:"
echo "  git checkout $ORIGINAL_BRANCH"
echo ""
