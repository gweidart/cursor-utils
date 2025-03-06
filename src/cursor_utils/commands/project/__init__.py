"""
Project command package for cursor-utils.

Key Components:
    project: Command for analyzing local project directories with Gemini

Project Dependencies:
    This file uses: command: For command implementation
    This file is used by: cursor_utils.commands: For command registration
"""

from cursor_utils.commands.project.command import project

__all__ = ["project"]
