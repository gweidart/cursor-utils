"""
Output rendering for cursor-utils with support for different output formats.

Key Components:
    OutputFormat: Enum of supported output formats
    OutputRenderer: Base class for output renderers
    PlainTextRenderer: Renderer for plain text output
    MarkdownRenderer: Renderer for markdown output
    JSONRenderer: Renderer for JSON output
    RichRenderer: Renderer for Rich-enhanced output
    RichBufferedStreamRenderer: Renderer for smooth streaming with Rich
    RichProgressIndicator: Enhanced progress indicator using Rich
    get_renderer: Factory function to get the appropriate renderer
    get_buffered_renderer: Factory function for buffered renderers

Project Dependencies:
    This file uses: errors: For output-related errors
                   rich: For enhanced terminal output
    This file is used by: CLI commands and service clients
"""

import json
import sys
import textwrap
import threading
import time
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Callable, Iterator
from enum import Enum, auto
from typing import Any, Optional, TextIO, TypeVar, Union

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
)
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from cursor_utils.core.errors import CommandError

R = TypeVar('R')  # Define R at the module level


class OutputFormat(Enum):
    """Supported output formats."""

    PLAIN = auto()
    MARKDOWN = auto()
    JSON = auto()
    RICH = auto()


class OutputError(CommandError):
    """Error related to output rendering."""

    def __init__(
        self, message: str, exit_code: int = 4, help_text: Optional[str] = None
    ):
        super().__init__(message, exit_code, help_text)


class ProgressIndicator:  # No changes needed here
    """Progress indicator for long-running operations."""

    def __init__(
        self, message: str = "Processing", chars: str = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏", delay: float = 0.1
    ):
        self.message = message
        self.chars = chars
        self.delay = delay
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._animate)
        self._thread.daemon = True
        self._thread.start()

    def stop(self) -> None:
        if self._thread:
            self._stop_event.set()
            self._thread.join()
            sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
            sys.stdout.flush()

    def _animate(self) -> None:
        i = 0
        while not self._stop_event.is_set():
            char = self.chars[i % len(self.chars)]
            sys.stdout.write(f"\r{self.message} {char}")
            sys.stdout.flush()
            time.sleep(self.delay)
            i += 1


class RichProgressIndicator:  # No changes needed here
    """Enhanced progress indicator using Rich."""

    def __init__(
        self,
        message: str = "Processing",
        transient: bool = True,
        auto_refresh: bool = True,
        refresh_per_second: int = 10,
    ):
        self.message = message
        self.transient = transient
        self.auto_refresh = auto_refresh
        self.refresh_per_second = refresh_per_second
        self._progress: Optional[Progress] = None
        self._task_id: Optional[TaskID] = None

    def start(self) -> None:
        self._progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            SpinnerColumn(),
            TimeRemainingColumn(),
            transient=self.transient,
            auto_refresh=self.auto_refresh,
            refresh_per_second=self.refresh_per_second,
        )
        self._progress.start()
        self._task_id = self._progress.add_task(self.message, total=None)

    def update(
        self,
        advance: Optional[float] = None,
        total: Optional[float] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> None:
        if self._progress and self._task_id is not None:
            self._progress.update(
                task_id=self._task_id,
                advance=advance,
                total=total,
                description=description,
                completed=completed is True,  # Correct way to handle Optional[bool]
            )

    def stop(self) -> None:
        if self._progress:
            self._progress.stop()
            self._progress = None
            self._task_id = None


class OutputRenderer(ABC):
    """Base class for output renderers."""

    def __init__(self, output: TextIO = sys.stdout):
        self.output = output

    @abstractmethod
    def render(self, data: Any) -> None:
        """Render data to the output stream."""

    @abstractmethod
    def render_streaming(self, data_stream: Iterator[Any]) -> None:
        """Render a stream of data."""

    async def render_streaming_async(self, data_stream: AsyncIterator[Any]) -> None:
        """
        Render an async stream (default implementation collects all chunks).
        """
        chunks: list[Any] = []
        async for chunk in data_stream:
            chunks.append(chunk)
        self.render_streaming(iter(chunks))

    def render_with_progress(
        self,
        operation: str,
        callback: Callable[[], R],  # Using the generic callback type
        initial_message: str = "Processing",
    ) -> R:
        indicator = ProgressIndicator(initial_message)
        indicator.start()
        try:
            result = callback()
            return result
        finally:
            indicator.stop()

    def render_error(self, message: str) -> None:
        print(f"Error: {message}", file=self.output)


class PlainTextRenderer(OutputRenderer):
    """Renderer for plain text output."""

    def _render_scalar(self, data: str | int | float | bool) -> None:
        print(str(data), file=self.output)

    def _render_list(self, data: list[Any] | tuple[Any, ...]) -> None:
        for item_value in data:
            print(str(item_value), file=self.output)

    def _render_dict(self, data: dict[Any, Any]) -> None:
        for key_value, value_item in data.items():
            print(f"{key_value}: {value_item}", file=self.output)

    def render(
        self,
        data: Union[str, int, float, bool, list[Any], tuple[Any, ...], dict[Any, Any]],
    ) -> None:
        if isinstance(data, str | int | float | bool):
            self._render_scalar(data)
        elif isinstance(data, list | tuple):
            self._render_list(data)
        elif data is dict:
            self._render_dict(data)
        else:
            try:
                print(str(data), file=self.output)  # Fallback for unexpected types
            except Exception as e:
                raise OutputError(f"Failed to render data as plain text: {e}")

    def render_streaming(self, data_stream: Iterator[Any]) -> None:
        try:
            for data in data_stream:
                if isinstance(data, str):
                    print(data, end="", flush=True, file=self.output)
                else:  # Handle non-string data in stream
                    print(str(data), end="", flush=True, file=self.output)
        except Exception as e:
            raise OutputError(f"Failed to render streaming data as plain text: {e}")

    async def render_streaming_async(
        self, data_stream: AsyncIterator[Any]
    ) -> None:  # Overriding for plain text
        try:
            async for data in data_stream:
                if isinstance(data, str):
                    print(data, end="", flush=True, file=self.output)
                else:  # Handle non-string data in stream
                    print(str(data), end="", flush=True, file=self.output)
        except Exception as e:
            raise OutputError(f"Failed to render streaming data as plain text: {e}")


class MarkdownRenderer(OutputRenderer):
    """Renderer for markdown output."""

    def _render_scalar(self, data: str) -> None:
        print(data, file=self.output)

    def _render_list(self, data: list[Any] | tuple[Any, ...]) -> None:
        for item_value in data:
            print(f"- {item_value!s}", file=self.output)

    def _render_dict(self, data: dict[Any, Any]) -> None:
        for key_value, value_item in data.items():
            print(f"**{key_value!s}**: {value_item!s}", file=self.output)

    def render(
        self, data: Union[str, list[Any], tuple[Any, ...], dict[Any, Any]]
    ) -> None:
        if isinstance(data, str):
            self._render_scalar(data)
        elif isinstance(data, list | tuple):
            self._render_list(data)
        elif data is dict:
            self._render_dict(data)
        else:
            try:
                print(str(data), file=self.output)  # Fallback
            except Exception as e:
                raise OutputError(f"Failed to render data as markdown: {e}")

    def render_streaming(self, data_stream: Iterator[Any]) -> None:
        #  (Same implementation as PlainTextRenderer, could be refactored into a base class)
        try:
            for data in data_stream:
                if isinstance(data, str):
                    print(data, end="", flush=True, file=self.output)
                else:
                    print(str(data), end="", flush=True, file=self.output)
        except Exception as e:
            raise OutputError(f"Failed to render streaming data as markdown: {e}")

    async def render_streaming_async(
        self, data_stream: AsyncIterator[Any]
    ) -> None:  # Overriding for markdown
        try:
            async for data in data_stream:
                if isinstance(data, str):
                    print(data, end="", flush=True, file=self.output)
                else:  # Handle non-string data in stream
                    print(str(data), end="", flush=True, file=self.output)
        except Exception as e:
            raise OutputError(f"Failed to render streaming data as markdown: {e}")


class JSONRenderer(OutputRenderer):
    """Renderer for JSON output."""

    def __init__(self, output: TextIO = sys.stdout, indent: int = 2):
        super().__init__(output)
        self.indent = indent
        self._buffer: list[Any] = []  # Still needed for buffering

    def render(self, data: Any) -> None:
        try:
            json_str = json.dumps(data, indent=self.indent)
            print(json_str, file=self.output)
        except Exception as e:
            raise OutputError(f"Failed to render data as JSON: {e}")

    def render_streaming(self, data_stream: Iterator[Any]) -> None:
        #  (Still buffers everything, as JSON can't be truly streamed)
        try:
            self._buffer = []
            for data in data_stream:
                self._buffer.append(data)
            self.render(self._buffer)
        except Exception as e:
            raise OutputError(f"Failed to render streaming data as JSON: {e}")


class RichRenderer(OutputRenderer):
    """Renderer using Rich."""

    def __init__(self, output: TextIO = sys.stdout):
        super().__init__(output)
        self.console = Console(file=output)

    def _render_string(self, data: str) -> None:
        dedented_data = textwrap.dedent(data)
        if "```" in data or "#" in data or "*" in data or "_" in data:
            self.console.print(Markdown(data))
        elif dedented_data.startswith(("def ", "class ", "import ", "from ")):
            self.console.print(Syntax(dedented_data, "python"))
        else:
            self.console.print(data)

    def _render_list(self, data: list[Any] | tuple[Any, ...]) -> None:
        for item_value in data:
            self.render(item_value)  # Recursive call for nested structures

    def _render_dict(self, data: dict[Any, Any]) -> None:
        table = Table(show_header=True)
        table.add_column("Key")
        table.add_column("Value")
        for key_value, value_item in data.items():
            table.add_row(str(key_value), str(value_item))
        self.console.print(table)

    def render(
        self, data: Union[str, list[Any], tuple[Any, ...], dict[Any, Any]]
    ) -> None:
        if isinstance(data, str):
            self._render_string(data)
        elif isinstance(data, list | tuple):
            self._render_list(data)
        elif data is dict:
            self._render_dict(data)
        else:
            self.console.print(str(data))  # Fallback

    def render_streaming(self, data_stream: Iterator[Any]) -> None:
        # (Using Rich Live for streaming)
        try:
            text = Text()
            with Live(text, console=self.console, refresh_per_second=15) as live:
                for data in data_stream:
                    if isinstance(data, str):
                        text.append(data)
                    else:
                        text.append(str(data))
                    live.update(text)
        except Exception as e:
            raise OutputError(f"Failed to render streaming data with Rich: {e}")

    def render_with_progress(
        self,
        operation: str,
        callback: Callable[[], R],  # Use generic callback type
        initial_message: str = "Processing",
    ) -> R:
        try:
            with Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(initial_message, total=None)
                try:
                    result = callback()
                    progress.update(task, completed=100)  # Mark as complete
                    return result
                finally:
                    if not progress.finished:
                        progress.update(task, completed=True)
        except Exception as e:
            raise OutputError(f"Failed to render progress with Rich: {e}")


class SilentProgressIndicator:  # For BufferedStreamRenderer
    def __init__(self, *args: Any, **kwargs: Any):
        pass

    def start(self):
        pass

    def stop(self):
        pass


class BufferedStreamRenderer(OutputRenderer):
    """Renderer for buffered streaming."""

    def __init__(
        self,
        output: TextIO = sys.stdout,
        buffer_size: int = 5,
        output_rate: float = 0.05,
    ):
        super().__init__(output)
        self.buffer_size = buffer_size
        self.output_rate = output_rate
        self.base_renderer = PlainTextRenderer(output)  # Use PlainTextRenderer

    def render(self, data: Any) -> None:
        self.base_renderer.render(data)  # Delegate to PlainTextRenderer

    def render_streaming(self, data_stream: Iterator[Any]) -> None:
        buffer: list[Any] = []
        indicator = SilentProgressIndicator("Receiving data")  # Use silent indicator
        indicator.start()
        try:
            for _ in range(self.buffer_size):
                try:
                    chunk = next(data_stream)
                    buffer.append(chunk)
                except StopIteration:
                    break
            indicator.stop()
            while buffer:
                chunk = buffer.pop(0)
                print(str(chunk), end="", flush=True, file=self.output)
                time.sleep(self.output_rate)
                try:
                    new_chunk = next(data_stream)
                    buffer.append(new_chunk)
                except StopIteration:
                    pass
        except Exception as e:
            indicator.stop()
            raise OutputError(f"Failed to render streaming data: {e}")


class RichBufferedStreamRenderer(OutputRenderer):
    """Renderer for buffered streaming with Rich."""

    def __init__(
        self,
        output: TextIO = sys.stdout,
        buffer_size: int = 5,
        output_rate: float = 0.05,
        refresh_per_second: int = 15,
    ):
        super().__init__(output)
        self.buffer_size = buffer_size
        self.output_rate = output_rate
        self.refresh_per_second = refresh_per_second
        self.console = Console(file=output)

    def render(
        self, data: Union[str, list[Any], tuple[Any, ...], dict[Any, Any]]
    ) -> None:
        # Delegate to the internal RichRenderer's methods
        if isinstance(data, str):
            self._render_string(data)
        elif isinstance(data, list | tuple):
            self._render_list(data)
        elif data is dict:
            self._render_dict(data)
        else:
            self.console.print(str(data))

    def _render_string(self, data: str) -> None:
        dedented_data = textwrap.dedent(data)
        if "```" in data or "#" in data or "*" in data or "_" in data:
            self.console.print(Markdown(data))
        elif dedented_data.startswith(("def ", "class ", "import ", "from ")):
            self.console.print(Syntax(dedented_data, "python"))
        else:
            self.console.print(data)

    def _render_list(self, data: list[Any] | tuple[Any, ...]) -> None:
        for item_value in data:
            self.render(item_value)  # Recursive call for nested structures

    def _render_dict(self, data: dict[Any, Any]) -> None:
        table = Table(show_header=True)
        table.add_column("Key")
        table.add_column("Value")
        for key_value, value_item in data.items():
            table.add_row(str(key_value), str(value_item))
        self.console.print(table)

    def render_streaming(self, data_stream: Iterator[Any]) -> None:
        buffer: list[Any] = []
        text = Text()
        progress = RichProgressIndicator("Receiving data")
        progress.start()

        try:
            for _ in range(self.buffer_size):
                try:
                    chunk = next(data_stream)
                    buffer.append(chunk)
                except StopIteration:
                    break
            progress.stop()

            with Live(
                text, console=self.console, refresh_per_second=self.refresh_per_second
            ) as live:
                while buffer:
                    chunk = buffer.pop(0)
                    if isinstance(chunk, str):
                        text.append(chunk)
                    else:
                        text.append(str(chunk))
                    live.update(text)
                    time.sleep(self.output_rate)
                    try:
                        new_chunk = next(data_stream)
                        buffer.append(new_chunk)
                    except StopIteration:
                        pass
        except Exception as e:
            progress.stop()
            raise OutputError(f"Failed to render streaming data with Rich: {e}")


def get_renderer(
    format_name: Union[str, OutputFormat] = OutputFormat.PLAIN,
    output: TextIO = sys.stdout,
) -> OutputRenderer:
    if isinstance(format_name, str):
        try:
            format_enum = OutputFormat[format_name.upper()]
        except KeyError:
            raise OutputError(
                f"Unsupported output format: {format_name}",
                help_text=f"Supported formats: {', '.join(f.name.lower() for f in OutputFormat)}",
            )
    else:
        format_enum = format_name

    if format_enum == OutputFormat.PLAIN:
        return PlainTextRenderer(output)
    elif format_enum == OutputFormat.MARKDOWN:
        return MarkdownRenderer(output)
    elif format_enum == OutputFormat.JSON:
        return JSONRenderer(output)
    elif format_enum == OutputFormat.RICH:
        return RichRenderer(output)
    else:
        raise OutputError(
            f"Unsupported output format: {format_enum}",
            help_text=f"Supported formats: {', '.join(f.name.lower() for f in OutputFormat)}",
        )


def get_buffered_renderer(
    format_name: Union[str, OutputFormat] = OutputFormat.PLAIN,
    output: TextIO = sys.stdout,
    buffer_size: int = 5,
    output_rate: float = 0.05,
    refresh_per_second: int = 15,
) -> Union[BufferedStreamRenderer, RichBufferedStreamRenderer]:
    if isinstance(format_name, str):
        try:
            format_enum = OutputFormat[format_name.upper()]
        except KeyError:
            raise OutputError(
                f"Unsupported output format: {format_name}",
                help_text=f"Supported formats: {', '.join(f.name.lower() for f in OutputFormat)}",
            )
    else:
        format_enum = format_name

    if format_enum == OutputFormat.RICH:
        return RichBufferedStreamRenderer(
            output, buffer_size, output_rate, refresh_per_second
        )
    else:
        return BufferedStreamRenderer(output, buffer_size, output_rate)
