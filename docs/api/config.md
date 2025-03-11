## Configuration API

The Configuration API provides a flexible and consistent way to manage configuration settings for Cursor-Utils. It handles loading, saving, and accessing configuration values with support for environment variable overrides.

### Overview

Configuration in Cursor-Utils follows these principles:

1. **Simple Storage**: Configuration is stored in a JSON file
2. **Environment Overrides**: Environment variables take precedence over stored configuration
3. **Standard Locations**: Configuration uses platform-specific standard locations
4. **Error Handling**: Clear error messages when configuration operations fail

### Configuration Storage

By default, configuration is stored in a JSON file at:

- **Linux/macOS**: `~/.config/cursor-utils/config.json`
- **Windows**: `%APPDATA%\cursor-utils\config.json`

You can customize this location by specifying a different path when loading configuration.

### Key Components

### Configuration Class

The `Configuration` class is the primary interface for working with configuration settings.

```python
from cursor_utils.core.config import load_configuration

# Load configuration from default location
config = load_configuration()

# Get a configuration value
api_key = config.get("gemini_api_key")

# Set a configuration value
config.set("default_format", "markdown")

# Delete a configuration value
config.delete("test_key")
```

### Environment Variables

Environment variables take precedence over stored configuration:

```bash
# Set Gemini API key via environment variable
export GEMINI_API_KEY=your-api-key

```

### API Reference

### `get_default_config_path()`

Get the default configuration path based on the platform.

**Returns**:
- `Path`: Path to the default configuration file

**Example**:
```python
from cursor_utils.core.config import get_default_config_path

# Get the default configuration path
config_path = get_default_config_path()
print(f"Configuration will be stored at: {config_path}")
```

### `class Configuration`

Configuration manager for cursor-utils.

#### `__init__(config_path=None)`

Initialize the configuration manager.

**Parameters**:
- `config_path` (Optional[Union[str, Path]]): Path to the configuration file, or None to use the default

**Example**:
```python
from cursor_utils.core.config import Configuration
from pathlib import Path

# Use default configuration path
config = Configuration()

# Use custom configuration path
custom_config = Configuration(Path.home() / "my-config.json")
```

#### `get(key, default=None)`

Get a configuration value with environment override.

**Parameters**:
- `key` (str): The configuration key
- `default` (Any): The default value if the key is not found

**Returns**:
- The configuration value

**Example**:
```python
from cursor_utils.core.config import load_configuration

config = load_configuration()

# Get API key with default
api_key = config.get("gemini_api_key", "default-key")

# Get output format with default
format = config.get("default_format", "rich")
```

#### `set(key, value)`

Set a configuration value and save to the config file.

**Parameters**:
- `key` (str): The configuration key
- `value` (Any): The configuration value

**Raises**:
- `ConfigError`: If the configuration cannot be saved

**Example**:
```python
from cursor_utils.core.config import load_configuration

config = load_configuration()

# Set API key
config.set("gemini_api_key", "your-api-key")

# Set default output format
config.set("default_format", "markdown")
```

#### `delete(key)`

Delete a configuration value and save to the config file.

**Parameters**:
- `key` (str): The configuration key

**Raises**:
- `ConfigError`: If the configuration cannot be saved

**Example**:
```python
from cursor_utils.core.config import load_configuration

config = load_configuration()

# Delete a configuration key
config.delete("test_key")
```

### `load_configuration(config_path=None)`

Load configuration from a file or default location.

**Parameters**:
- `config_path` (Optional[Union[str, Path]]): Path to the configuration file, or None to use the default

**Returns**:
- `Configuration`: Configuration object

**Raises**:
- `ConfigError`: If the configuration cannot be loaded

**Example**:
```python
from cursor_utils.core.config import load_configuration
from pathlib import Path

# Load from default location
config = load_configuration()

# Load from custom location
custom_config = load_configuration(Path.home() / "my-config.json")
```

### Common Configuration Keys

Cursor-Utils uses the following common configuration keys:

| Key | Description | Default | Used By |
|-----|-------------|---------|---------|
| `gemini_api_key` | Google Gemini API key | None | `gemini`, `project`, `repo` commands |
| `perplexity_api_key` | Perplexity API key | None | `web` command |
| `github_token` | GitHub personal access token | None | `github` command |
| `default_format` | Default output format | `rich` | All commands |
| `default_gemini_model` | Default Gemini model | `gemini-1.5-pro` | `gemini`, `project`, `repo` commands |
| `default_perplexity_model` | Default Perplexity model | `sonar` | `web` command |

### Error Handling

Configuration operations can raise `ConfigError` exceptions:

```python
from cursor_utils.core.config import load_configuration
from cursor_utils.core.errors import ConfigError

try:
    config = load_configuration()
    api_key = config.get("gemini_api_key")
    if not api_key:
        raise ConfigError(
            "API key for Gemini not found in configuration",
            help_text="Set your API key using: cursor-utils config set gemini_api_key YOUR_API_KEY"
        )
except ConfigError as e:
    print(f"Configuration error: {e.message}")
    if e.help_text:
        print(f"Help: {e.help_text}")
```

### Best Practices

1. **Use Environment Variables for Sensitive Data**: For CI/CD and shared environments
   ```bash
   export GEMINI_API_KEY=your-api-key
   ```

2. **Set Default Values**: Configure commonly used options as defaults
   ```python
   config.set("default_format", "markdown")
   config.set("default_gemini_model", "gemini-1.5-pro")
   ```

3. **Handle Missing Configuration**: Always check for required configuration
   ```python
   api_key = config.get("gemini_api_key")
   if not api_key:
       # Handle missing API key
   ```

4. **Provide Helpful Error Messages**: Include instructions for resolving issues
   ```python
   if not api_key:
       raise ConfigError(
           "API key not found",
           help_text="Set your API key using: cursor-utils config set gemini_api_key YOUR_API_KEY"
       )
   ``` 