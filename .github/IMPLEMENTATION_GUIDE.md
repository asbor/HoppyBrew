# Issue Tracker Implementation Guide

This guide provides step-by-step instructions for implementing the HoppyBrew issue tracker organization system.

## Prerequisites

- Repository admin/maintainer access
- GitHub CLI installed (optional, for automation)
- Node.js installed (if using automation tools)

---

## Part 1: Apply Labels (Estimated time: 15 minutes)

### Option A: Manual Creation via GitHub UI

1. **Navigate to Labels**
   - Go to: `https://github.com/asbor/HoppyBrew/labels`
   - Click "New label" button

2. **Create Each Label**
   - Use `.github/labels.yml` as reference
   - Copy name, color, and description
   - Create 40+ labels across all categories

### Option B: Automated Creation (Recommended)

#### Using GitHub CLI

```bash
# Install GitHub CLI if not already installed
# https://cli.github.com/

# Authenticate
gh auth login

# Create labels from YAML (requires jq)
cd .github
cat labels.yml | yq -r '.[] | [.name, .color, .description] | @tsv' | \
while IFS=$'\t' read -r name color description; do
  gh label create "$name" \
    --color "$color" \
    --description "$description" \
    --repo asbor/HoppyBrew || \
  gh label edit "$name" \
    --color "$color" \
    --description "$description" \
    --repo asbor/HoppyBrew
done
```

#### Using github-label-sync Tool

```bash
# Install the tool
npm install -g github-label-sync

# Create GitHub token with repo access
# https://github.com/settings/tokens

# Sync labels
github-label-sync \
  --access-token $GITHUB_TOKEN \
  --labels .github/labels.yml \
  asbor/HoppyBrew
```

#### Using Python Script

```python
#!/usr/bin/env python3
import os
import yaml
import requests

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = 'asbor'
REPO_NAME = 'HoppyBrew'

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

with open('.github/labels.yml', 'r') as f:
    labels = yaml.safe_load(f)

for label in labels:
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/labels'
    data = {
        'name': label['name'],
        'color': label['color'],
        'description': label.get('description', '')
    }
    
    # Try to create, update if exists
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 422:  # Already exists
        url = f"{url}/{label['name']}"
        response = requests.patch(url, headers=headers, json=data)
    
    print(f"{label['name']}: {response.status_code}")
```

---

## Part 2: Create Milestones (Estimated time: 10 minutes)

### Via GitHub UI

1. **Navigate to Milestones**
   - Go to: `https://github.com/asbor/HoppyBrew/milestones`
   - Click "New milestone" button

2. **Create v1.0 - Core Platform Release**
   - Title: `v1.0 - Core Platform Release`
   - Due date: `2026-03-31` (Q1 2026)
   - Description:
     ```
     Production-ready self-hosted brewing management platform
     
     Focus Areas:
     - Stable backend API with authentication
     - Core recipe management
     - Basic batch tracking
     - Inventory management fundamentals
     - Docker deployment
     - Essential documentation
     ```

3. **Create v1.1 - UX Enhancement**
   - Title: `v1.1 - UX Enhancement`
   - Due date: `2026-06-30` (Q2 2026)
   - Description: (from `.github/MILESTONES.md`)

4. **Create v1.2 - Integration Features**
   - Title: `v1.2 - Integration Features`
   - Due date: `2026-09-30` (Q3 2026)
   - Description: (from `.github/MILESTONES.md`)

5. **Create v2.0 - Advanced Features**
   - Title: `v2.0 - Advanced Features`
   - Due date: `2026-12-31` (Q4 2026)
   - Description: (from `.github/MILESTONES.md`)

6. **Create Technical Debt**
   - Title: `Technical Debt`
   - Due date: (leave blank - ongoing)
   - Description: "Ongoing code quality and maintenance"

7. **Create Documentation**
   - Title: `Documentation`
   - Due date: (leave blank - ongoing)
   - Description: "Comprehensive guides and references"

8. **Create Backlog**
   - Title: `Backlog`
   - Due date: (leave blank - future)
   - Description: "Unscheduled items for future consideration"

### Via GitHub CLI

```bash
# v1.0 - Core Platform Release
gh milestone create "v1.0 - Core Platform Release" \
  --repo asbor/HoppyBrew \
  --due-date 2026-03-31 \
  --description "Production-ready self-hosted brewing management platform"

# v1.1 - UX Enhancement
gh milestone create "v1.1 - UX Enhancement" \
  --repo asbor/HoppyBrew \
  --due-date 2026-06-30 \
  --description "Focus on user experience improvements"

# v1.2 - Integration Features
gh milestone create "v1.2 - Integration Features" \
  --repo asbor/HoppyBrew \
  --due-date 2026-09-30 \
  --description "External integrations and automation"

# v2.0 - Advanced Features
gh milestone create "v2.0 - Advanced Features" \
  --repo asbor/HoppyBrew \
  --due-date 2026-12-31 \
  --description "Advanced brewing management capabilities"

# Technical Debt (ongoing)
gh milestone create "Technical Debt" \
  --repo asbor/HoppyBrew \
  --description "Ongoing code quality and maintenance"

# Documentation (ongoing)
gh milestone create "Documentation" \
  --repo asbor/HoppyBrew \
  --description "Comprehensive guides and references"

# Backlog
gh milestone create "Backlog" \
  --repo asbor/HoppyBrew \
  --description "Unscheduled items for future consideration"
```

---

## Part 3: Create GitHub Project Board (Estimated time: 20 minutes)

### Step-by-Step UI Creation

1. **Create New Project**
   - Navigate to: `https://github.com/asbor/HoppyBrew/projects`
   - Click "New project" → "Board"
   - Name: "HoppyBrew Development Board"
   - Make public

2. **Configure Columns**
   
   Delete default columns and create:
   
   - **📥 Backlog**
   - **📋 Ready**
   - **🏗️ In Progress**
   - **👀 In Review**
   - **🧪 Testing**
   - **⏸️ Blocked/On Hold**
   - **✅ Done**
   - **🗄️ Archive**

3. **Add Custom Fields**
   
   Click "+ Add field":
   
   a. **Priority** (Single select)
      - 🔴 P0-critical
      - 🟠 P1-high
      - 🟡 P2-medium
      - 🟢 P3-low
   
   b. **Area** (Multi-select)
      - Backend, Frontend, Database, Docker, CI/CD, Testing, Security, Documentation
   
   c. **Difficulty** (Single select)
      - 🟢 Good First Issue
      - 🟡 Intermediate
      - 🔴 Advanced
   
   d. **Type** (Single select)
      - Bug 🐞, Feature 🚀, Enhancement ✨, Documentation 📚, etc.
   
   e. **Estimate** (Single select)
      - XS (1-4h), S (4-8h), M (8-16h), L (16-24h), XL (24+h)
   
   f. **Sprint** (Text)

4. **Create Views**
   
   Create these additional views:
   
   - **Sprint Board** (filter by current sprint)
   - **Backlog View** (show Backlog + Ready columns)
   - **Priority View** (filter P0 and P1)
   - **Contributor View** (filter good first issue)
   - **Team View** (table layout, group by assignee)
   - **Milestone View** (filter by milestone)

5. **Enable Automation**
   
   Configure workflows:
   
   - **Item added to project** → Set status to "Backlog"
   - **Item closed** → Set status to "Done"
   - **Pull request merged** → Set status to "Done"
   - **Pull request opened** → Set status to "In Progress"

6. **Add Existing Issues**
   
   - Click "Add items"
   - Search for existing issues
   - Add all open issues to the board

---

## Part 4: Issue Audit & Triage (Estimated time: 2-3 hours)

### Preparation

1. **Review Documentation**
   - Read `.github/TRIAGE.md`
   - Review `.github/LABELS.md`
   - Understand priority matrix

2. **Get Issue List**
   ```bash
   # Get all open issues
   gh issue list --repo asbor/HoppyBrew --limit 100 --state open
   ```

### Triage Process

For each open issue:

1. **Verify Information**
   - [ ] Title is clear
   - [ ] Description is complete
   - [ ] Steps to reproduce (if bug)

2. **Apply Type Label**
   - Choose ONE: bug, feature, enhancement, documentation, performance, security

3. **Apply Priority Label**
   - Use decision matrix from TRIAGE.md
   - Choose ONE: P0-critical, P1-high, P2-medium, P3-low

4. **Apply Area Labels**
   - Choose ALL that apply: area:backend, area:frontend, etc.

5. **Apply Difficulty (if applicable)**
   - For issues suitable for contributors
   - Choose ONE: good first issue, intermediate, advanced

6. **Assign Milestone**
   - Based on priority and roadmap
   - Use MILESTONES.md as guide

7. **Check for Duplicates**
   - Search for similar issues
   - Link or close duplicates

8. **Update Status**
   - Add `status:` label if needed
   - Move on project board

### Triage Script Template

```bash
#!/bin/bash
# Quick triage script

ISSUE_NUMBER=$1
REPO="asbor/HoppyBrew"

echo "Triaging issue #$ISSUE_NUMBER"

# Add type label
gh issue edit $ISSUE_NUMBER --repo $REPO --add-label "bug"

# Add priority label
gh issue edit $ISSUE_NUMBER --repo $REPO --add-label "P1-high"

# Add area label
gh issue edit $ISSUE_NUMBER --repo $REPO --add-label "area: backend"

# Assign milestone
gh issue edit $ISSUE_NUMBER --repo $REPO --milestone "v1.0 - Core Platform Release"

echo "Triage complete for #$ISSUE_NUMBER"
```

---

## Part 5: Close Outdated/Duplicate Issues (Estimated time: 1 hour)

### Identify Candidates

1. **Stale Issues** (no activity >6 months)
   ```bash
   gh issue list --repo asbor/HoppyBrew \
     --state open \
     --search "updated:<2024-05-11"
   ```

2. **Duplicate Issues**
   - Search for similar titles
   - Check linked issues

3. **Resolved Issues**
   - Check if already fixed in code
   - Verify against current main branch

### Closing Process

For each issue to close:

1. **Add Comment**
   ```
   Closing as [duplicate/stale/resolved]:
   - [Explanation]
   - [Link to duplicate or fix PR if applicable]
   - [Instructions if action needed]
   
   Feel free to reopen if this is still relevant.
   ```

2. **Apply Label**
   - `status: duplicate` or
   - `status: wontfix` or
   - `status: stale`

3. **Close Issue**
   ```bash
   gh issue close $ISSUE_NUMBER --repo asbor/HoppyBrew \
     --comment "Closing as resolved in PR #XXX"
   ```

---

## Part 6: Create Automation (Optional, Estimated time: 1 hour)

### Stale Issue Bot

Create `.github/workflows/stale.yml`:

```yaml
name: 'Close stale issues'
on:
  schedule:
    - cron: '0 0 * * *'  # Daily

permissions:
  issues: write
  pull-requests: write

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v8
        with:
          stale-issue-message: 'This issue has been inactive for 90 days. Please comment if still relevant.'
          close-issue-message: 'Closing due to inactivity. Feel free to reopen if needed.'
          days-before-stale: 90
          days-before-close: 30
          stale-issue-label: 'status: stale'
          exempt-issue-labels: 'status: blocked,status: on-hold,P0-critical,P1-high'
```

### Auto-Label PR Based on Files

Create `.github/workflows/auto-label.yml`:

```yaml
name: Auto Label PRs
on:
  pull_request:
    types: [opened, edited, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v4
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

Create `.github/labeler.yml`:

```yaml
'area: backend':
  - 'services/backend/**/*'
  - 'alembic/**/*'

'area: frontend':
  - 'services/nuxt3-shadcn/**/*'

'area: docker':
  - '**/Dockerfile'
  - 'docker-compose*.yml'

'area: ci-cd':
  - '.github/workflows/**/*'

'area: docs':
  - '**.md'
  - 'documents/**/*'

'area: testing':
  - '**/*test*.py'
  - '**/*test*.ts'
  - 'tests/**/*'
```

---

## Part 7: Verification (Estimated time: 30 minutes)

### Checklist

- [ ] All labels created and visible
- [ ] All milestones created
- [ ] Project board configured with columns
- [ ] Project board has custom fields
- [ ] Automation rules enabled
- [ ] All open issues labeled
- [ ] All open issues prioritized (P0-P3)
- [ ] 80%+ issues assigned to milestones
- [ ] Duplicate issues closed
- [ ] Stale issues addressed
- [ ] Documentation tested (create test issue)

### Testing

1. **Create Test Issue**
   - Use bug report template
   - Verify template works
   - Apply labels
   - Assign milestone
   - Add to project board

2. **Create Test PR**
   - Use PR template
   - Verify template works
   - Check auto-labeling
   - Verify board automation

3. **Verify Views**
   - Check all project board views
   - Verify filters work
   - Test search functionality

---

## Part 8: Communication (Estimated time: 30 minutes)

### Announce Changes

1. **Create Discussion Post**
   ```markdown
   # 🎉 New Issue Tracker Organization System
   
   We've implemented a comprehensive issue management system!
   
   ## What's New:
   - Enhanced issue templates
   - Comprehensive label system
   - Milestone-based planning
   - Project board for visual tracking
   - Triage guidelines
   
   ## Resources:
   - [Label Guide](.github/LABELS.md)
   - [Triage Process](.github/TRIAGE.md)
   - [Milestones](.github/MILESTONES.md)
   - [Project Board](.github/PROJECT_BOARD.md)
   
   ## For Contributors:
   Look for `good first issue` labels to get started!
   
   Questions? Reply to this discussion!
   ```

2. **Update README**
   - Link to project board
   - Link to contributing guide
   - Mention new templates

3. **Pin Important Issues**
   - Pin project board link
   - Pin contributing guidelines

---

## Maintenance Schedule

### Daily
- [ ] Check P0-critical issues
- [ ] Review new issues for triage

### Weekly
- [ ] Triage session (review all new issues)
- [ ] Backlog grooming
- [ ] Update project board

### Monthly
- [ ] Milestone review
- [ ] Label consistency check
- [ ] Close stale issues
- [ ] Update metrics

### Quarterly
- [ ] Process review
- [ ] Label system review
- [ ] Automation improvements

---

## Success Metrics

Track these over time:

- **Issue Health**
  - 100% labeled ✓
  - >90% prioritized ✓
  - >80% in milestones ✓
  - <30 total open ✓

- **Response Times**
  - First response <48h ✓
  - P0 resolution <24h ✓
  - P1 resolution <1 week ✓

- **Quality**
  - <5% duplicate rate ✓
  - <20% stale rate ✓
  - >80% contributor satisfaction ✓

---

## Troubleshooting

### Labels Not Syncing
- Check token permissions
- Verify YAML syntax
- Try manual creation

### Project Board Automation Not Working
- Check workflow permissions
- Verify automation rules
- Check event triggers

### Milestones Not Showing
- Verify milestone created
- Check date format
- Refresh page

---

## Resources

- [GitHub Labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
- [GitHub Milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones)
- [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Need Help?**
- Open a discussion
- Contact maintainers
- Check documentation

**Last Updated**: 2025-11-11
