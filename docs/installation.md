# Installation Guide

This guide covers all aspects of installing, configuring, and updating Cursor Utils.

## System Requirements

- Python 3.10 or newer (Python 3.11+ recommended for optimal performance)
- Cursor IDE (latest version recommended)
- 20MB of free disk space
- Internet connection for API-dependent features

## Installation Methods

### Using UV (Recommended)

[UV](https://github.com/astral-sh/uv) is a blazing-fast Python package installer and resolver that significantly outperforms pip in speed and dependency resolution.

```bash
# Install UV if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Install cursor-utils
uv pip install cursor-utils
```

UV will handle all dependencies correctly and ensure a clean installation.

### Using pip

If you prefer using the standard package manager:

```bash
pip install cursor-utils
```

For isolated installation, consider using a virtual environment:

```bash
uv venv --python pypy
```

```bash
source .venv/bin/activate  # On Unix/macOS
```

```bash
.venv\bin\activate     # On Windows
```

### Global installation

```bash
pip install cursor-utils
```

## Post-Installation Setup

After installation, initialize Cursor Utils in your project directory:

```bash
cd /path/to/your/project
```

```bash
cursor-utils install .
```

This will:
1. Create necessary configuration files
2. Set up default templates
3. Guide you through API key configuration
4. Initialize integration with Cursor IDE

Follow the interactive prompts to complete the setup process.

## API Key Configuration

Cursor Utils works best with the following API keys:

1. **Perplexity AI API Key** - For web search capabilities
2. **Google Gemini API Key** - For code generation and analysis
3. **GitHub Token** - For GitHub integration features

You can configure these during initial setup or later using:

```bash
cursor-utils config api_keys
```

Keys are stored securely in your local environment and never transmitted to external services except the corresponding API providers.

## Verifying Your Installation

To verify that Cursor Utils is installed correctly:

```bash
cursor-utils --version
```

You should see output similar to:
```
Cursor Utils version: 0.1.x
```

For a more comprehensive check, run:

```bash
cursor-utils --verify
```

This will:
- Verify all dependencies are correctly installed
- Check API key configurations
- Test connectivity to required services
- Validate your installation environment

## Troubleshooting

### Common Installation Issues

**Problem**: `Command not found` error when running `cursor-utils`
**Solution**: Ensure the Python installation directory is in your PATH. You may need to log out and log back in after installation.

**Problem**: Dependency conflicts
**Solution**: Use UV or a virtual environment for installation to isolate dependencies.

**Problem**: Permission errors during installation
**Solution**: On Unix-like systems, use `sudo` or install in user mode with `uv pip install --user cursor-utils`

### Getting Help

If you encounter issues not covered here:

1. Check the [GitHub issues](https://github.com/gweidart/cursor-utils/issues) for similar problems
2. Run `cursor-utils doctor` for diagnostic information
3. Open a new issue with detailed information about your environment and the error

## Upgrading

To update Cursor Utils to the latest version:

```bash
cursor-utils update
```

This command will:
1. Check for new versions
2. Back up your configuration
3. Update the package
4. Migrate configuration if needed
5. Verify the updated installation

You can also update manually using:

```bash
uv pip install --upgrade cursor-utils
```

## Uninstallation

If you need to remove Cursor Utils:

```bash
uv pip uninstall cursor-utils
```

This will remove the package but preserve your configuration files. To completely remove all traces:

```bash
cursor-utils uninstall --clean
```

## Development Installation

If you want to contribute to Cursor Utils or install the latest development version:

```bash
# Clone the repository
git clone https://github.com/gweidart/cursor-utils.git
```

```bash
cd cursor-utils
```

```bash
# Create and activate a virtual environment
uv venv .venv --python pypy
```

```bash
source .venv/bin/activate  # On Unix/macOS
```

```bash
# or
.venv\bin\activate     # On Windows
```

```bash
# Install development dependencies
uv pip sync requirements/requirements-dev.txt requirements/requirements-test.txt
```

```bash
# Install the package in development mode
uv pip install -e .
```

This installs Cursor Utils in development mode, allowing you to modify the code and immediately see the effects without reinstalling.