## Installation Guide

This guide provides detailed instructions for installing and configuring Cursor-Utils on various platforms.

[Install Cursor Utils :simple-pypi:](#){ .md-button .copy-js data-clipboard-text="pip install cursor-utils" }

=== "pip"

    ```bash
    pip install cursor-utils
    ```

=== "uv"

    ```bash
    uv pip install cursor-utils  # Recommended
    ```

=== "poetry"

    ```bash
    poetry add cursor-utils
    ```

=== "pipx"

    For a clean, isolated installation:

    ``` bash
    pipx install cursor-utils
    ```

    If you don't have pipx installed:

    ``` bash
    pip install pipx
    pipx ensurepath
    pipx install cursor-utils
    ```

### Verifying Installation

To verify that Cursor-Utils has been installed correctly:

```bash
cursor-utils --version
```

This should display the version number of the installed package.

### Upgrading your Cursor Agent

By now, you should have Cursor-Utils installed in your environment. Now its time to upgrade your Cursor Agent and install the latest version of Cursor-Utils in the current repo / project / directory:

???+ warning

    Even tho you have installed the latest version of Cursor-Utils in your environment, each time you start a new Cursor workspace, you need to run the `cursor-utils install .` command to install the latest version of Cursor-Utils in the current repo / project / directory.

```bash
cursor-utils install .
```
After running this command, your Cursor Agent will be updated with the new tools and commands. The command will also kickoff the api key setup process.

???+ info

    Please note the `.` is required to install the agent in the current repo / project / directory.


### API Key Setup

Cursor-Utils requires API keys for certain commands. Set up these keys using the `config` command:

=== "Gemini"

    1. Visit [Google AI Studio](https://ai.google.dev/) to obtain a Gemini API key
    2. Configure the key in Cursor-Utils:

    ```bash
    cursor-utils config set gemini_api_key YOUR_GEMINI_API_KEY
    ```

=== "Perplexity"

    1. Get a Perplexity API key from [Perplexity API docs](https://docs.perplexity.ai/)
    2. Configure the key:

    ```bash
    cursor-utils config set perplexity_api_key YOUR_PERPLEXITY_API_KEY
    ```

=== "GitHub"

    For GitHub integration, you need a GitHub Personal Access Token:

    1. Create a token at [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
    2. Configure the token:

    ```bash
    cursor-utils config set github_token YOUR_GITHUB_TOKEN
    ```

#### Updating Cursor-Utils

To update to the latest version:

```bash
cursor-utils update
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

