# Configuration System Reference

This reference provides detailed information about the Cursor Utils configuration system, including the implementation architecture, configuration storage, and API key management.

## Configuration Architecture

Cursor Utils uses a hierarchical configuration system with multiple sources of configuration values:

1. **Default values** - Built-in defaults for all settings
2. **Configuration file** - User-defined settings in YAML format
3. **Environment variables** - System-level configuration
4. **Command-line arguments** - Run-time overrides

The configuration system follows a cascading priority model where command-line arguments override environment variables, which override the configuration file, which override defaults.

## Implementation Details

The configuration system is implemented in `cursor_utils/config.py` with the `Config` class as the primary interface:

```python
class Config:
    """Manages configuration and API keys."""

    def __init__(self) -> None:
        """Initialize configuration manager."""
        self.console = Console()
        self.env_file = Path.cwd() / ".env"
        self.config_dir = Path.cwd() / "config"
        self.yaml_config = Path.cwd() / "cursor-utils.yaml"
        self.config_path = self.yaml_config

        # Ensure required files and directories exist
        self._ensure_env_file()
        self._ensure_config_dir()
        self._load_env()

        # Load configuration
        self.config = self.load_config()
```

The `APIKeyConfig` class handles API key validation and storage:

```python
@dataclass
class APIKeyConfig:
    """Configuration for an API key."""

    key_type: APIKeyType
    value: Optional[str] = None
    is_set: bool = False
```

### Configuration Loading Process

The configuration loading process follows these steps:

1. Check for default configuration template
2. Look for user configuration file
3. Load and parse the configuration
4. Validate configuration structure
5. Apply type coercion to ensure correct types
6. Set default values for missing fields

## Configuration File

Cursor Utils stores its configuration in `cursor-utils.yaml` in the current working directory. Here's a complete example configuration file with all available options:

```yaml
# Cursor Utils configuration
version: "0.1.0"

# General settings
settings:
  # Enable debug mode for verbose logging
  debug: false
  
  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  log_level: "INFO"

# Web/Perplexity settings
web:
  # Model to use for Perplexity queries (sonar, sonar-pro, sonar-reasoning, sonar-pro-reasoning)
  model: "sonar"
  
  # Response mode (copilot, concise)
  mode: "copilot"
  
  # Search focus (internet, scholar, writing, wolfram, youtube, reddit)
  search_focus: "internet"
  
  # Enable streaming responses
  stream: true

# Gemini settings
gemini:
  # Gemini model to use
  model: "gemini-pro"
  
  # Maximum tokens to generate
  max_output_tokens: 8000
  
  # Temperature for generation (0.0-1.0)
  temperature: 0.7
  
  # Top-p sampling parameter (0.0-1.0)
  top_p: 0.95
  
  # Top-k sampling parameter
  top_k: 40

# GitHub settings
github:
  # Source for GitHub token (env or config)
  token_source: "env"
  
  # Default GitHub owner/organization
  default_owner: ""
  
  # Default GitHub repository
  default_repo: ""
  
  # Directory for GitHub templates
  template_dir: "~/.cursor-utils/github-templates"

```

## API Key Management

Cursor Utils manages API keys securely using the following methods:

### API Key Types

```python
class APIKeyType(str, Enum):
    """Supported API key types."""

    GEMINI = "GEMINI_API_KEY"
    PERPLEXITY = "PERPLEXITY_API_KEY"
    GITHUB = "GITHUB_TOKEN"
```

### API Key Storage

API keys are stored primarily in environment variables, with support for:

1. **Environment variables** - Direct access to system environment variables
2. **`.env` file** - Local environment variable storage
3. **Secure keyring** - System keyring integration (if available)

API keys are never stored in plain text in the configuration file for security reasons.

### API Key Validation

API keys are validated before use to ensure they are:

1. Properly formatted
2. Not expired
3. Have correct permissions

The validation process varies by API provider:

```python
def validate_api_key(key_type: APIKeyType, value: str) -> bool:
    """
    Validate an API key.
    
    Args:
        key_type: Type of API key
        value: API key value
        
    Returns:
        True if valid, False otherwise
    """
    if not value:
        return False
        
    if key_type == APIKeyType.PERPLEXITY:
        # Perplexity keys are 32 character alphanumeric strings
        return bool(re.match(r'^[A-Za-z0-9]{32}$', value))
    elif key_type == APIKeyType.GEMINI:
        # Gemini keys typically start with 'AI' and are 39 characters
        return bool(re.match(r'^AI[A-Za-z0-9_-]{37}$', value))
    elif key_type == APIKeyType.GITHUB:
        # GitHub tokens are 40 character hexadecimal strings
        # or new fine-grained tokens with 'github_pat_' prefix
        return bool(re.match(r'^(ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{82})$', value))
    
    return False
```

## Environment Variables

Cursor Utils recognizes the following environment variables:

| Environment Variable | Description | Default |
|----------------------|-------------|---------|
| `PERPLEXITY_API_KEY` | API key for Perplexity AI | None |
| `GEMINI_API_KEY` | API key for Google Gemini | None |
| `GITHUB_TOKEN` | GitHub personal access token | None |
| `CURSOR_UTILS_DEBUG` | Enable debug mode | `False` |
| `CURSOR_UTILS_LOG_LEVEL` | Set logging level | `INFO` |
| `CURSOR_UTILS_CONFIG_PATH` | Custom config file path | `./cursor-utils.yaml` |

## Configuration API

### Basic Usage

```python
from cursor_utils.config import Config

# Initialize configuration
config = Config()

# Get a configuration value with a default fallback
debug_mode = config.get("settings.debug", default=False)

# Set a configuration value
config.set("web.model", "sonar-pro")

# Save changes to the configuration file
config.save()
```

### API Key Management

```python
from cursor_utils.config import Config, APIKeyType

# Initialize configuration
config = Config()

# Get an API key
perplexity_key = config.get_api_key(APIKeyType.PERPLEXITY)

# Set an API key (stores in environment or .env file)
config.set_api_key(APIKeyType.GEMINI, "YOUR_API_KEY")

# Check if API key is valid
is_valid = config.validate_api_key(APIKeyType.GITHUB, "github_pat_...")
```

### Advanced Configuration

```python
from cursor_utils.config import Config

# Initialize configuration
config = Config()

# Get all Gemini settings
gemini_config = config.get_section("gemini")

# Update multiple settings
config.update({
    "gemini.temperature": 0.5,
    "gemini.max_output_tokens": 4000
})

# Reset a section to defaults
config.reset_section("web")
```

## Command Line Interface

The configuration system is accessible through the `config` command:

```bash
# Show current configuration
cursor-utils config show

# Configure API keys
cursor-utils config api_keys

# Set a configuration value
cursor-utils config set web.model sonar-pro

# Reset to defaults
cursor-utils config reset gemini
```

## Configuration Migration

When the configuration version changes, Cursor Utils automatically migrates the configuration:

```python
def migrate_config(config: dict, current_version: str, target_version: str) -> dict:
    """
    Migrate configuration from current version to target version.
    
    Args:
        config: Current configuration
        current_version: Current version
        target_version: Target version
        
    Returns:
        Migrated configuration
    """
    # Migration logic here
    return config
```

## Custom Configuration Options

Users can add custom configuration options that aren't predefined:

```python
# Add a custom option
config.set("custom_options.my_setting", "my_value")

# Get a custom option
value = config.get("custom_options.my_setting", default="default_value")
```

## Configuration Validation

Configuration is validated to ensure it's properly structured:

```python
def validate_config(config: dict) -> tuple[bool, list[str]]:
    """
    Validate configuration structure.
    
    Args:
        config: Configuration to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Required sections
    if "settings" not in config:
        errors.append("Missing 'settings' section")
    
    # Type checking
    if "settings" in config and not isinstance(config["settings"], dict):
        errors.append("'settings' must be a dictionary")
    
    # Value validation
    if "web" in config and "model" in config["web"]:
        if config["web"]["model"] not in ["sonar", "sonar-pro", "sonar-reasoning", "sonar-pro-reasoning"]:
            errors.append(f"Invalid web model: {config['web']['model']}")
    
    return len(errors) == 0, errors
```

## Best Practices

1. **Use the API**: Always use the Config class instead of direct dictionary access
2. **Default Values**: Always provide default values when getting configuration
3. **Type Checking**: Validate types when processing configuration values
4. **Validate Early**: Check configuration at startup to catch errors early
5. **Handle Errors**: Gracefully handle missing or invalid configuration
6. **Security**: Never store sensitive API keys in the configuration file
7. **Migration**: Provide migration paths for configuration changes

## Configuration Options

### Web/Perplexity Options

| Option | Description | Default |
|--------|-------------|---------|
| `perplexity_api_key` | API key for Perplexity | - |
| `perplexity_model` | Perplexity model to use | `sonar` |
| `perplexity_mode` | Mode for responses | `copilot` |
| `perplexity_focus` | Search focus | `internet` |

### Gemini Options

| Option | Description | Default |
|--------|-------------|---------|
| `gemini_api_key` | API key for Google Gemini | - |
| `gemini_model` | Gemini model to use | `gemini-2.0-pro-exp-02-05` |
| `gemini_max_tokens` | Maximum tokens for responses | 8000 |

### GitHub Options

| Option | Description | Default |
|--------|-------------|---------|
| `github_token` | GitHub personal access token | - |
| `github_default_owner` | Default GitHub owner/organization | - |
| `github_default_repo` | Default GitHub repository | - |

## Managing Configuration

### Using the CLI

```bash
# Show current configuration
cursor-utils config show

# Set a configuration value
cursor-utils config set perplexity_api_key YOUR_API_KEY

# Reset a configuration value
cursor-utils config reset perplexity_model
```

### Environment Variables

Configuration can also be provided via environment variables:

- `PERPLEXITY_API_KEY`
- `GEMINI_API_KEY`
- `GITHUB_TOKEN` 