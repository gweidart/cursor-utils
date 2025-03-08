"""
Error handling for cursor-utils with consistent error types and handling.

Key Components:
    CommandError: Base class for command errors
    ConfigError: Error related to configuration
    ServiceError: Error related to external services
    handle_command_errors: Decorator for handling command errors

Project Dependencies:
    This file uses: None
    This file is used by: CLI commands and core functionality
"""

import asyncio
import functools
import inspect
import sys
from collections.abc import Callable, Coroutine
from enum import Enum, auto
from typing import Any, Optional, TypeVar, Union, cast

T = TypeVar("T", bound=Callable[..., Any])
CommandResult = Union[int, Coroutine[Any, Any, int]]


class ErrorSeverity(Enum):
    """Severity levels for errors."""

    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class CommandError(Exception):
    """Base class for command errors."""

    def __init__(
        self,
        message: str,
        exit_code: int = 1,
        help_text: Optional[str] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
    ):
        self.message = message
        self.exit_code = exit_code
        self.help_text = help_text
        self.severity = severity
        super().__init__(message)


class ConfigError(CommandError):
    """Error related to configuration."""

    def __init__(
        self,
        message: str,
        exit_code: int = 2,
        help_text: Optional[str] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
    ):
        super().__init__(message, exit_code, help_text, severity)


class ServiceError(CommandError):
    """Error related to external services."""

    def __init__(
        self,
        message: str,
        service_name: str,
        exit_code: int = 3,
        help_text: Optional[str] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
    ):
        self.service_name = service_name
        super().__init__(message, exit_code, help_text, severity)


def handle_command_errors(func: T) -> T:
    """
    Decorator to handle command errors consistently.

    Args:
        func: The function to decorate

    Returns:
        The decorated function

    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> int:
        try:
            result = func(*args, **kwargs)

            # Handle async functions
            if inspect.iscoroutine(result):
                try:
                    result = asyncio.run(result)
                except Exception as e:
                    print(f"Error in async execution: {e}", file=sys.stderr)
                    return 1

            if isinstance(result, int):
                return result
            return 0
        except CommandError as e:
            print(f"Error: {e.message}", file=sys.stderr)
            if e.help_text:
                print(f"\nHelp: {e.help_text}", file=sys.stderr)
            return e.exit_code
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 1

    return cast(T, wrapper)
