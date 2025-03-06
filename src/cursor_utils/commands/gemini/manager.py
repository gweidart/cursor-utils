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
        """Load gemini configuration from yaml file."""
        try:
            config = self.config.load_config()
            gemini_config = config.get("gemini", {})
            if not gemini_config or not all(
                k in gemini_config
                for k in ("model", "max_output_tokens", "temperature", "top_p", "top_k")
            ):
                return None
            return {
                "model": gemini_config["model"],
                "max_output_tokens": gemini_config["max_output_tokens"],
                "temperature": gemini_config["temperature"],
                "top_p": gemini_config["top_p"],
                "top_k": gemini_config["top_k"],
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
    ) -> None:
        """Save gemini configuration to yaml file."""
        try:
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
            self.config.save_config(config)
        except Exception as e:
            raise WebError(
                message="Failed to save gemini configuration",
                code=ErrorCodes.WEB_CONFIG_ERROR,
                causes=[str(e)],
                hint_stmt="Check your configuration file permissions",
            ) from e

    def get_client(self, api_key: str) -> genai.Client:
        """Get or create Google Gemini client."""
        try:
            # Always create a new client to ensure we're using the correct API key
            self._client = genai.Client(api_key=api_key)
            return self._client
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
