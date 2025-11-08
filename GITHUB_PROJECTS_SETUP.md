# GitHub Projects Setup Guide

**Purpose**: Instructions for setting up GitHub Projects for HoppyBrew multi-agent coordination  
**Last Updated**: November 8, 2025  
**Audience**: Project maintainers, coordinators

---

## 🎯 Overview

This guide provides step-by-step instructions to set up the 5 GitHub Project boards defined in `GITHUB_PROJECTS_ORGANIZATION.md` for efficient multi-agent task delegation.

---

## 📋 Project Board Definitions

### Project 1: 🔥 Critical Operations
- **Purpose**: P0-P1 priority issues requiring immediate attention
- **Columns**: Backlog, In Progress, Review, Done
- **Labels**: `priority:critical`, `priority:high`, `status:*`

### Project 2: ⚡ Feature Development
- **Purpose**: P2 priority core feature implementation
- **Columns**: Backlog, Design, In Progress, Review, Done
- **Labels**: `priority:medium`, `type:feature`, `agent-role:*`

### Project 3: 🔧 Infrastructure & DevOps
- **Purpose**: P2 priority infrastructure and DevOps improvements
- **Columns**: Backlog, Planning, In Progress, Testing, Done
- **Labels**: `priority:medium`, `type:infrastructure`, `agent-role:devops`

### Project 4: 📚 Documentation & Testing
- **Purpose**: P3 priority documentation and test coverage
- **Columns**: Backlog, In Progress, Review, Done
- **Labels**: `priority:low`, `type:documentation`, `type:testing`

### Project 5: 🌟 Enhancements & Future Features
- **Purpose**: P3-P4 priority nice-to-have features
- **Columns**: Backlog, Proposed, In Progress, Review, Done
- **Labels**: `priority:low`, `priority:future`, `type:enhancement`

---

## 🚀 Setup Instructions

### Option A: GitHub Web Interface

#### Step 1: Create Projects

1. Go to https://github.com/asbor/HoppyBrew/projects
2. Click "New project"
3. Select "Board" view
4. Name: "🔥 Critical Operations"
5. Description: "P0-P1 priority issues requiring immediate attention"
6. Click "Create"
7. Repeat for all 5 projects

#### Step 2: Configure Columns

For each project, set up columns:

**Project 1 (Critical Operations):**
- Backlog
- In Progress
- Review
- Done

**Project 2 (Feature Development):**
- Backlog
- Design
- In Progress
- Review
- Done

**Project 3 (Infrastructure):**
- Backlog
- Planning
- In Progress
- Testing
- Done

**Project 4 (Documentation & Testing):**
- Backlog
- In Progress
- Review
- Done

**Project 5 (Enhancements):**
- Backlog
- Proposed
- In Progress
- Review
- Done

#### Step 3: Configure Automation (per project)

Settings → Manage access → Automation:

**All projects:**
- ✅ When issue/PR is opened → Add to "Backlog"
- ✅ When issue/PR is closed → Move to "Done"
- ✅ When PR is merged → Move to "Done"

**Additional for each:**
- When label "status:in-progress" → Move to "In Progress"
- When label "status:review" → Move to "Review"
- When PR review requested → Move to "Review"

#### Step 4: Set up Labels

Repository → Issues → Labels → New label

**Priority Labels:**
```
priority:critical    #d73a4a  (red)
priority:high        #ff9800  (orange)
priority:medium      #fbca04  (yellow)
priority:low         #0e8a16  (green)
priority:future      #1d76db  (blue)
```

**Status Labels:**
```
status:backlog       #d4c5f9  (light purple)
status:in-progress   #0075ca  (blue)
status:review        #fbca04  (yellow)
status:blocked       #d73a4a  (red)
status:done          #0e8a16  (green)
```

**Type Labels:**
```
type:bug             #d73a4a  (red)
type:feature         #0075ca  (blue)
type:enhancement     #a2eeef  (light blue)
type:documentation   #0075ca  (blue)
type:testing         #d4c5f9  (purple)
type:infrastructure  #fef2c0  (light yellow)
type:security        #d73a4a  (red)
```

**Agent Role Labels:**
```
agent-role:backend       #d4c5f9  (purple)
agent-role:frontend      #c5def5  (light blue)
agent-role:devops        #fef2c0  (yellow)
agent-role:qa            #d4c5f9  (purple)
agent-role:data          #bfd4f2  (blue)
agent-role:docs          #c5def5  (light blue)
agent-role:security      #d73a4a  (red)
agent-role:any           #d1f0fd  (very light blue)
```

**Other Labels:**
```
agent-task           #7057ff  (purple)
good-first-issue     #7057ff  (purple)
help-wanted          #008672  (teal)
dependencies         #0366d6  (dark blue)
```

### Option B: GitHub CLI (Automated)

#### Prerequisites
```bash
gh auth login
cd /home/runner/work/HoppyBrew/HoppyBrew
```

#### Create Projects Script

Create `scripts/setup-projects.sh`:

```bash
#!/bin/bash

echo "🚀 Setting up GitHub Projects for HoppyBrew"
echo "==========================================="
echo ""

OWNER="asbor"
REPO="HoppyBrew"

# Function to create a project
create_project() {
    local title="$1"
    local description="$2"
    
    echo "📋 Creating project: $title"
    
    # Note: GitHub Projects V2 API requires GraphQL
    # This is a simplified version - may need adjustment
    gh api graphql -f query='
      mutation($ownerId: ID!, $title: String!) {
        createProjectV2(input: {
          ownerId: $ownerId,
          title: $title
        }) {
          projectV2 {
            id
            number
            title
          }
        }
      }' -f ownerId="$(gh api graphql -f query='query{viewer{id}}' --jq '.data.viewer.id')" \
         -f title="$title"
}

# Create projects
echo "Creating Project 1: Critical Operations..."
create_project "🔥 Critical Operations" "P0-P1 priority issues requiring immediate attention"

echo "Creating Project 2: Feature Development..."
create_project "⚡ Feature Development" "P2 priority core feature implementation"

echo "Creating Project 3: Infrastructure & DevOps..."
create_project "🔧 Infrastructure & DevOps" "P2 priority infrastructure improvements"

echo "Creating Project 4: Documentation & Testing..."
create_project "📚 Documentation & Testing" "P3 priority documentation and testing"

echo "Creating Project 5: Enhancements..."
create_project "🌟 Enhancements & Future Features" "P3-P4 priority nice-to-have features"

echo ""
echo "✅ Projects created! Configure columns and automation in GitHub web UI."
echo "📖 See GITHUB_PROJECTS_SETUP.md for detailed instructions."
```

#### Create Labels Script

Create `scripts/setup-labels.sh`:

```bash
#!/bin/bash

echo "🏷️  Setting up GitHub Labels for HoppyBrew"
echo "=========================================="
echo ""

OWNER="asbor"
REPO="HoppyBrew"

# Function to create or update label
create_label() {
    local name="$1"
    local color="$2"
    local description="$3"
    
    echo "Creating label: $name"
    gh label create "$name" --color "$color" --description "$description" --force
}

echo "Creating Priority Labels..."
create_label "priority:critical" "d73a4a" "Critical priority - immediate attention required"
create_label "priority:high" "ff9800" "High priority - needed soon"
create_label "priority:medium" "fbca04" "Medium priority - normal queue"
create_label "priority:low" "0e8a16" "Low priority - nice to have"
create_label "priority:future" "1d76db" "Future priority - long-term"

echo ""
echo "Creating Status Labels..."
create_label "status:backlog" "d4c5f9" "In backlog, not yet started"
create_label "status:in-progress" "0075ca" "Currently being worked on"
create_label "status:review" "fbca04" "In review, awaiting feedback"
create_label "status:blocked" "d73a4a" "Blocked by dependency or issue"
create_label "status:done" "0e8a16" "Completed"

echo ""
echo "Creating Type Labels..."
create_label "type:bug" "d73a4a" "Something isn't working"
create_label "type:feature" "0075ca" "New feature implementation"
create_label "type:enhancement" "a2eeef" "Enhancement to existing feature"
create_label "type:documentation" "0075ca" "Documentation changes"
create_label "type:testing" "d4c5f9" "Test-related changes"
create_label "type:infrastructure" "fef2c0" "Infrastructure or DevOps changes"
create_label "type:security" "d73a4a" "Security-related changes"

echo ""
echo "Creating Agent Role Labels..."
create_label "agent-role:backend" "d4c5f9" "Backend/API development"
create_label "agent-role:frontend" "c5def5" "Frontend/UI development"
create_label "agent-role:devops" "fef2c0" "DevOps/Infrastructure"
create_label "agent-role:qa" "d4c5f9" "Quality Assurance/Testing"
create_label "agent-role:data" "bfd4f2" "Data processing/ETL"
create_label "agent-role:docs" "c5def5" "Documentation"
create_label "agent-role:security" "d73a4a" "Security"
create_label "agent-role:any" "d1f0fd" "Any role can work on this"

echo ""
echo "Creating Other Labels..."
create_label "agent-task" "7057ff" "Task for AI agent"
create_label "good-first-issue" "7057ff" "Good for newcomers"
create_label "help-wanted" "008672" "Extra attention needed"
create_label "dependencies" "0366d6" "Pull requests that update dependencies"

echo ""
echo "✅ All labels created!"
```

#### Run Setup Scripts

```bash
# Make scripts executable
chmod +x scripts/setup-projects.sh scripts/setup-labels.sh

# Run label setup (this will work)
./scripts/setup-labels.sh

# For projects, use GitHub web UI (Projects V2 API is complex)
# Follow "Option A" instructions above for project creation
```

---

## 📊 Populating Projects with Tasks

### From TODO.md

Use the migration script to convert TODO.md items to GitHub issues:

Create `scripts/migrate-todo-to-issues.py`:

```python
#!/usr/bin/env python3
"""
Convert TODO.md items to GitHub issues with proper labels and project assignment.
"""

import re
import subprocess
import sys

TODO_FILE = "TODO.md"

# Map TODO sections to project numbers and priorities
SECTION_MAPPING = {
    "Critical Production Blockers": {
        "project": 1,
        "priority": "priority:critical",
        "type": "type:bug"
    },
    "Missing FK Indexes": {
        "project": 1,
        "priority": "priority:high",
        "type": "type:infrastructure"
    },
    "Backend APIs": {
        "project": 2,
        "priority": "priority:medium",
        "type": "type:feature",
        "role": "agent-role:backend"
    },
    "Frontend - Recipe Detail Page": {
        "project": 2,
        "priority": "priority:medium",
        "type": "type:feature",
        "role": "agent-role:frontend"
    },
    "Frontend - Inventory Pages": {
        "project": 2,
        "priority": "priority:medium",
        "type": "type:feature",
        "role": "agent-role:frontend"
    },
    "Frontend - Profile Pages": {
        "project": 2,
        "priority": "priority:medium",
        "type": "type:feature",
        "role": "agent-role:frontend"
    },
    "DevOps": {
        "project": 3,
        "priority": "priority:medium",
        "type": "type:infrastructure",
        "role": "agent-role:devops"
    },
    "Testing": {
        "project": 4,
        "priority": "priority:low",
        "type": "type:testing",
        "role": "agent-role:qa"
    },
    "Documentation": {
        "project": 4,
        "priority": "priority:low",
        "type": "type:documentation",
        "role": "agent-role:docs"
    },
    "Enhancements": {
        "project": 5,
        "priority": "priority:low",
        "type": "type:enhancement"
    }
}

def create_issue(title, body, labels, project):
    """Create a GitHub issue using gh CLI."""
    cmd = ["gh", "issue", "create", 
           "--title", title,
           "--body", body]
    
    for label in labels:
        cmd.extend(["--label", label])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issue_url = result.stdout.strip()
        print(f"✅ Created: {issue_url}")
        
        # Add to project (requires project number and issue URL)
        # Note: This requires gh project extension or GraphQL
        # For now, just print instruction
        print(f"   👉 Add to Project {project}: {issue_url}")
        
        return issue_url
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create issue: {e.stderr}")
        return None

def parse_todo_items(todo_file):
    """Parse TODO.md and extract uncompleted tasks."""
    with open(todo_file, 'r') as f:
        content = f.read()
    
    # Find all uncompleted tasks: - [ ] Task description
    pattern = r'^- \[ \] (.+)$'
    tasks = re.findall(pattern, content, re.MULTILINE)
    
    return tasks

def main():
    print("📋 Migrating TODO.md to GitHub Issues")
    print("=" * 50)
    print()
    
    tasks = parse_todo_items(TODO_FILE)
    print(f"Found {len(tasks)} uncompleted tasks in TODO.md")
    print()
    
    # For this example, just print what would be created
    print("Would create the following issues:")
    for i, task in enumerate(tasks[:10], 1):  # Limit to first 10 for example
        print(f"{i}. {task[:80]}...")
    
    print()
    print("⚠️  Note: Manual review recommended before creating all issues")
    print("💡 Suggestion: Review TODO.md sections and create issues incrementally")

if __name__ == "__main__":
    main()
```

**Manual Migration Recommended:**

Instead of bulk automation, create issues gradually:

1. **Week 1**: Migrate P0-P1 critical tasks to Project 1
2. **Week 2**: Migrate P2 feature tasks to Projects 2-3
3. **Week 3**: Migrate P3 documentation/testing to Project 4
4. **Ongoing**: Add P3-P4 enhancements to Project 5 as needed

### From ROADMAP.md

Use milestones for sprint planning:

1. Create GitHub Milestones for each sprint/phase
2. Link issues to appropriate milestone
3. Track milestone progress in Projects

```bash
# Create milestone
gh api repos/asbor/HoppyBrew/milestones -f title="Sprint 1: Equipment & Inventory" \
  -f description="Weeks 1-4" -f due_on="2025-12-06T00:00:00Z"

# Add issue to milestone
gh issue edit [ISSUE_NUMBER] --milestone "Sprint 1: Equipment & Inventory"
```

---

## 🔄 Project Board Workflows

### Workflow 1: New Issue Created

1. **Automatic**: Issue added to appropriate project's "Backlog"
2. **Manual**: Add labels (priority, type, agent-role)
3. **Automatic**: Appears in project board Backlog column

### Workflow 2: Agent Claims Task

1. Agent assigns issue to themselves
2. Agent adds "status:in-progress" label
3. **Automatic**: Issue moves to "In Progress" column
4. Agent creates branch and starts work

### Workflow 3: Work Completed

1. Agent creates PR with "Closes #[ISSUE]"
2. **Automatic**: PR linked to issue
3. **Automatic**: PR added to same project
4. Reviews requested → PR moves to "Review"

### Workflow 4: PR Merged

1. PR is merged
2. **Automatic**: Issue closed
3. **Automatic**: Issue and PR move to "Done"
4. Agent updates TODO.md (if coordinator)

---

## 📊 Monitoring & Maintenance

### Daily Tasks (Coordinator)

```bash
# Check project status
gh project view 1 --owner asbor
gh project view 2 --owner asbor

# Check active agents
gh issue list --state open --json number,title,assignees

# Check for blocked tasks
gh issue list --label "status:blocked"

# Check overdue tasks (if using milestones)
gh issue list --milestone "Sprint 1" --state open
```

### Weekly Tasks (Coordinator)

1. **Review completed tasks**: Close old Done items
2. **Rebalance priorities**: Adjust labels as needed
3. **Update TODO.md**: Sync with closed issues
4. **Generate report**: Summary for stakeholders
5. **Plan next sprint**: Move items from Backlog to In Progress

### Monthly Tasks (Coordinator)

1. **Review project structure**: Are boards working well?
2. **Analyze metrics**: Completion rates, bottlenecks
3. **Update documentation**: Reflect lessons learned
4. **Recognize contributors**: Celebrate achievements
5. **Plan roadmap**: Adjust based on progress

---

## 🛠️ Troubleshooting

### "Can't add items to project"

**Solution**: Check project permissions. You need admin or write access.

### "Automation not working"

**Solution**: 
1. Check Project Settings → Workflows
2. Verify automation rules are enabled
3. Labels must match exactly (case-sensitive)

### "Too many items in Backlog"

**Solution**: 
1. Close duplicate/obsolete issues
2. Move P3-P4 items to Project 5
3. Break large tasks into smaller ones

### "Agents confused about which project"

**Solution**: 
1. Add project number to issue description
2. Use labels consistently
3. Update AI_AGENT_COORDINATION_GUIDE.md with examples

---

## 📚 References

- **GitHub Projects Documentation**: https://docs.github.com/en/issues/planning-and-tracking-with-projects
- **GitHub CLI Projects**: https://cli.github.com/manual/gh_project
- **Repository Documentation**:
  - `GITHUB_PROJECTS_ORGANIZATION.md` - Project structure
  - `AI_AGENT_COORDINATION_GUIDE.md` - Agent workflows
  - `TODO.md` - Task source
  - `ROADMAP.md` - Strategic direction

---

## ✅ Checklist for Setup Completion

- [ ] All 5 projects created
- [ ] Columns configured for each project
- [ ] Automation rules set up
- [ ] All labels created
- [ ] Issue templates updated
- [ ] Migration plan defined
- [ ] P0-P1 tasks migrated to Project 1
- [ ] Sample P2 tasks in Projects 2-3
- [ ] Coordinator identified
- [ ] Agents notified of new system
- [ ] Documentation updated
- [ ] First sprint planned

---

**Questions?** Create an issue with label `type:documentation` and tag the coordinator.
