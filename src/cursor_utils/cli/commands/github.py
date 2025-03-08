"""
GitHub command for cursor-utils.

Key Components:
    github_commands: Commands to interact with GitHub

Project Dependencies:
    This file uses: parser: For command registration
                    github: For GitHub API access
                    output: For rendering results including Rich formatting
    This file is used by: CLI commands package
"""

from dataclasses import dataclass
from typing import Optional

import rich_click as click
from rich.progress import Progress, SpinnerColumn, TextColumn

from cursor_utils.cli.parser import (
    github_group,
    option,
    pass_context,
    print_error,
    print_info,
    print_success,
    validate_required_options,
)
from cursor_utils.core.output import OutputFormat, get_renderer
from cursor_utils.services.github import GitHubClient, GitHubError


@github_group.command(
    name="repo",
    help="Get repository information",
    short_help="Get repo info",
)
@option(
    "--owner",
    required=True,
    help="The repository owner (username or organization)",
    callback=validate_required_options,
)
@option(
    "--repo",
    required=True,
    help="The repository name",
    callback=validate_required_options,
)
@option(
    "--format",
    default="rich",
    help="Output format (plain, markdown, json, rich)",
    show_default=False,
    type=click.Choice(["plain", "markdown", "json", "rich"], case_sensitive=False),
)
def github_repo_command(
    owner: str,
    repo: str,
    format: str = "rich",
) -> int:
    """
    Get detailed information about a GitHub repository.

    This command retrieves information about a GitHub repository, including
    stars, forks, open issues, and more.

    Examples:
        cursor-utils github repo --owner ewels --repo rich-click

        cursor-utils github repo --owner microsoft --repo vscode --format markdown

    """
    # Initialize the client
    client = GitHubClient()

    # Initialize the renderer
    renderer = get_renderer(format)

    # Create a progress indicator
    if format.upper() == OutputFormat.RICH.name:
        with Progress(
            SpinnerColumn(),
            TextColumn(
                f"[bold blue]Getting repository information for [bold cyan]{owner}/{repo}"
            ),
            transient=True,
        ) as progress:
            progress.add_task("fetch")

            try:
                # Get repository information
                repo_info = client.get_repository(owner, repo)

                # Render the repository information
                print_info(
                    f"Repository information for {owner}/{repo}", "GitHub Repository"
                )
                renderer.render(repo_info)
                return 0
            except (GitHubError, ConnectionError, ValueError) as e:
                print_error(f"Error getting repository information: {e}")
                return 1
    else:
        click.echo(f"Getting repository information for {owner}/{repo}...")

        try:
            # Get repository information
            repo_info = client.get_repository(owner, repo)

            # Render the repository information
            renderer.render(repo_info)
            return 0
        except (GitHubError, ConnectionError, ValueError) as e:
            print_error(f"Error getting repository information: {e}")
            return 1


@github_group.command(
    name="issues",
    help="List issues for a repository",
    short_help="List repo issues",
)
@option(
    "--owner",
    required=True,
    help="The repository owner (username or organization)",
    callback=validate_required_options,
)
@option(
    "--repo",
    required=True,
    help="The repository name",
    callback=validate_required_options,
)
@option(
    "--state",
    default="open",
    help="The issue state (open, closed, all)",
    show_default=False,
    type=click.Choice(["open", "closed", "all"], case_sensitive=False),
)
@option(
    "--labels",
    default=None,
    help="Comma-separated list of labels to filter by",
)
@option(
    "--format",
    default="rich",
    help="Output format (plain, markdown, json, rich)",
    show_default=False,
    type=click.Choice(["plain", "markdown", "json", "rich"], case_sensitive=False),
)
def github_issues_command(
    owner: str,
    repo: str,
    state: str = "open",
    labels: Optional[str] = None,
    format: str = "rich",
) -> int:
    """
    List issues for a GitHub repository.

    This command retrieves issues from a GitHub repository with optional
    filtering by state and labels.

    Examples:
        cursor-utils github issues --owner ewels --repo rich-click

        cursor-utils github issues --owner microsoft --repo vscode --state closed

        cursor-utils github issues --owner microsoft --repo vscode --labels bug,documentation

    """
    # Initialize the client
    client = GitHubClient()

    # Initialize the renderer
    renderer = get_renderer(format)

    # Create a progress indicator
    if format.upper() == OutputFormat.RICH.name:
        with Progress(
            SpinnerColumn(),
            TextColumn(f"[bold blue]Getting issues for [bold cyan]{owner}/{repo}"),
            transient=True,
        ) as progress:
            progress.add_task("fetch")

            try:
                # Get issues
                issues = client.get_issues(
                    owner,
                    repo,
                    state=state,
                    labels=labels.split(",") if labels else None,
                )

                # Render the issues
                print_info(f"Issues for {owner}/{repo} ({state})", "GitHub Issues")
                renderer.render(issues)
                return 0
            except (GitHubError, ConnectionError, ValueError) as e:
                print_error(f"Error getting issues: {e}")
                return 1
    else:
        click.echo(f"Getting issues for {owner}/{repo}...")

        try:
            # Get issues
            issues = client.get_issues(
                owner, repo, state=state, labels=labels.split(",") if labels else None
            )

            # Render the issues
            renderer.render(issues)
            return 0
        except (GitHubError, ConnectionError, ValueError) as e:
            print_error(f"Error getting issues: {e}")
            return 1


@github_group.command(
    name="prs",
    help="List pull requests for a repository",
    short_help="List repo PRs",
)
@option(
    "--owner",
    required=True,
    help="The repository owner (username or organization)",
    callback=validate_required_options,
)
@option(
    "--repo",
    required=True,
    help="The repository name",
    callback=validate_required_options,
)
@option(
    "--state",
    default="open",
    help="The pull request state (open, closed, all)",
    show_default=False,
    type=click.Choice(["open", "closed", "all"], case_sensitive=False),
)
@option(
    "--base",
    default=None,
    help="Filter by base branch name",
)
@option(
    "--format",
    default="rich",
    help="Output format (plain, markdown, json, rich)",
    show_default=False,
    type=click.Choice(["plain", "markdown", "json", "rich"], case_sensitive=False),
)
def github_prs_command(
    owner: str,
    repo: str,
    state: str = "open",
    base: Optional[str] = None,
    format: str = "rich",
) -> int:
    """
    List pull requests for a GitHub repository.

    This command retrieves pull requests from a GitHub repository with optional
    filtering by state and base branch.

    Examples:
        cursor-utils github prs --owner ewels --repo rich-click

        cursor-utils github prs --owner microsoft --repo vscode --state closed

        cursor-utils github prs --owner microsoft --repo vscode --base main

    """
    # Initialize the client
    client = GitHubClient()

    # Initialize the renderer
    renderer = get_renderer(format)

    # Create a progress indicator
    if format.upper() == OutputFormat.RICH.name:
        with Progress(
            SpinnerColumn(),
            TextColumn(
                f"[bold blue]Getting pull requests for [bold cyan]{owner}/{repo}"
            ),
            transient=True,
        ) as progress:
            progress.add_task("fetch")

            try:
                # Get pull requests
                prs = client.get_pull_requests(owner, repo, state=state, base=base)

                # Render the pull requests
                print_info(
                    f"Pull requests for {owner}/{repo} ({state})",
                    "GitHub Pull Requests",
                )
                renderer.render(prs)
                return 0
            except (GitHubError, ConnectionError, ValueError) as e:
                print_error(f"Error getting pull requests: {e}")
                return 1
    else:
        click.echo(f"Getting pull requests for {owner}/{repo}...")

        try:
            # Get pull requests
            prs = client.get_pull_requests(owner, repo, state=state, base=base)

            # Render the pull requests
            renderer.render(prs)
            return 0
        except (GitHubError, ConnectionError, ValueError) as e:
            print_error(f"Error getting pull requests: {e}")
            return 1


@dataclass
class IssueParams:
    owner: str
    repo: str
    title: str
    body: str = ""
    labels: Optional[str] = None
    output_format: str = "rich"


@github_group.command(
    name="create-issue",
    help="Create a new issue in a repository",
    short_help="Create issue",
)
@option(
    "--owner",
    required=True,
    help="The repository owner (username or organization)",
    callback=validate_required_options,
)
@option(
    "--repo",
    required=True,
    help="The repository name",
    callback=validate_required_options,
)
@option(
    "--title",
    required=True,
    help="The issue title",
    callback=validate_required_options,
)
@option(
    "--body",
    default="",
    help="The issue body (description)",
)
@option(
    "--labels",
    default=None,
    help="Comma-separated list of labels to apply",
)
@option(
    "--format",
    default="rich",
    help="Output format (plain, markdown, json, rich)",
    show_default=False,
    type=click.Choice(["plain", "markdown", "json", "rich"], case_sensitive=False),
)
def github_create_issue_command(params: IssueParams) -> int:
    """
    Create a new issue in a GitHub repository.

    This command creates a new issue in a GitHub repository with the specified
    title, body, and optional labels.

    Examples:
        cursor-utils github create-issue --owner ewels --repo rich-click \
            --title "Bug report" --body "Description of the bug"

        cursor-utils github create-issue --owner microsoft --repo vscode --title "Feature request" --labels enhancement,feature

    """
    # Initialize the client
    client = GitHubClient()

    # Initialize the renderer
    renderer = get_renderer(params.output_format)

    # Create a progress indicator
    if params.output_format.upper() == OutputFormat.RICH.name:
        with Progress(
            SpinnerColumn(),
            TextColumn(
                f"[bold blue]Creating issue in [bold cyan]{params.owner}/{params.repo}"
            ),
            transient=True,
        ) as progress:
            progress.add_task("create")

            try:
                # Create the issue
                issue = client.create_issue(
                    params.owner,
                    params.repo,
                    title=params.title,
                    body=params.body,
                    labels=params.labels.split(",") if params.labels else None,
                )

                # Render the issue
                print_success(
                    f"Issue created: {issue.number} - {issue.title}", "Issue Created"
                )
                renderer.render(issue)
                return 0
            except (GitHubError, ConnectionError, ValueError) as e:
                print_error(f"Error creating issue: {e}")
                return 1
    else:
        click.echo(f"Creating issue in {params.owner}/{params.repo}...")

        try:
            # Create the issue
            issue = client.create_issue(
                params.owner,
                params.repo,
                title=params.title,
                body=params.body,
                labels=params.labels.split(",") if params.labels else None,
            )

            # Render the issue
            renderer.render(issue)
            return 0
        except (GitHubError, ConnectionError, ValueError) as e:
            print_error(f"Error creating issue: {e}")
            return 1


@github_group.command(
    name="create-pr",
    help="Create a new pull request in a repository",
    short_help="Create PR",
)
@option(
    "--owner",
    required=True,
    help="The repository owner (username or organization)",
    callback=validate_required_options,
)
@option(
    "--repo",
    required=True,
    help="The repository name",
    callback=validate_required_options,
)
@option(
    "--title",
    required=True,
    help="The pull request title",
    callback=validate_required_options,
)
@option(
    "--body",
    default="",
    help="The pull request body (description)",
)
@option(
    "--head",
    required=True,
    help="The name of the branch where your changes are implemented",
    callback=validate_required_options,
)
@option(
    "--base",
    required=True,
    help="The name of the branch you want the changes pulled into",
    callback=validate_required_options,
)
@option(
    "--format",
    default="rich",
    help="Output format (plain, markdown, json, rich)",
    show_default=False,
    type=click.Choice(["plain", "markdown", "json", "rich"], case_sensitive=False),
)
def github_create_pr_command(
    owner: str,
    repo: str,
    title: str,
    body: str = "",
    head: str = "",
    base: str = "",
    format: str = "rich",
) -> int:
    """
    Create a new pull request in a GitHub repository.

    This command creates a new pull request in a GitHub repository with the specified
    title, body, head branch, and base branch.

    Examples:
        cursor-utils github create-pr --owner ewels --repo rich-click --title "Add new feature" --head feature-branch --base main

        cursor-utils github create-pr --owner microsoft --repo vscode --title "Fix bug" --body "This PR fixes a bug" --head bugfix --base main

    """
    # Initialize the client
    client = GitHubClient()

    # Initialize the renderer
    renderer = get_renderer(format)

    # Create a progress indicator
    if format.upper() == OutputFormat.RICH.name:
        with Progress(
            SpinnerColumn(),
            TextColumn(
                f"[bold blue]Creating pull request in [bold cyan]{owner}/{repo}"
            ),
            transient=True,
        ) as progress:
            progress.add_task("create")

            try:
                # Create the pull request
                pr = client.create_pull_request(
                    owner, repo, title=title, body=body, head=head, base=base
                )

                # Render the pull request
                print_success(
                    f"Pull request created: {pr.number} - {pr.title}",
                    "Pull Request Created",
                )
                renderer.render(pr)
                return 0
            except (GitHubError, ConnectionError, ValueError) as e:
                print_error(f"Error creating pull request: {e}")
                return 1
    else:
        click.echo(f"Creating pull request in {owner}/{repo}...")

        try:
            # Create the pull request
            pr = client.create_pull_request(
                owner, repo, title=title, body=body, head=head, base=base
            )

            # Render the pull request
            renderer.render(pr)
            return 0
        except (GitHubError, ConnectionError, ValueError) as e:
            print_error(f"Error creating pull request: {e}")
            return 1


@github_group.command(
    name="help",
    help="Show help for GitHub commands",
    short_help="Show GitHub help",
)
@pass_context
def github_help_command(ctx: click.Context) -> int:
    """
    Show help information for GitHub commands.

    This command displays help information for all GitHub commands.
    """
    click.echo(ctx.get_help())
    return 0
