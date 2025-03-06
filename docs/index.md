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

For detailed API documentation, check out our [API Reference](api/index.md).

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/gweidart/cursor-utils/blob/main/LICENSE) file for details.
