#!/bin/bash

# GitHub Wiki Publisher Script
# This script publishes the locally generated wiki content to GitHub Wiki

set -euo pipefail

REPO_OWNER="asbor"
REPO_NAME="HoppyBrew"
WIKI_DIR="wiki"

echo "🚀 Publishing Wiki to GitHub..."

# Check if gh CLI is authenticated
if ! gh auth status > /dev/null 2>&1; then
    echo "❌ Error: GitHub CLI not authenticated. Run 'gh auth login' first."
    exit 1
fi

# Change to wiki directory
cd "$WIKI_DIR"

echo "📝 Publishing wiki pages..."

# Function to publish a single wiki page
publish_page() {
    local file="$1"
    local title="${file%.md}"
    
    # Convert filename to wiki page title
    # Replace dashes and underscores with spaces, handle special cases
    case "$title" in
        "Home")
            wiki_title="Home"
            ;;
        "_Sidebar")
            wiki_title="_Sidebar"
            ;;
        *)
            wiki_title="${title//-/ }"
            wiki_title="${wiki_title//_/ }"
            ;;
    esac
    
    echo "  📄 Publishing: $file → $wiki_title"
    
    # Read the file content
    content=$(cat "$file")
    
    # Create/update the wiki page using GitHub API
    gh api --method PUT \
        "repos/$REPO_OWNER/$REPO_NAME/pages/$title" \
        --field title="$wiki_title" \
        --field content="$content" \
        --field format="markdown" > /dev/null 2>&1 || {
        echo "    ⚠️  Warning: Failed to publish $file (may need manual creation)"
        return 1
    }
    
    echo "    ✅ Published: $wiki_title"
}

# Publish all markdown files
published_count=0
failed_count=0

for file in *.md; do
    if [[ -f "$file" ]]; then
        if publish_page "$file"; then
            ((published_count++))
        else
            ((failed_count++))
        fi
    fi
done

echo ""
echo "📊 Publication Summary:"
echo "  ✅ Successfully published: $published_count pages"
echo "  ⚠️  Failed to publish: $failed_count pages"

if [[ $failed_count -gt 0 ]]; then
    echo ""
    echo "ℹ️  Note: GitHub Wiki may need to be manually initialized."
    echo "   Visit: https://github.com/$REPO_OWNER/$REPO_NAME/wiki"
    echo "   Create the first page manually, then re-run this script."
fi

echo ""
echo "🌐 Wiki URL: https://github.com/$REPO_OWNER/$REPO_NAME/wiki"
echo "✨ Publication complete!"