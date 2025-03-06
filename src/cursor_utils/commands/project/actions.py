"""
Performs actions related to analyzing local projects with Gemini.

Key Components:
    collect_file_info(): Collects information about files in the project
    prepare_ranking_report(): Prepares a report of ranked files
    save_top_files(): Saves top-ranked files for analysis
    analyze_project(): Analyzes a local project directory

Project Dependencies:
    This file uses: cursor_utils.utils.file_rank_algo: For file ranking algorithm
    This file uses: cursor_utils.commands.gemini: For Gemini API integration
    This file is used by: command: For CLI interface
"""

import os
from pathlib import Path
from typing import Optional

import pathspec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern
from rich.console import Console

from cursor_utils.commands.gemini.actions import (
    ensure_config,
    format_response,
    get_api_key,
    stream_query_with_context,
)
from cursor_utils.commands.project.manager import ProjectError, ProjectManager
from cursor_utils.errors import ErrorCodes
from cursor_utils.types import GeminiConfig
from cursor_utils.utils.file_rank_algo import FileInfo, FileRanker, ProcessedFileInfo


def is_binary_file(file_path: Path) -> bool:
    """
    Check if a file is binary.

    Args:
        file_path: Path to the file

    Returns:
        bool: True if the file is binary, False otherwise

    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk  # A simple heuristic for binary files
    except Exception:
        return True  # If we can't read the file, assume it's binary


def collect_file_info(
    project_path: Path, exclude_dirs: Optional[list[str]] = None
) -> list[FileInfo]:
    """
    Collect information about files in the project.

    Args:
        project_path: Path to the project directory
        exclude_dirs: Directories to exclude

    Returns:
        List of FileInfo objects

    """
    if exclude_dirs is None:
        exclude_dirs = [
            ".git",
            ".github",
            "node_modules",
            "__pycache__",
            "venv",
            ".venv",
        ]

    # Check for .gitignore file
    gitignore_spec = None
    gitignore_path = project_path / ".gitignore"
    if gitignore_path.exists() and gitignore_path.is_file():
        with open(gitignore_path, "r", encoding="utf-8") as f:
            gitignore_spec = pathspec.PathSpec.from_lines(
                GitWildMatchPattern, f.readlines()
            )

    file_infos: list[FileInfo] = []

    for dirpath, dirnames, filenames in os.walk(project_path):
        # Skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        # Use Path for proper path handling
        dir_path = Path(dirpath)
        rel_dir = (
            dir_path.relative_to(project_path) if dir_path != project_path else Path("")
        )

        # Apply .gitignore patterns to directories
        if gitignore_spec:
            dirnames[:] = [
                d for d in dirnames if not gitignore_spec.match_file(str(rel_dir / d))
            ]

        for filename in filenames:
            file_path = dir_path / filename
            rel_path = file_path.relative_to(project_path)

            # Skip files matching .gitignore patterns
            if gitignore_spec and gitignore_spec.match_file(str(rel_path)):
                continue

            if file_path.is_file():
                try:
                    file_info: FileInfo = {
                        "path": str(file_path),
                        "type": file_path.suffix.lstrip("."),
                        "size": file_path.stat().st_size,
                        "time": file_path.stat().st_mtime,
                    }
                    file_infos.append(file_info)
                except Exception:  # noqa: S110
                    # Skip files that can't be accessed
                    pass

    return file_infos


def prepare_ranking_report(ranked_files: list[ProcessedFileInfo]) -> str:
    """
    Prepare a report of ranked files.

    Args:
        ranked_files: List of ranked files

    Returns:
        Report as string

    """
    report = "Top ranked files:\n\n"

    for i, file_info in enumerate(ranked_files[:20], 1):
        path = Path(file_info["path"])
        report += f"{i}. {path.name} (Score: {file_info['importance_score']:.2f})\n"
        report += f"   - Type: {file_info['type']}\n"
        report += f"   - Size: {file_info['size'] / 1024:.1f} KB\n"
        report += f"   - Path: {path}\n\n"

    return report


def save_top_files(
    ranked_files: list[ProcessedFileInfo], output_dir: Path, max_size_bytes: int
) -> list[Path]:
    """
    Save top-ranked files for analysis.

    Args:
        ranked_files: List of ranked files
        output_dir: Directory to save files
        max_size_bytes: Maximum total size in bytes

    Returns:
        List of saved file paths

    """
    saved_files: list[Path] = []
    total_size = 0
    total_context_size_limit = 2 * 1024 * 1024 * 1024  # 2GB total context size limit

    for file_info in ranked_files:
        if (
            total_size + file_info["size"] > max_size_bytes
            or total_size >= total_context_size_limit
        ):
            break

        try:
            # Skip non-text files or very large files
            if file_info["type"] in ["jpg", "jpeg", "png", "gif", "pdf", "zip", "exe"]:
                continue

            if file_info["size"] > 2 * 1024 * 1024 * 1024:  # Skip files > 2GB
                continue

            # Check if the file is binary
            file_path = Path(file_info["path"])
            if is_binary_file(file_path):
                continue

            # Read the file content
            with open(
                file_info["path"], "r", encoding="utf-8", errors="replace"
            ) as src_file:
                content = src_file.read()

                # Create output file
                relative_path = file_path.relative_to(file_path.parent.parent)
                output_path = output_dir / relative_path
                output_path.parent.mkdir(parents=True, exist_ok=True)

                with open(output_path, "w", encoding="utf-8") as out_file:
                    out_file.write(content)

                saved_files.append(output_path)
                total_size += file_info["size"]
        except Exception:  # noqa: S110
            # Skip files that can't be read or written
            pass

    return saved_files


async def analyze_project(
    project_path: Path,
    query: str,
    max_size_mb: int,
    type_weight: float,
    size_weight: float,
    time_weight: float,
    manager: ProjectManager,
    debug: bool = False,
) -> None:
    """
    Analyzes a local project with Gemini.

    Args:
        project_path: Path to the project
        query: Query for Gemini
        max_size_mb: Maximum size in MB
        type_weight: Weight for file type importance
        size_weight: Weight for file size importance
        time_weight: Weight for file creation time importance
        manager: ProjectManager instance
        debug: Whether to enable debug mode

    Raises:
        ProjectError: If the project is too large or no files are found

    """
    console = Console()
    temp_dir = Path(os.path.expanduser("~/.cursor_utils/temp"))
    temp_dir.mkdir(parents=True, exist_ok=True)
    output_dir = temp_dir / "project_files"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clear the output directory
    for file in output_dir.glob("**/*"):
        if file.is_file():
            file.unlink()

    # Get Gemini API key
    api_key = get_api_key()

    # Context information
    context_file = None
    response_text = ""

    try:
        # Ensure configuration
        config: GeminiConfig = ensure_config(manager.gemini_manager)

        with manager.create_progress() as progress:
            # Check project size
            size_task = progress.add_task("Checking project size...", total=None)
            project_size_mb = manager.validate_project_size(project_path, max_size_mb)  # type: ignore # noqa: F841
            progress.update(size_task, completed=True)

            # Collect file information
            files_task = progress.add_task("Collecting file information...", total=None)
            file_infos = collect_file_info(project_path)

            if not file_infos:
                raise ProjectError(
                    message="No files found in the project",
                    code=ErrorCodes.REPO_TOO_LARGE,  # Using available error code
                    causes=["Project directory may be empty", "Files may be excluded"],
                    hint_stmt="Check if the project directory contains files and they're not excluded.",
                )

            # Rank files by importance
            ranker = FileRanker(
                type_weight=type_weight,
                size_weight=size_weight,
                time_weight=time_weight,
            )
            ranked_files = ranker.rank_files(file_infos)
            progress.update(files_task, completed=True)

            if debug:
                console.print(prepare_ranking_report(ranked_files))

            # Save top files for analysis
            save_task = progress.add_task("Preparing files for analysis...", total=None)
            max_size_bytes = max_size_mb * 1024 * 1024
            saved_files = save_top_files(ranked_files, output_dir, max_size_bytes)
            progress.update(save_task, completed=True)

            if not saved_files:
                raise ProjectError(
                    message="No files could be saved for analysis",
                    code=ErrorCodes.REPO_TOO_LARGE,  # Using available error code
                    causes=[
                        "Files may be binary or non-text",
                        "Files may be too large",
                    ],
                    hint_stmt="Try a different project or adjust the maximum size.",
                )

            # Create a combined context file with the ranking report and the actual file contents
            context_file = temp_dir / "project_context.md"
            with open(context_file, "w", encoding="utf-8") as f:
                # First add the ranking report
                f.write("# Project Analysis Report\n\n")
                f.write(prepare_ranking_report(ranked_files))
                f.write("\n\n## Project Files\n\n")

                # Then add the content of each saved file
                for file_path in saved_files:
                    rel_path = file_path.relative_to(output_dir)
                    f.write(f"### File: {rel_path}\n\n")
                    f.write("```\n")
                    try:
                        with open(
                            file_path, "r", encoding="utf-8", errors="replace"
                        ) as src_file:
                            f.write(src_file.read())
                    except Exception as e:
                        if debug:
                            console.print(
                                f"[#d7af00]Warning: Failed to read file {rel_path}: {e!s}[/]"
                            )
                        f.write(f"*Error reading file {rel_path}*\n\n")
                    f.write("\n```\n\n")

        # Check the size of the combined context file
        context_size = context_file.stat().st_size
        if context_size > 2 * 1024 * 1024 * 1024:  # 2GB
            console.print(
                f"[bold yellow]Warning: Combined context is very large ({context_size / 1024 / 1024 / 1024:.2f} GB). This may exceed Gemini's limits.[/]"
            )

        # Build query with context
        project_query = (
            "I've analyzed a local project and want insights about it. "
            f"User Query: {query}\n\n"
            "Please use the attached files to provide a detailed analysis. "
            "The Project Analysis Report contains an overview of the most important files, "
            "and the other sections contain the actual source code from the project."
        )

        console.print("[#afafd7]Asking Gemini...[/]")
        console.print(f"[dim #af87ff]Query: {query}[/]")

        # Stream response from Gemini
        async for chunk in stream_query_with_context(
            query=project_query,
            model=config["model"],
            max_output_tokens=config["max_output_tokens"],
            temperature=config["temperature"],
            top_p=config["top_p"],
            top_k=config["top_k"],
            api_key=api_key,
            manager=manager.gemini_manager,
            context_file=context_file,
        ):
            if chunk["text"]:
                response_text += chunk["text"]

        # Display response
        if response_text:
            console.print(format_response(response_text))
        else:
            console.print("[#d70000]No response from Gemini[/]")

    except ProjectError:
        raise
    except Exception as e:
        raise ProjectError(
            message=f"Failed to analyze project: {e!s}",
            code=ErrorCodes.GENERAL_ERROR,
            causes=[str(e)],
            hint_stmt="Try again with a different project or query.",
        ) from e
