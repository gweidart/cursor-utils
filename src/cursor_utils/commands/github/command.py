"""
GitHub command implementation for repository management.

Key Components:
    github: Command function for GitHub operations

Project Dependencies:
    This file uses: actions: For command operations
    This file uses: manager: For configuration management
    This file uses: types: For type definitions
    This file is used by: github.__init__: For command registration
"""

from typing import Optional

import rich_click as click
from rich.console import Console

from cursor_utils.commands.github.actions import (
    analyze_repo,
    generate_pr_description,
    setup_repo,
    summarize_issues,
)
from cursor_utils.commands.github.manager import GitHubManager

console = Console()


@click.group(name="github")
@click.pass_context
def github(ctx: click.Context) -> None:
    """GitHub repository management commands.

    Provides AI-powered tools for GitHub repository management.
    """
    ctx.ensure_object(dict)
    ctx.obj["github_manager"] = GitHubManager()


@github.command()
@click.argument("owner", required=False)
@click.argument("repo", required=False)
@click.option("--detailed/--summary", default=False, help="Show detailed analysis")
@click.pass_context
def analyze(
    ctx: click.Context, owner: Optional[str], repo: Optional[str], detailed: bool
) -> None:
    """Analyze a GitHub repository.

    Provides AI-powered insights about the repository structure,
    code quality, and potential improvements.
    """
    manager = ctx.obj["github_manager"]
    analyze_repo(manager, owner, repo, detailed)


@github.command()
@click.argument("owner", required=False)
@click.argument("repo", required=False)
@click.option("--branch", default="main", help="Branch to create PR from")
@click.option("--title", help="PR title")
@click.option("--base", default="main", help="Base branch")
@click.pass_context
def pr(
    ctx: click.Context,
    owner: Optional[str],
    repo: Optional[str],
    branch: str,
    title: Optional[str],
    base: str,
) -> None:
    """Generate a PR description from commits.

    Uses AI to create a comprehensive PR description based on the commits
    between the base branch and the current branch.
    """
    manager = ctx.obj["github_manager"]
    generate_pr_description(manager, owner, repo, branch, title, base)


@github.command()
@click.argument("owner", required=False)
@click.argument("repo", required=False)
@click.option(
    "--state",
    default="open",
    type=click.Choice(["open", "closed", "all"]),
    help="Filter issues by state",
)
@click.option("--label", multiple=True, help="Filter issues by label")
@click.option("--limit", default=10, help="Maximum number of issues to summarize")
@click.pass_context
def issues(
    ctx: click.Context,
    owner: Optional[str],
    repo: Optional[str],
    state: str,
    label: list[str],
    limit: int,
) -> None:
    """Summarize GitHub issues.

    Uses AI to provide a concise summary of repository issues,
    identifying patterns and suggesting solutions.
    """
    manager = ctx.obj["github_manager"]
    summarize_issues(manager, owner, repo, state, label, limit)


@github.command()
@click.argument("name", required=True)
@click.option("--private/--public", default=False, help="Create a private repository")
@click.option("--template", help="Template to use for repository setup")
@click.pass_context
def setup(
    ctx: click.Context, name: str, private: bool, template: Optional[str]
) -> None:
    """Set up a new GitHub repository with best practices.

    Creates a new repository with recommended files and settings,
    including issue templates, PR templates, and GitHub Actions workflows.
    """
    manager = ctx.obj["github_manager"]
    setup_repo(manager, name, private, template)
