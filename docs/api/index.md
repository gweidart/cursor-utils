# API Reference

This section provides comprehensive information about the Cursor Utils API, its architecture, and how the different components interact.

## Architecture Overview

Cursor Utils follows a modular architecture with clear separation of concerns:

```
cursor_utils/
├── cli.py                # CLI entry point and command routing
├── commands/             # Command implementations
│   ├── web/              # Web search via Perplexity
│   ├── gemini/           # Google Gemini integration
│   ├── github/           # GitHub repository management
│   ├── repo/             # Repository analysis
│   ├── project/          # Local project analysis
│   ├── config/           # Configuration management
│   └── update/           # Self-update functionality
├── utils/                # Utility functions
│   └── file_rank_algo.py # File ranking algorithm
├── templates/            # Template files for code generation
├── errors.py             # Error handling system
├── types.py              # Type definitions
├── config.py             # Configuration management
└── version.py            # Version information
```

## Component Relationships

### Data Flow

1. **CLI Layer**: User input → Command routing → Command implementation
2. **Command Layer**: Command processing → API interaction → Result formatting
3. **Utility Layer**: Common functionality shared across commands

### Dependency Hierarchy

- `cli.py` depends on `commands/*`
- Each command module depends on:
  - `config.py` for configuration
  - `errors.py` for error handling
  - `types.py` for type definitions
  - `utils/*` for utility functions

## Core Modules

### CLI Module (`cli.py`)

The main entry point for the command-line interface, responsible for:

- Parsing command-line arguments
- Routing commands to their implementations
- Handling global flags and options
- Setting up the execution environment

```python
from cursor_utils import cli

# Run the CLI
cli.main()
```

### Commands Module (`commands/`)

Contains implementations for each command, with consistent structure:

- `__init__.py`: Exports the command entry point
- `command.py`: Defines the command interface with Click
- `actions.py`: Implements the command functionality
- `manager.py`: Handles command-specific state and dependencies

Each command follows the same pattern:

```python
# Command definition in command.py
@click.command()
@click.argument("argument")
@click.option("--option")
def command_name(argument, option):
    """Command description."""
    # Call to action implementation
```

### Configuration Module (`config.py`)

Manages configuration for the entire application:

- Loading and saving configuration
- Setting and retrieving configuration values
- Environment variable integration
- API key management

```python
from cursor_utils import config

# Get configuration
config = config.Config()
value = config.get("section.key", default="default")

# Set configuration
config.set("section.key", "value")
```

### Error Handling (`errors.py`)

Provides a robust error handling system:

- Standardized error classes
- Diagnostic information
- Error codes and messages
- Contextual error information

```python
from cursor_utils.errors import CursorUtilsError, ErrorCodes

try:
    # Operation that might fail
except Exception as e:
    raise CursorUtilsError(
        message="Operation failed",
        code=ErrorCodes.GENERAL_ERROR,
        causes=[str(e)],
        hint_stmt="Try this solution",
    )
```

### Type System (`types.py`)

Defines type definitions used throughout the application:

- TypedDict definitions for structured data
- Literal types for constrained values
- Union types for flexible interfaces
- Custom type aliases for better readability

```python
from cursor_utils.types import ConfigDict, ModelType

# Use type definitions
config: ConfigDict = {"version": "1.0.0", "settings": {"debug": False}}
model: ModelType = "sonar"
```

### Utilities Module (`utils/`)

Common utility functions and classes:

- File ranking algorithm
- File operations
- Network operations
- Text processing
- Output formatting

```python
from cursor_utils.utils.file_rank_algo import FileRanker

# Rank files by importance
ranker = FileRanker(type_weight=1.0, size_weight=0.8, time_weight=1.2)
ranked_files = ranker.rank_files(files)
```

## Command-Specific APIs

Each command provides its own API for programmatic use:

- [CLI Reference](cli.md): Command-line interface details
- [Commands Reference](commands.md): Command implementations
- [Configuration Reference](config.md): Configuration system
- [Utilities Reference](utils.md): Utility functions

## Error Handling

Cursor Utils uses a comprehensive error handling system:

- All errors inherit from `CursorUtilsError`
- Error codes are defined in `ErrorCodes` enum
- Errors include detailed diagnostic information
- Error messages provide helpful hints for resolution

## Extension Points

Cursor Utils can be extended in several ways:

1. **New Commands**: Add new command modules to `commands/`
2. **Custom Utilities**: Add new utility functions to `utils/`
3. **Additional Templates**: Add new templates to `templates/`
4. **API Integrations**: Add new API clients to interact with external services

## API Stability

The Cursor Utils API follows Semantic Versioning:

- Public APIs are stable within a major version
- Internal APIs may change between minor versions
- Experimental features are marked as such in documentation 