## API Reference

This section provides detailed documentation for all Cursor-Utils commands, their options, arguments, and usage patterns.

### Command Overview

Cursor-Utils provides the following core commands:

| Command | Description | Primary Use Cases |
|---------|-------------|-------------------|
| [`config`](../commands/config.md) | Manage configuration settings | Setting API keys, viewing/updating configurations |
| [`gemini`](../commands/gemini.md) | Generate content with Google's Gemini AI | Code generation, explanations, documentation |
| [`github`](../commands/github.md) | Interact with GitHub repositories | Repository management, issue tracking, PR creation |
| [`web`](../commands/web.md) | Perform web research using Perplexity AI | Technical research, documentation lookup, problem-solving |
| [`project`](../commands/project.md) | Analyze local project code | Code understanding, architecture analysis, onboarding |
| [`repo`](../commands/repo.md) | Analyze remote code repositories | Open-source exploration, dependency evaluation |

### Command Structure

All Cursor-Utils commands follow a consistent structure:

```
cursor-utils [COMMAND] [SUBCOMMAND] [OPTIONS] [ARGUMENTS]
```

### Global Options

These options are available across all commands:

| Option | Description | Example |
|--------|-------------|---------|
| `--help` | Display help information | `cursor-utils --help` |
| `--version` | Show version information | `cursor-utils --version` |
| `--format` | Specify output format | `cursor-utils --format json` |
| `--debug` | Enable debug output | `cursor-utils --debug` |

### Output Formats

All commands support the following output formats:

| Format | Description | Best For |
|--------|-------------|----------|
| `rich` | Colored and formatted terminal output | Interactive use |
| `plain` | Simple text without formatting | Log files, piping to other commands |
| `markdown` | Markdown formatted text | Documentation, note-taking |
| `json` | Structured JSON data | Programmatic use, automation |

### Command Details

For detailed documentation on each command, refer to the specific command pages:

### [`config` Command](../commands/config.md)

The `config` command manages persistent configuration settings, particularly API keys.

```bash
cursor-utils config {get|set|delete|list} [KEY] [VALUE]
```

### [`gemini` Command](../commands/gemini.md)

The `gemini` command generates content using Google's Gemini AI models.

```bash
cursor-utils gemini [OPTIONS] PROMPT
```

### [`github` Command](../commands/github.md)

The `github` command provides tools for interacting with GitHub repositories.

```bash
cursor-utils github COMMAND [OPTIONS]
```

### [`web` Command](../commands/web.md)

The `web` command searches the web using Perplexity AI to provide curated results.

```bash
cursor-utils web [OPTIONS] QUERY
```

### [`project` Command](../commands/project.md)

The `project` command analyzes local project code using Gemini AI.

```bash
cursor-utils project [OPTIONS] PROJECT_PATH QUERY
```

### [`repo` Command](../commands/repo.md)

The `repo` command analyzes and queries remote code repositories.

```bash
cursor-utils repo [OPTIONS] REPO_URL QUERY
```

### API Integration

Cursor-Utils integrates with several external APIs:

| API | Used By | Purpose |
|-----|---------|---------|
| Google Gemini | `gemini`, `project`, `repo` | AI-powered content generation and code analysis |
| Perplexity | `web` | Web search and research |
| GitHub | `github` | Repository interaction and management |

For information on configuring these APIs, see the [installation guide](../installation.md#api-key-setup) and the [`config` command documentation](../commands/config.md). 