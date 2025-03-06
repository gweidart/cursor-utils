"""
Install command package for Cursor Utils.

Key Components:
    install: CLI command for installing Cursor Utils

Project Dependencies:
    This file uses: command: For CLI interface
    This file is used by: cli: For command registration
"""

from cursor_utils.commands.install.command import install

__all__ = ["install"]
