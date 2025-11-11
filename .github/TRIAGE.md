# Issue Triage Guide

This guide helps maintainers and contributors systematically triage issues in the HoppyBrew project.

## Table of Contents
- [Triage Process](#triage-process)
- [Priority Assessment](#priority-assessment)
- [Label Application](#label-application)
- [Common Scenarios](#common-scenarios)
- [Automated Triage](#automated-triage)

## Triage Process

### 1. Initial Review (Within 48 hours)

**For all new issues:**

1. **Verify Completeness**
   - [ ] Issue title is clear and descriptive
   - [ ] Description provides sufficient context
   - [ ] Steps to reproduce (for bugs)
   - [ ] Expected vs actual behavior defined

2. **Request Missing Information**
   - Use comment template: "Thanks for the report! Could you provide [missing info]?"
   - Add `question` label
   - Set reminder for follow-up in 7 days

3. **Check for Duplicates**
   - Search existing issues
   - If duplicate: link to original, add `status: duplicate`, close
   - If related: link issues together

### 2. Classification

**Apply Type Label** (choose one):
- `bug` - Broken functionality
- `feature` - New capability request  
- `enhancement` - Improvement to existing feature
- `documentation` - Docs update needed
- `performance` - Speed/efficiency issue
- `security` - Security concern
- `question` - Needs clarification

**Apply Area Labels** (choose all that apply):
- `area: backend`
- `area: frontend`
- `area: database`
- `area: docker`
- `area: ci-cd`
- `area: testing`
- `area: security`
- `area: docs`

### 3. Priority Assignment

Use the priority matrix below to assign P0-P3:

```
Impact vs Urgency Matrix:
                    Low Urgency    High Urgency
High Impact         P2             P0/P1
Low Impact          P3             P2
```

**Priority Criteria:**

**P0-critical** (Fix within 24 hours):
- Production system is down
- Data loss or corruption
- Security vulnerability being exploited
- Blocks all users from core functionality

**P1-high** (Fix within 1 week):
- Major feature broken for many users
- Significant performance degradation
- Security vulnerability (not actively exploited)
- Important feature request with clear business value

**P2-medium** (Fix within 1 month):
- Minor bugs affecting some users
- Feature enhancements
- Technical debt
- Documentation improvements
- Moderate performance issues

**P3-low** (Backlog):
- Nice-to-have features
- Minor cosmetic issues
- Future considerations
- Low-impact improvements

### 4. Difficulty Assessment

For issues suitable for community contribution:

**`good first issue`** criteria:
- Well-defined scope (< 4 hours work)
- Clear acceptance criteria
- No deep codebase knowledge required
- Existing pattern to follow
- Minimal dependencies

**`intermediate`** criteria:
- Moderate scope (1-2 days work)
- Requires understanding of one subsystem
- Some architectural decisions needed
- Multiple components affected

**`advanced`** criteria:
- Large scope (> 2 days work)
- Requires deep system understanding
- Significant architectural changes
- Performance-critical code
- Security-sensitive areas

### 5. Milestone Assignment

Assign to milestone based on priority:

- **P0-critical**: Current sprint (or create "Hotfix" milestone)
- **P1-high**: Next release milestone (v1.x)
- **P2-medium**: Future release milestone (v1.x or v2.0)
- **P3-low**: "Backlog" or "Future" milestone

## Priority Assessment

### Priority Decision Tree

```
Is the system unusable? → YES → P0-critical
                       → NO ↓
Is it a security issue? → YES → P0 or P1 (based on severity)
                       → NO ↓
Are many users affected? → YES → P1-high
                        → NO ↓
Is it an enhancement? → YES → P2-medium or P3-low
                     → NO ↓
Is it well-documented? → YES → P2-medium
                      → NO → Add info, reassess
```

### Impact Assessment

**High Impact:**
- Affects core functionality (recipe management, batch tracking)
- Affects all or most users
- Causes data loss or corruption
- Security implications

**Medium Impact:**
- Affects non-core features
- Affects subset of users
- Workaround exists
- Quality of life improvements

**Low Impact:**
- Cosmetic issues
- Rare edge cases
- Future features
- Nice-to-have improvements

### Urgency Assessment

**High Urgency:**
- Users are blocked
- Security concerns
- Regulatory requirements
- Time-sensitive features

**Medium Urgency:**
- Users can work around
- Requested by multiple users
- Planned feature

**Low Urgency:**
- Nice to have
- Future consideration
- Low demand

## Label Application

### Complete Label Set Example

```
Type:       bug
Priority:   P1-high
Area:       area: backend, area: database
Status:     status: needs-discussion
Difficulty: intermediate
```

### Label Transitions

As issues progress, update status labels:

```
New Issue
  ↓
status: needs-discussion (if unclear)
  ↓
[discussed]
  ↓
status: in-progress (when PR opened)
  ↓
status: needs-review (when PR ready)
  ↓
status: needs-testing (after review)
  ↓
[merged/closed]
```

## Common Scenarios

### Scenario 1: Bug Report - Auth Failure

```
Type: bug
Priority: P0-critical (blocks users)
Area: area: backend, area: security
Status: [none initially]
Milestone: Hotfix

Action: Immediate investigation
```

### Scenario 2: Feature Request - Export Recipes

```
Type: feature
Priority: P2-medium
Area: area: backend, area: frontend
Difficulty: intermediate
Milestone: v1.2

Action: Schedule for future sprint
```

### Scenario 3: Documentation Gap

```
Type: documentation
Priority: P3-low
Area: area: docs
Difficulty: good first issue
Milestone: Documentation

Action: Good candidate for new contributors
```

### Scenario 4: Performance Degradation

```
Type: performance, bug
Priority: P1-high
Area: area: backend, area: database
Status: status: needs-discussion
Milestone: v1.1

Action: Profile and investigate
```

### Scenario 5: Unclear Issue

```
Type: question
Status: [none]
Labels: question

Action:
1. Ask for clarification
2. Set 7-day reminder
3. If no response after 14 days, add status: stale
4. Close after 30 days of inactivity
```

## Automated Triage

### Stale Issue Management

Issues automatically receive `status: stale` if:
- No activity for 6 months
- No assignee
- Not in a milestone
- Not labeled `status: blocked` or `status: on-hold`

**Stale issue workflow:**
1. Bot adds `status: stale` label
2. Bot comments: "This issue has been inactive for 6 months..."
3. Wait 14 days for response
4. If no response, bot closes issue
5. Issue can be reopened if needed

### Auto-labeling Rules

**Dependabot PRs:**
- `dependencies`
- `automated`
- Language label (`python`, `javascript`, etc.)
- Area label based on path

**GitHub Actions:**
- Auto-label based on changed files
- Frontend changes → `area: frontend`
- Backend changes → `area: backend`
- Test changes → `area: testing`

## Triage Meetings

### Weekly Triage Session

**Agenda:**
1. Review new issues (since last meeting)
2. Review `status: needs-discussion` issues
3. Update priorities for upcoming sprint
4. Identify `good first issue` candidates
5. Close stale or resolved issues

**Output:**
- All new issues labeled and prioritized
- Milestone assignments updated
- Action items identified

### Monthly Backlog Review

**Agenda:**
1. Review all P3-low issues
2. Close outdated issues
3. Re-prioritize based on feedback
4. Update roadmap
5. Plan next milestone

## Quality Metrics

Track these metrics to measure triage effectiveness:

- **Time to First Response**: Target < 48 hours
- **% Labeled Issues**: Target 100%
- **% Prioritized Issues**: Target > 90%
- **% Issues in Milestones**: Target > 80%
- **Stale Issue Ratio**: Target < 20%
- **Average Time to Close**: Varies by priority

## Escalation Path

**P0-critical issues:**
1. Notify team lead immediately
2. Create Slack/Discord alert (if applicable)
3. Schedule emergency meeting if needed
4. Post-mortem after resolution

**Unclear priority:**
1. Add `status: needs-discussion`
2. Bring to weekly triage meeting
3. Document decision in issue comments

## Resources

- [Label Taxonomy](LABELS.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Issue Templates](ISSUE_TEMPLATE/)
- [Roadmap](../ROADMAP.md)

## Questions?

Open a discussion in GitHub Discussions or reach out to maintainers.

---

**Last Updated**: 2025-11-11
**Maintained By**: HoppyBrew Core Team
