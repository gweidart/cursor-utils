# Contributing to Cursor Utils

Thank you for considering contributing to Cursor Utils! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the [Issues](https://github.com/gweidart/cursor-utils/issues).
2. If not, create a new issue using the bug report template.
3. Include as much detail as possible: steps to reproduce, expected behavior, actual behavior, and your environment.

### Suggesting Features

1. Check if the feature has already been suggested in the [Issues](https://github.com/gweidart/cursor-utils/issues).
2. If not, create a new issue using the feature request template.
3. Clearly describe the problem the feature would solve and the proposed solution.

### Pull Requests

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes, following the coding standards.
4. Add or update tests as necessary.
5. Update documentation as necessary.
6. Submit a pull request.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/gweidart/cursor-utils.git
cd cursor-utils
```

2. Create and activate a virtual environment:
```bash
uv venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install development dependencies:
```bash
uv pip sync requirements/requirements-dev.txt requirements/requirements-test.txt
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
- Use type hints for all function parameters and return values.
- Write docstrings for all modules, classes, and functions.
- Keep lines under 88 characters.
- Use meaningful variable and function names.

## Testing

- Write tests for all new features and bug fixes.
- Run the test suite before submitting a pull request:
```bash
pytest
```

## Documentation

- Update documentation for any changes to the API or functionality.
- Keep the README up to date.

## Versioning

We use [Semantic Versioning](https://semver.org/). Please ensure your changes are appropriately versioned.

## License

By contributing to Cursor Utils, you agree that your contributions will be licensed under the project's MIT License. 