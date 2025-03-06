"""
Manager module for gemini command configuration and client management.

Key Components:
    GeminiManager: Manages configuration and client lifecycle
    create_client: Factory function for client creation

Project Dependencies:
    This file uses: google.genai: For API client
    This file uses: types: For type definitions
    This file uses: errors: For standardized error handling
    This file is used by: actions: For client operations
"""

from typing import Optional

from google import genai
from rich.console import Console

from cursor_utils.config import Config
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.types import GeminiConfig

console = Console()


class GeminiManager:
    """Manager for gemini command configuration and client lifecycle."""

    def __init__(self) -> None:
        """Initialize gemini manager."""
        self._client: Optional[genai.Client] = None
        self.config = Config()

    def load_config(self) -> Optional[GeminiConfig]:
        """
        Load gemini configuration from yaml file.

        Returns:
            Optional[GeminiConfig]: Gemini configuration if found, None otherwise

        Raises:
            WebError: If configuration cannot be loaded

        """
        try:
            config = self.config.load_config()
            gemini_config = config.get("gemini", {})
            if not gemini_config or not all(
                k in gemini_config
                for k in ("model", "max_output_tokens", "temperature", "top_p", "top_k")
            ):
                return None

            # Validate configuration values
            model = gemini_config.get("model", "")
            max_output_tokens = gemini_config.get("max_output_tokens", 2048)
            temperature = gemini_config.get("temperature", 0.7)
            top_p = gemini_config.get("top_p", 0.95)
            top_k = gemini_config.get("top_k", 40)

            # Validate and sanitize values
            if not isinstance(model, str) or not model:
                console.print(
                    "[#d7af00]Warning: Invalid model in configuration. Using default.[/]"
                )
                model = "gemini-2.0-flash"

            if not isinstance(max_output_tokens, int) or max_output_tokens <= 0:
                console.print(
                    "[#d7af00]Warning: Invalid max_output_tokens in configuration. Using default.[/]"
                )
                max_output_tokens = 2048

            if (
                not isinstance(temperature, int | float)
                or temperature < 0
                or temperature > 1
            ):
                console.print(
                    "[#d7af00]Warning: Invalid temperature in configuration. Using default.[/]"
                )
                temperature = 0.7

            if not isinstance(top_p, int | float) or top_p < 0 or top_p > 1:
                console.print(
                    "[#d7af00]Warning: Invalid top_p in configuration. Using default.[/]"
                )
                top_p = 0.95

            if not isinstance(top_k, int) or top_k <= 0:
                console.print(
                    "[#d7af00]Warning: Invalid top_k in configuration. Using default.[/]"
                )
                top_k = 40

            return {
                "model": model,
                "max_output_tokens": max_output_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
            }
        except Exception as e:
            raise WebError(
                message="Failed to load gemini configuration",
                code=ErrorCodes.WEB_CONFIG_ERROR,
                causes=[str(e)],
                hint_stmt="Check your configuration file permissions and format",
            ) from e

    def save_config(
        self,
        model: str,
        max_output_tokens: int,
        temperature: float,
        top_p: float,
        top_k: int,
        silent: bool = False,
    ) -> None:
        """
        Save gemini configuration to yaml file.

        Args:
            model: Model to use for queries
            max_output_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling
            top_p: Top-p for sampling
            top_k: Top-k for sampling
            silent: Whether to suppress success message

        Raises:
            WebError: If configuration cannot be saved

        """
        try:
            # Validate parameters
            if not model:
                raise ValueError("Model cannot be empty")

            if max_output_tokens <= 0:
                raise ValueError("max_output_tokens must be positive")

            if temperature < 0 or temperature > 1:
                raise ValueError("temperature must be between 0 and 1")

            if top_p < 0 or top_p > 1:
                raise ValueError("top_p must be between 0 and 1")

            if top_k <= 0:
                raise ValueError("top_k must be positive")

            # Load existing config
            config = self.config.load_config()

            # Update gemini section
            gemini_config: GeminiConfig = {
                "model": model,
                "max_output_tokens": max_output_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
            }
            config["gemini"] = gemini_config

            # Save updated config
            self.config.save_config(config, silent=silent)
            if not silent:
                console.print("[#5f87ff]Gemini configuration saved successfully[/]")
        except ValueError as e:
            raise WebError(
                message="Invalid configuration values",
                code=ErrorCodes.WEB_CONFIG_ERROR,
                causes=[str(e)],
                hint_stmt="Please provide valid configuration values",
            ) from e
        except Exception as e:
            raise WebError(
                message="Failed to save gemini configuration",
                code=ErrorCodes.WEB_CONFIG_ERROR,
                causes=[str(e)],
                hint_stmt="Check your configuration file permissions",
            ) from e

    def get_client(self, api_key: str) -> genai.Client:
        """
        Get or create Google Gemini client.

        Args:
            api_key: Google Gemini API key

        Returns:
            genai.Client: Google Gemini client

        Raises:
            WebError: If client cannot be created

        """
        if not api_key:
            raise WebError(
                message="API key is required",
                code=ErrorCodes.INVALID_API_KEY,
                causes=["No API key provided"],
                hint_stmt="Please provide a valid Google Gemini API key",
            )

        try:
            # Always create a new client to ensure we're using the correct API key
            self._client = genai.Client(api_key=api_key)
            return self._client
        except ValueError as e:
            raise WebError(
                message="Invalid API key format",
                code=ErrorCodes.INVALID_API_KEY,
                causes=[str(e)],
                hint_stmt="Please check your API key format",
            ) from e
        except Exception as e:
            raise WebError(
                message="Failed to create Google Gemini client",
                code=ErrorCodes.WEB_API_ERROR,
                causes=[str(e)],
                hint_stmt="Check your API key and internet connection",
            ) from e


async def create_client(api_key: str) -> genai.Client:
    """Create a new Google Gemini client."""
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        raise WebError(
            message="Failed to create Google Gemini client",
            code=ErrorCodes.WEB_API_ERROR,
            causes=[str(e)],
            hint_stmt="Check your API key and internet connection",
        ) from e
