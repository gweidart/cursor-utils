# Commands Reference

This reference provides detailed information about each command in Cursor Utils, including implementation details, functionality, and usage examples.

## Command Structure

Each command in Cursor Utils follows a consistent structure:

```
commands/
├── <command_name>/
│   ├── __init__.py      # Exports the command
│   ├── command.py       # Click command definition
│   ├── actions.py       # Core functionality
│   ├── manager.py       # Command state management
│   └── types.py         # Command-specific types (optional)
```

This modular design ensures:
- Clear separation of concerns
- Consistent interfaces
- Testable components
- Maintainable code

## Web Command

The web command interfaces with Perplexity AI to provide real-time web search capabilities.

### Implementation

```python
# commands/web/command.py
@click.command()
@click.argument("query", nargs=-1, required=True)
@click.option(
    "--model",
    type=click.Choice(MODELS),
    help="Override the model specified in config",
)
def web(query, model=None, focus=None, mode=None):
    """Query Perplexity AI with your question."""
    # Implementation
```

### Core Functionality

The web command:
1. Validates the API key
2. Configures the Perplexity client
3. Streams the query to Perplexity AI
4. Processes and formats the streaming response
5. Displays the result in rich markdown format

### Usage Examples

```python
from cursor_utils.commands.web import actions

# Simple query
response = await actions.stream_query(
    query="Latest Python features",
    model="sonar",
    mode="copilot",
    search_focus="internet",
    api_key="your_api_key",
)

# Process streaming response
async for chunk in response:
    print(chunk["text"])
```

## Gemini Command

The Gemini command utilizes Google's Gemini API for AI-powered code generation and analysis.

### Implementation

```python
# commands/gemini/command.py
@click.command()
@click.argument("query", nargs=-1, required=True)
@click.option(
    "--append",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    multiple=True,
    help="File to include as context (can be used multiple times)",
)
def gemini(query, file=None, temp=None, max_tokens=None):
    """Query Google Gemini with your question."""
    # Implementation
```

### Core Functionality

The Gemini command:
1. Validates the API key
2. Loads any provided files as context
3. Configures the Gemini client with custom parameters
4. Processes the query with context
5. Displays the streamed response with formatting

### Usage Examples

```python
from cursor_utils.commands.gemini import actions

# Query with file context
response = await actions.stream_query_with_context(
    query="Explain this code",
    file_paths=["/path/to/file.py"],
    model="gemini-pro",
    temperature=0.7,
    max_tokens=2000,
    api_key="your_api_key",
)

# Process response
async for chunk in response:
    print(chunk["text"])
```

## Repository Analysis Command

The repo command analyzes GitHub repositories using a sophisticated file ranking algorithm.

### Implementation

```python
# commands/repo/command.py
@click.command()
@click.argument("repo_url", required=True)
@click.argument("query", nargs=-1, required=True)
def repo(repo_url, query, branch="main", include=None, max_size=2048):
    """Analyze a repository with context-aware answers."""
    # Implementation
```

### Core Functionality

The repo command:
1. Clones the repository
2. Ranks files using a priority algorithm
3. Filters and selects the most relevant files
4. Generates a report of the analysis
5. Sends the context and query to Gemini
6. Displays the response with rich formatting

### File Ranking Algorithm

The repository analysis uses a sophisticated file ranking algorithm:

```python
from cursor_utils.utils.file_rank_algo import FileRanker

ranker = FileRanker(
    type_weight=1.0,    # Importance of file type
    size_weight=0.8,    # Importance of file size
    time_weight=1.2,    # Importance of file creation time
)

ranked_files = ranker.rank_files(files)
```

### Usage Examples

```python
from cursor_utils.commands.repo import actions

# Analyze repository
response = await actions.analyze_repository(
    repo_url="https://github.com/user/repo",
    query="Explain the architecture",
)

print(response)
```

## Project Analysis Command

The project command analyzes local projects similar to the repo command.

### Implementation

```python
# commands/project/command.py
@click.command()
@click.argument("query", nargs=-1, required=True)
@click.option(
    "--path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=".",
    help="Path to the project directory",
)
@click.option(
    "--max-size",
    type=int,
    default=2048,
    help="Maximum size in MB to analyze",
)
def project(query, path=".", max_size=2048):
    """Analyze a local project with context-aware answers."""
    # Implementation
```

### Core Functionality

The project command:
1. Scans the local directory
2. Respects .gitignore patterns
3. Ranks files by importance
4. Selects the most relevant files
5. Generates a report of the analysis
6. Sends the context and query to Gemini
7. Displays the response with rich formatting

### Usage Examples

```python
from cursor_utils.commands.project import actions

# Analyze local project
response = await actions.analyze_project(
    project_path="/path/to/project",
    query="Document the API",
    max_size_mb=1024,
    type_weight=1.0,
    size_weight=0.8,
    time_weight=1.2,
)

print(response)
```

## GitHub Integration Command

The github command provides utilities for interacting with GitHub repositories.

### Implementation

```python
# commands/github/command.py
@click.group()
def github():
    """GitHub repository management commands."""
    pass

@github.command()
@click.argument("owner", required=True)
@click.argument("repo", required=True)
def analyze(owner, repo):
    """Analyze a GitHub repository."""
    # Implementation
    
@github.command()
@click.argument("owner", required=True)
@click.argument("repo", required=True)
def pr(owner, repo):
    """Generate PR description from commits."""
    # Implementation

@github.command()
@click.argument("issues", required=True)
@click.argument("repo", required=True)
def issues(repo_name):
    """Fetch remote repository issues"""

@github.command()
@click.argument("repo_name", required=True)
def setup(repo_name):
    """Set up a new GitHub repository with best practices."""
    # Implementation
```

### Core Functionality

The GitHub command provides:
1. Repository analysis
2. Pull request management
3. Issue management
4. Repository setup with best practices
5. Detailed reporting and statistics

### Usage Examples

```python
from cursor_utils.commands.github import actions

# Analyze repository
analysis = await actions.analyze_repository("owner", "repo")

# Generate PR description
pr_description = await actions.generate_pr_description("owner", "repo", pr_number=123)

# Set up new repository
result = await actions.setup_repository("new-repo", private=True, template="python")
```

## Configuration Command

The config command manages Cursor Utils configuration and API keys.

### Implementation

```python
# commands/config/command.py
@click.group()
def config():
    """Manage cursor-utils configuration."""
    pass

@config.command()
@click.option(
    "--show",
    is_flag=True,
    help="Skip interactive prompts and only show current status.",
)
def api_keys(non_interactive=False):
    """Configure API keys for enhanced features."""
    # Implementation
```

### Core Functionality

The config command:
1. Manages API keys securely
2. Displays configuration status
3. Sets and updates configuration values
4. Validates configuration integrity

### Configuration Structure

The configuration is stored in `~/.cursor-utils.yaml` with the following structure:

```yaml
version: "0.1.0"
settings:
  debug: false
  log_level: "INFO"
web:
  model: "sonar"
  mode: "copilot"
  search_focus: "internet"
gemini:
  model: "gemini-pro"
  max_output_tokens: 8000
  temperature: 0.7
github:
  token_source: "env"
  default_owner: ""
  default_repo: ""
```

### Usage Examples

```python
from cursor_utils.config import Config

# Get configuration
config = Config()

# Get a value
value = config.get("web.model")

# Set a value
config.set("web.mode", "concise")

# Save configuration
config.save()
```

## Update Command

The update command handles checking for and applying updates.

### Implementation

```python
# commands/update/command.py
@click.command()
@click.option(
    "--check",
    is_flag=True,
    help="Only check for updates, don't install them.",
)
def update(check_only=False):
    """Check for and apply updates."""
    # Implementation
```

### Core Functionality

The update command:
1. Checks for new versions of Cursor Utils
2. Compares with the current version
3. Backs up configuration
4. Applies updates using UV or pip
5. Verifies the installation
6. Migrates configuration if needed

### Usage Examples

```python
from cursor_utils.commands.update import actions

# Check for updates
latest_version = actions.check_for_updates()
if latest_version:
    # Apply updates
    success = actions.apply_update(latest_version)
```

## Installation Command

The install command handles initial setup and configuration.

### Implementation

```python
# commands/install/command.py
@click.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
)
def install(directory, force=False):
    """Install Cursor Utils in a directory."""
    # Implementation
```

### Core Functionality

The install command:
1. Creates necessary configuration files
2. Sets up templates
3. Guides through API key configuration
4. Initializes the environment for Cursor Utils
5. Validates the installation

### Usage Examples

```python
from cursor_utils.commands.install import actions

# Install in directory
success = actions.install_in_directory("/path/to/project", force=False)
```

## Extending Commands

Cursor Utils is designed to be extensible. You can add new commands by:

1. Creating a new directory in `commands/`
2. Implementing the command interface with Click
3. Adding the core functionality
4. Registering the command in `cli.py`

### Command Template

```python
# commands/new_command/command.py
import rich_click as click

@click.command()
@click.argument("arg", required=True)
@click.option("--option", help="Description of option")
def new_command(arg, option=None):
    """Description of the new command."""
    # Implementation
    
# Register in cli.py
from cursor_utils.commands.new_command import new_command
main.add_command(new_command)
``` 