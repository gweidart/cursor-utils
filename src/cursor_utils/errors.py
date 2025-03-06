"""
Error handling system for Cursor Utils.

Key Components:
    CursorUtilsError: Base diagnostic error class for all Cursor Utils errors
    InstallError: Diagnostic errors during installation
    UpdateError: Diagnostic errors during updates
    VersionError: Diagnostic errors related to version management
    ConfigError: Diagnostic errors related to configuration
    WebError: Diagnostic errors related to web commands
    RepoError: Diagnostic errors related to repository operations
    GitHubError: Diagnostic errors related to GitHub operations

Project Dependencies:
    This file uses: diagnostic: For structured error handling and reporting
    This file is used by: All command modules for standardized error handling
"""

from enum import Enum
from typing import Optional

from diagnostic import DiagnosticError, DiagnosticStyle


class CursorUtilsError(DiagnosticError):
    """Base diagnostic error class for all Cursor Utils errors."""

    docs_index = "https://github.com/gweidart/cursor-utils/errors/{code}.md"
    style = DiagnosticStyle(
        name="error",
        color="red",
        ascii_symbol="x",
        unicode_symbol="✗",
    )

    def __init__(
        self,
        *,
        message: str,
        code: str,
        causes: list[str],
        hint_stmt: Optional[str] = None,
    ) -> None:
        """Initialize with documentation URL."""
        super().__init__(
            message=message,
            code=code,
            causes=causes,
            hint_stmt=hint_stmt,
        )


class ErrorCodes(str, Enum):
    """Error codes for Cursor Utils."""

    # Install errors
    INVALID_PATH = "install-001"
    FILE_NOT_FOUND = "install-002"
    TEMPLATE_ERROR = "install-003"
    DIRECTORY_ERROR = "install-004"
    FILE_WRITE_ERROR = "install-005"
    ALREADY_INSTALLED = "install-006"

    # Update errors
    UPDATE_FAILED = "update-001"
    UNKNOWN_ERROR = "update-999"

    # Version errors
    VERSION_ERROR = "version-001"
    INVALID_VERSION = "version-002"

    # Config errors
    INVALID_API_KEY = "config-001"
    API_KEY_SAVE_ERROR = "config-002"
    API_KEY_READ_ERROR = "config-003"
    ENV_FILE_ERROR = "config-004"
    CONFIG_FILE_ERROR = "config-005"

    # Web command errors
    WEB_API_ERROR = "web-001"
    WEB_CONFIG_ERROR = "web-002"
    WEB_CONNECTION_ERROR = "web-003"
    WEB_TIMEOUT_ERROR = "web-004"
    WEB_STREAM_ERROR = "web-005"
    WEB_MODEL_ERROR = "web-006"

    # Gemini API errors
    GEMINI_API_ERROR = "gemini-001"
    GEMINI_MODEL_ERROR = "gemini-002"
    GEMINI_API_KEY_ERROR = "gemini-003"
    GEMINI_API_KEY_SAVE_ERROR = "gemini-004"
    GEMINI_FILE_ERROR = "gemini-005"

    # Repository errors
    REPO_CLONE_ERROR = "repo-001"
    REPO_TOO_LARGE = "repo-002"
    REPO_ANALYZE_ERROR = "repo-003"
    REPO_INVALID_URL = "repo-004"
    REPO_FILE_ERROR = "repo-005"

    # GitHub errors
    GITHUB_AUTH_ERROR = "github-001"
    GITHUB_API_ERROR = "github-002"
    GITHUB_REPO_NOT_FOUND = "github-003"
    GITHUB_PERMISSION_ERROR = "github-004"
    GITHUB_RATE_LIMIT = "github-005"

    # Project errors
    PROJECT_TOO_LARGE = "project-001"
    PROJECT_ANALYZE_ERROR = "project-002"
    PROJECT_INVALID_URL = "project-003"
    PROJECT_FILE_ERROR = "project-004"

    # General errors
    GENERAL_ERROR = "general-001"
    GENERAL_FILE_ERROR = "general-002"
    GENERAL_URL_ERROR = "general-003"
    GENERAL_ANALYZE_ERROR = "general-004"
    GENERAL_CLONE_ERROR = "general-005"
    GENERAL_INVALID_URL = "general-006"


class InstallError(CursorUtilsError):
    """Installation-related errors."""

    style = DiagnosticStyle(
        name="install_error", color="red", ascii_symbol="x", unicode_symbol="✗"
    )


class UpdateError(CursorUtilsError):
    """Update-related errors."""

    style = DiagnosticStyle(
        name="update_error", color="yellow", ascii_symbol="!", unicode_symbol="⚠"
    )


class VersionError(CursorUtilsError):
    """Version-related errors."""

    style = DiagnosticStyle(
        name="version_error",
        color="blue",
        ascii_symbol="v",
        unicode_symbol="ℹ",  # noqa: RUF001
    )


class ConfigError(CursorUtilsError):
    """Configuration-related errors."""

    style = DiagnosticStyle(
        name="config_error",
        color="red",
        ascii_symbol="x",
        unicode_symbol="✗",
    )


class WebError(CursorUtilsError):
    """Web command related errors."""

    style = DiagnosticStyle(
        name="web_error",
        color="magenta",
        ascii_symbol="w",
        unicode_symbol="🌐",
    )


class GitHubError(CursorUtilsError):
    """GitHub command related errors."""

    style = DiagnosticStyle(
        name="github_error",
        color="blue",
        ascii_symbol="g",
        unicode_symbol="🐙",
    )


class RepoError(CursorUtilsError):
    """Repository-related errors."""

    style = DiagnosticStyle(
        name="repo_error",
        color="cyan",
        ascii_symbol="r",
        unicode_symbol="📦",
    )


# Error messages
class ErrorMessages:
    """Error messages for cursor-utils."""

    MESSAGES: list[str] = []  # noqa: RUF012

    @classmethod
    def add_message(cls, message: str) -> None:
        """Add a message to the list."""
        cls.MESSAGES.append(message)

    @classmethod
    def get_messages(cls) -> list[str]:
        """Get all messages."""
        return cls.MESSAGES

    @classmethod
    def clear_messages(cls) -> None:
        """Clear all messages."""
        cls.MESSAGES = []
