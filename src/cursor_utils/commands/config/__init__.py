"""
Configuration command module for Cursor Utils.

Key Components:
    config: CLI command for managing configuration

Project Dependencies:
    This file uses: command: For CLI interface
    This file is used by: cli: For command registration
"""

from cursor_utils.commands.config.command import config

__all__ = ["config"]
