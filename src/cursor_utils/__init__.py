"""
Cursor-Utils: Enhanced capabilities for Cursor IDE users and AI agents.

Key Components:
    cli: Command-line interface for the package
    core: Core functionality including configuration and error handling
    services: External service clients (Gemini, GitHub, Perplexity)
    utils: Utility functions for filesystem, git, and text processing

Project Dependencies:
    This file uses: version: To expose the package version
    This file is used by: External packages importing cursor_utils
"""

from cursor_utils.version import __version__

__all__ = ["__version__"]
