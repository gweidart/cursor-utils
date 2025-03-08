# Installation Guide

This guide provides detailed instructions for installing and configuring Cursor-Utils on various platforms.

## System Requirements

Before installing Cursor-Utils, ensure your system meets the following requirements:

- **Python**: Python 3.10 or newer
- **Operating System**: Linux, macOS, or Windows
- **Disk Space**: At least 20MB of available disk space
- **Network**: Internet connection required for API access
- **Optional Dependencies**: Git (for repository analysis features)

## Installation Methods

### Using pip (Recommended)

The simplest way to install Cursor-Utils is using pip:

```bash
pip install cursor-utils
```
using uv:

```bash
uv pip install cursor-utils
```
using Poetry:

```bash
poetry add cursor-utils
```


### From Source

To install the latest development version:

```bash
git clone https://github.com/gweidart/cursor-utils.git
cd cursor-utils
pip install -e .
```

### Using pipx (Isolated Environment)

For a clean, isolated installation:

```bash
pipx install cursor-utils
```

If you don't have pipx installed:

```bash
pip install pipx
pipx ensurepath
pipx install cursor-utils
```

## Verifying Installation

To verify that Cursor-Utils has been installed correctly:

```bash
cursor-utils --version
```

This should display the version number of the installed package.

## API Key Setup

Cursor-Utils requires API keys for certain commands. Set up these keys using the `config` command:

### Google Gemini API

1. Visit [Google AI Studio](https://ai.google.dev/) to obtain a Gemini API key
2. Configure the key in Cursor-Utils:

```bash
cursor-utils config set gemini_api_key YOUR_GEMINI_API_KEY
```

### Perplexity API

1. Get a Perplexity API key from [Perplexity API docs](https://docs.perplexity.ai/)
2. Configure the key:

```bash
cursor-utils config set perplexity_api_key YOUR_PERPLEXITY_API_KEY
```

### GitHub API (Optional)

For GitHub integration, you need a GitHub Personal Access Token:

1. Create a token at [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Configure the token:

```bash
cursor-utils config set github_token YOUR_GITHUB_TOKEN
```

## Updating Cursor-Utils

To update to the latest version:

```bash
pip install --upgrade cursor-utils
```

## Troubleshooting

### Common Installation Issues

#### Permission Errors

If you encounter permission errors during installation:

```bash
pip install --user cursor-utils
```

#### Dependency Conflicts

If you experience dependency conflicts:

```bash
pip install --upgrade pip
pip install cursor-utils --ignore-installed
```

#### Path Issues

If the `cursor-utils` command is not found after installation:

1. Ensure Python's bin directory is in your PATH
2. For user installations, verify that `~/.local/bin` is in your PATH

Add to your shell profile (~/.bashrc, ~/.zshrc, etc.):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Getting Help

If you continue to experience issues:

1. Check the [GitHub repository](https://github.com/gweidart/cursor-utils) for known issues
2. Verify system requirements are met
3. Try installation in a clean virtual environment
4. Consult the advanced documentation at https://gweidart.github.io/cursor-utils/