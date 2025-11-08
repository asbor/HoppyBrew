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

### Pre-commit Hooks Setup (Recommended)
We use pre-commit hooks to automatically check code quality before commits:

```bash
# Install pre-commit tool
pip install pre-commit

# Install the git hook scripts
pre-commit install

# (Optional) Run against all files to test
pre-commit run --all-files
```

Pre-commit hooks will automatically:
- Format Python code with Black and Ruff
- Lint Python code with Ruff
- Format and lint JavaScript/TypeScript/Vue with ESLint and Prettier
- Check for common issues (trailing whitespace, merge conflicts, etc.)
- Detect secrets and credentials

### Running Tests
```bash
# Backend tests
cd services/backend
pytest -v

# Backend tests with coverage
pytest -v --cov=. --cov-report=term --cov-report=html

# Frontend unit tests
cd services/nuxt3-shadcn
yarn test

# Frontend tests with coverage
yarn test:coverage
```

### Code Quality Checks
```bash
# Python formatting
cd services/backend
black .

# Python linting
ruff check .

# Frontend linting
cd services/nuxt3-shadcn
yarn lint

# Frontend formatting
yarn format
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

## Questions?

- Open a Discussion for general questions
- Open an Issue for bugs or feature requests
- Check existing documentation in [`documents/`](documents/)

Thank you for contributing to HoppyBrew! 🍺
