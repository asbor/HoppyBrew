#!/usr/bin/env python3
"""
Script to identify and help clean up duplicate automated issues in the HoppyBrew repository.

This script finds:
1. Duplicate security scan issues (multiple issues with similar titles)
2. Duplicate CI failure issues for the same PR
3. Stale CI issues for closed/merged PRs

Usage:
    python tools/cleanup_duplicate_issues.py [--close-duplicates] [--dry-run]

Requirements:
    pip install PyGithub
    
    Set GITHUB_TOKEN environment variable with a token that has 'repo' access
"""

import os
import sys
import argparse
from collections import defaultdict
from datetime import datetime, timedelta

try:
    from github import Github
except ImportError:
    print("Error: PyGithub is not installed")
    print("Install it with: pip install PyGithub")
    sys.exit(1)


def get_github_client():
    """Get authenticated GitHub client."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Create a token at: https://github.com/settings/tokens")
        print("Required scope: repo")
        sys.exit(1)
    return Github(token)


def find_duplicate_security_issues(repo):
    """Find duplicate security scan issues."""
    print("\n=== Security Scan Issues ===\n")
    
    # Get all open issues with security-alert label
    security_issues = repo.get_issues(state='open', labels=['security-alert'])
    
    # Group by title pattern
    by_pattern = defaultdict(list)
    for issue in security_issues:
        if 'Security scan alerts' in issue.title:
            # Extract just the pattern, not the run ID
            if 'for' in issue.title:
                pattern = 'Security scan alerts for [RUN_ID]'
            else:
                pattern = issue.title
            by_pattern[pattern].append(issue)
    
    total_duplicates = 0
    for pattern, issues in by_pattern.items():
        if len(issues) > 1:
            print(f"Found {len(issues)} issues with pattern: {pattern}")
            print(f"  Keep newest: #{issues[0].number} - {issues[0].title}")
            print(f"  Duplicates to close:")
            for issue in issues[1:]:
                print(f"    - #{issue.number}: {issue.title} (created {issue.created_at})")
                total_duplicates += 1
            print()
    
    if total_duplicates == 0:
        print("No duplicate security issues found! ✅")
    
    return by_pattern


def find_duplicate_ci_issues(repo):
    """Find duplicate CI failure issues."""
    print("\n=== CI Failure Issues ===\n")
    
    # Get all open issues with ci-failure label
    ci_issues = repo.get_issues(state='open', labels=['ci-failure'])
    
    # Group by PR number
    by_pr = defaultdict(list)
    for issue in ci_issues:
        if 'CI failure on PR' in issue.title:
            # Extract PR number from title
            pr_number = issue.title.split('#')[-1]
            by_pr[pr_number].append(issue)
    
    total_duplicates = 0
    stale_issues = []
    
    for pr_number, issues in by_pr.items():
        if len(issues) > 1:
            print(f"Found {len(issues)} issues for PR #{pr_number}")
            print(f"  Keep newest: #{issues[0].number}")
            print(f"  Duplicates to close:")
            for issue in issues[1:]:
                print(f"    - #{issue.number}: {issue.title} (created {issue.created_at})")
                total_duplicates += 1
            print()
        
        # Check if PR is closed
        try:
            pr = repo.get_pull(int(pr_number))
            if pr.state == 'closed':
                stale_issues.extend(issues)
                print(f"PR #{pr_number} is {pr.state} - issues can be closed as stale")
        except Exception as e:
            print(f"Could not check PR #{pr_number}: {e}")
    
    if total_duplicates == 0:
        print("No duplicate CI issues found! ✅")
    
    if stale_issues:
        print(f"\n{len(stale_issues)} stale CI issues found (PR is closed/merged)")
    
    return by_pr, stale_issues


def close_duplicate_issues(repo, security_groups, ci_groups, stale_ci_issues, dry_run=True):
    """Close duplicate issues, keeping the most recent one."""
    if dry_run:
        print("\n=== DRY RUN MODE - No changes will be made ===\n")
    else:
        print("\n=== CLOSING DUPLICATE ISSUES ===\n")
    
    closed_count = 0
    
    # Close duplicate security issues
    for pattern, issues in security_groups.items():
        if len(issues) > 1:
            keeper = issues[0]
            for issue in issues[1:]:
                if not dry_run:
                    issue.create_comment(
                        f"Closing as duplicate of #{keeper.number}. "
                        f"Security scan tracking consolidated to that issue."
                    )
                    issue.edit(state='closed')
                print(f"{'[DRY RUN] Would close' if dry_run else 'Closed'} #{issue.number}")
                closed_count += 1
    
    # Close duplicate CI issues
    for pr_number, issues in ci_groups.items():
        if len(issues) > 1:
            keeper = issues[0]
            for issue in issues[1:]:
                if not dry_run:
                    issue.create_comment(
                        f"Closing as duplicate of #{keeper.number}. "
                        f"CI failure tracking consolidated to that issue."
                    )
                    issue.edit(state='closed')
                print(f"{'[DRY RUN] Would close' if dry_run else 'Closed'} #{issue.number}")
                closed_count += 1
    
    # Close stale CI issues
    for issue in stale_ci_issues:
        if not dry_run:
            issue.create_comment(
                "Closing as the associated PR is no longer open. "
                "CI issues are specific to PR validation runs."
            )
            issue.edit(state='closed')
        print(f"{'[DRY RUN] Would close' if dry_run else 'Closed'} stale issue #{issue.number}")
        closed_count += 1
    
    print(f"\nTotal issues {'that would be' if dry_run else ''} closed: {closed_count}")
    return closed_count


def main():
    parser = argparse.ArgumentParser(
        description='Find and optionally close duplicate automated issues'
    )
    parser.add_argument(
        '--close-duplicates',
        action='store_true',
        help='Actually close duplicate issues (default: just list them)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be closed without actually closing'
    )
    parser.add_argument(
        '--repo',
        default='asbor/HoppyBrew',
        help='GitHub repository (default: asbor/HoppyBrew)'
    )
    
    args = parser.parse_args()
    
    print(f"Analyzing repository: {args.repo}")
    
    gh = get_github_client()
    repo = gh.get_repo(args.repo)
    
    # Find duplicates
    security_groups = find_duplicate_security_issues(repo)
    ci_groups, stale_ci = find_duplicate_ci_issues(repo)
    
    # Close if requested
    if args.close_duplicates:
        close_duplicate_issues(
            repo,
            security_groups,
            ci_groups,
            stale_ci,
            dry_run=args.dry_run
        )
    else:
        print("\n💡 To close these duplicates, run with --close-duplicates")
        print("💡 To see what would be closed without making changes, add --dry-run")


if __name__ == '__main__':
    main()
