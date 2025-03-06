# Extending Cursor Utils

This guide provides detailed information on how to extend Cursor Utils with new commands, extend existing functionality, and integrate with the core architecture.

## Command Architecture

Cursor Utils follows a modular command architecture that makes it easy to add new functionality:

```
cursor_utils/commands/
├── __init__.py           # Command registry
├── base.py               # Command base class
├── command_template/     # Template for new commands
│   ├── __init__.py
│   ├── command.py        # Command implementation
│   └── models.py         # Command data models
└── your_command/         # Your new command
    ├── __init__.py
    ├── command.py
    └── models.py
```

## Command Implementation Pattern

Each command in Cursor Utils follows a standard implementation pattern:

### 1. Command Class

The command class handles the main functionality and CLI interface:

```python
from typing import Optional, List, Dict, Any
from pathlib import Path
from rich.console import Console

from cursor_utils.commands.base import BaseCommand
from cursor_utils.config import Config
from .models import YourCommandOptions


class YourCommand(BaseCommand):
    """
    Your command description.
    
    This command handles [describe what your command does].
    """
    
    name = "your_command"  # Command name used in CLI
    description = "Description of your command"  # Used in help text
    
    def __init__(self) -> None:
        """Initialize your command."""
        super().__init__()
        self.console = Console()
        self.config = Config()
    
    def setup_parser(self, parser) -> None:
        """
        Configure the command line argument parser.
        
        Args:
            parser: The argument parser to configure
        """
        # Add command-specific arguments
        parser.add_argument(
            "--option",
            help="Description of option",
            default="default_value",
        )
        
        # Add subcommands if needed
        subparsers = parser.add_subparsers(dest="subcommand")
        
        # Example subcommand
        sub_cmd = subparsers.add_parser("sub", help="Subcommand help")
        sub_cmd.add_argument("--sub-option", help="Subcommand option")
    
    def run(self, options: Dict[str, Any]) -> int:
        """
        Run the command with the provided options.
        
        Args:
            options: Command options parsed from CLI arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        # Convert raw options to typed options model
        opts = YourCommandOptions(**options)
        
        # Implement command logic
        try:
            # Your command implementation
            self.console.print(f"[bold green]Running your command with {opts}[/]")
            
            # Handle subcommands
            if opts.subcommand == "sub":
                return self._handle_subcommand(opts)
            
            # Main command logic
            result = self._process(opts)
            
            self.console.print("[bold green]Command completed successfully![/]")
            return 0
        except Exception as e:
            self.console.print(f"[bold red]Error executing command: {str(e)}[/]")
            if self.config.get("settings.debug", False):
                import traceback
                self.console.print(traceback.format_exc())
            return 1
    
    def _process(self, options: YourCommandOptions) -> Any:
        """
        Internal method for processing the command.
        
        Args:
            options: Command options
            
        Returns:
            Command result
        """
        # Implement your command's core functionality
        pass
    
    def _handle_subcommand(self, options: YourCommandOptions) -> int:
        """
        Handle subcommand execution.
        
        Args:
            options: Command options
            
        Returns:
            Exit code
        """
        # Implement subcommand logic
        self.console.print(f"Running subcommand with {options.sub_option}")
        return 0
```

### 2. Command Options Model

Define a Pydantic model to represent the command's options:

```python
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class SubcommandType(str, Enum):
    """Subcommand types."""
    
    SUB = "sub"
    # Add other subcommands


class YourCommandOptions(BaseModel):
    """Options for your command."""
    
    # Basic options
    option: str = Field(
        default="default_value",
        description="Description of the option",
    )
    
    # Subcommand handling
    subcommand: Optional[SubcommandType] = Field(
        default=None,
        description="Subcommand to execute",
    )
    
    # Subcommand options
    sub_option: Optional[str] = Field(
        default=None,
        description="Option for sub subcommand",
    )
    
    class Config:
        """Pydantic configuration."""
        
        extra = "ignore"  # Ignore extra fields from CLI parser
```

### 3. Command Registration

Register your command in `cursor_utils/commands/__init__.py`:

```python
from .your_command.command import YourCommand

# Register commands
COMMANDS = {
    # ... existing commands ...
    "your_command": YourCommand,
}
```

## Testing Your Command

Create tests for your command in the `tests/commands/` directory:

```python
import pytest
from unittest.mock import patch, MagicMock

from cursor_utils.commands.your_command.command import YourCommand
from cursor_utils.commands.your_command.models import YourCommandOptions


class TestYourCommand:
    """Test suite for YourCommand."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.command = YourCommand()
    
    def test_initialization(self):
        """Test command initialization."""
        assert self.command.name == "your_command"
        assert self.command.description
    
    def test_run_basic(self):
        """Test basic command execution."""
        options = {"option": "test_value"}
        
        with patch.object(self.command, '_process') as mock_process:
            result = self.command.run(options)
            
            assert result == 0
            mock_process.assert_called_once()
            
    def test_subcommand(self):
        """Test subcommand execution."""
        options = {
            "subcommand": "sub",
            "sub_option": "test_value"
        }
        
        with patch.object(self.command, '_handle_subcommand') as mock_handler:
            mock_handler.return_value = 0
            result = self.command.run(options)
            
            assert result == 0
            mock_handler.assert_called_once()
    
    def test_error_handling(self):
        """Test error handling during command execution."""
        options = {"option": "test_value"}
        
        with patch.object(self.command, '_process') as mock_process:
            mock_process.side_effect = ValueError("Test error")
            
            result = self.command.run(options)
            
            assert result != 0
```

## Command Template

Cursor Utils includes a template for new commands that you can copy to get started quickly:

```bash
cp -r cursor_utils/commands/command_template cursor_utils/commands/your_command
```

Then edit the files to implement your command.

## Integration with Core Components

### Configuration Integration

To integrate with the configuration system:

```python
from cursor_utils.config import Config

# In your command class
def __init__(self) -> None:
    super().__init__()
    self.config = Config()
    
    # Access configuration values
    self.debug = self.config.get("settings.debug", False)
    
    # Access command-specific configuration
    self.cmd_config = self.config.get(f"{self.name}", {})
    
    # Set default configuration
    if f"{self.name}" not in self.config.config:
        self.config.set(f"{self.name}", {
            "option1": "default1",
            "option2": "default2"
        })
        self.config.save()
```

### API Key Management

To integrate with the API key management system:

```python
from cursor_utils.config import Config, APIKeyType

# In your command class
def __init__(self) -> None:
    super().__init__()
    self.config = Config()
    
    # Define a new API key type if needed
    # First update cursor_utils/config.py to add your API key type
    # class APIKeyType(str, Enum):
    #     ...
    #     YOUR_API = "YOUR_API_KEY"
    
    # Get an API key
    self.api_key = self.config.get_api_key(APIKeyType.YOUR_API)
    
    # Validate the API key
    if not self.api_key or not self.config.validate_api_key(APIKeyType.YOUR_API, self.api_key):
        raise ValueError("Invalid or missing API key. Please set it with 'cursor-utils config api_keys'")
```

### Logging Integration

To integrate with the logging system:

```python
import logging
from cursor_utils.utils.logging import get_logger

# In your command class
def __init__(self) -> None:
    super().__init__()
    
    # Get a logger for your command
    self.logger = get_logger(self.name)
    
    # Log messages
    self.logger.debug("Debug message")
    self.logger.info("Info message")
    self.logger.warning("Warning message")
    self.logger.error("Error message")
```

### Progress Display

To display progress for long-running operations:

```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

# In your command method
def _process(self, options: YourCommandOptions) -> Any:
    """Process the command with a progress bar."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=self.console,
    ) as progress:
        # Create a task
        task = progress.add_task("Processing...", total=100)
        
        # Update progress
        for i in range(100):
            # Do some work
            time.sleep(0.1)
            
            # Update progress
            progress.update(task, advance=1)
        
        # Mark task as complete
        progress.update(task, completed=100)
```

## Advanced Integration Patterns

### Web API Integration

For commands that interact with web APIs:

```python
import httpx
from cursor_utils.utils.http import create_client

# In your command method
async def _fetch_data(self, url: str, api_key: str) -> Dict[str, Any]:
    """Fetch data from a web API."""
    async with create_client() as client:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
```

### File System Operations

For commands that interact with the file system:

```python
from pathlib import Path
import json

# In your command method
def _save_results(self, results: Dict[str, Any], output_path: Path) -> None:
    """Save results to a file."""
    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write results
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    self.console.print(f"[green]Results saved to {output_path}[/]")
```

### Command Composition

For commands that use other commands:

```python
from cursor_utils.commands import COMMANDS

# In your command method
def _process(self, options: YourCommandOptions) -> Any:
    """Process using other commands."""
    # Instantiate another command
    other_cmd = COMMANDS["other_command"]()
    
    # Prepare options for the other command
    other_options = {
        "option1": "value1",
        "option2": "value2",
    }
    
    # Run the other command
    result = other_cmd.run(other_options)
    
    # Check result
    if result != 0:
        raise ValueError("Failed to execute other command")
    
    # Continue with your command
    return "Success"
```

## Best Practices for Command Development

1. **Follow the Command Pattern**: Use the established command pattern for consistency
2. **Use Type Annotations**: Always use proper type annotations for better maintainability
3. **Document Thoroughly**: Document your command's purpose, options, and usage
4. **Handle Errors Gracefully**: Catch and handle exceptions, provide useful error messages
5. **Use Configuration**: Store command-specific configuration in the config system
6. **Write Tests**: Write comprehensive tests for your command
7. **Support Debug Mode**: Add detailed logging when debug mode is enabled
8. **Be User-Friendly**: Provide helpful error messages and progress information
9. **Support Dry Run**: For destructive operations, add a dry-run option
10. **Validate Input**: Validate input options before processing
11. **Use Rich for Output**: Use Rich for attractive console output
12. **Handle Signal Interrupts**: Gracefully handle Ctrl+C and other interrupts

## Command Line Interface Guidelines

When extending the CLI:

1. **Consistent Naming**: Use kebab-case for subcommand and option names
2. **Descriptive Help**: Provide clear help text for all options
3. **Sensible Defaults**: Set reasonable default values for options
4. **Short and Long Options**: Support both short (-o) and long (--option) forms
5. **Group Related Options**: Use argument groups to organize options
6. **Validate Early**: Validate command line arguments as early as possible
7. **Exit Codes**: Return appropriate exit codes (0 for success, non-zero for failure)

## Plugin System

For more advanced extensions, Cursor Utils supports a plugin system:

```python
from cursor_utils.plugins import register_plugin, PluginMeta

# Define your plugin
class YourPlugin(metaclass=PluginMeta):
    """Your plugin description."""
    
    name = "your_plugin"
    version = "0.1.0"
    
    def __init__(self):
        """Initialize your plugin."""
        pass
    
    def initialize(self):
        """Initialize the plugin when Cursor Utils starts."""
        pass
    
    def get_commands(self):
        """Return commands provided by this plugin."""
        from .commands import YourCommand
        return {"your_command": YourCommand}
    
    def cleanup(self):
        """Clean up resources when Cursor Utils exits."""
        pass

# Register your plugin
register_plugin(YourPlugin)
```

## Event System

Cursor Utils includes an event system that allows commands to communicate:

```python
from cursor_utils.events import EventBus, Event

# Define an event
class YourEvent(Event):
    """Event fired when something happens."""
    
    def __init__(self, data: Dict[str, Any]):
        """Initialize the event."""
        self.data = data

# In your command
def __init__(self) -> None:
    super().__init__()
    
    # Get the event bus
    self.event_bus = EventBus()
    
    # Register an event handler
    self.event_bus.subscribe("other_event", self._handle_event)
    
def _handle_event(self, event: Event) -> None:
    """Handle an event."""
    self.logger.debug(f"Received event: {event}")
    
def _process(self, options: YourCommandOptions) -> Any:
    """Process and fire an event."""
    # Do processing
    
    # Fire an event
    self.event_bus.publish(YourEvent({"result": "success"}))
```

## Packaging Your Extension

You can package your extension as a separate Python package:

```
your_cursor_extension/
├── pyproject.toml
├── README.md
├── src/
│   └── your_cursor_extension/
│       ├── __init__.py
│       ├── plugin.py       # Plugin definition
│       └── commands/       # Your commands
└── tests/
```

Example `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "your-cursor-extension"
version = "0.1.0"
description = "Your extension for Cursor Utils"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
dependencies = [
    "cursor-utils>=0.1.0",
]
requires-python = ">=3.8"

[project.entry_points.cursor_utils_plugins]
your_plugin = "your_cursor_extension.plugin:YourPlugin"
```

## Cookiecutter Template

Cursor Utils provides a Cookiecutter template for creating new commands and extensions:

```bash
pip install cookiecutter
cookiecutter gh:cursor-utils/extension-template
```

This will guide you through creating a new extension with all the necessary files and structure.

## Documentation

Always document your extension thoroughly:

1. **Command Help**: Update the command's `description` and argument help text
2. **README**: Create a README.md for your extension
3. **Examples**: Provide usage examples
4. **Integration**: Document how your extension integrates with other commands
5. **Configuration**: Document configuration options

## Contributing Back

If your extension would be useful to others, consider contributing it back to Cursor Utils:

1. Fork the Cursor Utils repository
2. Add your command or extension
3. Add tests and documentation
4. Submit a pull request

See the [Contributing Guide](../contributing.md) for more information. 