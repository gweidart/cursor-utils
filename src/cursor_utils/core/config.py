"""
Configuration management for cursor-utils with support for hierarchical configuration.

Key Components:
    Configuration: Main configuration class
    get_default_config_path: Get the default configuration path
    load_configuration: Load configuration from a file or default location

Project Dependencies:
    This file uses: errors: For configuration-related errors
    This file is used by: CLI commands and service clients
"""

import json
import os
from pathlib import Path
from typing import Any, Optional, Union

from cursor_utils.core.errors import ConfigError


def get_default_config_path() -> Path:
    """
    Get the default configuration path based on the platform.

    Returns:
        Path to the default configuration file

    """
    # Use XDG_CONFIG_HOME if available, otherwise use platform-specific defaults
    if os.environ.get("XDG_CONFIG_HOME"):
        base_dir = Path(os.environ["XDG_CONFIG_HOME"])
    elif os.name == "nt":  # Windows
        base_dir = Path(os.environ["APPDATA"])
    else:  # Unix-like
        base_dir = Path.home() / ".config"

    return base_dir / "cursor-utils" / "config.json"


class Configuration:
    """Configuration manager for cursor-utils."""

    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize the configuration manager.

        Args:
            config_path: Path to the configuration file, or None to use the default

        """
        self.config_path = (
            Path(config_path) if config_path else get_default_config_path()
        )
        self.data: dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """
        Load configuration from the config file.

        Raises:
            ConfigError: If the configuration file exists but cannot be loaded

        """
        if not self.config_path.exists():
            self.data = {}
            return

        try:
            with open(self.config_path, "r") as f:
                self.data = json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigError(
                f"Failed to parse configuration file: {e}",
                help_text="Ensure your configuration file is valid JSON.",
            )
        except Exception as e:
            raise ConfigError(f"Failed to load configuration: {e}")

    def _save_config(self) -> None:
        """
        Save configuration to the config file.

        Raises:
            ConfigError: If the configuration cannot be saved

        """
        # Ensure the directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.config_path, "w") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            raise ConfigError(f"Failed to save configuration: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value with environment override.

        Args:
            key: The configuration key
            default: The default value if the key is not found

        Returns:
            The configuration value

        """
        # Check environment variable first
        env_key = f"CURSOR_UTILS_{key.upper()}"
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return env_value

        # Then check configuration file
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value and save to the config file.

        Args:
            key: The configuration key
            value: The configuration value

        Raises:
            ConfigError: If the configuration cannot be saved

        """
        self.data[key] = value
        self._save_config()

    def delete(self, key: str) -> None:
        """
        Delete a configuration value and save to the config file.

        Args:
            key: The configuration key

        Raises:
            ConfigError: If the configuration cannot be saved

        """
        if key in self.data:
            del self.data[key]
            self._save_config()


def load_configuration(config_path: Optional[Union[str, Path]] = None) -> Configuration:
    """
    Load configuration from a file or default location.

    Args:
        config_path: Path to the configuration file, or None to use the default

    Returns:
        Configuration object

    Raises:
        ConfigError: If the configuration cannot be loaded

    """
    return Configuration(config_path)
