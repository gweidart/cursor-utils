"""
Handles version management and update checking for Cursor Utils.

Key Components:
    Legacy version functions: Backward compatibility functions that use VersionChecker

Project Dependencies:
    This file uses: commands.update.actions: For version checking functionality
    This file is used by: Various modules for version information
"""

from packaging.version import Version
from rich import print as rprint

from cursor_utils.commands.update.actions import VersionChecker
from cursor_utils.errors import ErrorCodes, UpdateError, VersionError

# Initialize rich console
console = rprint

# Constants
UTILS_TAG = "CURSOR UTILS INTEGRATION"


# Legacy function aliases for backward compatibility
def get_latest_version() -> str:
    """
    Get the latest version from PyPI.

    Returns:
        str: The latest version string

    Raises:
        VersionError: If the latest version could not be determined

    """
    try:
        return VersionChecker.get_latest_version()
    except UpdateError as e:
        # Convert UpdateError to VersionError for backward compatibility
        raise VersionError(
            message=str(e.message),
            code=ErrorCodes.VERSION_ERROR,
            causes=[str(cause) for cause in e.causes] if e.causes else [],
            hint_stmt=str(e.hint_stmt) if e.hint_stmt else None,
        )


def check_for_updates() -> str | None:  # type: ignore
    """Check for available updates.

    Returns the latest version if an update is available, None otherwise.
    """
    try:
        is_available, latest = VersionChecker.is_update_available()
        return latest if is_available else None
    except UpdateError as e:
        # Convert UpdateError to VersionError for backward compatibility
        raise VersionError(
            message=str(e.message),
            code=ErrorCodes.VERSION_ERROR,
            causes=[str(cause) for cause in e.causes] if e.causes else [],
            hint_stmt=str(e.hint_stmt) if e.hint_stmt else None,
        )


def format_update_message(*, current: str, latest: str) -> str:
    """Format the update message."""
    return VersionChecker.format_update_message(current=current, latest=latest)


def get_current_version() -> str | Version | None:
    """Extract the current version from .mdc file content."""
    try:
        return VersionChecker.get_current_version()
    except UpdateError as e:
        # Convert UpdateError to VersionError for backward compatibility
        raise VersionError(
            message=str(e.message),
            code=ErrorCodes.VERSION_ERROR,
            causes=[str(cause) for cause in e.causes] if e.causes else [],
            hint_stmt=str(e.hint_stmt) if e.hint_stmt else None,
        )


def validate_version(version: str) -> bool:
    """Validate version string format."""
    try:
        return VersionChecker.validate_version(version)
    except UpdateError as e:
        # Convert UpdateError to VersionError for backward compatibility
        raise VersionError(
            message=str(e.message),
            code=ErrorCodes.INVALID_VERSION,
            causes=[str(cause) for cause in e.causes] if e.causes else [],
            hint_stmt=str(e.hint_stmt) if e.hint_stmt else None,
        )


def compare_versions(current: str, target: str) -> bool:
    """Compare two version strings.

    Returns True if current version is older than target version.
    """
    try:
        return VersionChecker.compare_versions(current, target)
    except UpdateError as e:
        # Convert UpdateError to VersionError for backward compatibility
        raise VersionError(
            message=str(e.message),
            code=ErrorCodes.INVALID_VERSION,
            causes=[str(cause) for cause in e.causes] if e.causes else [],
            hint_stmt=str(e.hint_stmt) if e.hint_stmt else None,
        )
