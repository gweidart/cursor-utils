"""
Installation command for cursor-utils.

Key Components:
    install_command: Command to install cursor-utils

Project Dependencies:
    This file uses: parser: For command registration
                    fs: For filesystem operations
                    config: For configuration management
                    output: For rendering results including Rich formatting
    This file is used by: CLI commands package
"""

import os
import shutil
from pathlib import Path

import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Text

from cursor_utils.cli.parser import (
    command,
    option,
    print_error,
    print_info,
    print_success,
    print_warning,
)
from cursor_utils.core.config import load_configuration
from cursor_utils.utils.fs import ensure_directory, write_file


@command(
    name="install",
    help="Install cursor-utils and set up API keys",
    short_help="Install cursor-utils",
)
@click.argument(
    "path",
    default=".",
    type=click.Path(exists=True),
)
@option(
    "--force",
    is_flag=True,
    help="Force install. Overwrites existing installation.",
)
def install_command(
    path: str = ".",
    force: bool = False,
) -> int:
    """
    Install cursor-utils and set up API keys.

    Args:
        path: The path to install to (default: current directory)
        force: Force overwrite of existing files

    Returns:
        Exit code

    """
    console = Console()

    # Step 1: Create ~/.cursor/rules/ directory if it doesn't exist
    rules_dir = Path.home() / ".cursor" / "rules"
    try:
        print_info(f"Checking if {rules_dir} exists...")
        if not rules_dir.exists():
            print_info(f"Creating {rules_dir}...")
            ensure_directory(rules_dir)
            print_success(f"Created {rules_dir}")
        else:
            print_info(f"{rules_dir} already exists")
    except Exception as e:
        print_error(f"Failed to create {rules_dir}: {e}")
        return 1

    # Step 2: Copy cursor-utils.mdc to ~/.cursor/rules/
    try:
        source_file = (
            Path(__file__).parent.parent.parent / "models" / "cursor-utils.mdc"
        )
        target_file = rules_dir / "cursor-utils.mdc"

        if target_file.exists() and not force:
            overwrite = Confirm.ask(
                f"[yellow]File {target_file} already exists. Overwrite?[/yellow]",
                default=False,
            )
            if not overwrite:
                print_warning(f"Skipping copy of {source_file} to {target_file}")
                print_info("You can use --force to overwrite existing files")
                return 0

        print_info(f"Copying {source_file} to {target_file}...")
        shutil.copy2(source_file, target_file)
        print_success(f"Copied {source_file} to {target_file}")
    except Exception as e:
        print_error(f"Failed to copy cursor-utils.mdc: {e}")
        return 1

    # Step 3: Prompt for API keys
    config = load_configuration()

    # Gemini API key
    gemini_api_key = config.get("gemini_api_key")
    if gemini_api_key:
        print_info("Gemini API key is already configured")
        update_gemini = Confirm.ask(
            "[yellow]Do you want to update the Gemini API key?[/yellow]",
            default=False,
        )
        if update_gemini:
            gemini_api_key = Prompt.ask(
                "[cyan]Enter your Gemini API key[/cyan] (press Enter to skip)",
                password=True,
                default="",
            )
    else:
        print_info("Gemini API key is not configured")
        gemini_api_key = Prompt.ask(
            "[cyan]Enter your Gemini API key[/cyan] (press Enter to skip)",
            password=True,
            default="",
        )

    if gemini_api_key:
        config.set("gemini_api_key", gemini_api_key)
        print_success("Gemini API key configured")
        # Export as environment variable
        os.environ["GEMINI_API_KEY"] = gemini_api_key
    else:
        print_warning("Gemini API key not configured. Some features will be limited.")

    # Perplexity API key
    perplexity_api_key = config.get("perplexity_api_key")
    if perplexity_api_key:
        print_info("Perplexity API key is already configured")
        update_perplexity = Confirm.ask(
            "[yellow]Do you want to update the Perplexity API key?[/yellow]",
            default=False,
        )
        if update_perplexity:
            perplexity_api_key = Prompt.ask(
                "[cyan]Enter your Perplexity API key[/cyan] (press Enter to skip)",
                password=True,
                default="",
            )
    else:
        print_info("Perplexity API key is not configured")
        perplexity_api_key = Prompt.ask(
            "[cyan]Enter your Perplexity API key[/cyan] (press Enter to skip)",
            password=True,
            default="",
        )

    if perplexity_api_key:
        config.set("perplexity_api_key", perplexity_api_key)
        print_success("Perplexity API key configured")
        # Export as environment variable
        os.environ["PERPLEXITY_API_KEY"] = perplexity_api_key
    else:
        print_warning(
            "Perplexity API key not configured. Some features will be limited."
        )

    # GitHub API key
    github_api_key = config.get("github_api_key")
    if github_api_key:
        print_info("GitHub API key is already configured")
        update_github = Confirm.ask(
            "[yellow]Do you want to update the GitHub API key?[/yellow]",
            default=False,
        )
        if update_github:
            github_api_key = Prompt.ask(
                "[cyan]Enter your GitHub API key[/cyan] (press Enter to skip)",
                password=True,
                default="",
            )
    else:
        print_info("GitHub API key is not configured")
        github_api_key = Prompt.ask(
            "[cyan]Enter your GitHub API key[/cyan] (press Enter to skip)",
            password=True,
            default="",
        )

    if github_api_key:
        config.set("github_api_key", github_api_key)
        print_success("GitHub API key configured")
        # Export as environment variable
        os.environ["GITHUB_API_KEY"] = github_api_key
    else:
        print_warning("GitHub API key not configured. Some features will be limited.")

    # Step 4: Create .env file in current directory
    try:
        env_content = ""
        if gemini_api_key:
            env_content += f"GEMINI_API_KEY={gemini_api_key}\n"
        if perplexity_api_key:
            env_content += f"PERPLEXITY_API_KEY={perplexity_api_key}\n"
        if github_api_key:
            env_content += f"GITHUB_API_KEY={github_api_key}\n"

        if env_content:
            env_file = Path(path) / ".env"
            if env_file.exists() and not force:
                overwrite = Confirm.ask(
                    f"[yellow]File {env_file} already exists. Overwrite?[/yellow]",
                    default=False,
                )
                if not overwrite:
                    print_warning(f"Skipping creation of {env_file}")
                    print_info("You can use --force to overwrite existing files")
                else:
                    write_file(env_file, env_content)
                    print_success(f"Created {env_file}")
            else:
                write_file(env_file, env_content)
                print_success(f"Created {env_file}")
        else:
            print_warning("No API keys configured. Skipping .env file creation.")
    except Exception as e:
        print_error(f"Failed to create .env file: {e}")
        return 1

    # Final success message
    console.print(
        Panel(
            Text(
                "cursor-utils has been successfully installed!\n\n"
                "Your Cursor Agents can now use the following tools:\n"
                "  - cursor-utils web: Search the web using Perplexity AI\n"
                "  - cursor-utils gemini: Generate context awarecontent using Google's Gemini AI\n"
                "  - cursor-utils github: Interact with GitHub repositories\n"
                "  - cursor-utils project: Analyze local project code\n"
                "  - cursor-utils repo: Analyze and query remote code repositories\n"
                "  - cursor-utils config: Manage configuration settings\n\n"
                "For more information, run: cursor-utils --help",
                style="green",
            ),
            title="Installation Complete",
            title_align="center",
            border_style="green",
        )
    )

    return 0
