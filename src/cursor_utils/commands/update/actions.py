"""
Robust update system for cursor-utils package.

Key Components:
    VersionChecker: Handles version comparison and availability checks
    PackageManager: Abstract base class for package managers with concrete implementations
    DirectUpdater: Handles direct package updates without package managers
    UpdateOrchestrator: Coordinates the update process across different methods
    run_update(): Main entry point for update operations

Project Dependencies:
    This file uses: httpx, packaging, importlib: For HTTP requests, version parsing, and module handling
    This file is used by: update.manager: For update orchestration
    This file is used by: version: For version checking functionality
"""

import importlib.util
import platform
import shutil
import subprocess
import sys
from abc import ABC, abstractmethod
from enum import Enum, auto
from pathlib import Path
from typing import ClassVar, Optional, Union

import httpx
from packaging.version import Version, parse

from cursor_utils import __version__
from cursor_utils.errors import ErrorCodes, UpdateError

# Constants
UTILS_TAG = "CURSOR UTILS INTEGRATION"


def get_mdc_content() -> str:
    """Get the content of the .mdc file."""
    try:
        with open(".mdc", "r") as file:
            return file.read()
    except (FileNotFoundError, PermissionError) as e:
        raise UpdateError(
            message="Could not read .mdc file",
            code=ErrorCodes.UPDATE_FAILED,
            causes=[str(e)],
            hint_stmt="Make sure the .mdc file exists and is readable",
        )


class VersionChecker:
    """Handles version checking and comparison."""

    PYPI_URL: ClassVar[str] = "https://pypi.org/pypi/cursor-utils/json"
    REQUEST_TIMEOUT: ClassVar[float] = 10.0  # seconds

    @classmethod
    def get_latest_version(cls) -> str:
        """
        Get the latest version from PyPI.

        Returns:
            str: Latest version string

        Raises:
            UpdateError: If unable to fetch the latest version

        """
        try:
            with httpx.Client(timeout=cls.REQUEST_TIMEOUT) as client:
                response = client.get(cls.PYPI_URL)
                response.raise_for_status()
                data = response.json()
                return data["info"]["version"]
        except Exception as e:
            raise UpdateError(
                message="Could not fetch latest version from PyPI",
                code=ErrorCodes.UPDATE_FAILED,
                causes=[str(e)],
                hint_stmt="Check your internet connection and try again",
            )

    @classmethod
    def is_update_available(cls) -> tuple[bool, Optional[str]]:
        """
        Check if an update is available.

        Returns:
            Tuple[bool, Optional[str]]: (is_update_available, latest_version)

        """
        try:
            current_version = parse(__version__)
            latest_version_str = cls.get_latest_version()
            latest_version = parse(latest_version_str)

            if latest_version > current_version:
                return True, latest_version_str
            return False, None
        except Exception as e:
            raise UpdateError(
                message="Failed to check for updates",
                code=ErrorCodes.UPDATE_FAILED,
                causes=[str(e)],
                hint_stmt="Check your internet connection and try again",
            )

    @classmethod
    def format_update_message(cls, *, current: str, latest: str) -> str:
        """
        Format the update message.

        Args:
            current: Current version string
            latest: Latest version string

        Returns:
            str: Formatted update message

        """
        return (
            f"[bold #d7af00]Update available![/]\n"
            f"[#5f87ff]Current version[/]: [#ff0000]{current}[/]\n"
            f"[#5f87ff]Latest version[/]:  [#00ff00]{latest}[/]"
        )

    @classmethod
    def get_current_version(cls) -> Union[str, Version, None]:
        """
        Extract the current version.

        Returns:
            The current version or None if not found

        Raises:
            UpdateError: If there's an error getting the current version

        """
        try:
            content = get_mdc_content()
            if UTILS_TAG not in content:
                return None

            current_version = parse(__version__)
            latest_version = parse(cls.get_latest_version())
            if current_version >= Version("0.1.0"):
                return current_version
            else:
                raise UpdateError(
                    message="Error getting current version",
                    code=ErrorCodes.UPDATE_FAILED,
                    causes=[
                        f"Current version: {current_version}",
                        f"Latest version: {latest_version}",
                    ],
                    hint_stmt="Check your latest install of Cursor Utils",
                )
        except Exception as e:
            raise UpdateError(
                message="Failed to get current version",
                code=ErrorCodes.UPDATE_FAILED,
                causes=[str(e)],
                hint_stmt="Check your installation of Cursor Utils",
            )

    @classmethod
    def validate_version(cls, version: str) -> bool:
        """
        Validate version string format.

        Args:
            version: Version string to validate

        Returns:
            bool: True if valid, raises exception otherwise

        Raises:
            UpdateError: If version format is invalid

        """
        try:
            major, minor, patch = map(int, version.split("."))
            return all(x >= 0 for x in (major, minor, patch))
        except (ValueError, AttributeError):
            raise UpdateError(
                message=f"Invalid version format: {version}",
                code=ErrorCodes.UPDATE_FAILED,
                causes=[f"Version string '{version}' does not follow the format x.y.z"],
                hint_stmt="Version must be in the format: x.y.z where x, y, z are non-negative integers",
            )

    @classmethod
    def compare_versions(cls, current: str, target: str) -> bool:
        """
        Compare two version strings.

        Args:
            current: Current version string
            target: Target version string

        Returns:
            bool: True if current version is older than target version

        Raises:
            UpdateError: If version format is invalid

        """
        if not cls.validate_version(current) or not cls.validate_version(target):
            raise UpdateError(
                message="Invalid version format",
                code=ErrorCodes.UPDATE_FAILED,
                causes=[f"Current version: {current}", f"Target version: {target}"],
                hint_stmt="Both versions must be in the format: x.y.z where x, y, z are non-negative integers",
            )

        current_parts = list(map(int, current.split(".")))
        target_parts = list(map(int, target.split(".")))

        return current_parts < target_parts


class PackageManagerType(Enum):
    """Supported package manager types."""

    PIP = auto()
    UV = auto()
    PIPX = auto()
    CONDA = auto()


class PackageManager(ABC):
    """Abstract base class for package managers."""

    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        """Check if this package manager is available on the system."""

    @classmethod
    @abstractmethod
    def install_package(
        cls, package_name: str, version: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Install a package using this manager.

        Returns:
            Tuple[bool, str]: (success, message)

        """


class PipManager(PackageManager):
    """Standard pip package manager."""

    @classmethod
    def is_available(cls) -> bool:
        """Check if pip is available."""
        return shutil.which("pip") is not None or shutil.which("pip3") is not None

    @classmethod
    def install_package(
        cls, package_name: str, version: Optional[str] = None
    ) -> tuple[bool, str]:
        """Install a package using pip."""
        package_spec = f"{package_name}=={version}" if version else package_name

        # Determine pip command (pip or pip3)
        pip_cmd = "pip3" if shutil.which("pip3") is not None else "pip"

        # Determine if we should use --user flag (not in venv)
        user_flag: list[str] = []
        if not (
            hasattr(sys, "real_prefix")
            or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
        ):
            user_flag = ["--user"]

        cmd = [
            sys.executable,
            "-m",
            pip_cmd,
            "install",
            "--upgrade",
            *user_flag,
            package_spec,
        ]

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, f"Pip installation failed: {e.stderr}"
        except Exception as e:
            return False, f"Unexpected error during pip installation: {e!s}"


class UVManager(PackageManager):
    """UV package manager."""

    @classmethod
    def is_available(cls) -> bool:
        """Check if UV is available."""
        return shutil.which("uv") is not None

    @classmethod
    def install_package(
        cls, package_name: str, version: Optional[str] = None
    ) -> tuple[bool, str]:
        """Install a package using UV."""
        package_spec = f"{package_name}=={version}" if version else package_name

        # Determine if we should use --user flag (not in venv)
        user_flag: list[str] = []
        if not (
            hasattr(sys, "real_prefix")
            or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
        ):
            user_flag = ["--user"]

        try:
            result = subprocess.run(
                ["uv", "pip", "install", "--upgrade", *user_flag, package_spec],
                check=True,
                capture_output=True,
                text=True,
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, f"UV installation failed: {e.stderr}"
        except Exception as e:
            return False, f"Unexpected error during UV installation: {e!s}"


class PipxManager(PackageManager):
    """Pipx package manager for global tool installation."""

    @classmethod
    def is_available(cls) -> bool:
        """Check if pipx is available."""
        return shutil.which("pipx") is not None

    @classmethod
    def install_package(
        cls, package_name: str, version: Optional[str] = None
    ) -> tuple[bool, str]:
        """Install a package using pipx."""
        if version:
            package_spec = f"{package_name}=={version}"
        else:
            package_spec = package_name

        try:
            # Check if already installed with pipx
            check_result = subprocess.run(
                ["pipx", "list"],
                check=True,
                capture_output=True,
                text=True,
            )

            if package_name in check_result.stdout:
                # Package exists, upgrade it
                result = subprocess.run(
                    ["pipx", "upgrade", package_name],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            else:
                # Install new package
                result = subprocess.run(
                    ["pipx", "install", package_spec],
                    check=True,
                    capture_output=True,
                    text=True,
                )

            return True, result.stdout
        except subprocess.CalledProcessError as e:
            return False, f"Pipx installation failed: {e.stderr}"
        except Exception as e:
            return False, f"Unexpected error during pipx installation: {e!s}"


class DirectUpdater:
    """Handles direct package updates without package managers."""

    @classmethod
    def get_package_location(cls) -> Optional[Path]:
        """
        Get the location of the installed package.

        Returns:
            Optional[Path]: Path to the package or None if not found

        """
        try:
            spec = importlib.util.find_spec("cursor_utils")
            if not spec or not spec.origin:
                return None

            # Get the package directory
            package_path = Path(spec.origin).parent
            return package_path
        except Exception:
            return None

    @classmethod
    def is_editable_install(cls) -> bool:
        """
        Check if this is an editable install.

        Returns:
            bool: True if this is an editable install

        """
        try:
            package_path = cls.get_package_location()
            if not package_path:
                return False

            # Check for common editable install indicators
            path_str = str(package_path)
            return any(
                indicator in path_str
                for indicator in [".egg-link", "src", "-e", ".git"]
            )
        except Exception:
            return False

    @classmethod
    def get_download_url(cls, version: Optional[str] = None) -> str:
        """
        Get the download URL for the specified version or latest.

        Args:
            version: Optional specific version to download

        Returns:
            str: URL to download the package

        Raises:
            UpdateError: If unable to get the download URL

        """
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(VersionChecker.PYPI_URL)
                response.raise_for_status()
                data = response.json()

                if version:
                    # Find specific version
                    if version not in data["releases"]:
                        raise UpdateError(
                            message=f"Version {version} not found on PyPI",
                            code=ErrorCodes.INVALID_VERSION,
                            causes=["Specified version does not exist"],
                            hint_stmt="Check available versions on PyPI",
                        )
                    releases = data["releases"][version]
                else:
                    # Use latest version
                    latest_version = data["info"]["version"]
                    releases = data["releases"][latest_version]

                # Find wheel package for current Python version
                py_version = f"cp{sys.version_info.major}{sys.version_info.minor}"

                # Try to find a compatible wheel
                for release in releases:
                    if (
                        release["packagetype"] == "bdist_wheel"
                        and py_version in release["filename"]
                    ):
                        return release["url"]

                # Fall back to source distribution if wheel not found
                for release in releases:
                    if release["packagetype"] == "sdist":
                        return release["url"]

                raise UpdateError(
                    message="No compatible package found",
                    code=ErrorCodes.UPDATE_FAILED,
                    causes=[
                        "No wheel or source distribution available for your Python version"
                    ],
                    hint_stmt="Try updating with pip manually: pip install --upgrade cursor-utils",
                )
        except httpx.HTTPError as e:
            raise UpdateError(
                message="Failed to fetch package information from PyPI",
                code=ErrorCodes.WEB_CONNECTION_ERROR,
                causes=[str(e)],
                hint_stmt="Check your internet connection and try again",
            )

    @classmethod
    def update_package(cls, version: Optional[str] = None) -> tuple[bool, str]:
        """
        Update the package using direct download method.

        Args:
            version: Optional specific version to install

        Returns:
            Tuple[bool, str]: (success, message)

        """
        # Direct update is complex and risky - for production use,
        # we'll return instructions instead of attempting it
        return False, (
            "Direct update not supported in this version.\n"
            "Please use pip or another package manager to update."
        )


class UpdateOrchestrator:
    """Orchestrates the update process across multiple methods."""

    PACKAGE_MANAGERS: ClassVar[dict[PackageManagerType, type[PackageManager]]] = {
        PackageManagerType.UV: UVManager,
        PackageManagerType.PIP: PipManager,
        PackageManagerType.PIPX: PipxManager,
    }

    @classmethod
    def get_available_managers(cls) -> dict[PackageManagerType, type[PackageManager]]:
        """
        Get all available package managers on the system.

        Returns:
            Dict[PackageManagerType, Type[PackageManager]]: Available package managers

        """
        return {
            manager_type: manager_class
            for manager_type, manager_class in cls.PACKAGE_MANAGERS.items()
            if manager_class.is_available()
        }

    @classmethod
    def is_in_virtual_env(cls) -> bool:
        """
        Check if running in a virtual environment.

        Returns:
            bool: True if in a virtual environment

        """
        return hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
        )

    @classmethod
    def get_environment_info(cls) -> dict[str, str]:
        """
        Get information about the current environment.

        Returns:
            Dict[str, str]: Environment information

        """
        available_managers = cls.get_available_managers()
        manager_names = [m.name for m in available_managers.keys()]

        return {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "in_virtual_env": str(cls.is_in_virtual_env()),
            "available_managers": ", ".join(manager_names) if manager_names else "None",
        }

    @classmethod
    def get_update_instructions(cls, version: Optional[str] = None) -> str:
        """
        Get environment-specific update instructions.

        Args:
            version: Optional specific version to install

        Returns:
            str: Update instructions

        """
        env_info = cls.get_environment_info()
        version_spec = f"=={version}" if version else ""

        instructions = [
            f"To update cursor-utils{version_spec}:",
            "",
        ]

        if env_info["in_virtual_env"] == "True":
            # Virtual environment instructions
            instructions.extend([
                "Since you're in a virtual environment, use:",
                "",
                f"    python -m pip install --upgrade cursor-utils{version_spec}",
            ])

            if "UV" in env_info["available_managers"]:
                instructions.extend([
                    "",
                    "Or with UV:",
                    "",
                    f"    uv pip install --upgrade cursor-utils{version_spec}",
                ])
        else:
            # System installation instructions
            if env_info["platform"] == "Windows":
                instructions.extend([
                    "For Windows, use:",
                    "",
                    f"    pip install --user --upgrade cursor-utils{version_spec}",
                ])

                if "UV" in env_info["available_managers"]:
                    instructions.extend([
                        "",
                        "Or with UV:",
                        "",
                        f"    uv pip install --user --upgrade cursor-utils{version_spec}",
                    ])
            else:
                instructions.extend([
                    f"For {env_info['platform']}, use:",
                    "",
                    f"    pip install --user --upgrade cursor-utils{version_spec}",
                ])

                if "UV" in env_info["available_managers"]:
                    instructions.extend([
                        "",
                        "Or with UV:",
                        "",
                        f"    uv pip install --user --upgrade cursor-utils{version_spec}",
                    ])

        return "\n".join(instructions)

    @classmethod
    def install_package(
        cls,
        package_name: str,
        version: Optional[str] = None,
        preferred_managers: Optional[list[PackageManagerType]] = None,
    ) -> tuple[bool, str, Optional[PackageManagerType]]:
        """
        Install a package using available package managers.

        Args:
            package_name: Name of the package to install
            version: Optional version to install
            preferred_managers: Optional list of preferred managers in order

        Returns:
            Tuple[bool, str, Optional[PackageManagerType]]:
                (success, message, manager_used)

        """
        available_managers = cls.get_available_managers()

        if not available_managers:
            return False, "No package managers available on the system.", None

        # Determine the order to try managers
        if preferred_managers:
            # Try preferred managers first, then others
            manager_order = [
                m for m in preferred_managers if m in available_managers
            ] + [m for m in available_managers if m not in (preferred_managers or [])]
        else:
            # Default order: UV, PIP, PIPX
            manager_order = list(available_managers.keys())

        errors: list[str] = []

        # Try each manager in order
        for manager_type in manager_order:
            manager_class = available_managers[manager_type]
            success, message = manager_class.install_package(package_name, version)

            if success:
                return True, message, manager_type

            errors.append(f"{manager_type.name}: {message}")

        # If we get here, all managers failed
        error_details = "\n".join(errors)
        return False, f"All package managers failed:\n{error_details}", None


def run_update(version: Optional[str] = None) -> None:
    """
    Install a specific version of cursor-utils package using available methods.

    Args:
        version: Optional version to install. If None, installs latest.

    Raises:
        UpdateError: If the installation fails

    """
    try:
        # First, check if update is needed (unless specific version requested)
        if not version:
            try:
                update_available, latest_version = VersionChecker.is_update_available()
                if not update_available:
                    return  # Already up to date
                version = latest_version
            except Exception:  # noqa: S110
                # If version check fails, continue with update attempt
                pass

        # Try package managers if available
        available_managers = UpdateOrchestrator.get_available_managers()
        if available_managers:
            preferred_managers = [PackageManagerType.UV, PackageManagerType.PIP]
            success, _, _ = UpdateOrchestrator.install_package(
                "cursor-utils", version, preferred_managers
            )
            if success:
                return

        # If all automatic methods fail, provide instructions and raise error
        instructions = UpdateOrchestrator.get_update_instructions(version)
        raise UpdateError(
            message=f"Failed to update to version {version or 'latest'}",
            code=ErrorCodes.UPDATE_FAILED,
            causes=[
                "No compatible package manager found or all installation attempts failed"
            ],
            hint_stmt=instructions,
        )
    except UpdateError:
        # Re-raise UpdateError as is
        raise
    except Exception as e:
        # Wrap other exceptions
        raise UpdateError(
            message="Failed to update package",
            code=ErrorCodes.UNKNOWN_ERROR,
            causes=[str(e)],
            hint_stmt=UpdateOrchestrator.get_update_instructions(version),
        )


def run_pip_install(version: str | None = None) -> None:
    """
    Legacy function maintained for backward compatibility.
    Delegates to the new run_update function.

    Args:
        version: Optional version to install

    Raises:
        UpdateError: If the installation fails

    """
    run_update(version)
