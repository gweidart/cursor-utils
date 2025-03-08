# Error Reference

Cursor-Utils implements a structured error handling system that provides consistent error reporting, exit codes, and recovery mechanisms across all commands. This reference documents the error types, handling patterns, and how to interpret and troubleshoot errors.

## Error Types

Cursor-Utils defines a hierarchy of error types to handle different categories of issues:

| Error Class | Description | Exit Code | Use Cases |
|-------------|-------------|-----------|-----------|
| `CommandError` | Base class for all command errors | 1 | General command errors |
| `ConfigError` | Configuration-related errors | 2 | Missing API keys, invalid configuration |
| `ServiceError` | External service errors | 3 | API rate limits, network issues |

## Error Severity Levels

Errors are categorized by severity level:

| Severity | Description | Typical Action |
|----------|-------------|----------------|
| `INFO` | Informational message | No action required |
| `WARNING` | Potential issue that doesn't prevent execution | Consider addressing |
| `ERROR` | Issue that prevents successful execution | Must be resolved to proceed |
| `CRITICAL` | Serious issue that could affect system stability | Immediate action required |

## Exit Codes

Cursor-Utils uses standardized exit codes to indicate different types of failures:

| Exit Code | Meaning | Example Scenario |
|-----------|---------|------------------|
| 0 | Success | Command completed successfully |
| 1 | General command error | Invalid arguments, unexpected error |
| 2 | Configuration error | Missing API key, invalid configuration file |
| 3 | Service error | API rate limit exceeded, authentication failure |
| 4 | Input validation error | Invalid input format or parameters |

You can use these exit codes in shell scripts to handle errors programmatically:

```bash
cursor-utils web "Python best practices"
if [ $? -eq 2 ]; then
  echo "Configuration error - please set up your API keys"
  cursor-utils config list
fi
```

## Common Error Patterns

### API Key Errors

If you encounter configuration errors related to API keys:

```
Error: API key for Gemini not found in configuration
Help: Set your API key using: cursor-utils config set gemini_api_key YOUR_API_KEY
```

Resolution:
1. Obtain the appropriate API key from the service provider
2. Set the key using the `config` command:
   ```bash
   cursor-utils config set gemini_api_key YOUR_API_KEY
   ```

### Rate Limit Errors

When external services impose rate limits:

```
Error: Rate limit exceeded for Perplexity API
Help: Please wait before making additional requests or upgrade your API tier
```

Resolution:
1. Wait before making additional requests
2. Consider upgrading your API tier
3. Implement request throttling in automation scripts

### Network Errors

Issues connecting to external services:

```
Error: Unable to connect to GitHub API
Help: Check your network connection and try again
```

Resolution:
1. Verify your network connection
2. Check if the service is experiencing downtime
3. Try again later or check for proxy settings if applicable

## Error Handling in Code

For developers extending Cursor-Utils, the error handling system provides a consistent pattern:

1. Use the appropriate error class for different types of issues
2. Include helpful error messages and guidance
3. Leverage the `handle_command_errors` decorator for consistent handling

Example of proper error handling in a command:

```python
from cursor_utils.core.errors import ConfigError, handle_command_errors

@handle_command_errors
def my_command(api_key=None):
    if not api_key:
        raise ConfigError(
            message="API key not provided",
            help_text="Set your API key using: cursor-utils config set my_api_key YOUR_API_KEY",
            severity=ErrorSeverity.ERROR
        )
    # Rest of command implementation
```

## Debug Mode

For more detailed error information, enable debug mode:

```bash
cursor-utils --debug web "Python best practices"
```

Debug mode provides:
1. Full stack traces for unexpected errors
2. Request and response details for API calls
3. Configuration and environment information

## Best Practices for Error Handling

1. **Check Configuration First**: Many errors stem from configuration issues
   ```bash
   cursor-utils config list
   ```

2. **Verify API Keys**: Ensure API keys are set correctly and not expired
   ```bash
   cursor-utils config get gemini_api_key
   ```

3. **Read Help Text**: Error messages include specific guidance for resolution
   
4. **Start Simple**: When troubleshooting, begin with simple commands to isolate issues
   ```bash
   cursor-utils gemini "Hello world"
   ```

5. **Check Service Status**: For service errors, verify if the external service is operating normally 