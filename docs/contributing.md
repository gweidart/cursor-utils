# Contributing to Cursor-Utils

Thank you for your interest in contributing to Cursor-Utils! This guide will help you get started with the development process and outline our standards and expectations.

### Development Setup

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or newer
- Git
- A text editor or IDE (VS Code, PyCharm, etc.)
- UV package manager (recommended)

### Setting Up the Development Environment

1. **Fork the repository**

   Start by forking the Cursor-Utils repository on GitHub.

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/cursor-utils.git
   cd cursor-utils
   ```

3. **Create a virtual environment**

   Using UV (recommended):
   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

   Using standard venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install development dependencies**

   Using UV:
   ```bash
   uv pip install -e ".[dev]"
   ```

   Using pip:
   ```bash
   pip install -e ".[dev]"
   ```

5. **Install pre-commit hooks**

   ```bash
   pre-commit install
   ```

### Development Workflow

### Creating a New Feature

1. **Create a new branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement your changes**

   Follow the coding standards and ensure your code is well-tested.

3. **Run the tests**

   ```bash
   pytest
   ```

4. **Update documentation**

   If your changes affect the user interface or behavior, update the relevant documentation.

5. **Commit your changes**

   ```bash
   git add .
   git commit -m "Feature: Add your feature description"
   ```

6. **Push your changes**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a pull request**

   Go to the GitHub repository and create a pull request from your branch to the main branch.

### Fixing a Bug

1. **Create a new branch**

   ```bash
   git checkout -b fix/bug-description
   ```

2. **Implement your fix**

   Ensure you include tests that reproduce the bug and verify your fix.

3. **Run the tests**

   ```bash
   pytest
   ```

4. **Commit your changes**

   ```bash
   git add .
   git commit -m "Fix: Description of the bug fix"
   ```

5. **Push your changes**

   ```bash
   git push origin fix/bug-description
   ```

6. **Create a pull request**

   Go to the GitHub repository and create a pull request from your branch to the main branch.

### Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Use [Ruff](https://github.com/charliermarsh/ruff) for linting

### Type Annotations

- Use type annotations for all function parameters and return values
- Follow [PEP 484](https://www.python.org/dev/peps/pep-0484/) for type hints
- Use [PyRight](https://github.com/microsoft/pyright) for type checking

### Documentation

- Document all public functions, classes, and methods
- Follow [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Keep documentation up to date with code changes
- Include examples where appropriate

### Testing

- Write unit tests for all new functionality
- Aim for high test coverage, especially for core functionality
- Use pytest as the testing framework
- Mock external services in tests

### Commits

- Use conventional commit messages:
  - `Feature:` for new features
  - `Fix:` for bug fixes
  - `Docs:` for documentation changes
  - `Test:` for tests
  - `Refactor:` for code refactoring
  - `Chore:` for maintenance tasks
- Keep commits focused and atomic
- Reference issue numbers in commit messages where applicable

### Pull Request Process

1. **Fill in the pull request template** with all relevant information
2. **Ensure all checks pass** (tests, linting, etc.)
3. **Request a review** from a maintainer
4. **Address review feedback** promptly
5. **Update documentation** if necessary
6. **Squash commits** if requested by the reviewer

### Adding a New Command

To add a new command to Cursor-Utils:

1. **Create a new command file** in `src/cursor_utils/cli/commands/`
2. **Implement the command** following the existing command pattern
3. **Register the command** in `src/cursor_utils/cli/parser.py`
4. **Add tests** for the new command
5. **Document the command** in the appropriate documentation files

### Integrating with External Services

When adding a new service integration:

1. **Create a service client** in `src/cursor_utils/services/`
2. **Implement authentication** using Configuration for API keys
3. **Handle errors** appropriately using the error handling system
4. **Add tests** with mocked API responses
5. **Document the service** in the appropriate documentation files

### Release Process

Cursor-Utils follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward-compatible manner
- **PATCH** version for backward-compatible bug fixes

The release process is as follows:

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with the changes in the new version
3. **Create a pull request** for the version bump
4. **Merge the pull request** once approved
5. **Create a tag** for the new version
6. **Build and publish** the package to PyPI

### Getting Help

If you need help with the development process:

- **Check the documentation** in the `docs/` directory
- **Open an issue** with a question or discussion topic
- **Reach out to the maintainers** directly

### Code of Conduct

Please be respectful and constructive in your interactions with other contributors. We aim to foster an inclusive and welcoming community for all developers. 