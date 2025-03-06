"""
Actions for repository operations.

Key Components:
    clone_and_analyze_repo: Main function for cloning, analyzing and querying Gemini
    clone_repository: Clones a GitHub repository
    collect_file_info: Collects file information for ranking
    prepare_ranking_report: Prepares a structured report about ranked files

Project Dependencies:
    This file uses: file_rank_algo: For file ranking
    This file uses: gemini.actions: For Gemini API interaction
    This file uses: manager: For orchestration
    This file is used by: command: For CLI interface
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from rich.live import Live

from cursor_utils.commands.gemini.actions import (
    ensure_config,
    format_response,
    get_api_key,
    stream_query_with_context,
)
from cursor_utils.commands.repo.manager import RepoManager
from cursor_utils.errors import ErrorCodes, RepoError
from cursor_utils.utils.file_rank_algo import FileInfo, FileRanker, ProcessedFileInfo


def clone_repository(repo_url: str, target_dir: Path) -> None:
    """
    Clone a GitHub repository to a local directory.

    Args:
        repo_url: URL of the GitHub repository
        target_dir: Directory to clone the repository to

    Raises:
        RepoError: If cloning fails

    """
    try:
        subprocess.run(
            ["git", "clone", "--depth=1", repo_url, str(target_dir)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RepoError(
            message="Failed to clone repository",
            code=ErrorCodes.REPO_CLONE_ERROR,
            causes=[str(e.stderr)],
            hint_stmt="Ensure the repository URL is correct and you have internet access.",
        ) from e
    except Exception as e:
        raise RepoError(
            message="An unexpected error occurred during cloning",
            code=ErrorCodes.REPO_CLONE_ERROR,
            causes=[str(e)],
            hint_stmt="Ensure git is installed and available in your PATH.",
        ) from e


def collect_file_info(
    repo_path: Path, exclude_dirs: Optional[list[str]] = None
) -> list[FileInfo]:
    """
    Collect information about all files in the repository.

    Args:
        repo_path: Path to the repository
        exclude_dirs: List of directory names to exclude (e.g., .git, node_modules)

    Returns:
        List of FileInfo dictionaries

    """
    if exclude_dirs is None:
        exclude_dirs = [".git", "node_modules", "__pycache__", ".venv", ".pytest_cache"]

    file_info_list: list[FileInfo] = []

    for root, dirs, files in os.walk(repo_path):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            file_info: FileInfo = {"path": file_path}
            file_info_list.append(file_info)

    return file_info_list


def prepare_ranking_report(ranked_files: list[ProcessedFileInfo]) -> str:
    """
    Prepare a markdown report of the ranked files.

    Args:
        ranked_files: List of ranked file info

    Returns:
        Markdown formatted report

    """
    top_files = ranked_files[: min(50, len(ranked_files))]

    # Group files by type
    file_types: dict[str, list[ProcessedFileInfo]] = {}
    for file in top_files:
        file_type = file["type"]
        if file_type not in file_types:
            file_types[file_type] = []
        file_types[file_type].append(file)

    # Generate report
    report = ["# Repository Analysis Report\n"]
    report.append(f"## Top {len(top_files)} Files by Importance\n")

    for file_type, files in sorted(file_types.items()):
        report.append(f"### {file_type.upper()} Files\n")
        for file in sorted(files, key=lambda x: x["importance_score"], reverse=True):
            relative_path = os.path.basename(file["path"])
            size_kb = file["size"] / 1024
            report.append(
                f"- **{relative_path}** - Size: {size_kb:.2f} KB, "
                f"Score: {file['importance_score']:.2f}\n"
            )
        report.append("\n")

    return "".join(report)


def save_top_files(
    ranked_files: list[ProcessedFileInfo], output_dir: Path, max_size_bytes: int
) -> list[Path]:
    """
    Save the top-ranked files to an output directory, up to the max size limit.

    Args:
        ranked_files: List of ranked file info
        output_dir: Directory to save files to
        max_size_bytes: Maximum total size in bytes

    Returns:
        List of paths to saved files

    """
    output_dir.mkdir(parents=True, exist_ok=True)
    saved_files: list[Path] = []
    total_size = 0

    for file_info in ranked_files:
        if total_size + file_info["size"] > max_size_bytes:
            break

        # Create relative path for destination
        src_path = file_info["path"]
        rel_path = os.path.basename(src_path)
        dest_path = output_dir / rel_path

        # Copy file
        try:
            shutil.copy2(src_path, dest_path)
            saved_files.append(dest_path)
            total_size += file_info["size"]
        except (OSError, shutil.Error):
            # Skip files that can't be copied
            continue

    return saved_files


async def clone_and_analyze_repo(
    repo_url: str,
    query: str,
    max_size_mb: int,
    type_weight: float,
    size_weight: float,
    time_weight: float,
    manager: RepoManager,
    debug: bool = False,
) -> None:
    """
    Clone a GitHub repository, analyze it, and query Gemini with the results.

    Args:
        repo_url: URL of the GitHub repository
        query: Query to send to Gemini
        max_size_mb: Maximum size in MB of files to send to Gemini
        type_weight: Weight for file type importance
        size_weight: Weight for file size importance
        time_weight: Weight for file creation time importance
        manager: RepoManager instance
        debug: Whether to show debug information

    Raises:
        RepoError: If any step fails

    """
    console = manager.console
    max_size_bytes = max_size_mb * 1024 * 1024
    temp_dir = None
    output_dir = None

    try:
        # Get API key
        api_key = get_api_key()

        # Get Gemini configuration
        config = ensure_config(manager.gemini_manager)

        # Create progress display
        with manager.create_progress() as progress:
            # Clone repository
            clone_task = progress.add_task(
                "[#afafd7]Cloning repository[/]...", total=None
            )
            temp_dir = manager.create_temp_dir()
            clone_repository(repo_url, temp_dir)
            progress.update(clone_task, completed=True)

            # Validate repository size
            size_task = progress.add_task(
                "[#afafd7]Checking repository size...[/]", total=None
            )
            manager.validate_repo_size(temp_dir, max_size_mb)
            progress.update(size_task, completed=True)

            # Collect and rank files
            rank_task = progress.add_task(
                "[#afafd7]Ranking files by importance...[/]", total=None
            )
            file_info_list = collect_file_info(temp_dir)

            # Check for .gitignore files
            repo_gitignore = temp_dir / ".gitignore"
            cwd_gitignore = Path.cwd() / ".gitignore"

            # Use local .gitignore if it exists
            gitignore_path = None
            if cwd_gitignore.exists() and cwd_gitignore.is_file():
                if debug:
                    console.print(
                        f"[dim #af87ff]Using local .gitignore: {cwd_gitignore}[/]"
                    )
                gitignore_path = str(cwd_gitignore)
            elif repo_gitignore.exists() and repo_gitignore.is_file():
                if debug:
                    console.print(
                        f"[dim #af87ff]Using repository .gitignore: {repo_gitignore}[/]"
                    )
                gitignore_path = str(repo_gitignore)

            # Rank files
            ranker = FileRanker(
                type_weight=type_weight,
                size_weight=size_weight,
                time_weight=time_weight,
                gitignore_path=gitignore_path,
            )
            ranked_files = ranker.rank_files(file_info_list)
            progress.update(rank_task, completed=True)

            # Prepare output directory
            prep_task = progress.add_task(
                "[#afafd7]Preparing files for analysis...[/]", total=None
            )
            output_dir = Path(tempfile.mkdtemp(prefix="cursor_utils_repo_files_"))

            # Save ranking report
            report = prepare_ranking_report(ranked_files)
            report_path = output_dir / "ranking_report.md"
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report)

            # Save top files up to the size limit
            _ = save_top_files(ranked_files, output_dir, max_size_bytes)
            progress.update(prep_task, completed=True)

        # Craft query with repository analysis
        enhanced_query = (
            f"I've analyzed a GitHub repository and want insights about it. "
            f"The repository is from: {repo_url}\n\n"
            f"User Query: {query}\n\n"
            f"Please use the attached files to provide a detailed analysis."
        )

        # Send to Gemini
        console.print(f"[#afafd7]Querying Gemini about[/] [#5f87ff]{repo_url}[/]...")

        # Send the query with the report file as context
        response_text = ""
        with Live("", refresh_per_second=4) as live:
            async for chunk in stream_query_with_context(
                query=enhanced_query,
                model=config.get("model", "gemini-2.0-pro"),
                max_output_tokens=config.get("max_output_tokens", 2048),
                temperature=config.get("temperature", 0.7),
                top_p=config.get("top_p", 0.95),
                top_k=config.get("top_k", 40),
                api_key=api_key,
                manager=manager.gemini_manager,
                context_file=report_path,
            ):
                if chunk["text"]:
                    response_text += chunk["text"]
                    live.update(format_response(response_text))

    except RepoError:
        # Re-raise RepoError
        raise
    except Exception as e:
        raise RepoError(
            message="Failed to analyze repository",
            code=ErrorCodes.REPO_ANALYZE_ERROR,
            causes=[str(e)],
            hint_stmt="Check your permissions and network connection.",
        ) from e
    finally:
        # Clean up
        manager.cleanup()
        if output_dir:
            try:
                shutil.rmtree(output_dir)
            except Exception:
                if debug:
                    console.print(
                        "[d7af00]Warning: Failed to clean up output directory[/]"
                    )
