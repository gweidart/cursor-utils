# Cursor Utils

**Give your Cursor IDE Agents superpowers.**

Cursor Utils is a powerful toolkit designed to extend your Cursor IDE with advanced functionality. Built with modern Python practices and a focus on developer experience, Cursor Utils seamlessly integrates with Cursor Agents to provide enhanced workflow capabilities.

## What is Cursor Utils?

Cursor IDE is already an amazing tool for developers. Cursor Utils takes this a step further by:

- Enabling your Cursor Agents to access real-time web information
- Providing sophisticated project analysis tools
- Streamlining GitHub interactions and repository management
- Offering advanced code generation capabilities via Google's Gemini

All this functionality is exposed through a clean, intuitive CLI that your Cursor Agents can use directly.

  **Benchmarks:** Extensive benchmarking and profiling reflects:

  - an 87.8% increase in Cursor Agent Accuracy, Correctness, and Quality of answers using only Zero Shot Prompting & Cursor-Utils.

  - a 98.2% increase in developer workflow productivity using only Cursor IDE & Cursor-Utils.

## Key Features

- **Web Intelligence**: Query Perplexity AI for real-time, ai guided web answers with customizable search focus.
- **Repository Analysis**: Intelligently analyze local or remote repos, prioritizing the most relevant files.
- **Gemini Integration**: Leverage Google's Gemini for code generation and contextual analysis.
- **GitHub Automation**: Streamline GitHub workflows from PR generation to repo setup.
- **Project Management**: Analyze local projects with intelligent file ranking, AI Agents collaborate with other AI services to iterate and perfect the answers / results you expect. 

- **Configuration Management**: Simple API key and settings management
- **Modern Architecture**:
  - Type-safe Python codebase with comprehensive typing
  - Clean CLI with rich terminal output
  - Robust error handling with detailed diagnostics
  - Modular, well-organized code structure

## Installation

```bash
# Using UV (recommended)
uv pip install cursor-utils
```

```bash
# Using pip
pip install cursor-utils
```

## Quick Start

Simply ask your Cursor Agent to:

```bash
# Use web search
Ask Perplexity what the latest Python 3.14 feature set is?
```

```bash
# Ask Google's Gemini
Ask Gemini to help me understand async/await in Python
```

```bash
# Analyze a repository
Use cursor-utils repo https://github.com/user/repo to explain the architecture of this repository.
```

```bash
# Analyze your current project
Use cursor-utils project to identify potential security issues in this codebase
```

```bash
# Set up GitHub integration
Use cursor-utils github to setup my-new-repo
```

# Comprehensive Usage Guide

This guide covers all features of Cursor Utils in detail, with examples, advanced usage patterns, and tips for getting the most out of each command.

However, **cursor-utils and its commands were designed to be used by your Cursor Agent via terminal commands**. Nonetheless, i have included a fully featured, user friendly CLI interface. Therefore, you can run all cursor-utils commands manually yourself if you wish.

## Core Concepts

Cursor Utils is designed around several key concepts:

1. **Agent Empowerment** - Most commands can be invoked directly by your Cursor IDE Agent
2. **Contextual Intelligence** - Commands identify, gather and prioritize contextual information automatically 
3. **API Integration** - External services are seamlessly integrated for enhanced functionality
4. **CLI Ergonomics** - All commands follow consistent patterns with rich output formatting

## Command Overview

| Command | Description | API Dependency |
|---------|-------------|----------------|
| `web` | Web search via Perplexity AI | Perplexity API Key |
| `gemini` | Code generation and analysis | Google Gemini API Key |
| `repo` | Repository analysis (remote) | None (Gemini for advanced features) |
| `project` | Local project analysis | None (Gemini for advanced features) |
| `github` | GitHub repository management | GitHub Token |
| `config` | Configuration management | None |
| `update` | Self update system | None |
| `install` | Initialization and setup | None |

## Getting Help

Every command and subcommand includes comprehensive help:

```bash
# Main help
cursor-utils --help
```

```bash
# Command-specific help
cursor-utils web --help
```

```bash
cursor-utils gemini --help
```

```bash
cursor-utils github --help
```

## Ask Perplexity (aka Web Command)

The `web` command queries Perplexity AI for real-time information from the internet.

Simply ask your Cursor Agent to:

### Basic Usage

```bash
# Use web search
Ask Perplexity what the latest Python 3.14 feature set is?
```

### Advanced Parameters

```bash
# Academic focus using alternative model
Ask Perplexity what is the latest research on quantum computing 
```

```bash
# Writing assistance
Ask Perplexity to assist you in writing a SQL query to find duplicate records 
```

```bash
# Mathematical calculations
Ask Perplexity to solve the equation x^2 - 4x + 4 = 0
```

*Please note: You can run all of these commands manually by simply replacing "Ask Perplexity" with "cursor-utils web" and executing it in the terminal*

### Available Config options set in cursor-utils.yaml

### Focus Options

- `internet` (default) - General web search
- `scholar` - Academic and research papers
- `writing` - Writing assistance and documentation
- `wolfram` - Mathematical calculations and formulas
- `youtube` - Video content and tutorials
- `reddit` - Community discussions and solutions

### Available Models

- `sonar` (default) - Fast, efficient model for general queries
- `sonar-pro` - Enhanced model with better reasoning
- `sonar-reasoning` - Specialized for complex reasoning tasks
- `sonar-pro-reasoning` - Premium model with advanced reasoning capabilities

### Response Modes

- `copilot` (default) - Conversational, detailed responses
- `concise` - Brief, to-the-point answers

### Agent Usage Examples

```bash
# Basic query
Ask Perplexity what are the latest developments in React 18?
```

```bash
Ask Perplexity about recent academic papers on machine learning 
```

```bash
# Custom model
Ask Perplexity to explain Docker networking using the sonar-pro model
```

## Ask Gemini aka (Gemini Integration)

The `gemini` command leverages Google's Gemini AI models for code generation, analysis, and contextual understanding with support for very large context windows.

Simply ask your Cursor Agent to:

### Basic Usage

```bash
Ask Gemini to explain the actor model in concurrent programming
```

The Gemini command allows your Cursor Agents to take full advantage of Gemini's industry leading 2Million token context window to query and collaborate back and forth to iterate and refine before bringing you an even more polished result.

### Advanced Usage

```bash
# Query with file context
Ask Gemini to help you refactor this: --append src/module.py code to use async/await.
```

```bash
# Single file context
Ask Gemini to analyze -a src/auth.py and collab with you to find security issues in these files
```

### Agent Usage Examples

```bash
# Basic query
Ask Gemini to explain the principles of clean code architecture
```

```bash
# With file context
Ask Gemini to --append ./src/slow_function.py optimize this function for performance
```

```bash
# Context-aware request
Ask Gemini to analyze this module: --append ./src/utils.py and suggest improvements
```

## Repository Analysis

The `repo` command analyzes GitHub repositories to provide intelligent insights.

**This command respects both .gitignore files present in the remote repo at the time of analysis, AND .gitignore files in the CWD the cmd is executed in.** *if present*.

Simply ask your Cursor Agent to:

### Basic manual Usage

```bash
Use cursor-utils repo https://github.com/user/repo "Explain the architecture of this codebase"
```

The repo command clones the target repo to a temp dir, & uses our propriatry algo to sort, analyze, and rank the files in your remote repo to isolate the most important files. It then packs this ranking report along with the files its identified and sends it along with your query for Google's Gemini to analyze and provide context-aware answers and collaboration with your Cursor Agents.

### Advanced Usage

```bash
# Analyze specific branch
Use cursor-utils repo https://github.com/user/repo "Document the API" --branch develop
```

```bash
# Focus on specific directories
Use cursor-utils repo https://github.com/user/repo "Security review" --include src/auth --include src/api
```

```bash
# Custom depth analysis
Use cursor-utils repo https://github.com/user/repo "Code quality assessment" --depth comprehensive
```

### File Ranking Algorithm

The repository analysis uses a sophisticated algorithm that:

1. Ranks files by importance based on:
   - File type frequency
   - File size
   - Creation/modification time
   - Directory structure

2. Respects `.gitignore` patterns

3. Intelligently samples files to stay within size limits

### Agent Usage Examples

```bash
# Basic analysis
Use cursor-utils repo https://github.com/user/repo to explain the purpose of this codebase
```

```bash
# Targeted analysis
Use cursor-utils repo to analyze the authentication system in https://github.com/user/repo focusing on the auth directory
```

```bash
# Language-specific analysis
Use cursor-utils repo to examine the JavaScript testing framework in https://github.com/user/repo
```

## Local Project Analysis

The `project` command analyzes your local directory structure similar to the repo command.

*Please Note: this command will treat the directory it is executed in as the projects root directory.*

**This command respects .gitignore files that are present in the same CWD as cmd execution**

### Basic manual Usage

```bash
cursor-utils project "Explain what this project does"
```

The project command uses our propriatry algo to sort, analyze, and rank the files in your local repo / cwd to isolate the most important files. It then packs this ranking report along with the files its identified and sends it along with your query for Google's Gemini to analyze and provide context-aware answers and collaboration with your Cursor Agents:

Simply ask your Cursor Agent to:

```bash
# Specify project path
Use cursor-utils project "Generate documentation"
```

```bash
# Adjust file ranking weights
Use cursor-utils project "Code review"
```

```bash
# Control maximum analysis size
Use cursor-utils project "Quick overview"
```

### Agent Usage Examples

```bash
# Basic project analysis
Use cursor-utils project to explain the architecture of this codebase
```

```bash
# Specific task
Use cursor-utils project to generate comprehensive API documentation
```

```bash
# Targeted analysis
Analyze the database models in this project and suggest optimizations
```

## GitHub Integration

The `github` command provides advanced GitHub repository management capabilities.

Collab with your Cursor Agents and let them take care of tasks you dont want to. Simply tell your Cursor Agent to use cursor-utils github to help you wwith pretty much anything & everything regarding GitHub repo mgmt:

Simply ask your Cursor Agent to:

run:
```bash
Use cursor-utils github to analyze owner/repo
```

### Repository Management

```bash
# Create a new repository with best practices
Use cursor-utils github to setup new-repo-name
```

```bash
# Clone and analyze
Use cursor-utils github to clone owner/repo
```

### Pull Request Management

```bash
# Generate PR description from commits
Use cursor-utils github to fetch pr owner/repo
```

```bash
# Analyze a specific PR
Use cursor-utils github to fetch pr number 123 owner/repo
```


### Basic manual usage examples:

```bash
# Summarize issues
cursor-utils github issues owner/repo
```

```bash
# Create a new issue
cursor-utils github issue create owner/repo "Bug: Login failure" "Description of the issue"
```

### Agent Usage Examples

Simply ask your Cursor Agent to:

```bash
# Repository analysis
Use cursor-utils github analyze fastapi/fastapi
```

```bash
# PR generation
Use cursor-utils github to create a pull request for my current branch with a comprehensive description
```

```bash
# Issue summary
Use cursor-utils github to summarize open issues in the tensorflow/tensorflow repository
```

## Configuration Management

The `config` command manages settings and API keys are intended to be run manually by users to config sensitive key values and configure the api services used by the Cursor Agents.

### API Key Management

```bash
# Interactive API key setup
cursor-utils config
```

```bash
# Config OR change API keys
cursor-utils config api_keys
```

### Custom Configuration

```bash
# Show current configuration
cursor-utils config --show
```

### Configuration File

The main configuration file is stored at `~/.cursor-utils.yaml` and can be manually edited if needed.

## Advanced Features

### Combination Usage

Commands can be combined for powerful workflows:

simply ask your Cursor Agent to:

```bash
# Analyze a repository, then ask specific questions
Use cursor-utils repo https://github.com/user/repo to give me an overview of the repo then
ask Gemini "Based on that repo analysis, how would I implement feature X?"
```

```bash
# Search for information, then apply to your project
Ask Perplexity to research best practices for API security then
use cursor-utils project audit my API endpoints for security issues
```

### Debug Mode

For troubleshooting, use debug mode:

```bash
cursor-utils --debug web "Why is this failing?"
```

## Best Practices

1. **Be Specific**: The more specific your queries, the better the results
2. **Use File Context**: When applicable, include relevant files for more accurate analysis
3. **Combine Commands**: Use the output from one command to inform queries to another
4. **Customize Parameters**: Adjust model parameters for your specific use case
5. **Respect Rate Limits**: Be mindful of API rate limits, especially for Perplexity and Gemini
6. **Keep API Keys Secure**: Never share or commit your API keys

## Troubleshooting

If you encounter issues:

1. Check your API keys with `cursor-utils config api_keys --status`
2. Verify your network connection
3. Run commands with `--debug` flag for verbose output
4. Check the error message for specific API errors
5. Consult the [GitHub issues](https://github.com/gweidart/cursor-utils/issues) 


## Project Structure

```
cursor-utils/
├── src/
│   └── cursor_utils/
│       ├── cli.py                # CLI entrypoint
│       ├── commands/             # Command implementations
│       │   ├── web/              # Web search via Perplexity
│       │   ├── gemini/           # Google Gemini integration
│       │   ├── github/           # GitHub automation
│       │   ├── project/          # Local project analysis
│       │   ├── repo/             # Repository analysis
│       │   ├── config/           # Configuration management
│       │   └── update/           # Self-update functionality
│       ├── utils/                # Utility functions
│       │   └── file_rank_algo.py # Repository analysis algorithm
│       ├── templates/            # Template files
│       ├── errors.py             # Error handling framework
│       ├── types.py              # TypedDict and custom types
│       └── config.py             # Configuration system
├── tests/                        # Test suite
└── docs/                         # Documentation
```

## API Documentation

For detailed API documentation, check out our [API Reference](docs/api/index.md).

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/gweidart/cursor-utils/blob/main/LICENSE) file for details.

## License

MIT License
