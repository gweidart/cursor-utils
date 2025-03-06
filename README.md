# Cursor Utils

A modern CLI utility toolkit for Cursor, built with strict typing and modern Python practices.

## Features

- Modern CLI interface using Click
- Rich terminal output
- Comprehensive diagnostic tools
- Fully type-annotated codebase
- Modern Python packaging

## Installation

```bash
# Using UV (recommended)
uv pip install cursor-utils

# Using pip
pip install cursor-utils
```

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

## Usage

```bash
cursor-utils --help
```

## Development

- Code style is enforced using `black`, `isort`, and `ruff`
- Type checking is done with `mypy`
- Testing is done with `pytest`

## Packaging and Release Process

### Building the Package

To build the package locally:

```bash
# Using the build module
python -m build

# Or using the provided script
python scripts/publish.py --test
```

### Bumping the Version

To bump the version before a release:

```bash
# Bump patch version (0.0.X)
python scripts/bump_version.py patch

# Bump minor version (0.X.0)
python scripts/bump_version.py minor

# Bump major version (X.0.0)
python scripts/bump_version.py major
```

### Publishing to PyPI

To publish to PyPI:

```bash
# Test PyPI
python scripts/publish.py --test

# Production PyPI
python scripts/publish.py
```

### GitHub Releases

1. Create a new tag: `git tag v0.1.0`
2. Push the tag: `git push origin v0.1.0`
3. Create a new release on GitHub with the tag
4. The GitHub Actions workflow will automatically build and publish the package to PyPI

## License

MIT License
