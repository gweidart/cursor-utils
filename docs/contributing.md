# Contributing to Cursor Utils

Thank you for considering contributing to Cursor Utils! This guide provides comprehensive information on how to contribute effectively to the project.

## Code of Conduct

We're committed to fostering an open and welcoming environment. Please be respectful, inclusive, and considerate of others when contributing to this project. Harassment or offensive behavior of any kind will not be tolerated.

## Getting Started

### Prerequisites

- Python 3.10 or newer
- [UV](https://github.com/astral-sh/uv) for dependency management
- Git
- A GitHub account

### Development Environment Setup

1. **Fork the repository** on GitHub.

2. **Clone your fork locally**:
```bash
git clone https://github.com/gweidart/cursor-utils.git
```

```bash
cd cursor-utils
```

3. **Create and activate a virtual environment**:
```bash
uv venv .venv
```

```bash
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

4. **Install development dependencies**:
```bash
uv pip sync requirements/requirements-dev.txt requirements/requirements-test.txt
```

5. **Install pre-commit hooks**:
```bash
pre-commit install
```

6. **Install the package in development mode**:
```bash
pip install -e .
```

## Development Workflow

### Branching Strategy

- `main` - Production-ready code
- `develop` - Main development branch
- Feature branches - Created for specific features or bug fixes

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### Making Changes

1. Make your changes in your feature branch.
2. Add and commit your changes with a meaningful commit message:
```bash
git add .
```

```bash
git commit -m "Add feature: description of changes"
```

3. Make sure tests pass and linting is clean:
```bash
pytest
```

```bash
pre-commit run --all-files
```

4. Push your changes to your fork:
```bash
git push origin feature/your-feature-name
```
5. Open a Pull Request against the `develop` branch.

## Coding Standards

Cursor Utils follows strict coding standards to maintain code quality and consistency.

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Follow [PEP 257](https://www.python.org/dev/peps/pep-0257/) for docstrings
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Use [Ruff](https://github.com/charliermarsh/ruff) for linting

### Type Annotations

- Use type hints for all function parameters and return values
- Follow [PEP 484](https://www.python.org/dev/peps/pep-0484/) for type annotations
- Use `TypedDict` for complex dictionary structures
- Use `Optional` for parameters that may be `None`
- Use `Union` for parameters that may have multiple types
- Use `Protocol` classes for interface definitions

### Documentation

- Every module should have a docstring explaining its purpose
- Every function and class should have a docstring explaining:
  - What it does
  - Parameters (with types and descriptions)
  - Return values (with types and descriptions)
  - Exceptions raised
  - Examples (if applicable)

Example docstring format:

```python
def function_name(param1: str, param2: Optional[int] = None) -> bool:
    """
    Short description of function.

    Longer description explaining details, behavior, and use cases.

    Args:
        param1: Description of param1
        param2: Description of param2, default is None

    Returns:
        Description of return value

    Raises:
        ValueError: When and why this exception is raised

    Examples:
        >>> function_name("example", 42)
        True
    """
```

### Error Handling

- Use the standardized error handling system in `cursor_utils.errors`
- Use the `safe_execute` and `safe_execute_sync` decorators for command functions
- Provide clear error messages and helpful hints for users
- Use appropriate error codes from `ErrorCodes` enum

Example error handling:

```python
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.utils.command_helpers import safe_execute

@safe_execute(WebError, ErrorCodes.WEB_QUERY_ERROR)
async def web_command(query: str) -> None:
    # Command implementation
    pass
```

### Code Structure

- Keep functions and methods short and focused
- Use clear, descriptive variable and function names
- Limit line length to 88 characters
- Avoid deep nesting of control structures
- Follow the "Single Responsibility Principle"
- Use comments sparingly and only when necessary

## Testing Guidelines

### Test Requirements

- All new code should include tests
- Aim for at least 80% test coverage
- Tests should be fast and independent
- Mock external services and APIs

### Types of Tests

- **Unit tests** - Test individual functions and methods
- **Integration tests** - Test interactions between components
- **Functional tests** - Test complete features

### Running Tests

```bash
# Run all tests
pytest
```

```bash
# Run tests with coverage
pytest --cov=cursor_utils
```

```bash
# Run specific tests
pytest tests/test_specific.py
```

```bash
# Run tests matching a pattern
pytest -k "test_pattern"
```

## Pull Request Process

1. **Create a Pull Request** from your feature branch to the `develop` branch
2. **Fill out the PR template** with all required information
3. **Link to any relevant issues**
4. **Ensure CI checks pass**:
   - Tests should pass
   - Code should be properly formatted
   - No linting errors
   - Type checking should pass
5. **Request review** from at least one maintainer
6. **Address review comments** and update your PR as needed
7. Once approved, a maintainer will merge your PR

### PR Checklist

Before submitting your PR, check that:

- [ ] Code follows the style guidelines
- [ ] Tests are added or updated to cover changes
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear and descriptive
- [ ] All CI checks pass

## Reporting Bugs

1. Check if the bug has already been reported in the [Issues](https://github.com/gweidart/cursor-utils/issues)
2. If not, create a new issue using the bug report template
3. Include:
   - A clear and descriptive title
   - Steps to reproduce the bug
   - Expected behavior
   - Actual behavior
   - Your environment (OS, Python version, etc.)
   - Screenshots if applicable

## Suggesting Features

1. Check if the feature has already been suggested in the [Issues](https://github.com/gweidart/cursor-utils/issues)
2. If not, create a new issue using the feature request template
3. Include:
   - A clear and descriptive title
   - A detailed description of the proposed feature
   - The problem the feature would solve
   - Any alternatives you've considered
   - Examples of similar features in other projects, if applicable

## Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

## Release Process

1. **Update version** using bump-my-version:
```bash
python scripts/bump_version.py [major|minor|patch]
```
2. **Update CHANGELOG.md** with all notable changes
3. **Create a new release on GitHub** with release notes
4. **Build and publish to PyPI** through GitHub Actions

## Getting Help

If you have questions or need help with the contribution process:

- Open a discussion on GitHub
- Ask in the project's community chat
- Contact the maintainers directly

## License

By contributing to Cursor Utils, you agree that your contributions will be licensed under the project's MIT License. 