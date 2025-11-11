# Issue Tracker Quick Reference

Quick reference guide for HoppyBrew issue tracker management.

## 🏷️ Label Quick Reference

### Priority (Choose ONE)
- 🔴 `P0-critical` - Fix within 24h (blocking, security, data loss)
- 🟠 `P1-high` - Fix within 1 week (major bugs, important features)
- 🟡 `P2-medium` - Fix within 1 month (enhancements, tech debt)
- 🟢 `P3-low` - Backlog (nice-to-have, future)

### Type (Choose ONE)
- `bug` - Broken functionality
- `feature` - New capability
- `enhancement` - Improvement to existing
- `documentation` - Docs update
- `performance` - Speed/efficiency
- `security` - Security issue
- `refactoring` - Code quality

### Area (Choose ALL that apply)
- `area: backend` - Backend/API
- `area: frontend` - Frontend/UI
- `area: database` - Database
- `area: docker` - Containers
- `area: ci-cd` - CI/CD
- `area: testing` - Tests
- `area: security` - Security
- `area: docs` - Documentation

### Status (Choose ONE if needed)
- `status: blocked` - Waiting on dependency
- `status: in-progress` - Being worked on
- `status: needs-review` - Awaiting review
- `status: needs-testing` - Needs QA
- `status: needs-discussion` - Needs decision

### Difficulty (For contributor issues)
- `good first issue` - Easy, well-defined
- `intermediate` - Moderate complexity
- `advanced` - Deep knowledge needed

---

## 📋 Triage Checklist

Quick 5-step triage for new issues:

1. ✅ **Verify** - Is information complete?
2. 🏷️ **Type** - Add type label
3. 🎯 **Priority** - Use matrix below
4. 📍 **Area** - Add area labels
5. 🗓️ **Milestone** - Assign based on priority

### Priority Decision Matrix
```
                Low Urgency    High Urgency
High Impact     P2             P0/P1
Low Impact      P3             P2
```

---

## 🎯 Priority Guidelines

### P0-critical (24h SLA)
- ✋ System down
- 💥 Data loss/corruption
- 🔓 Active security breach
- 🚫 Blocks all users

### P1-high (1 week SLA)
- 🐛 Major bug affecting many users
- 🚀 High-value feature
- 🔒 Security vulnerability (not exploited)
- ⚡ Severe performance issue

### P2-medium (1 month SLA)
- 🔧 Minor bugs
- ✨ Enhancements
- 📚 Documentation
- ♻️ Technical debt

### P3-low (Backlog)
- 💡 Nice-to-have
- 🎨 Cosmetic
- 🔮 Future features
- 📊 Low-impact improvements

---

## 🗓️ Milestone Assignment

| Priority | Milestone |
|----------|-----------|
| P0 | Current sprint / Hotfix |
| P1 | Current or next release |
| P2 | Next 2-3 releases |
| P3 | Backlog |

### Active Milestones
- **v1.0** (Q1 2026) - Core Platform
- **v1.1** (Q2 2026) - UX Enhancement
- **v1.2** (Q3 2026) - Integrations
- **v2.0** (Q4 2026) - Advanced Features
- **Technical Debt** - Ongoing
- **Documentation** - Ongoing
- **Backlog** - Future

---

## 📊 Project Board Columns

```
📥 Backlog → 📋 Ready → 🏗️ In Progress → 👀 In Review → 🧪 Testing → ✅ Done
                              ↓
                      ⏸️ Blocked/On Hold
```

### Column Meanings
- **Backlog** - New/unscheduled
- **Ready** - Triaged, ready for work
- **In Progress** - Active development
- **In Review** - Code review
- **Testing** - Manual QA
- **Blocked** - Waiting on dependency
- **Done** - Merged/closed
- **Archive** - Historical (30+ days)

---

## 🎬 Common Actions

### Triage New Issue
```bash
# Add labels
gh issue edit <number> --add-label "bug,P1-high,area: backend"

# Assign milestone
gh issue edit <number> --milestone "v1.0 - Core Platform Release"

# Add to project
gh project item-add <project-number> --url <issue-url>
```

### Close Duplicate
```markdown
Closing as duplicate of #<number>.

[Explanation if needed]

Feel free to continue discussion on the original issue.
```
Label: `status: duplicate`, then close

### Close Stale
```markdown
Closing due to inactivity (90+ days). 

If this is still relevant, please comment and we'll reopen.
```
Label: `status: stale`, then close

### Close Won't Fix
```markdown
Thanks for the suggestion! After discussion, we've decided not to implement this because [reason].

[Alternative if applicable]
```
Label: `status: wontfix`, then close

---

## 📅 Weekly Routine

### Monday - Triage New Issues
- [ ] Review issues created last week
- [ ] Apply type, priority, area labels
- [ ] Assign milestones
- [ ] Move to Ready if P0/P1

### Wednesday - Backlog Review
- [ ] Review Backlog column
- [ ] Update priorities if needed
- [ ] Move Ready items to board
- [ ] Check for stale issues

### Friday - Sprint Planning
- [ ] Review Done column
- [ ] Plan next sprint work
- [ ] Update estimates
- [ ] Celebrate completions! 🎉

---

## 🔍 Quick Searches

### Find Issues to Triage
```
is:issue is:open no:label
```

### Find High Priority
```
is:issue is:open label:P0-critical,P1-high
```

### Find Good First Issues
```
is:issue is:open label:"good first issue"
```

### Find Stale Issues
```
is:issue is:open updated:<2024-05-11
```

### Find Blocked Issues
```
is:issue is:open label:"status: blocked"
```

---

## 📞 Escalation

### P0-critical Issue
1. 🚨 Alert team immediately
2. 🎯 Create hotfix milestone
3. 👤 Assign to available developer
4. 📝 Post-mortem after resolution

### Unclear Priority
1. ➕ Add `status: needs-discussion`
2. 📅 Schedule for next triage meeting
3. 📝 Document decision in comments

---

## 📚 Resources

| Document | Use For |
|----------|---------|
| [LABELS.md](LABELS.md) | Complete label reference |
| [TRIAGE.md](TRIAGE.md) | Detailed triage process |
| [MILESTONES.md](MILESTONES.md) | Milestone definitions |
| [PROJECT_BOARD.md](PROJECT_BOARD.md) | Board structure |
| [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) | Setup instructions |

---

## 💡 Pro Tips

- ⚡ Label PRs same as their issues
- 🔗 Always link related issues with "Related to #X"
- 📝 Use "Closes #X" in PR descriptions
- 🎯 Keep Backlog column under 30 items
- 🧹 Archive Done items after 30 days
- 🏷️ Review label consistency monthly
- 📊 Track metrics for continuous improvement
- 🙏 Thank contributors in issue comments!

---

**Last Updated**: 2025-11-11  
**Quick Reference Version**: 1.0
