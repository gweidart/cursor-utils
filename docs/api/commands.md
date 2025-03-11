## Commands Reference

This page provides an overview of all available commands in Cursor-Utils. For detailed documentation on each command, follow the links to the individual command pages.

### Command Overview

Cursor-Utils provides the following core commands:

| Command | Description | Documentation |
|---------|-------------|---------------|
| [`config`](#config-command) | Manage configuration settings | [config command](../commands/config.md) |
| [`gemini`](#gemini-command) | Generate content with Google's Gemini AI | [gemini command](../commands/gemini.md) |
| [`github`](#github-command) | Interact with GitHub repositories | [github command](../commands/github.md) |
| [`web`](#web-command) | Perform web research using Perplexity AI | [web command](../commands/web.md) |
| [`project`](#project-command) | Analyze local project code | [project command](../commands/project.md) |
| [`repo`](#repo-command) | Analyze and query remote code repositories | [repo command](../commands/repo.md) |

### Command Summaries

### Config Command

The `config` command manages persistent configuration settings, particularly API keys.

```bash
cursor-utils config {get|set|delete|list} [KEY] [VALUE]
```

**Key Features:**
- Store and retrieve API keys securely
- List all configuration values
- Set default values for command options
- Support for environment variable overrides

[Learn more about the config command →](../commands/config.md)

### Gemini Command

The `gemini` command generates content using Google's Gemini AI models.

```bash
cursor-utils gemini [OPTIONS] PROMPT
```

**Key Features:**
- Generate code, documentation, and explanations
- Select from multiple Gemini models
- Customize generation parameters
- Format output in various formats

[Learn more about the gemini command →](../commands/gemini.md)

### GitHub Command

The `github` command provides tools for interacting with GitHub repositories.

```bash
cursor-utils github COMMAND [OPTIONS]
```

**Key Features:**
- Get repository information
- List and manage issues
- List and manage pull requests
- Create new issues and pull requests

[Learn more about the github command →](../commands/github.md)

### Web Command

The `web` command searches the web using Perplexity AI to provide curated results.

```bash
cursor-utils web [OPTIONS] QUERY
```

**Key Features:**
- Perform intelligent web searches
- Get curated results for technical queries
- Select from multiple Perplexity models
- Format output in various formats

[Learn more about the web command →](../commands/web.md)

### Project Command

The `project` command analyzes local project code using Google's Gemini AI.

```bash
cursor-utils project [OPTIONS] PROJECT_PATH QUERY
```

**Key Features:**
- Analyze local codebases
- Get AI-powered insights about code structure
- Ask questions about code functionality
- Limit analysis to specific files or directories

[Learn more about the project command →](../commands/project.md)

### Repo Command

The `repo` command analyzes and queries remote code repositories.

```bash
cursor-utils repo [OPTIONS] REPO_URL QUERY
```

**Key Features:**
- Analyze remote repositories
- Clone and analyze specific branches
- Get AI-powered insights about code structure
- Ask questions about code functionality

[Learn more about the repo command →](../commands/repo.md)

### Common Command Patterns

All Cursor-Utils commands follow these common patterns:

### Output Formatting

All commands support multiple output formats:

```bash
cursor-utils COMMAND --format {plain|markdown|json|rich}
```

### Help Information

All commands provide detailed help information:

```bash
cursor-utils COMMAND --help
```

### Error Handling

All commands use consistent error handling with meaningful exit codes:

```bash
cursor-utils COMMAND
if [ $? -ne 0 ]; then
  echo "Command failed"
fi
```

### Command Relationships

Commands in Cursor-Utils are designed to work together:

- **Configuration**: The `config` command manages settings used by all other commands
- **Content Generation**: The `gemini` command provides AI-powered content generation
- **Research**: The `web` command provides research capabilities
- **Code Analysis**: The `project` and `repo` commands analyze code
- **GitHub Integration**: The `github` command manages GitHub repositories

### Best Practices

1. **Set Default Configuration**: Use the `config` command to set default values
   ```bash
   cursor-utils config set default_format markdown
   ```

2. **Combine Commands**: Use command output in scripts
   ```bash
   REPO_INFO=$(cursor-utils github repo --owner microsoft --repo vscode --format json)
   REPO_NAME=$(echo $REPO_INFO | jq -r '.name')
   ```

3. **Use Appropriate Models**: Select the right model for your task
   ```bash
   # For creative content
   cursor-utils gemini --model gemini-2.0-pro-exp "Generate test scenarios"
   
   # For factual research
   cursor-utils web --model sonar-reasoning "Explain ACID properties"
   ```

4. **Limit Analysis Scope**: For large repositories, limit the scope
   ```bash
   cursor-utils project . --max-files 20 "Explain the authentication system"
   ```

## Command Documentation

For detailed documentation on each command, refer to the dedicated command pages:

- [`config` Command](../commands/config.md)
- [`gemini` Command](../commands/gemini.md)
- [`github` Command](../commands/github.md)
- [`web` Command](../commands/web.md)
- [`project` Command](../commands/project.md)
- [`repo` Command](../commands/repo.md) 