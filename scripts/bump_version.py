#!/usr/bin/env python3
"""
Script to bump the version in version.py.

Usage:
    python scripts/bump_version.py [major|minor|patch]

Options:
    major   Bump the major version (X.0.0)
    minor   Bump the minor version (0.X.0)
    patch   Bump the patch version (0.0.X) - default
"""

import argparse
import re
import sys
from pathlib import Path


def get_current_version() -> str:
    """Get the current version from version.py."""
    version_file = Path("src/cursor_utils/version.py")
    if not version_file.exists():
        print(f"Error: Version file not found at {version_file}")
        sys.exit(1)

    content = version_file.read_text()
    match = re.search(r'__version__ = "([^"]+)"', content)
    if not match:
        print("Error: Could not find version string in version.py")
        sys.exit(1)

    return match.group(1)


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse a version string into a tuple of (major, minor, patch)."""
    try:
        parts = version.split(".")
        if len(parts) != 3:
            raise ValueError("Version must have three parts: major.minor.patch")

        return tuple(map(int, parts))  # type: ignore
    except Exception as e:
        print(f"Error parsing version '{version}': {e}")
        sys.exit(1)


def bump_version(current: str, part: str) -> str:
    """Bump the version according to the specified part."""
    major, minor, patch = parse_version(current)

    if part == "major":
        return f"{major + 1}.0.0"
    elif part == "minor":
        return f"{major}.{minor + 1}.0"
    elif part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        print(f"Error: Unknown version part '{part}'")
        sys.exit(1)


def update_version(version: str) -> None:
    """Update the version in version.py."""
    version_file = Path("src/cursor_utils/version.py")
    content = version_file.read_text()

    # Update the version
    new_content = re.sub(
        r'__version__ = "[^"]+"', f'__version__ = "{version}"', content
    )

    # Write the updated content
    version_file.write_text(new_content)
    print(f"Updated version to {version} in {version_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump the version in version.py")
    parser.add_argument(
        "part",
        choices=["major", "minor", "patch"],
        default="patch",
        nargs="?",
        help="Which part of the version to bump (default: patch)",
    )

    args = parser.parse_args()

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("Error: This script must be run from the project root directory.")
        sys.exit(1)

    # Get the current version
    current_version = get_current_version()
    print(f"Current version: {current_version}")

    # Bump the version
    new_version = bump_version(current_version, args.part)
    print(f"New version: {new_version}")

    # Update the version
    update_version(new_version)


if __name__ == "__main__":
    main()
