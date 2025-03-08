"""
Command-line interface for cursor-utils.

Key Components:
    main: Main entry point for the CLI
    commands: Submodule containing command implementations

Project Dependencies:
    This file uses: parser: For parsing command-line arguments
    This file is used by: External callers of the CLI
"""

import sys
from typing import Optional

# Import commands to register them with the CLI
# This import is needed to register all commands
import cursor_utils.cli.commands  # type: ignore # noqa: F401
from cursor_utils.cli.parser import parse_args


def main(args: Optional[list[str]] = None) -> int:
    """
    Main entry point for the cursor-utils CLI.

    Args:
        args: Command-line arguments, or None to use sys.argv

    Returns:
        Exit code

    """
    return parse_args(args)


if __name__ == "__main__":
    sys.exit(main())
