"""
Manager module for web command configuration and client management.

Key Components:
    WebManager: Manages configuration and client lifecycle
    create_client: Factory function for client creation

Project Dependencies:
    This file uses: pyplexityai: For API client
    This file uses: types: For type definitions
    This file uses: errors: For standardized error handling
    This file is used by: actions: For client operations
"""

from typing import Any, Optional

from pyplexityai import AsyncPerplexityClient
from rich.console import Console

from cursor_utils.config import Config
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.types import ModelType, ModeType, SearchFocusType, WebConfig

console = Console()


class WebManager:
    """Manager for web command configuration and client lifecycle."""

    def __init__(self) -> None:
        """Initialize web manager."""
        self._client: Optional[AsyncPerplexityClient] = None
        self.config = Config()

    def load_config(self) -> Optional[dict[str, Any | str | None]]:
        """
        Load web configuration from yaml file.

        Returns:
            Optional[WebConfig]: Web configuration if found, None otherwise

        Raises:
            WebError: If configuration cannot be loaded

        """
        try:
            config = self.config.load_config()
            web_config = config.get("web", {})
            if not web_config or not all(
                k in web_config for k in ("model", "mode", "search_focus")
            ):
                return None

            # Validate configuration values
            model = web_config.get("model")
            mode = web_config.get("mode")
            search_focus = web_config.get("search_focus")

            # Check if values are valid
            if model not in [
                "sonar",
                "sonar-pro",
                "sonar-reasoning",
                "sonar-pro-reasoning",
            ]:
                console.print(
                    f"[#d7af00]Warning: Unknown model '{model}' in configuration. Using default.[/]"
                )
                model = "sonar"

            if mode not in ["concise", "copilot"]:
                console.print(
                    f"[#d7af00]Warning: Unknown mode '{mode}' in configuration. Using default.[/]"
                )
                mode = "concise"

            if search_focus not in [
                "internet",
                "scholar",
                "writing",
                "wolfram",
                "youtube",
                "reddit",
            ]:
                console.print(
                    f"[#d7af00]Warning: Unknown search focus '{search_focus}' in configuration. Using default.[/]"
                )
                search_focus = "internet"

            return {
                "model": model,
                "mode": mode,
                "search_focus": search_focus,
            }
        except Exception as e:
            raise WebError(
                message="Failed to load web configuration",
                code=ErrorCodes.WEB_CONFIG_ERROR,
                causes=[str(e)],
                hint_stmt="Check your configuration file permissions and format",
            ) from e

    def save_config(
        self, model: ModelType, mode: ModeType, search_focus: SearchFocusType
    ) -> None:
        """
        Save web configuration to yaml file.

        Args:
            model: Model to use for queries
            mode: Mode to use for queries
            search_focus: Search focus to use for queries

        Raises:
            WebError: If configuration cannot be saved

        """
        try:
            # Load existing config
            config = self.config.load_config()

            # Update web section
            web_config: WebConfig = {
                "model": model,
                "mode": mode,
                "search_focus": search_focus,
            }
            config["web"] = web_config

            # Save updated config
            self.config.save_config(config)
            console.print("[#5f87ff]Web configuration saved successfully[/]")
        except Exception as e:
            raise WebError(
                message="Failed to save web configuration",
                code=ErrorCodes.WEB_CONFIG_ERROR,
                causes=[str(e)],
                hint_stmt="Check your configuration file permissions",
            ) from e

    def get_client(self, api_key: str) -> AsyncPerplexityClient:
        """
        Get or create Perplexity AI client.

        Args:
            api_key: Perplexity API key

        Returns:
            AsyncPerplexityClient: Perplexity AI client

        Raises:
            WebError: If client cannot be created

        """
        if not api_key:
            raise WebError(
                message="API key is required",
                code=ErrorCodes.INVALID_API_KEY,
                causes=["No API key provided"],
                hint_stmt="Please provide a valid Perplexity API key",
            )

        try:
            # Always create a new client to ensure we're using the correct API key
            self._client = AsyncPerplexityClient(api_key=api_key)
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
                message="Failed to create Perplexity AI client",
                code=ErrorCodes.WEB_API_ERROR,
                causes=[str(e)],
                hint_stmt="Check your API key and internet connection",
            ) from e


async def create_client(api_key: str) -> AsyncPerplexityClient:
    """Create a new Perplexity AI client."""
    try:
        return AsyncPerplexityClient(api_key=api_key)
    except Exception as e:
        raise WebError(
            message="Failed to create Perplexity AI client",
            code=ErrorCodes.WEB_API_ERROR,
            causes=[str(e)],
            hint_stmt="Check your API key and internet connection",
        ) from e
