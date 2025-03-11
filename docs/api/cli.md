## Command-Line Interface

Cursor-Utils provides a consistent and intuitive command-line interface designed to streamline development workflows. This page documents the CLI structure, conventions, and common patterns.

### Command Structure

The Cursor-Utils CLI follows a command-subcommand pattern:

```bash
cursor-utils [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS] [ARGUMENTS]
```

### Global Options

These options apply to all commands:

| Option | Description | Default |
|--------|-------------|---------|
| `--debug` | Enable debug output | Disabled |
| `--help`, `-h` | Show help message and exit | - |
| `--version`, `-v` | Show version information | - |

### Commands

Cursor-Utils provides the following main commands:

| Command | Description | Documentation |
|---------|-------------|---------------|
| `config` | Manage configuration settings | [config command](../commands/config.md) |
| `gemini` | Generate content with Google's Gemini AI | [gemini command](../commands/gemini.md) |
| `github` | Interact with GitHub repositories | [github command](../commands/github.md) |
| `web` | Perform web research using Perplexity AI | [web command](../commands/web.md) |
| `project` | Analyze local project code | [project command](../commands/project.md) |
| `repo` | Analyze and query remote code repositories | [repo command](../commands/repo.md) |

### Common Command Options

While each command has specific options, many share these common options:

| Option | Description | Default | Available In |
|--------|-------------|---------|-------------|
| `--format` | Output format (plain, markdown, json, rich) | `rich` | All commands |
| `--help`, `-h` | Show command-specific help | - | All commands |
| `--model` | AI model to use | Varies by command | gemini, web, project, repo |

### Output Formats

All commands support multiple output formats, controlled by the `--format` option:

| Format | Description | Best For |
|--------|-------------|----------|
| `rich` | Enhanced terminal output with colors and formatting | Interactive use |
| `plain` | Simple text without formatting | Log files, piping to other tools |
| `markdown` | Markdown formatted text | Documentation, note-taking |
| `json` | Structured JSON data | Programmatic use, automation |

Example:

```bash
cursor-utils gemini --format markdown "Write a function to validate email addresses"
```

### Error Handling

Cursor-Utils provides consistent error handling across all commands:

1. **Error Messages**: Clear, descriptive error messages are displayed in the terminal
2. **Exit Codes**: Non-zero exit codes indicate failure:
   - `0`: Success
   - `1`: General error
   - `2`: Configuration error
   - `3`: Network/API error
   - `4`: Input validation error


### Environment Variables

Cursor-Utils supports configuration via environment variables, following the pattern `CURSOR_UTILS_` followed by the uppercase configuration key:

| Environment Variable | Description | Example |
|----------------------|-------------|---------|
| `CURSOR_UTILS_GEMINI_API_KEY` | Google Gemini API key | `export CURSOR_UTILS_GEMINI_API_KEY=your-key` |
| `CURSOR_UTILS_PERPLEXITY_API_KEY` | Perplexity API key | `export CURSOR_UTILS_PERPLEXITY_API_KEY=your-key` |
| `CURSOR_UTILS_GITHUB_TOKEN` | GitHub personal access token | `export CURSOR_UTILS_GITHUB_TOKEN=your-token` |
| `CURSOR_UTILS_DEFAULT_FORMAT` | Default output format | `export CURSOR_UTILS_DEFAULT_FORMAT=markdown` |
| `CURSOR_UTILS_DEBUG` | Enable debug mode | `export CURSOR_UTILS_DEBUG=1` |

Environment variables take precedence over configuration file values.

### Command Completion

Cursor-Utils supports command completion for Bash and Zsh shells. To enable it:

### Bash

Add to your `~/.bashrc`:

```bash
eval "$(cursor-utils --completion bash)"
```

### Zsh

Add to your `~/.zshrc`:

```bash
eval "$(cursor-utils --completion zsh)"
```

### Redirection

Output can be redirected to files:

```bash
cursor-utils gemini --format markdown "Write documentation for REST API best practices" > rest-best-practices.md
```

### Exit Codes

Cursor-Utils commands return meaningful exit codes:

| Exit Code | Meaning | Example Scenario |
|-----------|---------|------------------|
| 0 | Success | Command completed successfully |
| 1 | General error | Unexpected runtime error |
| 2 | Configuration error | Missing or invalid API key |
| 3 | Network/API error | API rate limit exceeded |
| 4 | Input validation error | Invalid command arguments |


### Progress Indicators

For operations that may take time, Cursor-Utils displays progress indicators:

1. **Spinners**: For operations without measurable progress
2. **Progress Bars**: For operations with known stages
3. **Streaming Output**: For results that can be displayed incrementally

These indicators are automatically disabled when:
- Output is not to a terminal (piping or redirection)
- The `--format` option is set to `plain` or `json`

### Common Usage Patterns

### Chaining Commands

Commands can be chained together for complex workflows:

```bash
# Research a topic, then generate code based on findings
RESEARCH=$(cursor-utils web --format plain "Best practices for Node.js error handling")
cursor-utils gemini "Generate a Node.js error handling utility based on these best practices: $RESEARCH"
```

### Conditional Execution

Use exit codes for conditional execution:

```bash
# Only create an issue if analysis finds vulnerabilities
cursor-utils project . "Find security vulnerabilities" && cursor-utils github create-issue --owner your-username --repo your-repo --title "Security vulnerabilities found"
```

### Debug Mode

For troubleshooting, enable debug mode with the `--debug` flag:

```bash
cursor-utils --debug gemini "Generate a function"
```

This provides additional information:
- API request details
- Configuration values being used
- Performance metrics
- Internal operation steps

### Configuration Precedence

When determining configuration values, Cursor-Utils follows this precedence (highest to lowest):

1. Command-line arguments
2. Environment variables
3. Configuration file values
4. Default values

This allows flexible configuration while maintaining clear override rules.

For detailed documentation on each command, refer to:

- [`config` Command](../commands/config.md)
- [`gemini` Command](../commands/gemini.md)
- [`github` Command](../commands/github.md)
- [`web` Command](../commands/web.md)
- [`project` Command](../commands/project.md)
- [`repo` Command](../commands/repo.md) 