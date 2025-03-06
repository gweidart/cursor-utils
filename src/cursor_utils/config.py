"""
Manages configuration and API keys for Cursor Utils.

Key Components:
    Config: Handles configuration management and API key storage
    APIKeys: Manages API key validation and storage

Project Dependencies:
    This file uses: python-dotenv: For .env file management
    This file is used by: cli: For configuration management
"""

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, TypeVar, cast

import yaml
from dotenv import load_dotenv, set_key
from rich.console import Console

from cursor_utils.errors import ConfigError, ErrorCodes
from cursor_utils.types import ConfigDict

# Type variable for generic type safety
T = TypeVar('T')

# Constants
DEFAULT_CONFIG_TEMPLATE = Path(__file__).parent / "templates" / "default_config.yaml"
DEFAULT_VERSION = "1.0.0"
DEFAULT_LOG_LEVEL = "INFO"


class APIKeyType(str, Enum):
    """Supported API key types."""

    GEMINI = "GEMINI_API_KEY"
    PERPLEXITY = "PERPLEXITY_API_KEY"
    GITHUB = "GITHUB_TOKEN"

    @property
    def description(self) -> str:
        """Get human-readable description of the API key."""
        return {
            self.GEMINI: "Google Gemini API Key",
            self.PERPLEXITY: "Perplexity AI API Key",
            self.GITHUB: "GitHub Personal Access Token",
        }[self]

    @property
    def feature_impact(self) -> str:
        """Get description of features impacted if key is missing."""
        return {
            self.GEMINI: "AI code generation and contextual analysis features will be limited",
            self.PERPLEXITY: "AI guided web search features will be unavailable",
            self.GITHUB: "GitHub integration features will be unavailable",
        }[self]


@dataclass
class APIKeyConfig:
    """Configuration for an API key."""

    key_type: APIKeyType
    value: Optional[str] = None
    is_set: bool = False


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

    def _load_default_config(self) -> ConfigDict:
        """
        Load default configuration from template.

        Returns:
            ConfigDict: Default configuration

        Raises:
            ConfigError: If template cannot be loaded

        """
        try:
            if not DEFAULT_CONFIG_TEMPLATE.exists():
                # Fallback to hardcoded defaults if template is missing
                return {
                    "version": DEFAULT_VERSION,
                    "settings": {
                        "debug": False,
                        "log_level": DEFAULT_LOG_LEVEL,
                    },
                }

            with open(DEFAULT_CONFIG_TEMPLATE, "r") as f:
                config = yaml.safe_load(f)
                if not isinstance(config, dict):
                    raise ConfigError(
                        message="Invalid template format",
                        code=ErrorCodes.CONFIG_FILE_ERROR,
                        causes=["Template must be a valid YAML dictionary"],
                        hint_stmt="Check template file format.",
                    )
                return cast(ConfigDict, config)

        except yaml.YAMLError as e:
            raise ConfigError(
                message="Failed to parse template file",
                code=ErrorCodes.CONFIG_FILE_ERROR,
                causes=[str(e)],
                hint_stmt="Check template YAML syntax.",
            )
        except Exception as e:
            raise ConfigError(
                message="Failed to load template file",
                code=ErrorCodes.CONFIG_FILE_ERROR,
                causes=[str(e)],
                hint_stmt="Check template file permissions.",
            )

    def load_config(self) -> ConfigDict:
        """
        Load configuration from file.

        Returns:
            ConfigDict: Configuration dictionary

        Raises:
            ConfigError: If configuration file is invalid

        """
        try:
            # Ensure config directory exists
            self._ensure_config_dir()

            # Check if config file exists
            if not self.config_path.exists():
                # Create default config if it doesn't exist
                default_config = self._load_default_config()
                self.save_config(default_config)
                return default_config

            # Load config from file
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data: ConfigDict = yaml.safe_load(f)

            # Validate config
            if not config_data:
                raise ConfigError(
                    message="Invalid configuration file",
                    code=ErrorCodes.CONFIG_FILE_ERROR,
                    causes=["Configuration file is not a valid YAML dictionary"],
                    hint_stmt="Try deleting the configuration file and running 'cursor-utils config init' to recreate it.",
                )

            # Ensure required fields exist
            if "version" not in config_data:
                config_data["version"] = DEFAULT_VERSION

            if "settings" not in config_data:
                config_data["settings"] = {
                    "debug": False,
                    "log_level": DEFAULT_LOG_LEVEL,
                }
            else:
                # Ensure settings fields exist
                if "debug" not in config_data["settings"]:
                    config_data["settings"]["debug"] = False
                if "log_level" not in config_data["settings"]:
                    config_data["settings"]["log_level"] = DEFAULT_LOG_LEVEL

            # Save validated config
            self.save_config(config_data)
            return config_data
        except yaml.YAMLError as e:
            raise ConfigError(
                message="Invalid YAML in configuration file",
                code=ErrorCodes.CONFIG_FILE_ERROR,
                causes=[str(e)],
                hint_stmt="Try deleting the configuration file and running 'cursor-utils config init' to recreate it.",
            ) from e
        except OSError as e:
            raise ConfigError(
                message="Error reading configuration file",
                code=ErrorCodes.CONFIG_FILE_ERROR,
                causes=[str(e)],
                hint_stmt="Check file permissions and try again.",
            ) from e
        except Exception as e:
            raise ConfigError(
                message="Unexpected error loading configuration",
                code=ErrorCodes.CONFIG_FILE_ERROR,
                causes=[str(e)],
                hint_stmt="Try deleting the configuration file and running 'cursor-utils config init' to recreate it.",
            ) from e

    def save_config(self, config: ConfigDict, silent: bool = False) -> None:
        """
        Save configuration to yaml file.

        Args:
            config: Configuration dictionary to save
            silent: Whether to suppress success message

        Raises:
            ConfigError: If configuration cannot be saved

        """
        try:
            # Ensure parent directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_path, "w") as f:
                yaml.safe_dump(config, f, default_flow_style=False, sort_keys=False)

            if not silent:
                self.console.print(
                    "[#00d700]Configuration saved successfully![/#00d700]"
                )
        except yaml.YAMLError as e:
            raise ConfigError(
                message="Failed to serialize configuration",
                code=ErrorCodes.CONFIG_FILE_ERROR,
                causes=[str(e)],
                hint_stmt="Check configuration data structure.",
            )
        except Exception as e:
            raise ConfigError(
                message="Failed to save configuration file",
                code=ErrorCodes.CONFIG_FILE_ERROR,
                causes=[str(e)],
                hint_stmt="Check file permissions and try again.",
            )

    def _ensure_env_file(self) -> None:
        """
        Ensure .env file exists.

        Raises:
            ConfigError: If file cannot be created

        """
        try:
            if not self.env_file.exists():
                self.env_file.touch()
        except Exception as e:
            raise ConfigError(
                message="Failed to create environment file",
                code=ErrorCodes.ENV_FILE_ERROR,
                causes=[str(e)],
                hint_stmt="Check file permissions and try again.",
            )

    def _load_env(self) -> None:
        """
        Load environment variables from .env file.

        Raises:
            ConfigError: If file cannot be loaded

        """
        try:
            load_dotenv(self.env_file)
        except Exception as e:
            raise ConfigError(
                message="Failed to load environment file",
                code=ErrorCodes.ENV_FILE_ERROR,
                causes=[str(e)],
                hint_stmt="Check file permissions and try again.",
            )

    def get_api_key(self, key_type: APIKeyType) -> Optional[str]:
        """
        Get an API key from environment.

        Args:
            key_type: Type of API key to get

        Returns:
            Optional[str]: API key if set, None otherwise

        Raises:
            ConfigError: If environment file cannot be read

        """
        try:
            return os.getenv(key_type)
        except Exception as e:
            raise ConfigError(
                message=f"Failed to get {key_type.description}",
                code=ErrorCodes.API_KEY_READ_ERROR,
                causes=[str(e)],
                hint_stmt="Check environment file permissions and try again.",
            )

    def set_api_key(self, key_type: APIKeyType, value: str) -> None:
        """
        Set an API key in .env file.

        Args:
            key_type: Type of API key to set
            value: API key value

        Raises:
            ConfigError: If key cannot be saved

        """
        try:
            # Try to write to the file first
            set_key(str(self.env_file), str(key_type), value)
            # Only update environment if file write succeeds
            os.environ[str(key_type)] = value
        except Exception as e:
            raise ConfigError(
                message=f"Failed to save {key_type.description}",
                code=ErrorCodes.API_KEY_SAVE_ERROR,
                causes=[str(e)],
                hint_stmt="Check environment file permissions and try again.",
            )

    def check_api_key(self, key_type: APIKeyType) -> APIKeyConfig:
        """
        Check if an API key is set.

        Args:
            key_type: Type of API key to check

        Returns:
            APIKeyConfig: Configuration status for the key

        Raises:
            ConfigError: If key status cannot be checked

        """
        try:
            value = self.get_api_key(key_type)
            return APIKeyConfig(
                key_type=key_type,
                value=value,
                is_set=bool(value),
            )
        except Exception as e:
            raise ConfigError(
                message=f"Failed to check {key_type.description}",
                code=ErrorCodes.API_KEY_READ_ERROR,
                causes=[str(e)],
                hint_stmt="Check environment file permissions and try again.",
            )

    def get_all_api_keys(self) -> list[APIKeyConfig]:
        """
        Get status of all API keys.

        Returns:
            list[APIKeyConfig]: List of API key configurations

        Raises:
            ConfigError: If key status cannot be retrieved

        """
        try:
            return [self.check_api_key(key_type) for key_type in APIKeyType]
        except Exception as e:
            raise ConfigError(
                message="Failed to get API key status",
                code=ErrorCodes.API_KEY_READ_ERROR,
                causes=[str(e)],
                hint_stmt="Check environment file permissions and try again.",
            )

    def _ensure_config_dir(self) -> None:
        """Ensure config directory exists."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ConfigError(
                message="Failed to create config directory",
                code=ErrorCodes.CONFIG_FILE_ERROR,
                causes=[str(e)],
                hint_stmt="Check directory permissions and try again.",
            )
