"""
Text processing utilities for cursor-utils.

Key Components:
    truncate_text: Truncate text to a maximum length.
    wrap_text: Wrap text to a maximum width.
    strip_ansi: Strip ANSI escape sequences from text.
    highlight_code: Highlight code syntax.

Project Dependencies:
    This file uses: None
    This file is used by: CLI commands and output renderers.
"""

import re
import textwrap
from typing import Optional

from rich.console import Console
from rich.syntax import Syntax, SyntaxTheme
from rich.theme import Theme

# Regular expression for matching ANSI escape sequences.
ANSI_ESCAPE_PATTERN: re.Pattern[str] = re.compile(
    r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length.

    Args:
        text: The text to truncate.
        max_length: The maximum length.
        suffix: The suffix to append if truncated.

    Returns:
        The truncated text.

    """
    if len(text) <= max_length:
        return text

    # Ensure we have room for the suffix.
    if max_length <= len(suffix):
        return suffix[:max_length]

    return text[: max_length - len(suffix)] + suffix


def wrap_text(text: str, width: int = 80) -> str:
    """Wrap text to a maximum width (using textwrap).

    Args:
        text: The text to wrap.
        width: The maximum width.

    Returns:
        The wrapped text.

    """
    return textwrap.fill(text, width=width)


def strip_ansi(text: str) -> str:
    """Strip ANSI escape sequences from text.

    Args:
        text: The text to strip.

    Returns:
        The stripped text.

    """
    return ANSI_ESCAPE_PATTERN.sub("", text)


def highlight_code(
    code: str,
    rich_theme: str | SyntaxTheme,
    language: Optional[str] = None,
    line_numbers: bool = False,
    use_rich: bool = False,
) -> str:
    """Highlight code syntax (with optional Rich support).

    Args:
        code: The code to highlight.
        language: The language for syntax highlighting.
        line_numbers: Whether to include line numbers.
        use_rich: Whether to use Rich for highlighting.
        rich_theme: The Rich theme to use (optional).

    Returns:
        The highlighted code.

    """
    code = code.strip()

    if use_rich:
        if rich_theme:
            custom_theme = Theme.read(str(rich_theme))
            console = Console(theme=custom_theme)
        else:
            console = Console()

        syntax = Syntax(
            code, language or "text", line_numbers=line_numbers, theme=rich_theme
        )
        with console.capture() as capture:
            console.print(syntax)
        return capture.get()

    # Fallback to Markdown if Rich is not used:
    if code.startswith("```") and code.endswith("```"):
        code = code[3:-3].strip()

    if line_numbers:
        lines = code.splitlines()
        width = len(str(len(lines)))
        numbered_lines: list[str] = []  # Explicitly type the list
        for i, line in enumerate(lines, 1):
            numbered_lines.append(f"{i:{width}} | {line}")
        code = "\n".join(numbered_lines)

    lang_str = language or ""
    return f"```{lang_str}\n{code}\n```"
