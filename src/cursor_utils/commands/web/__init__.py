"""
Web command for querying Perplexity AI.

Key Components:
    web: Web command for querying Perplexity AI

Project Dependencies:
    This file uses: pyplexityai: For Perplexity AI API integration
    This file is used by: cli: For command registration
"""

from cursor_utils.commands.web.command import web

__all__ = ["web"]
