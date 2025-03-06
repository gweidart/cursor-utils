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

## Error Handling Architecture

The error handling system in Cursor Utils has been refactored to provide a more consistent and user-friendly experience:

- **Base Error Class**: `CursorUtilsError` extends `DiagnosticError` to provide rich error information
- **Error Categories**: Specialized error classes for each module (e.g., `WebError`, `ConfigError`)
- **Error Codes Enum**: `ErrorCodes` enum provides standardized error codes
- **Decorators**: `safe_execute` and `safe_execute_sync` decorators for standardized error handling
- **Centralized Handling**: `handle_command_error` function for consistent error presentation

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
| `install-006` | Already installed | [ALREADY_INSTALLED](install-006.md) |

### Update Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `update-001` | Update failed | [UPDATE_FAILED](update-001.md) |
| `update-999` | Update not available | [UPDATE_NOT_AVAILABLE](update-999.md) |

### Version Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `version-001` | Version error | [VERSION_ERROR](version-001.md) |
| `version-002` | Invalid version | [VERSION_INVALID](version-002.md) |

### Configuration Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `config-001` | Configuration file error | [CONFIG_FILE_ERROR](config-001.md) |
| `config-002` | Configuration validation error | [CONFIG_VALIDATION_ERROR](config-002.md) |
| `config-003` | Configuration key error | [CONFIG_KEY_ERROR](config-003.md) |
| `config-004` | Environment file error | [ENV_FILE_ERROR](config-004.md) |
| `config-005` | Configuration save error | [CONFIG_SAVE_ERROR](config-005.md) |

### Web Command Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `web-001` | Web configuration error | [WEB_CONFIG_ERROR](web-001.md) |
| `web-002` | Web API error | [WEB_API_ERROR](web-002.md) |
| `web-003` | Invalid API key | [INVALID_API_KEY](web-003.md) |
| `web-004` | Web query error | [WEB_QUERY_ERROR](web-004.md) |
| `web-005` | Web connection error | [WEB_CONNECTION_ERROR](web-005.md) |
| `web-006` | Web timeout error | [WEB_TIMEOUT_ERROR](web-006.md) |

### Gemini API Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `gemini-001` | Gemini API error | [GEMINI_API_ERROR](gemini-001.md) |
| `gemini-002` | Gemini model error | [GEMINI_MODEL_ERROR](gemini-002.md) |
| `gemini-003` | Gemini API key error | [GEMINI_API_KEY_ERROR](gemini-003.md) |
| `gemini-004` | Gemini API key save error | [GEMINI_API_KEY_SAVE_ERROR](gemini-004.md) |
| `gemini-005` | Gemini file error | [GEMINI_FILE_ERROR](gemini-005.md) |

### Repository Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `repo-001` | Repository clone error | [REPO_CLONE_ERROR](repo-001.md) |
| `repo-002` | Repository too large | [REPO_TOO_LARGE](repo-002.md) |
| `repo-003` | Repository analysis error | [REPO_ANALYZE_ERROR](repo-003.md) |
| `repo-004` | Repository URL error | [REPO_URL_ERROR](repo-004.md) |
| `repo-005` | Repository file error | [REPO_FILE_ERROR](repo-005.md) |

### GitHub Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `github-001` | GitHub API error | [GITHUB_API_ERROR](github-001.md) |
| `github-002` | GitHub authentication error | [GITHUB_AUTH_ERROR](github-002.md) |
| `github-003` | GitHub repository error | [GITHUB_REPO_ERROR](github-003.md) |
| `github-004` | GitHub PR error | [GITHUB_PR_ERROR](github-004.md) |
| `github-005` | GitHub issue error | [GITHUB_ISSUE_ERROR](github-005.md) |

### Project Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `project-001` | Project too large | [PROJECT_TOO_LARGE](project-001.md) |
| `project-002` | Project analysis error | [PROJECT_ANALYZE_ERROR](project-002.md) |
| `project-003` | Project invalid URL | [PROJECT_INVALID_URL](project-003.md) |
| `project-004` | Project file error | [PROJECT_FILE_ERROR](project-004.md) |

### General Errors

| Error Code | Description | Documentation |
|------------|-------------|---------------|
| `general-001` | Unknown error | [UNKNOWN_ERROR](general-001.md) |
| `general-002` | General error | [GENERAL_ERROR](general-002.md) |

## Using the Error System in Code

If you're contributing to Cursor Utils, here's how to use the error system:

```python
from cursor_utils.errors import ErrorCodes, WebError
from cursor_utils.utils.command_helpers import safe_execute

@safe_execute(WebError, ErrorCodes.WEB_QUERY_ERROR)
async def web_command(query: str) -> None:
    # Command implementation
    pass
```

For synchronous functions:

```python
from cursor_utils.errors import ErrorCodes, ConfigError
from cursor_utils.utils.command_helpers import safe_execute_sync

@safe_execute_sync(ConfigError, ErrorCodes.CONFIG_FILE_ERROR)
def config_command() -> None:
    # Command implementation
    pass
```

## Troubleshooting Common Errors

For detailed troubleshooting information about specific errors, click on the corresponding error code link in the tables above. 