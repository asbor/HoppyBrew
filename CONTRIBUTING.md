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

### Pre-commit Hooks Setup
We use pre-commit hooks to automatically check code quality before each commit.

```bash
# Install pre-commit (if not already installed)
pip install pre-commit

# Install the git hooks (run from repository root)
pre-commit install

# Optional: Run on all files to check current state
pre-commit run --all-files
```

The pre-commit hooks will automatically run:
- **Python**: Black (formatting), isort (imports), Flake8 (linting), mypy (type checking), Bandit (security)
- **JavaScript/TypeScript**: Prettier (formatting), ESLint (linting)
- **General**: Trailing whitespace, end-of-file fixes, YAML/JSON validation

If any check fails, the commit will be blocked. Fix the issues and try again.

To bypass hooks in emergencies (not recommended):
```bash
git commit --no-verify -m "Emergency fix"
```

### Running Tests
```bash
# Backend tests
cd services/backend
TESTING=1 pytest -v

# Backend tests with coverage
TESTING=1 pytest --cov=. --cov-report=html

# Frontend unit tests
cd services/nuxt3-shadcn
yarn test:unit

# Frontend E2E tests
yarn test:e2e
```

For comprehensive testing documentation, see [TESTING.md](TESTING.md).

## Coding Standards

### Code Quality Tools
We use automated tools to maintain code quality:
- **Black**: Python code formatting (line length: 88)
- **isort**: Python import sorting
- **Flake8**: Python linting (max line length: 120)
- **mypy**: Python static type checking
- **Pylint**: Additional Python code quality checks
- **Bandit**: Python security linting
- **Prettier**: JavaScript/TypeScript/Vue formatting
- **ESLint**: JavaScript/TypeScript linting

These tools run automatically via pre-commit hooks. You can also run them manually:

```bash
# Python formatting
cd services/backend
black .
isort .

# Python linting
flake8 .
pylint $(git ls-files '*.py')

# Python type checking
mypy .

# Python security check
bandit -r . -c pyproject.toml

# JavaScript/TypeScript formatting and linting
cd services/nuxt3-shadcn
yarn format:fix
yarn lint:fix
```

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
   - Ensure all tests pass: `TESTING=1 pytest -v`
   - Check coverage meets threshold: `TESTING=1 pytest --cov=. --cov-report=term`
   - Run pre-commit hooks: `pre-commit run --all-files`
   - Run code formatters (Black for Python, Prettier for JS/TS)
   - Update documentation if needed
   - Add/update tests for your changes

2. **PR Description**
   - Clearly describe what your PR does
   - Reference any related issues (#issue-number)
   - Include screenshots for UI changes
   - List any breaking changes
   - Mention if coverage targets are met

3. **Code Review**
   - Address all review comments
   - Keep the PR focused on a single feature/fix
   - Rebase on main if needed to resolve conflicts
   - Ensure CI checks pass

4. **Merging**
   - PRs require at least one approval
   - All CI/CD checks must pass (tests, coverage, linting)
   - Coverage must be ≥80% for backend, ≥70% for frontend
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

## Questions?

- Open a Discussion for general questions
- Open an Issue for bugs or feature requests
- Check existing documentation in [`documents/`](documents/)

Thank you for contributing to HoppyBrew! 🍺
