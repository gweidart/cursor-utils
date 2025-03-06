"""
Type definitions for cursor-utils.

Key Components:
    ModelType: Type for model selection
    StreamResponse: Type for streaming response
    ConfigDict: Type for configuration dictionary
    GitHubConfig: Type for GitHub command configuration

Project Dependencies:
    This file uses: typing: For type definitions
    This file is used by: commands: For type safety
"""

from typing import Literal, TypedDict

from typing_extensions import NotRequired

# Model types
ModelType = Literal[
    "sonar",
    "sonar-pro",
    "sonar-reasoning",
    "sonar-pro-reasoning",
]

ModeType = Literal[
    "concise",
    "copilot",
]

SearchFocusType = Literal[
    "internet",
    "scholar",
    "writing",
    "wolfram",
    "youtube",
    "reddit",
]


# Configuration dictionary type
class SettingsDict(TypedDict):
    """Type definition for settings configuration."""

    debug: bool
    log_level: str


class WebConfig(TypedDict, total=True):
    """Type definition for web command configuration."""

    model: ModelType
    mode: ModeType
    search_focus: SearchFocusType


class GeminiConfig(TypedDict, total=True):
    """Type definition for Gemini command configuration."""

    model: str
    max_output_tokens: int
    temperature: float
    top_p: float
    top_k: int


class GitHubConfig(TypedDict, total=True):
    """Type definition for GitHub command configuration."""

    token_source: Literal["env", "config"]
    default_owner: str
    default_repo: str
    template_dir: str


class ConfigDict(TypedDict, total=True):
    """Type definition for configuration dictionary."""

    version: str
    settings: SettingsDict
    web: NotRequired[WebConfig]
    gemini: NotRequired[GeminiConfig]
    github: NotRequired[GitHubConfig]
    custom_options: NotRequired[dict[str, str]]


# Stream response type
class StreamResponse(TypedDict, total=True):
    """Type definition for stream response."""

    text: str
    done: bool
