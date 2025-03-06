"""
Pure business logic for configuration operations.

Key Components:
    validate_api_key(): Validates API key format
    save_api_key(): Saves API key to environment
    get_api_key_status(): Gets API key configuration status

Project Dependencies:
    This file uses: config: For configuration management
    This file is used by: config.manager: For configuration orchestration
"""

from typing import NoReturn

from cursor_utils.config import APIKeyConfig, APIKeyType, Config
from cursor_utils.errors import ConfigError, ErrorCodes


def validate_api_key(key: str, key_type: APIKeyType) -> None:
    """
    Validate an API key.

    Args:
        key: API key to validate
        key_type: Type of API key to validate

    Raises:
        ConfigError: If key is invalid

    """
    if not key or key.isspace():
        raise ConfigError(
            message="API key cannot be empty",
            code=ErrorCodes.API_KEY_SAVE_ERROR,
            causes=["API key is empty or whitespace"],
            hint_stmt="Please provide a valid API key.",
        )

    if len(key.strip()) < 10:
        raise ConfigError(
            message="API key is too short",
            code=ErrorCodes.API_KEY_SAVE_ERROR,
            causes=["API key is shorter than 10 characters"],
            hint_stmt="API keys are typically longer than 10 characters.",
        )

    # Key-specific validation
    if key_type == APIKeyType.GEMINI and not key.startswith("AI"):
        raise ConfigError(
            message="Invalid Google Gemini API Key",
            code=ErrorCodes.API_KEY_SAVE_ERROR,
            causes=["API key must start with 'AI'"],
            hint_stmt="Please provide a valid Gemini API key starting with 'AI'.",
        )

    if key_type == APIKeyType.GITHUB and len(key) < 40:
        raise ConfigError(
            message="Invalid GitHub Token",
            code=ErrorCodes.API_KEY_SAVE_ERROR,
            causes=["Token must be at least 40 characters"],
            hint_stmt="Please provide a valid GitHub token.",
        )


def raise_validation_error(
    *, key_type: APIKeyType, message: str, cause: str, hint: str
) -> NoReturn:
    """
    Raise a validation error with consistent formatting.

    Args:
        key_type: Type of API key being validated
        message: Error message
        cause: Cause of the error
        hint: Hint for fixing the error

    Raises:
        ConfigError: Always raises with formatted error details

    """
    raise ConfigError(
        message=message,
        code=ErrorCodes.INVALID_API_KEY,
        causes=[cause],
        hint_stmt=hint,
    )


def save_api_key(cfg: Config, key_type: APIKeyType, value: str) -> None:
    """
    Save an API key to configuration.

    Args:
        cfg: Configuration instance
        key_type: Type of API key to save
        value: API key value to save

    Raises:
        ConfigError: If key cannot be saved

    """
    try:
        validate_api_key(value, key_type)
        cfg.set_api_key(key_type, value)
    except Exception as e:
        raise ConfigError(
            message=f"Failed to save {key_type.description}",
            code=ErrorCodes.API_KEY_SAVE_ERROR,
            causes=[str(e)],
            hint_stmt="Please check the API key and try again.",
        )


def get_api_key_status(cfg: Config) -> list[APIKeyConfig]:
    """
    Get status of all API keys.

    Args:
        cfg: Configuration manager instance

    Returns:
        list[APIKeyConfig]: List of API key configurations

    Raises:
        ConfigError: If API key status cannot be retrieved

    """
    try:
        return cfg.get_all_api_keys()
    except Exception as e:
        raise ConfigError(
            message="Failed to get API key status",
            code=ErrorCodes.API_KEY_READ_ERROR,
            causes=[str(e)],
            hint_stmt="Check environment file permissions and try again.",
        )
