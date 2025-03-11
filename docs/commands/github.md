## GitHub Command

The `github` command provides a suite of tools for interacting with GitHub repositories directly from the terminal, enabling efficient repository management, issue tracking, and pull request handling without switching to a browser.

### Syntax

```bash
cursor-utils github SUBCOMMAND [OPTIONS]
```

### Subcommands

| Subcommand | Description | Syntax |
|------------|-------------|--------|
| `repo` | Get repository information | `cursor-utils github repo [OPTIONS]` |
| `issues` | List repository issues | `cursor-utils github issues [OPTIONS]` |
| `prs` | List repository pull requests | `cursor-utils github prs [OPTIONS]` |
| `create-issue` | Create a new issue | `cursor-utils github create-issue [OPTIONS]` |
| `create-pr` | Create a new pull request | `cursor-utils github create-pr [OPTIONS]` |
| `help` | Show GitHub command help | `cursor-utils github help [SUBCOMMAND]` |

### Common Options

These options apply to most GitHub subcommands:

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--owner` | Repository owner (username or organization) | None (Required) | `--owner microsoft` |
| `--repo` | Repository name | None (Required) | `--repo vscode` |
| `--format` | Output format (plain, markdown, json, rich) | `rich` | `--format json` |
| `--help` | Show subcommand help | - | `--help` |

### Configuration

Before using the `github` command, you need to set up your GitHub personal access token:

```bash
cursor-utils config set github_token YOUR_GITHUB_TOKEN
```

You can create a personal access token at [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens). Ensure your token has the appropriate scopes for the operations you want to perform.

### Subcommand Details

### Repository Information (`repo`)

Get detailed information about a GitHub repository.

#### Syntax

```bash
cursor-utils github repo --owner OWNER --repo REPO [OPTIONS]
```

#### Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--owner` | Repository owner | None (Required) | `--owner microsoft` |
| `--repo` | Repository name | None (Required) | `--repo vscode` |
| `--format` | Output format | `rich` | `--format json` |

#### Example

```bash
cursor-utils github repo --owner microsoft --repo vscode
```

### List Issues (`issues`)

List issues in a GitHub repository with filtering options.

#### Syntax

```bash
cursor-utils github issues --owner OWNER --repo REPO [OPTIONS]
```

#### Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--owner` | Repository owner | None (Required) | `--owner microsoft` |
| `--repo` | Repository name | None (Required) | `--repo vscode` |
| `--state` | Issue state (open, closed, all) | `open` | `--state closed` |
| `--limit` | Maximum number of issues to return | `10` | `--limit 20` |
| `--labels` | Filter by labels (comma-separated) | None | `--labels bug,enhancement` |
| `--assignee` | Filter by assignee | None | `--assignee username` |
| `--format` | Output format | `rich` | `--format markdown` |

#### Examples

List open issues:

```bash
cursor-utils github issues --owner microsoft --repo vscode
```

List closed issues with specific labels:

```bash
cursor-utils github issues --owner microsoft --repo vscode --state closed --labels bug,critical
```

### List Pull Requests (`prs`)

List pull requests in a GitHub repository with filtering options.

#### Syntax

```bash
cursor-utils github prs --owner OWNER --repo REPO [OPTIONS]
```

#### Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--owner` | Repository owner | None (Required) | `--owner microsoft` |
| `--repo` | Repository name | None (Required) | `--repo vscode` |
| `--state` | PR state (open, closed, all) | `open` | `--state closed` |
| `--limit` | Maximum number of PRs to return | `10` | `--limit 20` |
| `--base` | Base branch filter | None | `--base main` |
| `--head` | Head branch filter | None | `--head feature-branch` |
| `--format` | Output format | `rich` | `--format json` |

#### Examples

List open pull requests:

```bash
cursor-utils github prs --owner microsoft --repo vscode
```

List PRs for a specific branch:

```bash
cursor-utils github prs --owner microsoft --repo vscode --head feature-branch
```

### Create Issue (`create-issue`)

Create a new issue in a GitHub repository.

#### Syntax

```bash
cursor-utils github create-issue --owner OWNER --repo REPO --title TITLE [OPTIONS]
```

#### Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--owner` | Repository owner | None (Required) | `--owner your-username` |
| `--repo` | Repository name | None (Required) | `--repo your-repo` |
| `--title` | Issue title | None (Required) | `--title "Bug: Application crashes"` |
| `--body` | Issue body/description | None | `--body "The application crashes when..."` |
| `--labels` | Issue labels (comma-separated) | None | `--labels bug,critical` |
| `--assignees` | Assignees (comma-separated) | None | `--assignees username1,username2` |
| `--format` | Output format | `rich` | `--format json` |

#### Examples

Create a simple issue:

```bash
cursor-utils github create-issue --owner your-username --repo your-repo --title "Bug: Login page not working"
```

Create a detailed issue with labels and assignees:

```bash
cursor-utils github create-issue --owner your-username --repo your-repo --title "Feature Request: Dark Mode" --body "Please add dark mode support to improve accessibility and user experience." --labels enhancement,ui --assignees ui-team
```

### Create Pull Request (`create-pr`)

Create a new pull request in a GitHub repository.

#### Syntax

```bash
cursor-utils github create-pr --owner OWNER --repo REPO --title TITLE --head HEAD --base BASE [OPTIONS]
```

#### Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--owner` | Repository owner | None (Required) | `--owner your-username` |
| `--repo` | Repository name | None (Required) | `--repo your-repo` |
| `--title` | PR title | None (Required) | `--title "Add dark mode"` |
| `--head` | Head branch | None (Required) | `--head feature-branch` |
| `--base` | Base branch | None (Required) | `--base main` |
| `--body` | PR description | None | `--body "This PR implements..."` |
| `--draft` | Mark as draft PR | `false` | `--draft` |
| `--reviewers` | Requested reviewers (comma-separated) | None | `--reviewers username1,username2` |
| `--format` | Output format | `rich` | `--format json` |

#### Examples

Create a simple pull request:

```bash
cursor-utils github create-pr --owner your-username --repo your-repo --title "Fix login bug" --head bugfix-login --base main
```

Create a detailed draft pull request with reviewers:

```bash
cursor-utils github create-pr --owner your-username --repo your-repo --title "Implement dark mode" --head feature-dark-mode --base develop --body "This PR implements dark mode according to the design specs in issue #42." --draft --reviewers design-lead,frontend-lead
```

### Use Cases

### Repository Management

- Quickly check repository information:
  ```bash
  cursor-utils github repo --owner microsoft --repo vscode
  ```

- Monitor open issues and PRs:
  ```bash
  cursor-utils github issues --owner your-username --repo your-repo
  cursor-utils github prs --owner your-username --repo your-repo
  ```

### Issue Tracking

- Find specific issues:
  ```bash
  cursor-utils github issues --owner facebook --repo react --labels bug,high-priority
  ```

- Create issues from the terminal:
  ```bash
  cursor-utils github create-issue --owner your-username --repo your-repo --title "Bug: Form validation fails" --labels bug
  ```

### Pull Request Workflow

- Check PR status:
  ```bash
  cursor-utils github prs --owner your-username --repo your-repo --state open
  ```

- Create a PR after completing a feature:
  ```bash
  cursor-utils github create-pr --owner your-username --repo your-repo --title "Add user settings page" --head feature-user-settings --base main
  ```

### Advanced Techniques

### Complex Filtering

Combine multiple filters for precise results:

```bash
cursor-utils github issues --owner kubernetes --repo kubernetes --state open --labels bug,critical --limit 50
```

### Output Processing

Use with other command-line tools for further processing:

```bash
# Extract issue numbers and titles
cursor-utils github issues --owner microsoft --repo vscode --format json | jq '.[] | {number: .number, title: .title}'
```

#### Automation

Use in scripts for automation:

```bash
#!/bin/bash

# Generate changelog and create a release PR
CHANGES=$(cursor-utils gemini "Generate a changelog for the features and fixes in the following commits: $(git log --oneline origin/main..HEAD)")

cursor-utils github create-pr --owner your-username --repo your-repo --title "Release v1.2.0" --head develop --base main --body "$CHANGES"
```

### Best Practices

1. **Use Authentication**: Always set up your GitHub token for full functionality
   ```bash
   cursor-utils config set github_token YOUR_GITHUB_TOKEN
   ```

2. **Be Specific with Filters**: Use filters to reduce noise in issue/PR listings
   ```bash
   cursor-utils github issues --owner facebook --repo react --labels bug --state open
   ```

3. **Choose Appropriate Output Format**: 
   - Use `rich` for interactive use
   - Use `json` for scripting and automation
   - Use `markdown` for documentation

4. **Create Detailed Issues/PRs**: Include sufficient context in issues and PRs
   ```bash
   cursor-utils github create-issue --title "Bug: Login fails" --body "Steps to reproduce:\n1. Navigate to login page\n2. Enter valid credentials\n3. Click submit\n\nExpected: User is logged in\nActual: Error 500 is displayed"
   ```

5. **Link Related Resources**: Reference issues in PRs and vice versa
   ```bash
   cursor-utils github create-pr --title "Fix for login bug" --body "Resolves #42"
   ```

### Troubleshooting

### Authentication Issues

If you receive authentication errors:

```
Error: Authentication failed
```

Verify your GitHub token is correctly set:

```bash
cursor-utils config get github_token
```

If it's missing or incorrect, set it:

```bash
cursor-utils config set github_token YOUR_GITHUB_TOKEN
```

### Permission Issues

If you receive permission errors:

```
Error: You don't have permission to perform this action
```

Ensure your GitHub token has the appropriate scopes:
- For repository access: `repo` scope
- For creating issues: `repo` scope
- For creating PRs: `repo` scope
- For public repositories only: `public_repo` scope

### Rate Limiting

If you encounter rate limiting:

```
Error: API rate limit exceeded
```

GitHub has rate limits on API usage. Wait until the rate limit resets or use a token with higher limits.

### Repository Not Found

If you receive a repository not found error:

```
Error: Repository not found
```

Verify the owner and repository name are correct:

```bash
cursor-utils github repo --owner correct-username --repo correct-repo-name
```

Also ensure your token has access to the specified repository. 