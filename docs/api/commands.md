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

## Standardized Error Handling

All commands use standardized error handling through the `safe_execute` and `safe_execute_sync` decorators:

```python
# For async commands
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.utils.command_helpers import safe_execute

@safe_execute(WebError, ErrorCodes.WEB_QUERY_ERROR)
async def web_action(query: str) -> None:
    # Command implementation
    pass

# For synchronous commands
from cursor_utils.errors import ErrorCodes, ConfigError
from cursor_utils.utils.command_helpers import safe_execute_sync

@safe_execute_sync(ConfigError, ErrorCodes.CONFIG_FILE_ERROR)
def config_action() -> None:
    # Command implementation
    pass
```

This approach ensures:
- Consistent error messages
- Proper error categorization
- Helpful diagnostic information
- Clear suggestions for resolution

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
1. Validates the API key using `get_api_key`
2. Configures the Perplexity client with appropriate settings
3. Streams the query to Perplexity AI
4. Formats and displays the response

### Error Handling

```python
# commands/web/actions.py
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.utils.command_helpers import safe_execute
from cursor_utils.utils.api_helpers import get_api_key

@safe_execute(WebError, ErrorCodes.WEB_QUERY_ERROR)
async def execute_web(query: str, model: Optional[str] = None, focus: Optional[str] = None, mode: Optional[str] = None) -> None:
    # Get API key
    api_key = get_api_key(APIKeyType.PERPLEXITY, "PERPLEXITY_API_KEY")
    
    # Configure client
    client = PerplexityClient(api_key=api_key)
    
    # Execute query
    await client.query(query, model=model, focus=focus, mode=mode)
```

## Gemini Command

The Gemini command leverages Google's Gemini AI models for code generation and analysis.

### Implementation

```python
# commands/gemini/command.py
@click.command()
@click.argument("query", nargs=-1, required=True)
@click.option(
    "--append", "-a",
    help="Append file content to the query",
)
def gemini(query, append=None):
    """Query Google Gemini with your question."""
    # Implementation
```

### Core Functionality

The Gemini command:
1. Validates the API key using `get_api_key`
2. Loads file content if specified with `--append`
3. Configures the Gemini client with appropriate settings
4. Sends the query to Gemini AI
5. Formats and displays the response

### Error Handling

```python
# commands/gemini/actions.py
from cursor_utils.errors import ErrorCodes, GeminiError
from cursor_utils.utils.command_helpers import safe_execute
from cursor_utils.utils.api_helpers import get_api_key

@safe_execute(GeminiError, ErrorCodes.GEMINI_API_ERROR)
async def execute_gemini(query: str, file_path: Optional[str] = None) -> None:
    # Get API key
    api_key = get_api_key(APIKeyType.GEMINI, "GEMINI_API_KEY")
    
    # Load file content if specified
    file_content = None
    if file_path:
        with open(file_path, "r") as f:
            file_content = f.read()
    
    # Configure client
    client = GeminiClient(api_key=api_key)
    
    # Execute query
    await client.query(query, context=file_content)
```

## Repo Command

The repo command analyzes GitHub repositories to provide intelligent insights.

### Implementation

```python
# commands/repo/command.py
@click.command()
@click.argument("repo_url", required=True)
@click.argument("query", nargs=-1, required=True)
@click.option(
    "--branch",
    help="Specify a branch to analyze",
)
def repo(repo_url, query, branch=None):
    """Analyze a GitHub repository."""
    # Implementation
```

### Core Functionality

The repo command:
1. Clones the repository to a temporary directory
2. Analyzes the repository structure
3. Ranks files by importance using `FileRanker`
4. Sends the query and ranked files to Gemini AI
5. Formats and displays the response

### Error Handling

```python
# commands/repo/actions.py
from cursor_utils.errors import ErrorCodes, RepoError
from cursor_utils.utils.command_helpers import safe_execute
from cursor_utils.utils.file_rank_algo import FileRanker

@safe_execute(RepoError, ErrorCodes.REPO_CLONE_ERROR)
async def execute_repo(repo_url: str, query: str, branch: Optional[str] = None) -> None:
    # Clone repository
    repo_path = await clone_repository(repo_url, branch)
    
    # Analyze repository
    files = analyze_repository(repo_path)
    
    # Rank files
    ranker = FileRanker()
    ranked_files = ranker.rank_files(files)
    
    # Execute query
    await execute_query(query, ranked_files)
```

## Project Command

The project command analyzes local projects to provide intelligent insights.

### Implementation

```python
# commands/project/command.py
@click.command()
@click.argument("query", nargs=-1, required=True)
@click.option(
    "--path",
    help="Specify a project path to analyze",
)
def project(query, path=None):
    """Analyze a local project."""
    # Implementation
```

### Core Functionality

The project command:
1. Analyzes the project structure
2. Ranks files by importance using `FileRanker`
3. Sends the query and ranked files to Gemini AI
4. Formats and displays the response

### Error Handling

```python
# commands/project/actions.py
from cursor_utils.errors import ErrorCodes, ProjectError
from cursor_utils.utils.command_helpers import safe_execute
from cursor_utils.utils.file_rank_algo import FileRanker

@safe_execute(ProjectError, ErrorCodes.PROJECT_ANALYZE_ERROR)
async def execute_project(query: str, path: Optional[str] = None) -> None:
    # Determine project path
    project_path = path or os.getcwd()
    
    # Analyze project
    files = analyze_project(project_path)
    
    # Rank files
    ranker = FileRanker()
    ranked_files = ranker.rank_files(files)
    
    # Execute query
    await execute_query(query, ranked_files)
```

## GitHub Command

The GitHub command provides advanced GitHub repository management capabilities.

### Implementation

```python
# commands/github/command.py
@click.group()
def github():
    """GitHub repository management."""
    pass

@github.command()
@click.argument("owner_repo", required=True)
def analyze(owner_repo):
    """Analyze a GitHub repository."""
    # Implementation

@github.command()
@click.argument("name", required=True)
@click.option(
    "--private/--public",
    default=True,
    help="Create a private repository",
)
def setup(name, private):
    """Set up a new GitHub repository."""
    # Implementation
```

### Core Functionality

The GitHub command:
1. Validates the GitHub token using `get_api_key`
2. Performs the requested GitHub operation
3. Formats and displays the response

### Error Handling

```python
# commands/github/actions.py
from cursor_utils.errors import ErrorCodes, GitHubError
from cursor_utils.utils.command_helpers import safe_execute
from cursor_utils.utils.api_helpers import get_api_key

@safe_execute(GitHubError, ErrorCodes.GITHUB_API_ERROR)
async def execute_github_analyze(owner_repo: str) -> None:
    # Get GitHub token
    token = get_api_key(APIKeyType.GITHUB, "GITHUB_TOKEN")
    
    # Configure client
    client = GitHubClient(token=token)
    
    # Execute analysis
    await client.analyze_repository(owner_repo)
```

## Config Command

The config command manages settings and API keys.

### Implementation

```python
# commands/config/command.py
@click.group()
def config():
    """Configuration management."""
    pass

@config.command()
@click.option(
    "--show",
    is_flag=True,
    help="Show current configuration",
)
def api_keys(show):
    """Manage API keys."""
    # Implementation
```

### Core Functionality

The config command:
1. Loads and validates configuration
2. Performs the requested configuration operation
3. Saves configuration changes

### Error Handling

```python
# commands/config/actions.py
from cursor_utils.errors import ErrorCodes, ConfigError
from cursor_utils.utils.command_helpers import safe_execute_sync
from cursor_utils.utils.config_helpers import load_config, save_config

@safe_execute_sync(ConfigError, ErrorCodes.CONFIG_FILE_ERROR)
def execute_config_api_keys(show: bool = False) -> None:
    # Load configuration
    config = load_config(manager, "api_keys")
    
    # Show configuration if requested
    if show:
        display_config(config)
        return
    
    # Update configuration
    updated_config = update_api_keys(config)
    
    # Save configuration
    save_config(manager, "api_keys", updated_config)
```

## Install Command

The install command initializes Cursor Utils in a project.

### Implementation

```python
# commands/install/command.py
@click.command()
@click.option(
    "--force",
    is_flag=True,
    help="Force installation even if already installed",
)
def install(force):
    """Initialize Cursor Utils in the current directory."""
    # Implementation
```

### Core Functionality

The install command:
1. Checks if Cursor Utils is already installed
2. Creates necessary configuration files
3. Sets up default templates
4. Guides the user through API key configuration

### Error Handling

```python
# commands/install/actions.py
from cursor_utils.errors import ErrorCodes, InstallError
from cursor_utils.utils.command_helpers import safe_execute_sync

@safe_execute_sync(InstallError, ErrorCodes.INSTALL_ALREADY_INSTALLED)
def execute_install(force: bool = False) -> None:
    # Check if already installed
    if is_installed() and not force:
        raise ValueError("Cursor Utils is already installed")
    
    # Create configuration files
    create_config_files()
    
    # Set up templates
    setup_templates()
    
    # Guide through API key configuration
    configure_api_keys()
```

## Update Command

The update command updates Cursor Utils to the latest version.

### Implementation

```python
# commands/update/command.py
@click.command()
def update():
    """Update Cursor Utils to the latest version."""
    # Implementation
```

### Core Functionality

The update command:
1. Checks for new versions
2. Backs up configuration
3. Updates the package
4. Migrates configuration if needed
5. Verifies the updated installation

### Error Handling

```python
# commands/update/actions.py
from cursor_utils.errors import ErrorCodes, UpdateError
from cursor_utils.utils.command_helpers import safe_execute_sync

@safe_execute_sync(UpdateError, ErrorCodes.UPDATE_FAILED)
def execute_update() -> None:
    # Check for new versions
    new_version = check_for_updates()
    
    # Back up configuration
    backup_configuration()
    
    # Update package
    update_package(new_version)
    
    # Migrate configuration
    migrate_configuration()
    
    # Verify installation
    verify_installation()
```

## Best Practices for Command Implementation

When implementing commands:

1. **Use standardized error handling**:
   - Use `safe_execute` for async functions
   - Use `safe_execute_sync` for synchronous functions
   - Provide appropriate error classes and codes

2. **Centralize API key management**:
   - Use `get_api_key` to retrieve API keys
   - Use `validate_api_key` to validate API keys
   - Handle missing or invalid keys gracefully

3. **Simplify configuration handling**:
   - Use `ensure_config` to validate and apply defaults
   - Use `load_config` to load configuration sections
   - Use `save_config` to save configuration changes

4. **Follow consistent command structure**:
   - Define command interface in `command.py`
   - Implement core functionality in `actions.py`
   - Manage command state in `manager.py`
   - Export command from `__init__.py` 