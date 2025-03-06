# Utilities Reference

This reference provides documentation on the utility modules used in Cursor Utils, focusing on the actual implementations present in the codebase.

## Utility Architecture

Cursor Utils has a comprehensive utility architecture with several key modules:

```
cursor_utils/utils/
├── __init__.py         # Exports utility functions
├── command_helpers.py  # Standardized error handling
├── api_helpers.py      # API key management
├── config_helpers.py   # Configuration utilities
└── file_rank_algo.py   # Repository analysis algorithm
```

The `__init__.py` file exports the key utility functions and classes:

```python
from cursor_utils.utils.api_helpers import get_api_key, validate_api_key
from cursor_utils.utils.command_helpers import safe_execute, safe_execute_sync
from cursor_utils.utils.config_helpers import ensure_config, load_config, save_config
from cursor_utils.utils.file_rank_algo import FileRanker

__all__ = [
    "get_api_key",
    "validate_api_key",
    "safe_execute",
    "safe_execute_sync",
    "ensure_config",
    "load_config",
    "save_config",
    "FileRanker",
]
```

## Command Helpers

The command helpers module (`cursor_utils/utils/command_helpers.py`) provides standardized error handling for commands.

### Key Functions

#### safe_execute

```python
def safe_execute(
    error_class: Type[CursorUtilsError],
    error_code: ErrorCodes,
    message: Optional[str] = None,
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    """
    Decorator for async functions that provides standardized error handling.
    
    Args:
        error_class: The error class to use for exceptions
        error_code: The error code to use for exceptions
        message: Optional custom error message
        
    Returns:
        Decorated function with standardized error handling
    """
```

This decorator:
1. Wraps an async function with standardized error handling
2. Catches exceptions and converts them to appropriate error types
3. Provides consistent error messages and diagnostic information

#### safe_execute_sync

```python
def safe_execute_sync(
    error_class: Type[CursorUtilsError],
    error_code: ErrorCodes,
    message: Optional[str] = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for synchronous functions that provides standardized error handling.
    
    Args:
        error_class: The error class to use for exceptions
        error_code: The error code to use for exceptions
        message: Optional custom error message
        
    Returns:
        Decorated function with standardized error handling
    """
```

This decorator:
1. Wraps a synchronous function with standardized error handling
2. Catches exceptions and converts them to appropriate error types
3. Provides consistent error messages and diagnostic information

#### handle_command_error

```python
def handle_command_error(
    error: Exception,
    error_class: Type[CursorUtilsError],
    error_code: ErrorCodes,
    message: Optional[str] = None,
) -> NoReturn:
    """
    Handle command errors with standardized error reporting.
    
    Args:
        error: The original exception
        error_class: The error class to use
        error_code: The error code to use
        message: Optional custom error message
        
    Raises:
        CursorUtilsError: Standardized error with diagnostic information
    """
```

This function:
1. Converts exceptions to standardized error types
2. Adds diagnostic information and hints
3. Provides consistent error reporting

### Usage Example

```python
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.utils.command_helpers import safe_execute

@safe_execute(WebError, ErrorCodes.WEB_QUERY_ERROR)
async def web_command(query: str) -> None:
    # Command implementation that might raise exceptions
    response = await api_client.query(query)
    if not response:
        raise ValueError("Empty response from API")
    await process_response(response)
```

## API Helpers

The API helpers module (`cursor_utils/utils/api_helpers.py`) provides centralized API key management.

### Key Functions

#### get_api_key

```python
def get_api_key(key_type: APIKeyType, env_var: str) -> str:
    """
    Get API key with standardized error handling.
    
    Args:
        key_type: The type of API key to get
        env_var: The environment variable name for the API key
        
    Returns:
        The API key string
        
    Raises:
        WebError: If the API key is not found or invalid
    """
```

This function:
1. Checks environment variables for API keys
2. Falls back to configuration file if not found in environment
3. Validates the API key format
4. Provides helpful error messages if the key is missing or invalid

#### validate_api_key

```python
def validate_api_key(api_key: str, key_type: APIKeyType, env_var: str) -> None:
    """
    Validate API key with standardized error handling.
    
    Args:
        api_key: The API key to validate
        key_type: The type of API key
        env_var: The environment variable name for the API key
        
    Raises:
        WebError: If the API key is invalid
    """
```

This function:
1. Validates the API key format
2. Checks for common issues like empty keys or placeholder values
3. Provides helpful error messages for invalid keys

### Usage Example

```python
from cursor_utils.config import APIKeyType
from cursor_utils.utils.api_helpers import get_api_key

# Get Perplexity API key
api_key = get_api_key(APIKeyType.PERPLEXITY, "PERPLEXITY_API_KEY")

# Use the API key
client = PerplexityClient(api_key=api_key)
```

## Config Helpers

The config helpers module (`cursor_utils/utils/config_helpers.py`) provides simplified configuration handling.

### Key Functions

#### ensure_config

```python
def ensure_config(
    manager: ConfigManager,
    required_keys: list[str],
    defaults: dict[str, Any],
) -> dict[str, Any]:
    """
    Ensure configuration exists with standardized error handling.
    
    Args:
        manager: The configuration manager
        required_keys: List of required configuration keys
        defaults: Default values for configuration keys
        
    Returns:
        Configuration dictionary with all required keys
        
    Raises:
        ConfigError: If configuration cannot be loaded or validated
    """
```

This function:
1. Loads configuration from the manager
2. Validates that all required keys are present
3. Applies default values for missing keys
4. Provides helpful error messages for configuration issues

#### load_config

```python
def load_config(
    manager: ConfigManager,
    section: str,
) -> dict[str, Any]:
    """
    Load configuration with standardized error handling.
    
    Args:
        manager: The configuration manager
        section: The configuration section to load
        
    Returns:
        Configuration dictionary for the specified section
        
    Raises:
        ConfigError: If configuration cannot be loaded
    """
```

This function:
1. Loads configuration for a specific section
2. Handles missing sections gracefully
3. Provides helpful error messages for configuration issues

#### save_config

```python
def save_config(
    manager: ConfigManager,
    section: str,
    config: dict[str, Any],
) -> None:
    """
    Save configuration with standardized error handling.
    
    Args:
        manager: The configuration manager
        section: The configuration section to save
        config: The configuration dictionary to save
        
    Raises:
        ConfigError: If configuration cannot be saved
    """
```

This function:
1. Saves configuration for a specific section
2. Validates the configuration before saving
3. Provides helpful error messages for configuration issues

### Usage Example

```python
from cursor_utils.config import ConfigManager
from cursor_utils.utils.config_helpers import ensure_config, load_config, save_config

# Define required keys and defaults
required_keys = ["model", "mode", "search_focus"]
defaults = {
    "model": "sonar",
    "mode": "copilot",
    "search_focus": "internet",
}

# Ensure configuration exists
config = ensure_config(manager, required_keys, defaults)

# Load configuration
web_config = load_config(manager, "web")

# Save configuration
save_config(manager, "web", web_config)
```

## File Ranking Algorithm

The file ranking algorithm (`cursor_utils/utils/file_rank_algo.py`) provides functionality to rank files based on their type, size, and creation time, while respecting `.gitignore` patterns.

### Core Data Types

The module defines several typed dictionaries for file information:

```python
class BaseFileInfo(TypedDict):
    """Base file information with just the path."""
    
    path: str


class ProcessedFileInfo(BaseFileInfo):
    """Processed file information with additional metadata."""
    
    type: str
    size: int
    creation_time: float
    importance_score: float


class FileInfo(TypedDict, total=False):
    """File information with optional fields."""
    
    path: str
    type: NotRequired[str]
    size: NotRequired[int]
    creation_time: NotRequired[float]
```

### FileRanker Class

The `FileRanker` class is the primary utility exported from the utils module:

```python
class FileRanker:
    """
    Ranks files based on a weighted score calculated from type frequency,
    file size, and creation time.
    
    Files matching .gitignore patterns are excluded by default.
    """
    
    def __init__(
        self,
        type_weight: float = 0.4,
        size_weight: float = 0.3,
        time_weight: float = 0.3,
        gitignore_path: Optional[str] = None,
        gitinclude_path: Optional[str] = None,
    ) -> None:
        """
        Initialize the file ranker with specified weights.
        
        Args:
            type_weight: Weight for file type in importance calculation
            size_weight: Weight for file size in importance calculation
            time_weight: Weight for creation time in importance calculation
            gitignore_path: Path to .gitignore file (optional)
            gitinclude_path: Path to .gitinclude file (optional)
        """
```

### Key Methods

The `FileRanker` class provides the following key methods:

#### rank_files

```python
def rank_files(self, files: list[FileInfo]) -> list[ProcessedFileInfo]:
    """
    Rank files based on their importance.
    
    Args:
        files: List of file information dictionaries
        
    Returns:
        List of processed file information dictionaries with importance scores,
        sorted in descending order of importance
    """
```

This method:
1. Filters files based on gitignore/gitinclude patterns
2. Computes type frequency across all files
3. Calculates normalized scores for type, size, and creation time
4. Computes a weighted importance score for each file
5. Returns files sorted by importance score

### Usage Example

```python
from cursor_utils.utils.file_rank_algo import FileRanker

# Initialize with sample files
files = [
    {"path": "file1.py", "size": 1000, "creation_time": 1600000000},
    {"path": "file2.js", "size": 2000, "creation_time": 1600001000},
    {"path": "file3.md", "size": 500, "creation_time": 1600002000},
    {"path": "file4.py", "size": 1500, "creation_time": 1600003000},
]

# Create ranker with custom weights
ranker = FileRanker(
    type_weight=0.5,
    size_weight=0.3,
    time_weight=0.2,
)

# Rank files
ranked_files = ranker.rank_files(files)

# Print results
for file in ranked_files:
    print(f"{file['path']}: {file['importance_score']:.4f}")
```

## Best Practices for Using Utilities

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

4. **Optimize file ranking**:
   - Customize weights based on your specific use case
   - Provide complete file information when possible
   - Use gitignore/gitinclude paths to filter files appropriately
   - Process the results as needed for your specific use case