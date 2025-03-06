"""
GitHub command actions.

Key Components:
    ensure_auth: Ensures GitHub authentication
    analyze_repo: Analyzes a GitHub repository
    generate_pr_description: Generates PR description from commits
    summarize_issues: Summarizes GitHub issues
    setup_repo: Sets up a new GitHub repository

Project Dependencies:
    This file uses: PyGithub: For GitHub API integration
    This file uses: manager: For GitHub API access
    This file uses: errors: For standardized error handling
    This file uses: utils.command_helpers: For standardized command execution
    This file is used by: command: For command implementation
"""

from pathlib import Path
from typing import Optional

from github import Github
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from cursor_utils.commands.github.manager import GitHubManager
from cursor_utils.errors import ErrorCodes, GitHubError
from cursor_utils.utils.command_helpers import safe_execute

console = Console()


@safe_execute(GitHubError, ErrorCodes.GITHUB_AUTH_ERROR)
def ensure_auth(manager: GitHubManager) -> Github:
    """
    Ensure GitHub authentication.

    Args:
        manager: GitHub manager instance

    Returns:
        Authenticated GitHub client

    Raises:
        GitHubError: If authentication fails

    """
    return manager.get_github_client()


@safe_execute(GitHubError, ErrorCodes.GITHUB_REPO_ERROR)
def analyze_repo(
    manager: GitHubManager, owner: Optional[str], repo: Optional[str], detailed: bool
) -> None:
    """
    Analyze a GitHub repository.

    Args:
        manager: GitHub manager instance
        owner: Repository owner (username or organization)
        repo: Repository name
        detailed: Whether to show detailed analysis

    Raises:
        GitHubError: If repository analysis fails

    """
    github = ensure_auth(manager)  # type: ignore # noqa: F841
    repository = manager.get_repository(owner, repo)

    with console.status(f"Analyzing repository {repository.full_name}..."):
        # Basic repository info
        table = Table(title=f"Repository: {repository.full_name}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Description", repository.description or "No description")
        table.add_row("Stars", str(repository.stargazers_count))
        table.add_row("Forks", str(repository.forks_count))
        table.add_row("Open Issues", str(repository.open_issues_count))
        table.add_row("Default Branch", repository.default_branch)
        table.add_row("Language", repository.language or "Not specified")
        table.add_row("Created", str(repository.created_at))
        table.add_row("Last Updated", str(repository.updated_at))

        console.print(table)

        if detailed:
            # Get contributors
            contributors_table = Table(title="Top Contributors")
            contributors_table.add_column("Username", style="cyan")
            contributors_table.add_column("Contributions", style="green")

            for contributor in repository.get_contributors()[:10]:
                contributors_table.add_row(
                    contributor.login, str(contributor.contributions)
                )

            console.print(contributors_table)

            # Get languages
            languages = repository.get_languages()
            if languages:
                lang_table = Table(title="Languages")
                lang_table.add_column("Language", style="cyan")
                lang_table.add_column("Bytes", style="green")

                for lang, bytes_count in languages.items():
                    lang_table.add_row(lang, str(bytes_count))

                console.print(lang_table)

                # Get recent commits
                commits_table = Table(title="Recent Commits")
                commits_table.add_column("SHA", style="cyan")
                commits_table.add_column("Author", style="green")
                commits_table.add_column("Message", style="yellow")
                commits_table.add_column("Date", style="blue")

                for commit in repository.get_commits()[:5]:
                    commits_table.add_row(
                        commit.sha[:7],
                        commit.author.login if commit.author else "Unknown",
                        commit.commit.message.split("\n")[0],
                        str(commit.commit.author.date),
                    )

                console.print(commits_table)

                # AI analysis would go here
                console.print(
                    Panel(
                        "AI analysis of repository structure and quality would be generated here",
                        title="AI Analysis",
                    )
                )


@safe_execute(GitHubError, ErrorCodes.GITHUB_REPO_ERROR)
def generate_pr_description(
    manager: GitHubManager,
    owner: Optional[str],
    repo: Optional[str],
    branch: str,
    title: Optional[str],
    base: str,
) -> None:
    """
    Generate a PR description from commits.

    Args:
        manager: GitHub manager instance
        owner: Repository owner (username or organization)
        repo: Repository name
        branch: Branch to create PR from
        title: PR title (optional)
        base: Base branch

    Raises:
        GitHubError: If PR description generation fails

    """
    github = ensure_auth(manager)  # type: ignore # noqa: F841
    repository = manager.get_repository(owner, repo)

    with console.status(f"Generating PR description for {branch}..."):
        # Get commits between base and branch
        comparison = repository.compare(base, branch)

        if not comparison.commits:
            console.print("[yellow]No commits found between branches[/]")
            return

        # Extract commit messages
        commit_messages = [commit.commit.message for commit in comparison.commits]

        # Generate PR title if not provided
        first_line = commit_messages[0].split('\n')[0]
        pr_title = title or f"{branch}: {first_line}"

        # Generate PR description
        description = "## Changes in this PR\n\n"

        # Group commits by type (assuming conventional commits)
        features: list[str] = []
        fixes: list[str] = []
        docs: list[str] = []
        refactors: list[str] = []
        tests: list[str] = []
        other: list[str] = []

        for msg in commit_messages:
            first_line = msg.split("\n")[0]
            if first_line.startswith("feat"):
                features.append(first_line)
            elif first_line.startswith("fix"):
                fixes.append(first_line)
            elif first_line.startswith("docs"):
                docs.append(first_line)
            elif first_line.startswith("refactor"):
                refactors.append(first_line)
            elif first_line.startswith("test"):
                tests.append(first_line)
            else:
                other.append(first_line)

        if features:
            description += "### Features\n\n"
            for feat in features:
                description += f"- {feat}\n"
            description += "\n"

        if fixes:
            description += "### Fixes\n\n"
            for fix in fixes:
                description += f"- {fix}\n"
            description += "\n"

        if docs:
            description += "### Documentation\n\n"
            for doc in docs:
                description += f"- {doc}\n"
            description += "\n"

        if refactors:
            description += "### Refactoring\n\n"
            for refactor in refactors:
                description += f"- {refactor}\n"
            description += "\n"

        if tests:
            description += "### Tests\n\n"
            for test in tests:
                description += f"- {test}\n"
            description += "\n"

        if other:
            description += "### Other\n\n"
            for item in other:
                description += f"- {item}\n"
            description += "\n"

        # Add footer
        description += "\n## Checklist\n\n"
        description += "- [ ] Tests added/updated\n"
        description += "- [ ] Documentation updated\n"
        description += "- [ ] Code follows project style guidelines\n"

        # Display the result
        console.print(
            Panel(f"[#af87ff]PR Title:[/] {pr_title}", title="Generated PR Title")
        )
        console.print(Panel(Markdown(description), title="Generated PR Description"))

        # Offer to create PR
        console.print("\n[#af87ff]To create this PR, run:[/]")
        console.print(
            f'gh pr create --base {base} --head {branch} --title "{pr_title}" --body "$(cat pr_description.md)"'
        )

        # Save description to file
        with open("pr_description.md", "w") as f:
            f.write(description)
        console.print("[#00d700]PR description saved to pr_description.md[/]")


@safe_execute(GitHubError, ErrorCodes.GITHUB_REPO_ERROR)
def summarize_issues(
    manager: GitHubManager,
    owner: Optional[str],
    repo: Optional[str],
    state: str,
    labels: list[str],
    limit: int,
) -> None:
    """
    Summarize GitHub issues.

    Args:
        manager: GitHub manager instance
        owner: Repository owner (username or organization)
        repo: Repository name
        state: Issue state (open, closed, all)
        labels: List of labels to filter by
        limit: Maximum number of issues to summarize

    Raises:
        GitHubError: If issue summarization fails

    """
    github = ensure_auth(manager)  # type: ignore # noqa: F841
    repository = manager.get_repository(owner, repo)

    with console.status(f"Summarizing issues for {repository.full_name}..."):
        # Get issues
        from github.Issue import Issue

        issues: list[Issue] = []

        if labels:
            for issue in repository.get_issues(state=state, labels=labels)[:limit]:
                issues.append(issue)
        else:
            for issue in repository.get_issues(state=state)[:limit]:
                issues.append(issue)

        if not issues:
            console.print("[yellow]No issues found matching criteria[/]")
            return

        # Display issues
        issues_table = Table(title=f"Issues for {repository.full_name}")
        issues_table.add_column("#", style="cyan")
        issues_table.add_column("Title", style="green")
        issues_table.add_column("State", style="yellow")
        issues_table.add_column("Labels", style="blue")
        issues_table.add_column("Created", style="magenta")

        for issue in issues:
            label_str = ", ".join([label.name for label in issue.labels])
            issues_table.add_row(
                str(issue.number),
                issue.title,
                issue.state,
                label_str,
                str(issue.created_at),
            )

        console.print(issues_table)

        # AI summary would go here
        console.print(
            Panel(
                "AI summary of issues would be generated here, identifying patterns and suggesting solutions",
                title="AI Issue Summary",
            )
        )


@safe_execute(GitHubError, ErrorCodes.GITHUB_REPO_ERROR)
def setup_repo(
    manager: GitHubManager, name: str, private: bool, template: Optional[str]
) -> None:
    """
    Set up a new GitHub repository with best practices.

    Args:
        manager: GitHub manager instance
        name: Repository name
        private: Whether to create a private repository
        template: Template to use for repository setup

    Raises:
        GitHubError: If repository setup fails

    """
    github = ensure_auth(manager)
    user = github.get_user()

    with console.status(f"Setting up repository {name}..."):
        # Create repository
        repository = user.create_repo(
            name=name,
            private=private,
            auto_init=True,
            gitignore_template="Python",
            license_template="mit",
        )

        console.print(f"[#00d700]Repository created: {repository.html_url}[/]")

        # Get template directory
        template_dir = None
        if template and manager.github_config:
            base_template_dir = Path(manager.github_config.get("template_dir", ""))
            template_dir = base_template_dir / template

            if not template_dir.exists():
                console.print(
                    f"[#d7af00]Template directory not found: {template_dir}[/]"
                )
                template_dir = None

        # Create standard files
        files_to_create = [
            {
                "path": ".github/ISSUE_TEMPLATE/bug_report.md",
                "content": Path(__file__).parent.parent.parent.parent
                / "templates"
                / "github"
                / "bug_report.md",
            },
            {
                "path": ".github/ISSUE_TEMPLATE/feature_request.md",
                "content": Path(__file__).parent.parent.parent.parent
                / "templates"
                / "github"
                / "feature_request.md",
            },
            {
                "path": ".github/pull_request_template.md",
                "content": Path(__file__).parent.parent.parent.parent
                / "templates"
                / "github"
                / "pull_request_template.md",
            },
            {
                "path": ".github/workflows/python-tests.yml",
                "content": Path(__file__).parent.parent.parent.parent
                / "templates"
                / "github"
                / "python_tests.yml",
            },
            {
                "path": "CONTRIBUTING.md",
                "content": Path(__file__).parent.parent.parent.parent
                / "templates"
                / "github"
                / "contributing.md",
            },
        ]

        for file_info in files_to_create:
            try:
                # Check if file exists in template directory
                content_path = file_info["content"]
                if template_dir:
                    template_file = template_dir / file_info["path"]
                    if template_file.exists():
                        content_path = template_file

                # Read content from file
                content = content_path.read_text()

                # Create file in repository
                repository.create_file(
                    path=file_info["path"],
                    message=f"Add {file_info['path']}",
                    content=content,
                )
                console.print(f"[#00d700]Created file: {file_info['path']}[/]")
            except Exception as e:
                console.print(f"[#d70000]Error creating {file_info['path']}: {e!s}[/]")

        console.print(
            Panel(
                f"Repository {repository.html_url} has been set up with best practices!",
                title="Repository Setup Complete",
            )
        )
