# Contributing to this project

Thank you for your interest in contributing to this project! Here are some guidelines to help you get started.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to contribute

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request

## Development setup

1. Clone the repository
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

## Testing

Run tests with pytest:
```bash
pytest
```

## Code style

This project uses:
- black for code formatting
- isort for import sorting
- ruff for linting
- pyright for type checking

Pre-commit hooks will automatically check your code before committing. 