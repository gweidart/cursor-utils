"""
Common utilities for API key management.

This module provides standardized functions for retrieving, validating, and managing API keys.
It implements a consistent approach to API key handling across different services.

Key Components:
    get_api_key: Get API key with standardized error handling
    validate_api_key: Validate API key with standardized error handling

Examples:
    Getting an API key:
    ```python
    from cursor_utils.config import APIKeyType
    from cursor_utils.utils.api_helpers import get_api_key

    # Get Perplexity API key
    api_key = get_api_key(APIKeyType.PERPLEXITY, "PERPLEXITY_API_KEY")
    ```

    Validating an API key:
    ```python
    from cursor_utils.config import APIKeyType
    from cursor_utils.utils.api_helpers import validate_api_key

    # Validate Gemini API key
    validate_api_key(api_key, APIKeyType.GEMINI, "GEMINI_API_KEY")
    ```

Project Dependencies:
    This file uses: cursor_utils.config: For API key storage
    This file uses: cursor_utils.errors: For error handling
    This file is used by: commands: For API key management

"""

import os

import click
from rich.console import Console

from cursor_utils.config import APIKeyType, Config
from cursor_utils.errors import ErrorCodes, WebError

console = Console()


def get_api_key(key_type: APIKeyType, env_var: str) -> str:
    """
    Get API key with standardized error handling.

    This function attempts to retrieve an API key from multiple sources in the following order:
    1. Environment variable
    2. Configuration file
    3. User prompt (interactive)

    If the API key is provided via prompt, it will be saved to the configuration file
    for future use.

    Args:
        key_type: Type of API key to get (e.g., APIKeyType.PERPLEXITY)
        env_var: Environment variable name for the API key (e.g., "PERPLEXITY_API_KEY")

    Returns:
        API key string

    Raises:
        WebError: If API key is not found or invalid

    Example:
        ```python
        from cursor_utils.config import APIKeyType

        # Get Perplexity API key
        api_key = get_api_key(APIKeyType.PERPLEXITY, "PERPLEXITY_API_KEY")
        ```

    """
    # Try to get API key from environment
    api_key = os.environ.get(env_var, "")

    if api_key:
        return api_key

    # Try to get API key from config
    config = Config()
    api_key_config = config.check_api_key(key_type)

    if api_key_config.is_set and api_key_config.value:
        return api_key_config.value

    # Prompt user for API key
    console.print(
        f"[yellow]No {key_type.description} found in environment or config[/]"
    )
    console.print(f"You can set it in the environment as {env_var}")
    console.print("Or you can set it in the config with: cursor-utils config api_keys")

    try:
        api_key = click.prompt(
            f"Enter your {key_type.description}", hide_input=True, type=str
        )

        if not api_key:
            raise WebError(
                message=f"No {key_type.description} provided",
                code=ErrorCodes.INVALID_API_KEY,
                causes=["API key is required for this operation"],
                hint_stmt=f"Set {env_var} environment variable or run 'cursor-utils config api_keys'",
            )

        # Save API key to config
        config.set_api_key(key_type, api_key)
        return api_key

    except click.Abort:
        raise WebError(
            message="API key input aborted",
            code=ErrorCodes.INVALID_API_KEY,
            causes=["User aborted API key input"],
            hint_stmt=f"Set {env_var} environment variable or run 'cursor-utils config api_keys'",
        )


def validate_api_key(api_key: str, key_type: APIKeyType, env_var: str) -> None:
    """
    Validate API key with standardized error handling.

    This function performs basic validation on an API key:
    1. Checks if the API key is empty
    2. Checks if the API key meets minimum length requirements

    More specific validation can be added for different API key types.

    Args:
        api_key: API key to validate
        key_type: Type of API key (e.g., APIKeyType.PERPLEXITY)
        env_var: Environment variable name for the API key (e.g., "PERPLEXITY_API_KEY")

    Raises:
        WebError: If API key is invalid

    Example:
        ```python
        from cursor_utils.config import APIKeyType

        # Validate Gemini API key
        validate_api_key(api_key, APIKeyType.GEMINI, "GEMINI_API_KEY")
        ```

    """
    if not api_key:
        raise WebError(
            message=f"Invalid {key_type.description}",
            code=ErrorCodes.INVALID_API_KEY,
            causes=["API key is empty or not set"],
            hint_stmt=f"Set {env_var} environment variable or run 'cursor-utils config api_keys'",
        )

    # Basic validation - API keys should be at least 8 characters
    if len(api_key) < 8:
        raise WebError(
            message=f"Invalid {key_type.description}",
            code=ErrorCodes.INVALID_API_KEY,
            causes=["API key is too short"],
            hint_stmt=f"Check your {key_type.description} and try again",
        )
