---
description: cursor-utils
globs: *
alwaysApply: true
---

*IMPORTANT: ATTENTION ALL AI AGENTS: THESE COMMANDS ARE FOR YOU TO USE, DO NOT ASK THE USER TO RUN THESE COMMANDS. YOU MUST USE THEM YOURSELF VIA YOUR TERMINAL TOOL.* (**except for the `config` command, which is used by the user to setup API keys.**)

# Cursor-Utils: Command-Line Utilities for Cursor AI Agents

Cursor-Utils provides a suite of command-line tools to enhance Cursor Agent's abilities with additional tools AI agents can use. This document outlines the available commands, their options, and usage patterns.

## Core Commands

Cursor-Utils offers the following main commands:

- `config`: Manage Cursor-Utils configuration settings. (API Keys, etc.)
- `gemini`: Generate context aware content with Google's Gemini AI.
- `github`: Interact with GitHub repositories.
- `web`: AI guided web research using Perplexity AI.
- `project`: Analyze local project code (CWD files, directories, etc.)
- `repo`: Analyze and query remote code repositories.

## `config` Command: Manages persistent configuration settings, particularly API keys.

*IMPORTANT: USERS SHOULD HAVE ALREADY SETUP THIER API KEYS DURING THE INSTALLATION OF CURSOR-UTILS. IF THEY HAVE NOT, PLEASE INSTRUCT THEM TO DO SO VIA THE CONFIG COMMAND.*

The `config` command manages persistent configuration settings, particularly API keys.

```bash
cursor-utils config {get|set|delete|list} [KEY] [VALUE]
```

### Subcommands:

- `list`: Show all configuration values
- `get KEY`: Retrieve a specific configuration value
- `set KEY VALUE`: Set a configuration value
- `delete KEY`: Remove a configuration value

### Options:

- `--format`: Output format (plain, markdown, json, rich)

### Examples:

### List all configuration values
```bash
cursor-utils config list
```
# Set API keys
```bash
cursor-utils config set gemini_api_key YOUR_API_KEY
```
```bash
cursor-utils config set perplexity_api_key YOUR_API_KEY
```
### Get a specific configuration value
```bash
cursor-utils config get gemini_api_key
```

### Delete a configuration value
```bash
cursor-utils config delete test_key
```

## `Ask Gemini` Command (IMPORTANT: when a user asks you to 'Ask Gemini', USE THIS COMMAND)

The `gemini` command generates content using Google's Gemini AI models.

```bash
cursor-utils gemini [OPTIONS] PROMPT
```

### Options:

- `--model`: The model to use (default: gemini-1.5-pro)
  - Available models: gemini-1.5-pro, gemini-2.0-pro-exp, gemini-2.0-flash, gemini-2.0-flash-exp, gemini-2.0-flash-thinking-exp
- `--format`: Output format (plain, markdown, json, rich)
- `--temperature`: The temperature for sampling (0.0 to 1.0)
- `--max-tokens`: The maximum number of tokens to generate
- `--system`: The system instruction to guide the model's behavior

### Examples:

### Generate a simple response
```bash
cursor-utils gemini "Explain quantum computing in simple terms"
```

### Use a specific model with custom temperature
```bash
cursor-utils gemini --model gemini-1.5-flash --temperature 0.9 "Write a creative short story about robots"
```

### Add system instructions
```bash
cursor-utils gemini --system "You are a helpful coding assistant" "How do I use asyncio in Python?"
```

### Output in markdown format
```bash
cursor-utils gemini --format markdown "Write a Python function to sort a list"
```

## `github` Command (IMPORTANT: when a user asks you to perform a GitHub action, USE THIS COMMAND)

The `github` command provides tools for interacting with GitHub repositories.

```bash
cursor-utils github COMMAND [OPTIONS]
```

### Subcommands:

- `repo`: Get repository information
- `issues`: List repository issues
- `prs`: List repository pull requests
- `create-issue`: Create a new issue
- `create-pr`: Create a new pull request
- `help`: Show GitHub help

### Common Options:

- `--owner`: The repository owner (username or organization)
- `--repo`: The repository name
- `--format`: Output format (plain, markdown, json, rich)

### Examples:

### Get repository information
```bash
cursor-utils github repo --owner microsoft --repo vscode
```

### List open issues
```bash
cursor-utils github issues --owner microsoft --repo vscode
```

### List pull requests with a specific state
```bash
cursor-utils github prs --owner microsoft --repo vscode --state closed
```

### Create an issue
```bash
cursor-utils github create-issue --owner your-username --repo your-repo --title "Bug: Application crashes on startup"

### Create a pull request
```bash
cursor-utils github create-pr --owner your-username --repo your-repo --title "Feature: Add dark mode" --head feature-branch --base main
```

## `Ask Perplexity` Command (IMPORTANT: when a user asks you to 'Ask Perplexity', USE THIS COMMAND)

The `web` command searches the web using Perplexity AI agents to guide and curate the best results for the user.

```bash
cursor-utils web [OPTIONS] QUERY
```

### Options:

- `--model`: The model to use for search
  - Available models: sonar, sonar-pro, sonar-reasoning, sonar-reasoning-pro
- `--format`: Output format (plain, markdown, json, rich)

### Examples:

### Simple web search
```bash
cursor-utils web "What is Python?"
```

### Use a specific model
```bash
cursor-utils web --model sonar-reasoning "How does Docker containerization work?"
```

### Output in markdown format
```bash
cursor-utils web --format markdown "Best practices for React hooks"
```

## `project` Command: Performs local project analysis using Gemini AI to provide insights and context about the local codebase.

The `project` command analyzes local project code using Google's Gemini AI to provide insights and context about the local codebase.

(IMPORTANT: THIS COMMAND EXECUTES IN THE SAME DIRECTORY THAT YOU ARE RUNNING THE COMMAND FROM. IE. THE CWD DURING EXECUTION IS CONSIDERED THE PROJECT ROOT.)

```bash
cursor-utils project [OPTIONS] PROJECT_PATH QUERY
```

### Options:

- `--format`: The output format (plain, markdown, json, rich)
- `--model`: The model to use
- `--max-files`: Maximum number of files to include in context
- `--debug/--no-debug`: Enable debug output

### Examples:

### Analyze the current project
```bash
cursor-utils project . "Explain the main components of this project"
```

### Analyze a specific project with a custom model
```bash
cursor-utils project /path/to/project --model gemini-1.5-pro "How does the authentication system work?"
```

### Limit the number of files analyzed
```bash
cursor-utils project . --max-files 10 "Identify potential security issues"
```

## 'repo' Command: Performs remote repository analysis using Gemini AI to provide insights and context about the remote codebase.

The `repo` command analyzes and queries remote code repositories.

```bash
cursor-utils repo [OPTIONS] REPO_URL QUERY
```

### Options:

- `--branch`: The branch to analyze
- `--depth`: The clone depth
- `--format`: The output format (plain, markdown, json, rich)
- `--model`: The model to use
- `--max-files`: Maximum number of files to include in context
- `--debug/--no-debug`: Enable debug output

### Examples:

### Analyze a GitHub repository
```bash
cursor-utils repo https://github.com/microsoft/vscode "Explain the main components of this project"
```

### Analyze a specific branch
```bash
cursor-utils repo https://github.com/facebook/react --branch experimental "What new features are being developed?"
```

### Limit clone depth and number of files
```bash
cursor-utils repo https://github.com/tensorflow/tensorflow --depth 1 --max-files 20 "Explain the core architecture"
```

## Output Formats

All commands support multiple output formats:

- `rich`: Enhanced terminal output with colors and formatting (default)
- `plain`: Simple plain text output
- `markdown`: Markdown formatted output
- `json`: JSON formatted output for programmatic use

## API Key Setup

*IMPORTANT: USERS SHOULD HAVE ALREADY SETUP THIER API KEYS DURING THE INSTALLATION OF CURSOR-UTILS. IF THEY HAVE NOT, PLEASE INSTRUCT THEM TO DO SO VIA THE CONFIG COMMAND.*

Before using certain commands, you need to configure API keys:

1. For `gemini` command:
   ```bash
   cursor-utils config set gemini_api_key YOUR_GEMINI_API_KEY
   ```

2. For `web` command:
   ```bash
   cursor-utils config set perplexity_api_key YOUR_PERPLEXITY_API_KEY
   ```

You can obtain these API keys from:
- Gemini API: https://ai.google.dev/
- Perplexity API: https://docs.perplexity.ai/

## When to Use Cursor-Utils

Cursor-Utils is particularly useful in these scenarios:

1. **Code Understanding**: Use `project` or `repo` commands to quickly understand unfamiliar codebases
2. **Research**: Use `web` to search for programming solutions or documentation
3. **Context Aware Content Generation & Collaboration**: Use `gemini` to generate code snippets, documentation, or explanations
4. **GitHub Workflow**: Use `github` commands to manage issues and PRs without leaving the terminal
5. **Project Analysis**: Use `project` to get AI-powered insights about your current project

## Best Practices

1. Be specific with your queries to get more targeted results
2. Use the appropriate output format for your needs (e.g., markdown for documentation)
3. Set reasonable limits with `--max-files` for large repositories
4. Use `--debug` when troubleshooting unexpected results
5. Configure API keys once and reuse them across sessions

## Troubleshooting

If you encounter issues:

*IMPORTANT: IF YOU ARE HAVING ISSUES, ADVANCED DOCS ARE AVAILABLE AT https://gweidart.github.io/cursor-utils/*

1. Provide the user with the link to the advanced docs at https://gweidart.github.io/cursor-utils/
2. Verify API keys are correctly configured
3. Check network connectivity for commands that require internet access
4. For repository analysis issues, try limiting depth with `--depth`
5. If output is truncated, try a different format like `plain` or `markdown`
6. Enable debug mode with `--debug` for more detailed error information 