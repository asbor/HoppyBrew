# GitHub Configuration & Documentation

This directory contains GitHub-specific configuration files, issue templates, and documentation for the HoppyBrew project.

## 📁 Directory Contents

### Issue Templates (`ISSUE_TEMPLATE/`)
Templates for creating consistent, well-structured issues:

- **[bug-report---.md](ISSUE_TEMPLATE/bug-report---.md)** - Report bugs and broken functionality
- **[feature-request---.md](ISSUE_TEMPLATE/feature-request---.md)** - Suggest new features
- **[security-vulnerability.md](ISSUE_TEMPLATE/security-vulnerability.md)** - Report security issues (use responsibly)
- **[documentation-improvement.md](ISSUE_TEMPLATE/documentation-improvement.md)** - Suggest doc improvements
- **[performance-issue.md](ISSUE_TEMPLATE/performance-issue.md)** - Report performance problems

### Pull Request Template
- **[PULL_REQUEST_TEMPLATE.md](PULL_REQUEST_TEMPLATE.md)** - Standardized PR description with checklists

### Workflow Automation (`workflows/`)
GitHub Actions workflows for CI/CD:

- **agent-coordination.yml** - AI agent coordination
- **docker-build.yml** - Docker image builds
- **e2e-tests.yml** - End-to-end testing
- **frontend-quality.yml** - Frontend linting and tests
- **main-build-deploy.yml** - Main build and deployment
- **pr-validation.yml** - Pull request validation
- **python-quality.yml** - Python linting and tests
- **release.yml** - Release automation
- **security-scan.yml** - Security scanning
- **test-suite.yml** - Comprehensive test suite

### Configuration Files
- **[dependabot.yml](dependabot.yml)** - Automated dependency updates
- **[labels.yml](labels.yml)** - Label definitions for automation
- **[COMMIT_TEMPLATE.txt](COMMIT_TEMPLATE.txt)** - Commit message template

### Documentation

#### Issue Management
- **[LABELS.md](LABELS.md)** - Comprehensive label taxonomy and usage guidelines
- **[TRIAGE.md](TRIAGE.md)** - Issue triage process and decision trees
- **[MILESTONES.md](MILESTONES.md)** - Milestone definitions and planning
- **[PROJECT_BOARD.md](PROJECT_BOARD.md)** - Project board structure and workflow

## 🚀 Quick Start

### For Issue Reporters
1. Choose the appropriate issue template
2. Fill out all required sections
3. Apply suggested labels (maintainers will adjust)
4. Reference related issues if applicable

### For Contributors
1. Review [LABELS.md](LABELS.md) to understand label meanings
2. Find issues tagged with `good first issue`
3. Follow the [PR template](PULL_REQUEST_TEMPLATE.md) when submitting
4. See [../CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines

### For Maintainers
1. Follow [TRIAGE.md](TRIAGE.md) for triaging new issues
2. Use [labels.yml](labels.yml) to keep labels consistent
3. Assign issues to milestones per [MILESTONES.md](MILESTONES.md)
4. Maintain project board per [PROJECT_BOARD.md](PROJECT_BOARD.md)

## 📊 Label System

We use a comprehensive label taxonomy with the following categories:

### Type Labels
Define what kind of issue/PR:
- `bug`, `feature`, `enhancement`, `documentation`, `performance`, `security`, `refactoring`

### Priority Labels
Indicate urgency:
- `P0-critical` (24h SLA)
- `P1-high` (1 week SLA)
- `P2-medium` (1 month SLA)
- `P3-low` (Backlog)

### Area Labels
Identify affected components:
- `area: backend`, `area: frontend`, `area: database`, `area: docker`, `area: ci-cd`, etc.

### Status Labels
Track lifecycle:
- `status: blocked`, `status: in-progress`, `status: needs-review`, `status: needs-testing`, etc.

### Difficulty Labels
Help contributors:
- `good first issue`, `intermediate`, `advanced`

See [LABELS.md](LABELS.md) for complete definitions.

## 🗺️ Milestones

Current active milestones:

- **v1.0 - Core Platform Release** (Q1 2026) - Production-ready platform
- **v1.1 - UX Enhancement** (Q2 2026) - User experience improvements
- **v1.2 - Integration Features** (Q3 2026) - External integrations
- **v2.0 - Advanced Features** (Q4 2026) - Advanced capabilities
- **Technical Debt** (Ongoing) - Code quality maintenance
- **Documentation** (Ongoing) - Documentation improvements

See [MILESTONES.md](MILESTONES.md) for detailed definitions and planning.

## 📋 Triage Process

### Priority Decision Matrix
```
Impact vs Urgency:
                    Low Urgency    High Urgency
High Impact         P2             P0/P1
Low Impact          P3             P2
```

### Weekly Triage Checklist
- [ ] Review new issues (apply labels)
- [ ] Assign priorities
- [ ] Assign milestones
- [ ] Identify blockers
- [ ] Mark good first issues
- [ ] Close stale/duplicates

See [TRIAGE.md](TRIAGE.md) for detailed process.

## 🎯 Project Board

We use GitHub Projects for visual tracking:

### Columns
1. 📥 **Backlog** - New and unscheduled
2. 📋 **Ready** - Triaged and ready for work
3. 🏗️ **In Progress** - Active development
4. 👀 **In Review** - Code review in progress
5. 🧪 **Testing** - Ready for testing/QA
6. ⏸️ **Blocked/On Hold** - Waiting on dependencies
7. ✅ **Done** - Completed and merged
8. 🗄️ **Archive** - Historical reference

See [PROJECT_BOARD.md](PROJECT_BOARD.md) for complete structure and automation.

## 🔒 Security

### Reporting Security Issues
Use the [security-vulnerability.md](ISSUE_TEMPLATE/security-vulnerability.md) template for non-critical issues.

For critical security vulnerabilities, please report privately:
- Email: [Project maintainers]
- GitHub Security Advisories: Preferred method

See [../SECURITY.md](../SECURITY.md) for complete security policy.

## 🤖 Automation

### Dependabot
- Automated dependency updates
- Configured for Python, Node.js, Docker, GitHub Actions
- Weekly schedule with PR limits

### GitHub Actions
- PR validation (linting, tests, security)
- Automated builds and deployments
- Security scanning
- Test coverage reporting

### Project Board Automation
- Auto-add new issues to Backlog
- Auto-move based on PR status
- Stale issue detection
- Label synchronization

## 📈 Metrics & Health

Track project health with:

### Issue Metrics
- Time to first response: Target < 48h
- % Labeled issues: Target 100%
- % Prioritized issues: Target > 90%
- % In milestones: Target > 80%

### Code Quality
- Test coverage: Target > 70%
- Code quality score: Target > B
- Security vulnerabilities: Target 0 critical/high

### Workflow Efficiency
- Cycle time (Ready → Done)
- PR review time
- Build success rate
- Deployment frequency

## 🔄 Maintenance Schedule

### Daily
- Monitor critical (P0) issues
- Review failed CI/CD runs
- Triage new security alerts

### Weekly
- Issue triage session
- Backlog grooming
- Sprint planning (bi-weekly)

### Monthly
- Milestone review
- Label consistency check
- Metrics review
- Automation cleanup

### Quarterly
- Technical debt assessment
- Process improvements
- Tool evaluation

## 📚 Additional Resources

### Internal
- [../CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [../ROADMAP.md](../ROADMAP.md) - Project roadmap
- [../SECURITY.md](../SECURITY.md) - Security policy
- [../README.md](../README.md) - Project overview

### External
- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [GitHub Projects Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🤝 Contributing

We welcome contributions! Please:

1. Read [../CONTRIBUTING.md](../CONTRIBUTING.md)
2. Check [PROJECT_BOARD.md](PROJECT_BOARD.md) for available work
3. Follow issue templates when reporting
4. Follow PR template when contributing
5. Respect our code of conduct

## 💬 Questions?

- **General questions**: Open a [Discussion](https://github.com/asbor/HoppyBrew/discussions)
- **Bug reports**: Use the [bug report template](ISSUE_TEMPLATE/bug-report---.md)
- **Feature requests**: Use the [feature request template](ISSUE_TEMPLATE/feature-request---.md)
- **Documentation issues**: Use the [documentation template](ISSUE_TEMPLATE/documentation-improvement.md)

---

**Last Updated**: 2025-11-11  
**Maintained By**: HoppyBrew Core Team
