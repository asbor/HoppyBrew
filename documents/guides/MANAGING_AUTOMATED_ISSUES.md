# Managing Automated Issues

## Overview

This repository uses automated workflows to create GitHub issues for:
- Security scan findings (daily + on push to main)
- CI/CD validation failures (on pull requests)

## Issue Types

### Security Scan Issues
**Label:** `security-alert`, `automated`  
**Title:** "Security scan alerts - Dependencies"  
**When created:** When Python or Node dependency vulnerabilities are detected

These issues are now **automatically updated** instead of creating duplicates. The workflow:
1. Checks for an existing open issue with the same title
2. If found: Updates the existing issue body and adds a comment with the new scan results
3. If not found: Creates a new issue

### CI Failure Issues
**Label:** `ci-failure`, `automated`  
**Title:** "CI failure on PR #XXX"  
**When created:** When PR validation fails (backend lint, backend tests, or frontend build)

These issues are now **automatically updated** per PR. The workflow:
1. Checks for an existing open issue for the same PR number
2. If found: Updates the existing issue body and adds a comment with new results
3. If not found: Creates a new issue

## Cleanup Process

### For Security Issues
If you have **duplicate security alert issues** (multiple issues with titles like "Security scan alerts for 19190598088"):
1. Keep the most recent one or create a consolidated issue titled "Security scan alerts - Dependencies"
2. Close all others as duplicates with a comment: "Consolidated into #XXX"
3. The updated workflow will now update the kept issue instead of creating new ones

### For CI Failure Issues  
If you have **duplicate CI failure issues** for the same PR:
1. Keep the most recent one
2. Close others as duplicates
3. When the PR CI passes or is closed, close the issue

## Prevention

The workflows have been updated (as of this commit) to:
- Use static, descriptive titles instead of run IDs
- Update existing issues instead of creating new ones
- Add timestamped comments for each run
- Track the run ID in the issue body/comments for debugging

## Manual Cleanup Script

If you need to clean up many duplicate issues at once, you can use the GitHub CLI:

```bash
# List all open security-alert issues
gh issue list --label security-alert --state open --json number,title

# Close duplicate issues (replace XXX with issue numbers)
for issue in 272 273 274 275; do
  gh issue close $issue --comment "Duplicate of #276 - consolidated security tracking issue"
done

# List all open ci-failure issues
gh issue list --label ci-failure --state open --json number,title

# Close stale CI issues for closed/merged PRs
# Check if PR is closed/merged before closing the issue
```

## Best Practices

1. **Don't close security issues until vulnerabilities are fixed** - Even if they're duplicates, keep one open to track resolution
2. **Close CI issues when PR is closed/merged** - These are transient and should be cleaned up
3. **Review automated issues regularly** - Check weekly to ensure the automation is working correctly
4. **Fix root causes** - Don't just close issues; update dependencies or fix code to resolve them

## Disabling Automated Issue Creation

If you want to disable automated issue creation temporarily:

1. **For security scans:** Comment out the "MCP: Auto-issue for vulnerabilities" step in `.github/workflows/security-scan.yml`
2. **For CI failures:** Comment out the "MCP: Auto-create CI failure issue" step in `.github/workflows/pr-validation.yml`

The workflows will still run and report results in the Actions tab, but won't create issues.
