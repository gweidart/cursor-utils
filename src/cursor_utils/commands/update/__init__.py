"""
Update command package.

Key Components:
    update: CLI command for updating Cursor Utils
    run_pip_install: Function to install packages via pip

Project Dependencies:
    This file uses: command: For CLI interface
    This file uses: actions: For update operations
"""

from cursor_utils.commands.update.actions import run_pip_install
from cursor_utils.commands.update.command import update

__all__ = ["run_pip_install", "update"]
