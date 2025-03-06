"""
Common utilities for command implementations.

This module provides standardized error handling and execution patterns for CLI commands.
It helps reduce code duplication and ensures consistent error handling across the application.

Key Components:
    handle_command_error: Centralized error handling for commands
    safe_execute: Execute an async function with standardized error handling
    safe_execute_sync: Execute a synchronous function with standardized error handling

Examples:
    Using safe_execute for async commands:
    ```python
    @safe_execute(WebError, ErrorCodes.WEB_QUERY_ERROR)
    async def async_web(ctx: click.Context, query: str) -> None:
        # Your command implementation here
        pass
    ```

    Using safe_execute_sync for synchronous commands:
    ```python
    @safe_execute_sync(ConfigError, ErrorCodes.CONFIG_FILE_ERROR)
    def execute_config(manager: ConfigManager, show: bool) -> None:
        # Your command implementation here
        pass
    ```

Project Dependencies:
    This file uses: rich: For console output
    This file uses: click: For command context
    This file is used by: commands: For error handling

"""

import functools
from collections.abc import Callable
from typing import Any, Optional, TypeVar, cast

import click
from rich.console import Console

from cursor_utils.errors import CursorUtilsError, ErrorCodes

console = Console()

T = TypeVar('T')
R = TypeVar('R')


def handle_command_error(
    error: Exception,
    ctx: click.Context,
    error_cls: type[CursorUtilsError],
    default_code: ErrorCodes,
    default_message: str = "An unexpected error occurred",
    default_hint: str = "This is likely a bug, please report it",
    debug: bool = False,
) -> None:
    """
    Handle command errors in a standardized way.

    This function provides a centralized way to handle errors in commands.
    It distinguishes between expected errors (instances of error_cls),
    user aborts, and unexpected errors. For unexpected errors, it wraps them
    in the specified error class with the provided default code and message.

    Args:
        error: The exception that was raised
        ctx: Click context
        error_cls: Error class to use for wrapping unexpected errors
        default_code: Default error code to use
        default_message: Default error message
        default_hint: Default hint message
        debug: Whether to print debug information

    Example:
        ```python
        try:
            # Command implementation
        except Exception as e:
            handle_command_error(
                error=e,
                ctx=ctx,
                error_cls=WebError,
                default_code=ErrorCodes.WEB_QUERY_ERROR,
                debug=debug,
            )
        ```

    """
    if isinstance(error, error_cls):
        console.print(str(error))
    elif isinstance(error, click.Abort):
        pass  # User aborted, exit silently
    else:
        # Wrap unexpected errors
        wrapped_error = error_cls(
            message=default_message,
            code=default_code,
            causes=[str(error)],
            hint_stmt=default_hint,
        )
        console.print(str(wrapped_error))

    if debug:
        console.print_exception()

    ctx.exit(1)


def safe_execute(
    error_cls: type[CursorUtilsError],
    default_code: ErrorCodes,
    default_message: str = "An unexpected error occurred",
    default_hint: str = "This is likely a bug, please report it",
) -> Callable[[Callable[..., R]], Callable[..., Optional[R]]]:
    """
    Decorator for safely executing async functions with standardized error handling.

    This decorator wraps an async function with standardized error handling.
    It extracts the Click context from the function arguments and uses it
    to handle errors in a standardized way.

    Args:
        error_cls: Error class to use for wrapping unexpected errors
        default_code: Default error code to use
        default_message: Default error message
        default_hint: Default hint message

    Returns:
        Decorator function

    Example:
        ```python
        @safe_execute(WebError, ErrorCodes.WEB_QUERY_ERROR)
        async def async_web(ctx: click.Context, query: str) -> None:
            # Your command implementation here
            pass
        ```

    """

    def decorator(func: Callable[..., R]) -> Callable[..., Optional[R]]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Optional[R]:
            # Extract ctx and debug from kwargs or use defaults
            ctx = kwargs.get('ctx', None)
            if ctx is None:
                for arg in args:
                    if isinstance(arg, click.Context):
                        ctx = arg
                        break

            if ctx is None:
                raise ValueError("Context not found in arguments")

            debug = getattr(ctx.obj, 'DEBUG', False) if hasattr(ctx, 'obj') else False

            try:
                return func(*args, **kwargs)
            except Exception as e:
                handle_command_error(
                    error=e,
                    ctx=cast(click.Context, ctx),
                    error_cls=error_cls,
                    default_code=default_code,
                    default_message=default_message,
                    default_hint=default_hint,
                    debug=debug,
                )
                return None

        return wrapper

    return decorator


def safe_execute_sync(
    error_cls: type[CursorUtilsError],
    default_code: ErrorCodes,
    default_message: str = "An unexpected error occurred",
    default_hint: str = "This is likely a bug, please report it",
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """
    Decorator for safely executing synchronous functions with standardized error handling.

    This decorator is designed for functions that don't need a Click context.
    It provides standardized error handling for synchronous functions.

    Args:
        error_cls: Error class to use for wrapping unexpected errors
        default_code: Default error code to use
        default_message: Default error message
        default_hint: Default hint message

    Returns:
        Decorator function

    Example:
        ```python
        @safe_execute_sync(ConfigError, ErrorCodes.CONFIG_FILE_ERROR)
        def execute_config(manager: ConfigManager, show: bool) -> None:
            # Your command implementation here
            pass
        ```

    """

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            debug = kwargs.get('debug', False)

            try:
                return func(*args, **kwargs)
            except error_cls as e:
                console.print(f"[#d70000]✗[/#d70000] {e!s}")
                if debug:
                    console.print_exception()
                raise click.exceptions.Exit(1)
            except Exception as e:
                wrapped_error = error_cls(
                    message=default_message,
                    code=default_code,
                    causes=[str(e)],
                    hint_stmt=default_hint,
                )
                console.print(f"[#d70000]✗[/#d70000] {wrapped_error!s}")
                if debug:
                    console.print_exception()
                raise click.exceptions.Exit(1)

        return wrapper

    return decorator
