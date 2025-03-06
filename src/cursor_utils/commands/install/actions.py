"""
Pure business logic for installation operations.

Key Components:
    find_mdc_file(): Locates the .mdc file in a project
    check_existing_installation(): Checks if cursor-utils is installed
    get_template_content(): Gets template content for installation
    format_template(): Formats template with version and timestamp
    create_cursor_dir(): Creates .cursor directory
    write_mdc_file(): Writes content to .mdc file

Project Dependencies:
    This file uses: pathlib: For file operations
    This file uses: datetime: For timestamp generation
    This file uses: re: For version extraction
    This file is used by: install.manager: For installation orchestration
"""

import datetime
import re
from pathlib import Path

from cursor_utils import __version__
from cursor_utils.errors import ErrorCodes, InstallError

# Version extraction pattern
VERSION_PATTERN = re.compile(r'version:\s*([0-9]+\.[0-9]+\.[0-9]+)')


def find_mdc_file(project_path: Path) -> Path | None:  # type: ignore
    """
    Find the .mdc file in the project.

    Args:
        project_path: Path to the project root

    Returns:
        Optional[Path]: Path to the .mdc file if found, None otherwise

    Raises:
        InstallError: If project path does not exist

    """
    if not project_path.exists():
        raise InstallError(
            message="Project path does not exist",
            code=ErrorCodes.INVALID_PATH,
            causes=[f"Path {project_path} does not exist"],
            hint_stmt="Ensure the project path exists before installation.",
        )

    mdc_file = project_path / ".cursor" / "rules" / "default.mdc"
    return mdc_file if mdc_file.exists() else None


def check_existing_installation(mdc_file: Path | None) -> tuple[bool, str | None]:  # type: ignore
    """
    Check if cursor-utils is already installed.

    Args:
        mdc_file: Path to the .mdc file

    Returns:
        Tuple[bool, Optional[str]]: (is_installed, current_version)

    Raises:
        InstallError: If .mdc file cannot be read

    """
    if not mdc_file or not mdc_file.exists():
        return False, None

    try:
        content = mdc_file.read_text()

        # Check if this is a cursor-utils file
        if "CURSOR UTILS INTEGRATION" not in content:
            return False, None

        # Extract version using regex
        version_match = VERSION_PATTERN.search(content)
        if version_match:
            return True, version_match.group(1)

        # Fallback to checking if it exists but version can't be determined
        return True, "unknown"
    except Exception as e:
        raise InstallError(
            message="Failed to read .mdc file",
            code=ErrorCodes.FILE_NOT_FOUND,
            causes=[str(e)],
            hint_stmt="Check file permissions and ensure the file is not corrupted.",
        )


def get_template_content() -> str:
    """
    Get the template content for the .mdc file.

    Returns:
        str: Template content

    Raises:
        InstallError: If template cannot be read

    """
    try:
        template_path = (
            Path(__file__).parent.parent.parent / "templates" / "cursor_utils.md"
        )
        return template_path.read_text()
    except Exception as e:
        raise InstallError(
            message="Failed to read template",
            code=ErrorCodes.TEMPLATE_ERROR,
            causes=[str(e)],
            hint_stmt="Ensure the cursor_utils.md template exists in the templates directory.",
        )


def format_template(template_content: str, install_path: Path) -> str:
    """
    Format the template with version information and timestamp.

    Args:
        template_content: Raw template content
        install_path: Path where cursor-utils is being installed

    Returns:
        str: Formatted template content

    Raises:
        InstallError: If template formatting fails

    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_content = template_content.format(
            version=__version__,
            timestamp=timestamp,
            install_path=str(install_path.absolute()),
        )
        return formatted_content
    except Exception as e:
        raise InstallError(
            message="Failed to format template",
            code=ErrorCodes.TEMPLATE_ERROR,
            causes=[str(e)],
            hint_stmt="Ensure the template has valid placeholders for version, timestamp, and install_path.",
        )


def create_cursor_dir(project_dir: Path) -> Path:
    """
    Create the .cursor directory if it doesn't exist.

    Args:
        project_dir: Path to the project root

    Returns:
        Path: Path to the .cursor directory

    Raises:
        InstallError: If directory cannot be created

    """
    cursor_dir = project_dir / ".cursor"
    try:
        if not cursor_dir.exists():
            cursor_dir.mkdir(parents=True)
        return cursor_dir
    except Exception as e:
        raise InstallError(
            message="Failed to create .cursor directory",
            code=ErrorCodes.DIRECTORY_ERROR,
            causes=[str(e)],
            hint_stmt="Check directory permissions and ensure you have write access.",
        )


def write_mdc_file(cursor_dir: Path, content: str) -> None:
    """
    Write content to the .mdc file.

    Args:
        cursor_dir: Path to the .cursor directory
        content: Content to write

    Raises:
        InstallError: If file cannot be written

    """
    # Create rules directory if it doesn't exist
    rules_dir = cursor_dir / "rules"
    try:
        if not rules_dir.exists():
            rules_dir.mkdir(parents=True)
    except Exception as e:
        raise InstallError(
            message="Failed to create rules directory",
            code=ErrorCodes.DIRECTORY_ERROR,
            causes=[str(e)],
            hint_stmt="Check directory permissions and ensure you have write access.",
        )

    # Write to the correct path: .cursor/rules/default.mdc
    mdc_path = rules_dir / "default.mdc"
    try:
        mdc_path.write_text(content)
    except Exception as e:
        raise InstallError(
            message="Failed to write .mdc file",
            code=ErrorCodes.FILE_WRITE_ERROR,
            causes=[str(e)],
            hint_stmt="Check file permissions and ensure you have write access.",
        )
