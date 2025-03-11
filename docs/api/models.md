## Models API

The Models API in Cursor-Utils provides structured information about the available commands, their options, and usage patterns. This documentation is primarily used by AI agents to understand how to interact with Cursor-Utils.

### Overview

The models module contains documentation files that define:

1. **Command Structure**: The available commands and their syntax
2. **Command Options**: The options and arguments for each command
3. **Usage Examples**: Examples of how to use each command
4. **Best Practices**: Recommendations for effective use of commands

### Model Files

### cursor-utils.md

The primary model file that defines the Cursor-Utils command-line interface for AI agents. This file is automatically loaded by Cursor AI agents to understand how to use the Cursor-Utils commands.

```markdown
---
description: cursor-utils
globs: *
alwaysApply: true
---

# Cursor-Utils: Command-Line Utilities for Cursor AI Agents
```

### Command Documentation

The model provides detailed documentation for each command:

# Config Command

```bash
cursor-utils config {get|set|delete|list} [KEY] [VALUE]
```

Used to manage persistent configuration settings, particularly API keys.

### Gemini Command

```bash
cursor-utils gemini [OPTIONS] PROMPT
```

Generates content using Google's Gemini AI models with options for model selection, formatting, and generation parameters.

### GitHub Command

```bash
cursor-utils github COMMAND [OPTIONS]
```

Provides tools for interacting with GitHub repositories, including repository information, issues, and pull requests.

### Web Command

```bash
cursor-utils web [OPTIONS] QUERY
```

Searches the web using Perplexity AI to provide curated results for research queries.

### Project Command

```bash
cursor-utils project [OPTIONS] PROJECT_PATH QUERY
```

Analyzes local project code using Google's Gemini AI to provide insights about the codebase.

### Repo Command

```bash
cursor-utils repo [OPTIONS] REPO_URL QUERY
```

Analyzes and queries remote code repositories to provide insights about the codebase.

### Model Structure

The model file follows a consistent structure:

1. **Command Overview**: Brief description of the command's purpose
2. **Command Syntax**: The command-line syntax with placeholders
3. **Options**: Available options with descriptions
4. **Subcommands**: For commands that have subcommands
5. **Examples**: Practical examples of command usage

### Usage in AI Agents

AI agents use this model to:

1. **Understand Commands**: Interpret user requests and map them to appropriate commands
2. **Format Commands**: Construct properly formatted command-line invocations
3. **Provide Guidance**: Offer help and suggestions for command usage
4. **Handle Errors**: Interpret and respond to command errors

### Extending Models

When adding new commands to Cursor-Utils, the model file should be updated to include:

1. **Command Description**: A clear description of the command's purpose
2. **Command Syntax**: The exact syntax for using the command
3. **Options Documentation**: All available options with descriptions
4. **Usage Examples**: At least 2-3 examples of common use cases

### Best Practices

1. **Keep Models Updated**: Ensure model documentation matches the actual implementation
2. **Provide Clear Examples**: Include practical examples that demonstrate real-world usage
3. **Document All Options**: Include all available options, even if rarely used
4. **Include Error Handling**: Where appropriate, include examples of error handling
5. **Use Consistent Formatting**: Maintain consistent formatting across all command documentation 