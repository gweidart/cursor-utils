"""
Filesystem utilities for cursor-utils.

Key Components:
    ensure_directory: Ensure a directory exists
    get_temp_dir: Get a temporary directory
    read_file: Read a file
    write_file: Write a file
    list_files: List files in a directory
    is_binary_file: Check if a file is binary

Project Dependencies:
    This file uses: errors: For filesystem-related errors
    This file is used by: CLI commands and service clients
"""

import tempfile
from pathlib import Path
from typing import Optional, Union

from cursor_utils.core.errors import CommandError


class FilesystemError(CommandError):
    """Error related to filesystem operations."""

    def __init__(
        self,
        message: str,
        path: Union[str, Path],
        exit_code: int = 5,
        help_text: Optional[str] = None,
    ):
        self.path = str(path)
        super().__init__(message, exit_code, help_text)


def ensure_directory(path: Union[str, Path]) -> Path:
    """
    Ensure a directory exists.

    Args:
        path: The directory path

    Returns:
        The directory path as a Path object

    Raises:
        FilesystemError: If the directory cannot be created

    """
    path_obj = Path(path)
    try:
        path_obj.mkdir(parents=True, exist_ok=True)
        return path_obj
    except Exception as e:
        raise FilesystemError(
            f"Failed to create directory: {e}",
            path,
            help_text="Ensure you have permission to create the directory.",
        )


def get_temp_dir(prefix: str = "cursor_utils_") -> Path:
    """
    Get a temporary directory.

    Args:
        prefix: The prefix for the directory name

    Returns:
        The temporary directory path

    Raises:
        FilesystemError: If the temporary directory cannot be created

    """
    try:
        return Path(tempfile.mkdtemp(prefix=prefix))
    except Exception as e:
        raise FilesystemError(
            f"Failed to create temporary directory: {e}",
            "temp",
            help_text="Ensure you have permission to create temporary files.",
        )


def read_file(path: Union[str, Path], binary: bool = False) -> Union[str, bytes]:
    """
    Read a file.

    Args:
        path: The file path
        binary: Whether to read the file in binary mode

    Returns:
        The file contents

    Raises:
        FilesystemError: If the file cannot be read

    """
    path_obj = Path(path)
    if not path_obj.exists():
        raise FilesystemError(
            f"File not found: {path}", path, help_text="Ensure the file exists."
        )

    try:
        mode = "rb" if binary else "r"
        with open(path_obj, mode) as f:
            return f.read()
    except Exception as e:
        raise FilesystemError(
            f"Failed to read file: {e}",
            path,
            help_text="Ensure you have permission to read the file.",
        )


def write_file(
    path: Union[str, Path], content: Union[str, bytes], binary: bool = False
) -> None:
    """
    Write a file.

    Args:
        path: The file path
        content: The file contents
        binary: Whether to write the file in binary mode

    Raises:
        FilesystemError: If the file cannot be written

    """
    path_obj = Path(path)

    # Ensure the parent directory exists
    ensure_directory(path_obj.parent)

    try:
        mode = "wb" if binary else "w"
        with open(path_obj, mode) as f:
            f.write(content)
    except Exception as e:
        raise FilesystemError(
            f"Failed to write file: {e}",
            path,
            help_text="Ensure you have permission to write to the file.",
        )


def list_files(
    directory: Union[str, Path], pattern: str = "*", recursive: bool = False
) -> list[Path]:
    """
    List files in a directory.

    Args:
        directory: The directory path
        pattern: The glob pattern to match
        recursive: Whether to search recursively

    Returns:
        The list of file paths

    Raises:
        FilesystemError: If the directory cannot be read

    """
    dir_path = Path(directory)
    if not dir_path.exists():
        raise FilesystemError(
            f"Directory not found: {directory}",
            directory,
            help_text="Ensure the directory exists.",
        )

    if not dir_path.is_dir():
        raise FilesystemError(
            f"Not a directory: {directory}",
            directory,
            help_text="Ensure the path is a directory.",
        )

    try:
        if recursive:
            return list(dir_path.glob(f"**/{pattern}"))
        else:
            return list(dir_path.glob(pattern))
    except Exception as e:
        raise FilesystemError(
            f"Failed to list files: {e}",
            directory,
            help_text="Ensure you have permission to read the directory.",
        )


def is_binary_file(path: Union[str, Path]) -> bool:
    """
    Check if a file is binary.

    Args:
        path: The file path

    Returns:
        True if the file is binary, False otherwise

    Raises:
        FilesystemError: If the file cannot be read

    """
    try:
        with open(Path(path), "rb") as f:
            chunk = f.read(1024)
            return b"\0" in chunk
    except Exception as e:
        raise FilesystemError(
            f"Failed to check if file is binary: {e}",
            path,
            help_text="Ensure you have permission to read the file.",
        )
