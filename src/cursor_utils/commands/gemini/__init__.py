"""
Gemini command module for cursor-utils.

Key Components:
    gemini: Command for querying Google Gemini

Project Dependencies:
    This file uses: command: For command implementation
    This file is used by: cli: For command registration
"""

from cursor_utils.commands.gemini.command import gemini

__all__ = ["gemini"]
