# AI Agent Coordination Guide

**Purpose**: Practical guide for AI agents working on HoppyBrew project  
**Last Updated**: November 8, 2025  
**For**: AI Agents, Coordinators, Contributors

---

## 🚀 Quick Start for AI Agents

### 1. Orient Yourself

**First-time agents, read these in order:**
1. This document (you're here!)
2. `GITHUB_PROJECTS_ORGANIZATION.md` - Project structure
3. `TODO.md` - Current task list
4. `ROADMAP.md` - Project direction
5. `CONTRIBUTING.md` - Contribution guidelines

### 2. Identify Your Role

Match your capabilities to one of these roles:

| Your Expertise | Role | Focus Areas |
|---------------|------|-------------|
| Python, FastAPI, SQLAlchemy | **Backend Agent** | APIs, models, database |
| Vue.js, Nuxt, TypeScript | **Frontend Agent** | Components, pages, UI |
| Docker, CI/CD, Linux | **DevOps Agent** | Infrastructure, automation |
| Testing, pytest, Vitest | **QA Agent** | Tests, coverage, quality |
| Data processing, ETL | **Data Agent** | Imports, integrations |
| Technical writing | **Documentation Agent** | Docs, guides, README |
| Security, auth, encryption | **Security Agent** | Vulnerabilities, hardening |

**Can't decide?** You're a **General Agent** - pick tasks marked for any role.

### 3. Find Your First Task

**Option A: From GitHub Projects** (Recommended)
```bash
# View available tasks
gh project item-list 1 --owner asbor  # Critical Operations
gh project item-list 2 --owner asbor  # Feature Development

# Filter by your role
gh issue list --label "agent-role:backend" --state open
gh issue list --label "agent-role:frontend" --state open
```

**Option B: From TODO.md**
1. Open `TODO.md`
2. Find unchecked `[ ]` items in your domain
3. Check if GitHub issue exists for it
4. If not, create one using `.github/ISSUE_TEMPLATE/agent-task.md`

**Task Selection Criteria:**
- ✅ Matches your role/expertise
- ✅ Not assigned to another agent
- ✅ Priority appropriate for current phase
- ✅ No unresolved dependencies
- ✅ Estimated time fits your availability

### 4. Claim Your Task

```bash
# Assign the issue to yourself
gh issue edit [ISSUE_NUMBER] --add-assignee @me

# Add status label
gh issue edit [ISSUE_NUMBER] --add-label "status:in-progress"

# Leave a comment with your plan
gh issue comment [ISSUE_NUMBER] --body "Starting work on this. ETA: [X hours/days]"
```

### 5. Do the Work

Follow these practices:

**Branch Naming:**
```bash
git checkout -b agent/[role]/[issue-number]-brief-description
# Examples:
# agent/backend/226-add-foreign-key-indexes
# agent/frontend/145-recipe-detail-components
# agent/devops/148-ci-cd-pipeline
```

**Commit Messages:**
```
[#ISSUE] Component: Brief description

Detailed explanation of what changed and why.

- Bullet point for significant change 1
- Bullet point for significant change 2

Closes #[ISSUE_NUMBER]
```

**Code Quality:**
- Run tests: `make test` or `pytest -v`
- Run linters: `make lint` or existing linters
- Follow existing code style
- Add tests for new code
- Update documentation

### 6. Submit Your Work

**Create Pull Request:**
```bash
# Push your branch
git push origin agent/[role]/[issue-number]-brief-description

# Create PR (gh CLI)
gh pr create --title "[#ISSUE] Component: Brief description" \
  --body "Closes #[ISSUE_NUMBER]\n\n[Description of changes]" \
  --assignee @me
```

**PR Description Template:**
```markdown
## 🎯 Changes

[Brief summary of what this PR does]

## 🔗 Related Issue

Closes #[ISSUE_NUMBER]

## ✅ Checklist

- [ ] Tests added/updated
- [ ] Tests passing locally
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Follows code style

## 🧪 Testing Done

[Describe how you tested these changes]

## 📸 Screenshots

[For UI changes, add screenshots]

## 💡 Notes

[Any additional context for reviewers]
```

### 7. Handle Review

**If changes requested:**
1. Make the requested changes
2. Push to the same branch
3. Reply to review comments
4. Request re-review when done

**If approved:**
1. Wait for merge (coordinator or maintainer will merge)
2. Delete your local branch after merge
3. Update task status in project board
4. Move on to next task!

---

## 🚫 Avoiding Conflicts

### File Conflict Matrix

This table shows which files are safe to edit in parallel:

| File/Directory | Can Multiple Agents Edit? | Coordination Needed? |
|----------------|---------------------------|----------------------|
| `services/backend/app/api/endpoints/` | ✅ Yes (different files) | ❌ No |
| `services/backend/app/models/` | ✅ Yes (different files) | ❌ No |
| `services/backend/app/schemas/` | ✅ Yes (different files) | ❌ No |
| `services/nuxt3-shadcn/pages/` | ✅ Yes (different files) | ❌ No |
| `services/nuxt3-shadcn/components/` | ✅ Yes (different files) | ❌ No |
| `docker-compose.yml` | ❌ One at a time | ✅ Yes - check with DevOps |
| `Makefile` | ❌ One at a time | ✅ Yes - check with coordinator |
| `requirements.txt` | ⚠️ Coordinate | ✅ Yes - announce in PR |
| `package.json` | ⚠️ Coordinate | ✅ Yes - announce in PR |
| `alembic/versions/` | ❌ One at a time | ✅ Yes - strict coordination |
| `TODO.md` | ❌ Coordinator only | ✅ N/A - read-only for agents |
| `ROADMAP.md` | ❌ Coordinator only | ✅ N/A - read-only for agents |

**Safe Zones for Parallel Work:**

**Backend Agents:**
- Different endpoint files
- Different model files
- Different schema files
- Different service modules

**Frontend Agents:**
- Different page files
- Different component files
- Different composable files
- Different stores (when using Pinia)

**DevOps Agents:**
- Different workflow files in `.github/workflows/`
- Different Docker files (Dockerfile.backend vs Dockerfile.frontend)
- Different script files in `scripts/`

**Documentation Agents:**
- Different markdown files in `documents/`
- Different guide files
- Different README sections (coordinate if same file)

### Coordination Protocol

**Before starting work on a shared file:**

1. **Check GitHub for open PRs:**
   ```bash
   gh pr list --state open | grep [FILENAME]
   ```

2. **Announce your intention:**
   - Comment on your issue: "Will be editing [FILENAME]"
   - Check for conflicts with other agents' issues

3. **If conflict detected:**
   - Coordinate in issue comments
   - One agent waits for the other to finish
   - Or: Split the work differently to avoid the shared file

### Merge Conflict Resolution

**If you encounter a merge conflict:**

1. **Don't panic!** Merge conflicts are normal.

2. **Update your branch:**
   ```bash
   git fetch origin main
   git merge origin/main
   ```

3. **Resolve conflicts:**
   - Open conflicted files
   - Look for `<<<<<<<`, `=======`, `>>>>>>>` markers
   - Decide which changes to keep
   - Remove conflict markers
   - Test that everything still works

4. **Commit resolution:**
   ```bash
   git add [resolved-files]
   git commit -m "Resolve merge conflicts with main"
   git push
   ```

5. **If stuck:**
   - Ask coordinator for help in PR comments
   - Coordinator can help resolve complex conflicts

---

## 📊 Task Prioritization

### When to Pick High Priority (P0-P1)

**Do pick if:**
- You have the right expertise
- You can complete it quickly (within 1-3 days)
- No dependencies blocking you
- It's currently blocking other work

**Don't pick if:**
- You're unfamiliar with the codebase area
- It requires extensive research
- Other agents are better suited
- Dependencies aren't resolved yet

### When to Pick Medium Priority (P2)

**Do pick if:**
- All P0-P1 tasks are assigned or not suited to you
- You have time for a 3-7 day task
- You want to build a complete feature
- It matches your expertise

### When to Pick Low Priority (P3-P4)

**Do pick if:**
- You're new and want to learn the codebase
- You want a quick win (P3 simple tasks)
- All higher priorities are assigned
- You're exploring new areas of the codebase

---

## 🎯 Domain-Specific Guidance

### For Backend Agents

**Common Tasks:**
- Adding new API endpoints
- Creating database models
- Writing migrations
- Adding business logic
- Optimizing queries

**Key Files:**
- `services/backend/app/api/endpoints/` - API routes
- `services/backend/app/models/` - SQLAlchemy models
- `services/backend/app/schemas/` - Pydantic schemas
- `services/backend/app/services/` - Business logic
- `alembic/versions/` - Database migrations

**Testing:**
```bash
cd services/backend
pytest tests/test_[your_area].py -v
```

**Common Patterns:**
```python
# Endpoint pattern
@router.get("/{id}", response_model=schema.Response)
async def get_item(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item
```

### For Frontend Agents

**Common Tasks:**
- Creating new pages
- Building UI components
- Integrating with APIs
- Adding forms and validation
- Improving UX

**Key Files:**
- `services/nuxt3-shadcn/pages/` - Page components
- `services/nuxt3-shadcn/components/` - Reusable components
- `services/nuxt3-shadcn/composables/` - Shared logic
- `services/nuxt3-shadcn/stores/` - State management

**Testing:**
```bash
cd services/nuxt3-shadcn
npm run test  # When tests are set up
npm run dev   # For manual testing
```

**Common Patterns:**
```vue
<script setup lang="ts">
// Use composition API
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

const { data, loading, error, fetchData } = useApi('/api/endpoint')

onMounted(async () => {
  await fetchData()
})
</script>
```

### For DevOps Agents

**Common Tasks:**
- Docker configuration
- CI/CD pipelines
- Build optimization
- Deployment automation
- Monitoring setup

**Key Files:**
- `docker-compose.yml` - Local development
- `.github/workflows/` - CI/CD
- `Makefile` - Build automation
- `scripts/` - Helper scripts

**Testing:**
```bash
# Test Docker build
docker-compose build

# Test services start
docker-compose up -d

# Check health
docker-compose ps
```

### For QA Agents

**Common Tasks:**
- Writing unit tests
- Writing integration tests
- E2E test setup
- Improving test coverage
- Test infrastructure

**Key Files:**
- `services/backend/tests/` - Backend tests
- `services/nuxt3-shadcn/tests/` - Frontend tests (to be created)
- `pytest.ini` - Pytest configuration
- `.github/workflows/test.yml` - Test automation

**Testing:**
```bash
# Run with coverage
cd services/backend
pytest --cov=app --cov-report=term-missing

# Run specific test
pytest tests/test_recipes.py::test_create_recipe -v
```

### For Documentation Agents

**Common Tasks:**
- Updating README
- Writing user guides
- API documentation
- Code documentation
- Troubleshooting guides

**Key Files:**
- `README.md` - Main documentation
- `documents/` - Additional docs
- `api_endpoint_catalog.md` - API reference
- `CONTRIBUTING.md` - Contributor guide

**Best Practices:**
- Use clear, simple language
- Add code examples
- Include screenshots for UI
- Keep docs up-to-date with code
- Link related documents

---

## 🐛 Troubleshooting

### "Issue already assigned to another agent"

**Solution:** Pick a different task. The assigned agent is working on it.

### "Merge conflicts in my PR"

**Solution:** See "Merge Conflict Resolution" section above.

### "Tests failing after my changes"

**Solution:**
1. Run tests locally to reproduce
2. Check if your changes broke existing functionality
3. Fix the breaking changes or update tests if behavior change is intentional
4. Push the fixes

### "Don't understand the task requirements"

**Solution:**
1. Read related documentation links in the issue
2. Check similar completed PRs for examples
3. Ask questions in issue comments
4. Tag the coordinator for clarification

### "Task is blocked by dependency"

**Solution:**
1. Check the blocking issue's status
2. If blocked issue is unassigned, consider working on it first
3. If blocked issue is assigned, pick a different task
4. Update your issue with status note

### "Found a bug while working on feature"

**Solution:**
1. If minor: Fix it in your PR and mention in description
2. If major: Create separate issue for the bug
3. If critical: Report immediately and tag as P0

---

## 📈 Success Metrics

**Good agent performance:**
- ✅ 80%+ of claimed tasks completed
- ✅ < 2 days average time from claim to PR
- ✅ < 10% merge conflicts
- ✅ 95%+ tests passing on first PR
- ✅ Clear commit messages and PR descriptions
- ✅ Documentation updated with code

**Red flags:**
- ❌ Claiming many tasks but not completing them
- ❌ PRs with failing tests
- ❌ Large PRs that change too much
- ❌ Not following code style
- ❌ Not responding to review comments
- ❌ Creating merge conflicts repeatedly

---

## 🎓 Learning Resources

### Understanding the Codebase

**Backend:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- Existing endpoints: `services/backend/app/api/endpoints/`

**Frontend:**
- [Nuxt 3 Documentation](https://nuxt.com/)
- [Vue 3 Documentation](https://vuejs.org/)
- Existing pages: `services/nuxt3-shadcn/pages/`

**Project Structure:**
- Read `README.md` for architecture overview
- Read `ROADMAP.md` for project goals
- Read `CONTRIBUTING.md` for style guide

### Example PRs to Learn From

Check closed PRs for examples of good work:
```bash
gh pr list --state closed --limit 10
```

Look for PRs with:
- Clear descriptions
- Good test coverage
- Clean commit history
- Proper documentation

---

## 🤝 Getting Help

### From Coordinator

**Ask coordinator when:**
- Task requirements unclear
- Merge conflicts too complex
- Need architectural guidance
- Blocked by another agent's work
- Found critical bug

**How to ask:**
- Comment on your issue
- Tag `@coordinator` (if applicable)
- Be specific about the problem
- Suggest possible solutions

### From Other Agents

**Coordinate with other agents when:**
- Working on related features
- Editing shared files
- Need domain expertise
- Resolving merge conflicts

**How to coordinate:**
- Comment in related issues
- Reference their PR/issue
- Suggest collaboration approach

### From Documentation

**Check these first:**
- This document (AI_AGENT_COORDINATION_GUIDE.md)
- `GITHUB_PROJECTS_ORGANIZATION.md`
- `CONTRIBUTING.md`
- `README.md`
- `TODO.md` and `ROADMAP.md`

---

## 🎉 After Your First Task

**Congratulations!** You've completed your first task. Here's what's next:

1. **Reflect on the process:**
   - What went well?
   - What was confusing?
   - How can we improve?

2. **Update your capacity:**
   - Can you take on another task?
   - Same complexity or more challenging?
   - Same domain or try something new?

3. **Pick your next task:**
   - Use lessons learned
   - Maybe try a different area
   - Or go deeper in your specialty

4. **Share knowledge:**
   - Document anything not covered here
   - Suggest improvements to guides
   - Help other agents in comments

---

## 📞 Quick Reference

### Essential Commands

```bash
# View tasks
gh issue list --state open --label "agent-task"

# Claim task
gh issue edit [#] --add-assignee @me

# Create branch
git checkout -b agent/[role]/[#]-description

# Run tests
make test  # or cd services/backend && pytest -v

# Create PR
gh pr create --title "[#] Title" --body "Closes #[#]"

# Check PR status
gh pr status

# View project board
gh project item-list [1|2|3|4|5] --owner asbor
```

### Essential Files

- **Task Planning:** `TODO.md`, `ROADMAP.md`
- **Coordination:** This file, `GITHUB_PROJECTS_ORGANIZATION.md`
- **Contributing:** `CONTRIBUTING.md`
- **Architecture:** `README.md`, `DEPLOYMENT_GUIDE.md`

### Essential Links

- GitHub Projects: https://github.com/asbor/HoppyBrew/projects
- Issues: https://github.com/asbor/HoppyBrew/issues
- Pull Requests: https://github.com/asbor/HoppyBrew/pulls

---

**Welcome to the team! Let's build something amazing together! 🍺**
