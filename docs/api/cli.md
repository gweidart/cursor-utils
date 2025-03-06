# CLI Reference

This reference provides comprehensive details about the Cursor Utils CLI interface, implementation, and usage patterns.

## CLI Architecture

The Cursor Utils CLI is built using [Rich Click](https://github.com/ewels/rich-click), an enhanced version of [Click](https://click.palletsprojects.com/) that provides rich formatting and improved help output. The CLI follows a multi-level command structure with a main entry point and multiple nested subcommands.

### Command Structure

```
cursor-utils
├── web             # Perplexity web search
├── gemini          # Google Gemini integration
├── repo            # Repository analysis
├── project         # Local project analysis
├── github          # GitHub integration
│   ├── analyze     # Repository analysis
│   ├── clone       # Clone repository
│   ├── issues      # Issue management
│   ├── pr          # Pull request management
│   └── setup       # Repository setup
├── config          # Configuration management
│   └── api_keys    # API key management
├── update          # Self update
└── install         # Installation and setup
```

## Implementation Details

The CLI is implemented in `cursor_utils/cli.py` as a Click command group. Each subcommand is registered using the `add_command` method:

```python
import rich_click as click
from rich.console import Console
from rich.traceback import install as install_rich_traceback

from cursor_utils.commands import (
    config, gemini, github, install, project, repo, update, web
)

# Install rich traceback handler
install_rich_traceback()

# Initialize rich console
console = Console()

@click.group()
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show the version and exit.",
)
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Enable debug mode.",
)
@click.pass_context
def main(ctx, debug):
    """Cursor Utils CLI tool."""
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    if debug:
        console.print("[#af87ff]Debug mode enabled[/]")

# Register commands
main.add_command(config)
main.add_command(gemini)
main.add_command(github)
main.add_command(install)
main.add_command(project)
main.add_command(repo)
main.add_command(update)
main.add_command(web)
```

Each command is implemented in its own module within the `commands` package, following a consistent pattern:

1. Command interface defined with `rich_click`
2. Implementation in an actions module
3. State management in a manager module

## Global Options

These options are available for all commands:

| Option | Type | Description |
|--------|------|-------------|
| `--version` | Flag | Show version information and exit |
| `--debug/--no-debug` | Boolean | Enable or disable debug mode |
| `--help` | Flag | Show help information and exit |

## Command-Specific Options

### Web Command

```bash
cursor-utils web [OPTIONS] QUERY
```
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--model` | Choice | `sonar` | Perplexity model to use |

Config options can be fine tuned and set within cursor-utils.yaml

| Config Option | Type | Default | Description |
|--------|------|---------|-------------|
| `model` | Choice | `sonar` | Perplexity model to use |
| `focus` | Choice | `internet` | Search focus |
| `mode` | Choice | `copilot` | Response mode |

### Gemini Command

```bash
cursor-utils gemini [OPTIONS] [QUERY]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--append` | Path | None | File to append as context |

Config options can be fine tuned and set wit cursor-utils.yaml.
| Config Option | Type | Default | Description |
|--------|------|---------|-------------|
| `temp` | Float | `0.7` | Temperature for generation |
| `top-p` | Float | `0.95` | Top-p sampling parameter |
| `max-tokens` | Integer | `8000` | Maximum tokens to generate |

### Repo Command

```bash
cursor-utils repo [REPO_URL] [QUERY]
```

### Project Command

```bash
cursor-utils project [QUERY]
```

### GitHub Command

```bash
cursor-utils github [OPTIONS] [COMMAND] [ARGS]
```

Multiple subcommands available - see `cursor-utils github --help` for a complete list.

### Config Command

```bash
cursor-utils config [OPTIONS]
```

| Subcommand | Description |
|------------|-------------|
| `show` | Skip interactive prompts & Show current configuration |

## Exit Codes

The CLI returns the following exit codes:

| Exit Code | Description |
|-----------|-------------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid command usage |
| 130 | Operation cancelled by user |

## Environment Variables

The CLI checks for the following environment variables:

| Variable | Description |
|----------|-------------|
| `PERPLEXITY_API_KEY` | API key for Perplexity AI |
| `GEMINI_API_KEY` | API key for Google Gemini |
| `GITHUB_TOKEN` | GitHub personal access token |

## Example Usage

### Basic Examples

```bash
# Show help
cursor-utils --help
```

```bash
# Show version
cursor-utils --version
```

```bash
# Enable debug mode
cursor-utils --debug web "Python async/await"
```

### Web Search Examples

```bash
# Academic focus using alternative model
Ask Perplexity what is the latest research on quantum computing 
```

```bash
# Writing assistance
Ask Perplexity to assist you in writing a SQL query to find duplicate records 
```

```bash
# Mathematical calculations
Ask Perplexity to solve the equation x^2 - 4x + 4 = 0
```

### Gemini Examples

```bash
# Basic query
Ask Gemini to explain the principles of clean code architecture
```

```bash
# With file context
Ask Gemini to optimize the following: --append ./src/slow_function.py function for performance 
```

```bash
# Context-aware request
Ask Gemini to analyze the current module and suggest improvements
```


### Repository Analysis Examples

```bash
# Analyze repository
Use cursor-utils repo https://github.com/user/repo to review code architecture
```

```bash
# Focus on specific directories
Use cursor-utils repo https://github.com/user/repo to perform a ecurity review
```

```bash
# Analyze specific branch
Use cursor-utils repo https://github.com/user/repo to generate API documentation
```

### GitHub Integration Examples

```bash
# Repository analysis
Use cursor-utils github analyze fastapi/fastapi
```

```bash
# PR generation
Use cursor-utils github to create a pull request for my current branch with a comprehensive description
```

```bash
# Issue summary
Use cursor-utils github to summarize open issues in the tensorflow/tensorflow repository
```

## Advanced Usage

### Piping and Redirection

The CLI supports standard Unix piping and redirection:

```bash
# Save output to file
Use cursor-utils repo https://github.com/user/repo to get an architectural overview and save the resulting output to a new file named architecture.md

# Pipe through grep
Use cursor-utils github issues user/repo | grep "bug"
```

### Command Composition

Commands can be composed for advanced workflows:

```bash
# Generate report from web search
Ask Perplexity about the latest security best practices, save the resulting output to a new file named security_report.txt

# Use report as context for Gemini
Ask Gemini to review --append ./src/slow_function.py
 and apply the security practices to my code
```

## Error Handling

The CLI includes comprehensive error handling with rich output:

- Detailed error messages with error codes
- Contextual hints for resolving issues
- Stack traces in debug mode
- Color-coded output for different error types 