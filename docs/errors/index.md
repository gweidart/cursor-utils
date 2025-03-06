# Cursor Utils Error Reference

This documentation provides detailed information about error codes in Cursor Utils, including their causes, potential solutions, and examples.

## Error System Overview

Cursor Utils uses a structured error system with consistent error codes and diagnostic information. Each error includes:

- A unique error code (e.g., `install-001`)
- A descriptive message
- Potential causes
- Suggested solutions
- Links to related documentation

When an error occurs, it is presented with detailed diagnostic information to help you troubleshoot the issue.

## Error Code Format

Error codes follow this format: `{category}-{number}`

- **Category**: Identifies the module or feature area (e.g., `install`, `config`, `web`)
- **Number**: A three-digit identifier for the specific error

For example, `install-001` represents the first error type in the installation module.

## Error Categories

| Category | Description |
|----------|-------------|
| `install` | Installation-related errors |
| `update` | Update-related errors |
| `version` | Version-related errors |
| `config` | Configuration-related errors |
| `web` | Web command related errors |
| `gemini` | Gemini API related errors |
| `repo` | Repository-related errors |
| `github` | GitHub command related errors |
| `project` | Project analysis related errors |
| `general` | General purpose errors |

## Error Code Reference

### Installation Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `install-001` | Invalid path specification | [INVALID_PATH](install-001.md) |
| `install-002` | File not found during installation | [FILE_NOT_FOUND](install-002.md) |
| `install-003` | Error processing template | [TEMPLATE_ERROR](install-003.md) |
| `install-004` | Error creating or accessing directory | [DIRECTORY_ERROR](install-004.md) |
| `install-005` | Error writing to file | [FILE_WRITE_ERROR](install-005.md) |
| `install-006` | Tool is already installed | [ALREADY_INSTALLED](install-006.md) |

### Update Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `update-001` | Update process failed | [UPDATE_FAILED](update-001.md) |
| `update-999` | Unknown error during update | [UNKNOWN_ERROR](update-999.md) |

### Version Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `version-001` | General version error | [VERSION_ERROR](version-001.md) |
| `version-002` | Invalid version format | [INVALID_VERSION](version-002.md) |

### Configuration Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `config-001` | Invalid API key | [INVALID_API_KEY](config-001.md) |
| `config-002` | Error saving API key | [API_KEY_SAVE_ERROR](config-002.md) |
| `config-003` | Error reading API key | [API_KEY_READ_ERROR](config-003.md) |
| `config-004` | Error with .env file | [ENV_FILE_ERROR](config-004.md) |
| `config-005` | Error with configuration file | [CONFIG_FILE_ERROR](config-005.md) |

### Web Command Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `web-001` | Error with Perplexity API | [WEB_API_ERROR](web-001.md) |
| `web-002` | Error with web command configuration | [WEB_CONFIG_ERROR](web-002.md) |
| `web-003` | Connection error during web command | [WEB_CONNECTION_ERROR](web-003.md) |
| `web-004` | Timeout during web command | [WEB_TIMEOUT_ERROR](web-004.md) |
| `web-005` | Error with streaming response | [WEB_STREAM_ERROR](web-005.md) |
| `web-006` | Error with model selection | [WEB_MODEL_ERROR](web-006.md) |

### Gemini API Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `gemini-001` | Error with Gemini API | [GEMINI_API_ERROR](gemini-001.md) |
| `gemini-002` | Error with Gemini model | [GEMINI_MODEL_ERROR](gemini-002.md) |
| `gemini-003` | Error with Gemini API key | [GEMINI_API_KEY_ERROR](gemini-003.md) |
| `gemini-004` | Error saving Gemini API key | [GEMINI_API_KEY_SAVE_ERROR](gemini-004.md) |
| `gemini-005` | Error with file in Gemini command | [GEMINI_FILE_ERROR](gemini-005.md) |

### Repository Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `repo-001` | Error cloning repository | [REPO_CLONE_ERROR](repo-001.md) |
| `repo-002` | Repository size exceeds limits | [REPO_TOO_LARGE](repo-002.md) |
| `repo-003` | Error analyzing repository | [REPO_ANALYZE_ERROR](repo-003.md) |
| `repo-004` | Invalid repository URL | [REPO_INVALID_URL](repo-004.md) |
| `repo-005` | Error with file in repository | [REPO_FILE_ERROR](repo-005.md) |

### GitHub Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `github-001` | GitHub authentication error | [GITHUB_AUTH_ERROR](github-001.md) |
| `github-002` | GitHub API error | [GITHUB_API_ERROR](github-002.md) |
| `github-003` | GitHub repository not found | [GITHUB_REPO_NOT_FOUND](github-003.md) |
| `github-004` | GitHub permission error | [GITHUB_PERMISSION_ERROR](github-004.md) |
| `github-005` | GitHub rate limit exceeded | [GITHUB_RATE_LIMIT](github-005.md) |

### Project Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `project-001` | Project size exceeds limits | [PROJECT_TOO_LARGE](project-001.md) |
| `project-002` | Error analyzing project | [PROJECT_ANALYZE_ERROR](project-002.md) |
| `project-003` | Invalid project URL | [PROJECT_INVALID_URL](project-003.md) |
| `project-004` | Error with file in project | [PROJECT_FILE_ERROR](project-004.md) |

## Handling Errors

### Reading Error Messages

When you encounter an error, it will be displayed in this format:

```
× ERROR: [Error message]
  Code: [error code] (e.g., install-001)
  
  Causes:
  - [Potential cause 1]
  - [Potential cause 2]
  
  Suggestion: [Hint or suggestion for resolution]
  
  For more information: https://gweidart.github.io/cursor-utils/errors/[error-code].md
```

### Common Resolution Steps

1. **Check API Keys**: Many errors relate to missing or invalid API keys. Run `cursor-utils config api_keys` to check and set up your API keys.

2. **Check Configuration**: Verify your configuration by running `cursor-utils config show`.

3. **Check Internet Connection**: For API-related errors, ensure you have a stable internet connection.

4. **Check File Permissions**: For file-related errors, check that you have the necessary permissions.

5. **Check GitHub Token**: For GitHub-related errors, verify your GitHub token with `cursor-utils config api_keys`.

6. **Enable Debug Mode**: Run commands with the `--debug` flag to get more detailed error information.

## Creating Custom Error Handlers

You can create custom error handlers for your extensions of Cursor Utils:

```python
from cursor_utils.errors import CursorUtilsError, ErrorCodes

def handle_my_error():
    try:
        # Your code here
        pass
    except Exception as e:
        # Create a descriptive error
        raise CursorUtilsError(
            message="Failed to process data",
            code=ErrorCodes.GENERAL_ERROR,
            causes=[
                "The data format may be invalid",
                "The input file might be corrupted"
            ],
            hint_stmt="Try providing a valid JSON file"
        )
```

## Submitting Bug Reports

If you encounter an error that you cannot resolve, please submit a bug report with the following information:

1. The full error message and code
2. Steps to reproduce the error
3. Your Cursor Utils version (`cursor-utils --version`)
4. Your operating system and version
5. Any relevant configuration settings or command options

Submit bug reports on [GitHub Issues](https://github.com/gweidart/cursor-utils/issues) with the "bug" label. 