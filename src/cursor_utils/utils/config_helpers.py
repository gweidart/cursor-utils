"""
Common utilities for configuration management.

This module provides standardized functions for loading, saving, and ensuring
configuration exists. It implements a consistent approach to configuration
management across different commands and services.

Key Components:
    ensure_config: Ensure configuration exists with standardized error handling
    load_config: Load configuration with standardized error handling
    save_config: Save configuration with standardized error handling

Examples:
    Ensuring configuration exists:
    ```python
    from cursor_utils.utils.config_helpers import ensure_config

    # Define required keys and defaults
    required_keys = ["model", "mode", "search_focus"]
    defaults = {
        "model": "sonar",
        "mode": "copilot",
        "search_focus": "internet",
    }

    # Ensure configuration exists
    config = ensure_config(manager, required_keys, defaults)
    ```

    Loading configuration:
    ```python
    from cursor_utils.utils.config_helpers import load_config

    # Load web configuration
    web_config = load_config(manager, "web")
    ```

    Saving configuration:
    ```python
    from cursor_utils.utils.config_helpers import save_config

    # Save web configuration
    save_config(manager, "web", web_config)
    ```

Project Dependencies:
    This file uses: cursor_utils.config: For configuration storage
    This file uses: cursor_utils.errors: For error handling
    This file is used by: commands: For configuration management

"""

from typing import Any, Optional, Protocol, TypeVar

from rich.console import Console

from cursor_utils.errors import ConfigError, ErrorCodes

T = TypeVar('T')
console = Console()


class ConfigManager(Protocol):
    """Protocol for configuration manager objects."""

    def load_config(self) -> Optional[dict[str, Any]]:
        """Load configuration."""
        ...

    def save_config(self, **kwargs: Any) -> None:
        """Save configuration."""
        ...


def ensure_config(
    manager: ConfigManager,
    required_keys: list[str],
    defaults: dict[str, Any],
    silent: bool = False,
) -> dict[str, Any]:
    """
    Ensure configuration exists with standardized error handling.

    This function checks if a configuration exists and has all required keys.
    If not, it creates a new configuration with default values.

    The function follows these steps:
    1. Try to load existing configuration
    2. Check if configuration exists and has all required keys
    3. If not, create a new configuration with default values
    4. Save the new configuration

    Args:
        manager: Manager object with load_config and save_config methods
        required_keys: List of required configuration keys
        defaults: Default values for configuration keys
        silent: Whether to suppress success messages

    Returns:
        Configuration dictionary with all required keys

    Raises:
        ConfigError: If configuration cannot be loaded or created

    Example:
        ```python
        # Define required keys and defaults
        required_keys = ["model", "mode", "search_focus"]
        defaults = {
            "model": "sonar",
            "mode": "copilot",
            "search_focus": "internet",
        }

        # Ensure configuration exists
        config = ensure_config(manager, required_keys, defaults)
        ```

    """
    try:
        # Try to load existing config
        config = manager.load_config()

        # Check if config exists and has all required keys
        if config is not None and all(k in config for k in required_keys):
            return config

        # Print message if creating new config and not in silent mode
        if not silent:
            console.print(
                "[yellow]No configuration found. Creating default configuration.[/]"
            )

        # Create new config with defaults
        new_config: dict[str, Any] = {}
        for key, value in defaults.items():
            new_config[key] = config.get(key, value) if config else value

        # Save new config
        manager.save_config(**new_config, silent=silent)
        return new_config

    except Exception as e:
        raise ConfigError(
            message="Failed to load or create configuration",
            code=ErrorCodes.CONFIG_FILE_ERROR,
            causes=[str(e)],
            hint_stmt="Check your configuration file permissions and format",
        ) from e


class ConfigWithManager(Protocol):
    """Protocol for objects with a config attribute."""

    config: Any


def load_config(
    manager: ConfigWithManager, config_name: str
) -> Optional[dict[str, Any]]:
    """
    Load configuration with standardized error handling.

    This function loads a specific section of the configuration.
    If the section does not exist, it returns an empty dictionary.

    The function follows these steps:
    1. Load the entire configuration
    2. Return the specified section or an empty dictionary if not found

    Args:
        manager: Manager object with config attribute
        config_name: Name of the configuration section (e.g., "web", "gemini")

    Returns:
        Configuration dictionary or empty dictionary if not found

    Raises:
        ConfigError: If configuration cannot be loaded

    Example:
        ```python
        # Load web configuration
        web_config = load_config(manager, "web")
        ```

    """
    try:
        config = manager.config.load_config()
        return config.get(config_name, {})
    except Exception as e:
        raise ConfigError(
            message=f"Failed to load {config_name} configuration",
            code=ErrorCodes.CONFIG_FILE_ERROR,
            causes=[str(e)],
            hint_stmt="Check your configuration file permissions and format",
        ) from e


def save_config(
    manager: ConfigWithManager,
    config_name: str,
    config_data: dict[str, Any],
    silent: bool = False,
) -> None:
    """
    Save configuration with standardized error handling.

    This function saves a specific section of the configuration.
    It preserves other sections of the configuration.

    The function follows these steps:
    1. Load the entire configuration
    2. Update the specified section
    3. Save the updated configuration

    Args:
        manager: Manager object with config attribute
        config_name: Name of the configuration section (e.g., "web", "gemini")
        config_data: Configuration data to save
        silent: Whether to suppress success messages

    Raises:
        ConfigError: If configuration cannot be saved

    Example:
        ```python
        # Save web configuration
        web_config = {"model": "sonar", "mode": "copilot", "search_focus": "internet"}
        save_config(manager, "web", web_config)
        ```

    """
    try:
        # Load existing config
        config = manager.config.load_config()

        # Update config section
        config[config_name] = config_data

        # Save updated config
        manager.config.save_config(config, silent=silent)

        # Print success message if not in silent mode
        if not silent:
            console.print(
                f"[#5f87ff]{config_name.capitalize()} configuration saved successfully[/]"
            )

    except Exception as e:
        raise ConfigError(
            message=f"Failed to save {config_name} configuration",
            code=ErrorCodes.CONFIG_FILE_ERROR,
            causes=[str(e)],
            hint_stmt="Check your configuration file permissions and format",
        ) from e
