# Contributing to HoppyBrew

Thank you for your interest in contributing to HoppyBrew! This document provides guidelines and best practices for contributing to this project.

## Table of Contents
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [AI Agent Collaboration](#ai-agent-collaboration)

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/HoppyBrew.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit your changes with descriptive messages
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker (optional, for containerized development)
- PostgreSQL (for production) or SQLite (for development/testing)

### Backend Setup
```bash
cd services/backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd services/nuxt3-shadcn
yarn install
```

### Running Tests
```bash
# Backend tests
cd services/backend
pytest -v

# Frontend tests (when available)
cd services/nuxt3-shadcn
yarn test
```

## Coding Standards

### Python (Backend)
- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black formatter default)
- Use meaningful variable and function names
- Add docstrings to all public functions and classes

### JavaScript/TypeScript (Frontend)
- Use TypeScript for type safety
- Follow the existing code style
- Use meaningful component and variable names
- Add JSDoc comments for complex functions

### General Guidelines
- Write self-documenting code
- Keep functions small and focused (single responsibility)
- Avoid code duplication (DRY principle)
- Use dependency injection instead of module-level singletons
- Handle errors gracefully with appropriate logging

## Testing

### Backend Testing
- All new features must include tests
- Aim for >80% code coverage
- Test files should be in `services/backend/tests/`
- Use pytest fixtures for common test setup
- Mock external dependencies

Example test structure:
```python
def test_feature_name(client, db_session):
    # Arrange
    test_data = {"key": "value"}
    
    # Act
    response = client.post("/endpoint", json=test_data)
    
    # Assert
    assert response.status_code == 200
    assert response.json()["key"] == "value"
```

### Frontend Testing
- Component tests for all UI components
- Integration tests for complex workflows
- E2E tests for critical user journeys

## Pull Request Process

1. **Before Submitting**
   - Ensure all tests pass: `pytest -v`
   - Run code formatters (Black for Python)
   - Update documentation if needed
   - Add/update tests for your changes

2. **PR Description**
   - Clearly describe what your PR does
   - Reference any related issues (#issue-number)
   - Include screenshots for UI changes
   - List any breaking changes

3. **Code Review**
   - Address all review comments
   - Keep the PR focused on a single feature/fix
   - Rebase on main if needed to resolve conflicts

4. **Merging**
   - PRs require at least one approval
   - All CI/CD checks must pass
   - Squash commits when merging to keep history clean

## AI Agent Collaboration

This project supports multi-agent AI collaboration. If you're an AI agent:

1. Review [`AI_AGENT_MANIFEST.md`](AI_AGENT_MANIFEST.md) for collaboration guidelines
2. Check [`ROADMAP.md`](ROADMAP.md) for project direction
3. Review [`TODO.md`](TODO.md) for actionable tasks
4. Follow the same coding standards as human contributors
5. Include detailed commit messages explaining your changes
6. Run all tests before committing
7. Document any assumptions or limitations in your implementation

## Issue Reporting

When reporting bugs:
- Use the bug report template
- Include steps to reproduce
- Provide environment details (OS, Python version, etc.)
- Include relevant error messages and logs

When requesting features:
- Use the feature request template
- Clearly describe the use case
- Explain the expected behavior
- Consider implementation complexity

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Give credit where credit is due

## Dependency Management

### Philosophy
We maintain a proactive approach to dependency management to:
- Keep dependencies current with security patches
- Minimize breaking changes through regular small updates
- Maintain compatibility across the stack
- Prevent accumulation of technical debt

### Automated Tools
- **Dependabot**: Automatically creates PRs for dependency updates weekly
- **Security Scanning**: Daily scans with pip-audit, yarn audit, and Trivy
- **Dependency Review**: Blocks PRs with high-severity vulnerabilities

### Update Process

#### For Maintainers
1. **Review Dependabot PRs**
   - Check the changelog for breaking changes
   - Review test results in CI
   - Merge patch updates quickly (x.y.Z)
   - Test minor updates locally before merging (x.Y.0)
   - Plan major updates carefully (X.0.0)

2. **Manual Updates**
   - Check for outdated dependencies: `pip list --outdated` or `npm outdated`
   - Categorize by risk level (see DEPENDENCY_AUDIT.md)
   - Update in phases: patch → minor → major
   - Always run full test suite after updates

3. **Security Updates**
   - Prioritize security patches immediately
   - Check vulnerability details in GitHub Security
   - Test authentication and sensitive operations
   - Document any workarounds or breaking changes

#### For Contributors
When adding new dependencies:

**Python (services/backend/requirements.txt):**
```bash
# Add to requirements.txt with specific version
pip install package-name==x.y.z
pip freeze | grep package-name >> requirements.txt
# Run tests
pytest -v
```

**Node.js (services/nuxt3-shadcn/package.json):**
```bash
# Add with exact version
npm install package-name@x.y.z
# Or yarn
yarn add package-name@x.y.z
# Run tests
npm test
```

**Dependency Review Checklist:**
- [ ] Is this dependency actively maintained?
- [ ] Does it have known security vulnerabilities?
- [ ] Is the license compatible (check LICENSE.txt)?
- [ ] Can we use an existing dependency instead?
- [ ] Is the version pinned (not using wildcard ranges)?
- [ ] Have you run the test suite?

### Version Pinning Strategy
- **Production dependencies**: Pin to exact versions (e.g., `package==1.2.3`)
- **Development dependencies**: Pin to exact versions for consistency
- **Lock files**: Always commit `yarn.lock` or `package-lock.json`

### Risk Categories

#### 🟢 Low Risk - Patch Updates (x.y.Z)
- Bug fixes only
- No breaking changes
- Quick review and merge
- Example: `2.0.30 → 2.0.44`

#### 🟡 Medium Risk - Minor Updates (x.Y.0)
- New features added
- Possible deprecations
- Requires testing
- Example: `2.7.3 → 2.12.4`

#### 🔴 High Risk - Major Updates (X.0.0)
- Breaking changes expected
- Requires migration plan
- Extensive testing needed
- Dedicated PR with documentation
- Example: `3.11.2 → 4.0.0`

### Testing Requirements

**Before merging dependency updates:**
- [ ] All CI/CD checks pass
- [ ] Backend tests pass: `pytest -v`
- [ ] Frontend tests pass: `npm test`
- [ ] Security scans pass (pip-audit, yarn audit)
- [ ] Manual smoke testing completed
- [ ] No new linter warnings

**For Major Updates:**
- [ ] Review migration guide
- [ ] Update related documentation
- [ ] Test all affected features
- [ ] Update CHANGELOG.md
- [ ] Consider backward compatibility

### Emergency Security Updates

If a critical vulnerability is discovered:

1. **Immediate Response**
   ```bash
   # Check vulnerability details
   pip-audit -r requirements.txt  # Python
   npm audit                      # Node.js
   ```

2. **Apply Fix**
   - Update to patched version immediately
   - Create emergency PR
   - Skip normal review cycle if critical

3. **Validate**
   - Run full test suite
   - Deploy to staging
   - Monitor for issues

4. **Document**
   - Update SECURITY_SUMMARY.md
   - Document in PR and CHANGELOG.md
   - Notify team of changes

### Resources
- [DEPENDENCY_AUDIT.md](DEPENDENCY_AUDIT.md) - Current audit report
- [Dependabot Configuration](.github/dependabot.yml)
- [Security Scanning Workflow](.github/workflows/security-scan.yml)
- [Python Packaging Guide](https://packaging.python.org/)
- [npm Documentation](https://docs.npmjs.com/)

## Questions?

- Open a Discussion for general questions
- Open an Issue for bugs or feature requests
- Check existing documentation in [`documents/`](documents/)

Thank you for contributing to HoppyBrew! 🍺
