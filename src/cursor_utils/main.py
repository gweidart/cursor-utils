"""
Main entry point for cursor-utils.

Key Components:
    main: Main entry point for the package

Project Dependencies:
    This file uses: cli: For the command-line interface
    This file is used by: External callers of the package
"""

import sys
from typing import Optional

from cursor_utils.cli import main as cli_main


def main(args: Optional[list[str]] = None) -> int:
    """
    Main entry point for cursor-utils.

    Args:
        args: Command-line arguments, or None to use sys.argv

    Returns:
        Exit code

    """
    return cli_main(args)


if __name__ == "__main__":
    sys.exit(main())
