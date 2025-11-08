#!/bin/bash

# Script to help manually merge the remaining Dependabot PRs
# Run this script as the repository owner to merge the PRs that require workflow scope

set -e

echo "🚀 Merging Dependabot PRs that require workflow scope..."
echo "Note: This requires repository owner permissions"
echo

# List of PRs to merge
PRS=(
    "233:chore(ci)(deps): bump actions/setup-python from 5 to 6"
    "235:chore(ci)(deps): bump actions/download-artifact from 4 to 6" 
    "237:chore(ci)(deps): bump docker/build-push-action from 5 to 6"
    "247:chore(deps)(deps): bump @vueuse/core from 10.9.0 to 12.8.2"
)

echo "Checking PR status..."
for pr_info in "${PRS[@]}"; do
    pr_num="${pr_info%%:*}"
    pr_title="${pr_info#*:}"
    
    echo "📋 PR #$pr_num: $pr_title"
    
    # Check if PR exists and is open
    if gh pr view "$pr_num" --json state,mergeable >/dev/null 2>&1; then
        state=$(gh pr view "$pr_num" --json state --jq '.state')
        mergeable=$(gh pr view "$pr_num" --json mergeable --jq '.mergeable')
        
        echo "   Status: $state, Mergeable: $mergeable"
        
        if [[ "$state" == "OPEN" ]]; then
            if [[ "$mergeable" == "MERGEABLE" ]]; then
                echo "✅ PR #$pr_num is ready to merge"
                
                # Ask for confirmation
                read -p "   Merge PR #$pr_num? (y/N): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    echo "   🔄 Merging PR #$pr_num..."
                    if gh pr merge "$pr_num" --squash --delete-branch; then
                        echo "   ✅ Successfully merged PR #$pr_num"
                    else
                        echo "   ❌ Failed to merge PR #$pr_num"
                    fi
                else
                    echo "   ⏭️  Skipped PR #$pr_num"
                fi
            else
                echo "⚠️  PR #$pr_num is not mergeable (conflicts?)"
                read -p "   Try to rebase PR #$pr_num? (y/N): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    gh pr comment "$pr_num" --body "@dependabot rebase"
                    echo "   🔄 Rebase triggered for PR #$pr_num"
                fi
            fi
        else
            echo "   ℹ️  PR #$pr_num is $state"
        fi
    else
        echo "   ❌ PR #$pr_num not found or not accessible"
    fi
    echo
done

echo "🎯 Summary:"
echo "- These are all GitHub Actions dependency updates"
echo "- They improve CI/CD pipeline with latest action versions"
echo "- PR #247 (@vueuse/core) is a major version bump - test carefully"
echo "- All other PRs are minor/patch updates with good compatibility"
echo

echo "📚 Manual merge commands (if preferred):"
echo "gh pr merge 233 --squash --delete-branch  # setup-python v5→v6"
echo "gh pr merge 235 --squash --delete-branch  # download-artifact v4→v6"
echo "gh pr merge 237 --squash --delete-branch  # docker/build-push-action v5→v6"
echo "gh pr view 247  # Review @vueuse/core v10→v12 changes first"
echo

echo "✨ After merging, run: git pull --no-rebase"