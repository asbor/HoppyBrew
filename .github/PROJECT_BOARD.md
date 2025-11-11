# Project Board Structure

This document outlines the recommended GitHub Project board structure for HoppyBrew issue tracking and workflow management.

## Overview

HoppyBrew uses GitHub Projects (Beta) for visual tracking of issues and pull requests across milestones. The project board follows a Kanban-style workflow with automated state transitions.

## Board Configuration

### Board Name
**HoppyBrew Development Board**

### Board Type
- **Type**: Table view with status workflow
- **Access**: Public (visible to all)
- **Automation**: Enabled

---

## Columns (Status)

### 1. 📥 Backlog
**Description**: New and unscheduled issues  
**Criteria**:
- Newly created issues
- P3-low priority items
- Issues without milestone assignment
- Items pending triage

**Auto-add**:
- All new issues (via automation)

**Auto-move**:
- Issues with no activity for 90 days → Archive

---

### 2. 📋 Ready
**Description**: Triaged and ready for development  
**Criteria**:
- Fully triaged with labels
- Clear acceptance criteria
- No blockers
- Assigned to milestone
- P0-P2 priority

**Manual moves from**: Backlog (after triage)

**Auto-move**:
- When issue assigned to developer → In Progress

---

### 3. 🏗️ In Progress
**Description**: Actively being worked on  
**Criteria**:
- Has assignee
- Has `status: in-progress` label
- Active PR exists
- Developer actively working

**Auto-add**:
- When PR created and linked to issue
- When issue assigned to developer

**Auto-move**:
- When PR marked ready for review → In Review
- When stale for 14 days → Blocked/On Hold

---

### 4. 👀 In Review
**Description**: Code review in progress  
**Criteria**:
- PR submitted and ready for review
- Has `status: needs-review` label
- Awaiting reviewer feedback
- CI checks passing

**Auto-add**:
- When PR marked ready for review

**Auto-move**:
- When changes requested → In Progress
- When approved and CI passing → Testing

---

### 5. 🧪 Testing
**Description**: Ready for testing/QA  
**Criteria**:
- PR approved
- CI passing
- Has `status: needs-testing` label
- Awaiting manual testing or deployment

**Auto-add**:
- When PR approved and CI passing

**Auto-move**:
- When PR merged → Done
- When issues found → In Progress

---

### 6. ⏸️ Blocked/On Hold
**Description**: Cannot proceed due to dependencies  
**Criteria**:
- Has `status: blocked` or `status: on-hold` label
- Waiting on external dependency
- Waiting on design decision
- Waiting on other PR

**Manual moves from**: Any column

**Auto-move**:
- When blocker resolved → Ready (if not started) or In Progress (if started)

---

### 7. ✅ Done
**Description**: Completed and merged  
**Criteria**:
- PR merged
- Issue closed
- Feature deployed
- Documentation updated

**Auto-add**:
- When PR merged
- When issue closed

**Auto-move**:
- After 30 days → Archive

---

### 8. 🗄️ Archive
**Description**: Historical reference  
**Criteria**:
- Closed for >30 days
- Won't fix items
- Duplicates
- Out of scope

**Auto-add**:
- Closed issues after 30 days
- Issues with `status: duplicate` or `status: wontfix`

---

## Custom Fields

### Priority
**Type**: Single select  
**Options**:
- 🔴 P0-critical
- 🟠 P1-high
- 🟡 P2-medium
- 🟢 P3-low

**Source**: Synced from `P0-critical`, `P1-high`, `P2-medium`, `P3-low` labels

---

### Area
**Type**: Multi-select  
**Options**:
- Backend
- Frontend
- Database
- Docker
- CI/CD
- Testing
- Security
- Documentation

**Source**: Synced from `area:` labels

---

### Difficulty
**Type**: Single select  
**Options**:
- 🟢 Good First Issue
- 🟡 Intermediate
- 🔴 Advanced

**Source**: Synced from difficulty labels

---

### Type
**Type**: Single select  
**Options**:
- Bug 🐞
- Feature 🚀
- Enhancement ✨
- Documentation 📚
- Performance ⚡
- Security 🔒
- Refactoring ♻️

**Source**: Synced from type labels

---

### Milestone
**Type**: Single select  
**Options**: (Dynamic from GitHub milestones)
- v1.0 - Core Platform Release
- v1.1 - UX Enhancement
- v1.2 - Integration Features
- v2.0 - Advanced Features
- Technical Debt
- Documentation
- Backlog

**Source**: Synced from GitHub milestone assignment

---

### Estimate
**Type**: Single select  
**Options**:
- XS (1-4 hours) - 1 point
- S (4-8 hours) - 2 points
- M (8-16 hours) - 3 points
- L (16-24 hours) - 5 points
- XL (24+ hours) - 8 points

**Usage**: Set during sprint planning

---

### Sprint
**Type**: Text  
**Format**: "Sprint {number} - {start_date}"  
**Example**: "Sprint 1 - 2025-11-11"

**Usage**: Updated during sprint planning

---

## Views

### 1. Main Board (Kanban)
**Default view** - Status columns with cards  
**Filters**: None (shows all)  
**Group by**: Status  
**Sort**: Priority (high to low), then Updated (recent first)

---

### 2. Sprint Board
**Purpose**: Current sprint work  
**Filters**: 
- Sprint = Current sprint
- Status ≠ Done, Archive

**Group by**: Status  
**Sort**: Priority

---

### 3. Backlog View
**Purpose**: Triage and planning  
**Filters**: 
- Status = Backlog OR Ready
- Milestone ≠ null

**Group by**: Priority  
**Sort**: Created (oldest first)

---

### 4. Priority View
**Purpose**: Focus on high-priority items  
**Filters**: 
- Priority = P0 OR P1
- Status ≠ Done, Archive

**Group by**: Priority, then Area  
**Sort**: Updated (recent first)

---

### 5. Contributor View
**Purpose**: Find contribution opportunities  
**Filters**: 
- Difficulty = Good First Issue OR help wanted label
- Status = Ready

**Group by**: Area  
**Sort**: Created (oldest first)

---

### 6. Team View
**Purpose**: Team capacity and assignment  
**Layout**: Table  
**Columns**: Issue, Assignee, Priority, Estimate, Status, Sprint  
**Filters**: 
- Status = In Progress OR In Review OR Testing
- Assignee ≠ null

**Group by**: Assignee  
**Sort**: Priority

---

### 7. Milestone View
**Purpose**: Release planning  
**Layout**: Table  
**Columns**: Issue, Type, Priority, Status, Estimate  
**Filters**: Milestone = [selected milestone]  
**Group by**: Status  
**Sort**: Priority

---

## Automation Rules

### Issue Opened
**Trigger**: New issue created  
**Actions**:
1. Add to project board → Backlog column
2. Apply `status: needs-triage` label (temporary)

---

### Issue Triaged
**Trigger**: All required labels added (type, priority, area)  
**Actions**:
1. Remove `status: needs-triage` label
2. If P0 or P1 → Move to Ready column
3. If P2 or P3 → Keep in Backlog

---

### Issue Assigned
**Trigger**: Issue assigned to user  
**Actions**:
1. Add `status: in-progress` label
2. Move to In Progress column
3. Add to current sprint (if not already assigned)

---

### PR Opened
**Trigger**: PR created with issue reference  
**Actions**:
1. Link to issue
2. Move issue to In Progress
3. Copy labels from issue to PR

---

### PR Ready for Review
**Trigger**: PR marked ready (draft → ready)  
**Actions**:
1. Add `status: needs-review` label
2. Move issue to In Review
3. Request reviews from code owners

---

### PR Changes Requested
**Trigger**: Reviewer requests changes  
**Actions**:
1. Move issue back to In Progress
2. Update `status: in-progress` label

---

### PR Approved
**Trigger**: PR approved and CI passing  
**Actions**:
1. Add `status: needs-testing` label (if manual testing required)
2. Move issue to Testing
3. Notify in Slack/Discord (if configured)

---

### PR Merged
**Trigger**: PR merged to main  
**Actions**:
1. Move issue to Done
2. Close linked issues (if "Closes #X" in PR)
3. Remove all status labels
4. Add comment with release note

---

### Issue Closed
**Trigger**: Issue closed  
**Actions**:
1. Move to Done (if not duplicate/wontfix)
2. If duplicate/wontfix → Move to Archive
3. Link to duplicate or explanation

---

### Stale Issue Detection
**Trigger**: No activity for 90 days (Backlog) or 14 days (In Progress)  
**Actions**:
1. Add `status: stale` label
2. Add comment asking for status
3. Move to Blocked/On Hold
4. Close after 30 additional days if no response

---

## Board Metrics

Track these metrics for project health:

### Velocity
- Story points completed per sprint
- Trend over time
- Team capacity utilization

### Flow Metrics
- Cycle time (Ready → Done)
- Lead time (Created → Done)
- WIP limits respected

### Quality Metrics
- Bugs reopened ratio
- PR revision rounds
- Test coverage impact

### Health Indicators
- Age of oldest Ready item
- Number of Blocked items
- Backlog size trend

---

## Sprint Ceremonies

### Sprint Planning (Bi-weekly)
1. Review completed work from previous sprint
2. Pull items from Ready column
3. Estimate and assign
4. Set sprint goal
5. Update Sprint field

### Daily Standup (Daily)
1. Review In Progress column
2. Identify blockers → Move to Blocked
3. Update estimates
4. Reassign if needed

### Sprint Review (Bi-weekly)
1. Demo completed work from Done column
2. Gather feedback
3. Update documentation
4. Close milestone if complete

### Sprint Retrospective (Bi-weekly)
1. Review metrics
2. Identify improvements
3. Create action items
4. Update processes

### Backlog Grooming (Weekly)
1. Review Backlog column
2. Triage new issues
3. Update priorities
4. Move Ready items to Ready column
5. Archive stale items

---

## Access and Permissions

### Maintainers
- Full access to board
- Can edit all fields
- Can move items between columns
- Can archive items

### Contributors
- Read access to board
- Can comment on items
- Can update own assigned items
- Cannot move items between columns

### Public
- View-only access
- Can see all public issues
- Cannot edit or move items

---

## Setup Instructions

### Creating the Project Board

1. Navigate to repository → Projects → New project
2. Choose "Board" template
3. Configure columns as defined above
4. Add custom fields
5. Set up views
6. Enable automation rules

### Importing Existing Issues

```bash
# Use GitHub CLI to bulk add issues
gh project item-add [project-number] --owner asbor --url [issue-url]
```

### Automation via GitHub Actions

See `.github/workflows/project-automation.yml` for custom automation beyond GitHub's built-in features.

---

## Best Practices

### For Maintainers
- Triage new issues within 48 hours
- Keep Backlog column groomed (< 30 items)
- Review Blocked items weekly
- Update milestone progress monthly
- Archive Done items after 30 days

### For Contributors
- Update issue status when starting work
- Link PRs to issues with "Closes #X"
- Request review when PR ready
- Update estimates if work is larger than expected
- Comment on blocked items with context

### For Everyone
- Use the board as source of truth
- Keep issue descriptions up to date
- Add context in comments
- Link related issues
- Celebrate completions! 🎉

---

## References

- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [Triage Guide](.github/TRIAGE.md)
- [Label Taxonomy](.github/LABELS.md)
- [Milestone Definitions](.github/MILESTONES.md)

---

**Last Updated**: 2025-11-11  
**Maintained By**: HoppyBrew Core Team
