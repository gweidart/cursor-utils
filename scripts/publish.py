#!/usr/bin/env python3
"""
Script to build and publish the package to PyPI.

Usage:
    python scripts/publish.py [--test] [--version VERSION]

Options:
    --test      Upload to TestPyPI instead of PyPI
    --version   Specify a version to use (overrides the version in version.py)
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], check: bool = True) -> str:
    """Run a shell command and return its output."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, check=check)
    return result.stdout.strip()


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


def build_package() -> None:
    """Build the package using build."""
    print("Building package...")
    run_command([sys.executable, "-m", "build"])
    print("Package built successfully.")


def publish_package(test: bool = False) -> None:
    """Publish the package to PyPI or TestPyPI."""
    cmd = [sys.executable, "-m", "twine", "upload", "dist/*"]

    if test:
        cmd.extend(["--repository", "testpypi"])

    print(f"Publishing to {'TestPyPI' if test else 'PyPI'}...")
    run_command(cmd)
    print("Package published successfully.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build and publish the package to PyPI"
    )
    parser.add_argument(
        "--test", action="store_true", help="Upload to TestPyPI instead of PyPI"
    )
    parser.add_argument(
        "--version",
        help="Specify a version to use (overrides the version in version.py)",
    )

    args = parser.parse_args()

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("Error: This script must be run from the project root directory.")
        sys.exit(1)

    # Update version if specified
    if args.version:
        update_version(args.version)

    # Clean dist directory
    if Path("dist").exists():
        print("Cleaning dist directory...")
        for file in Path("dist").glob("*"):
            file.unlink()

    # Build the package
    build_package()

    # Publish the package
    publish_package(test=args.test)


if __name__ == "__main__":
    main()
