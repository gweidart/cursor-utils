# API_KEY_READ_ERROR (config-003)

## Error Description

This error occurs when Cursor Utils fails to read an API key from its configuration or environment file. This could be due to permission issues, file system problems, or other issues with accessing or parsing the stored API keys.

## Example Error

```
× ERROR: Failed to read API key
  Code: config-003
  
  Causes:
  - The .env file does not exist
  - Insufficient permissions to read the .env file
  - The .env file format is invalid
  - The specified API key is not found in the configuration
  
  Suggestion: Check that the .env file exists and has the correct permissions
  
  For more information: https://gweidart.github.io/cursor-utils/errors/config-003.md
```

## Common Causes

1. **Missing .env File**: The .env file doesn't exist or is not in the expected location.
2. **Permission Issues**: The user doesn't have read permissions for the .env file.
3. **Invalid Format**: The .env file has an invalid format or syntax.
4. **Missing Key**: The requested API key is not defined in the .env file.
5. **Environment Variables**: Environment variable conflicts or overrides.
6. **File Corruption**: The .env file is corrupted or incomplete.

## Solutions

### Check if the .env file exists

Verify that the .env file exists:

```bash
# Linux/macOS
ls -la ~/.env

# Windows (PowerShell)
Test-Path ~/.env
```

### Check file permissions

Ensure you have read permissions for the .env file:

```bash
# Linux/macOS
ls -la ~/.env
chmod 600 ~/.env  # Make it readable and writable only by you for security

# Windows (PowerShell)
Get-Acl ~/.env
```

### Check the .env file format

Verify that the .env file has the correct format:

```bash
# Linux/macOS
cat ~/.env

# Windows (PowerShell)
Get-Content ~/.env
```

The .env file should contain key-value pairs like:
```
PERPLEXITY_API_KEY=your-key-here
GEMINI_API_KEY=your-key-here
GITHUB_TOKEN=your-token-here
```

Each key-value pair should be on a separate line with no extra spaces around the equals sign.

### Set up the API key

If the API key is missing, set it up:

```bash
cursor-utils config api_keys --type [KEY_TYPE]
```

Where `[KEY_TYPE]` is one of:
- `PERPLEXITY` - For Perplexity AI (web search)
- `GEMINI` - For Google Gemini (code generation)
- `GITHUB` - For GitHub API access

### Specify an alternative .env file

You can specify an alternative location for the .env file:

```bash
cursor-utils config api_keys --type [KEY_TYPE] --env-file /path/to/alternative/.env
```

### Create a new .env file

If the .env file is missing or corrupted, create a new one:

```bash
# Linux/macOS
touch ~/.env
chmod 600 ~/.env  # Secure permissions

# Windows (PowerShell)
"" | Out-File -FilePath "$HOME\.env"
```

Then set up your API keys again:

```bash
cursor-utils config api_keys --type PERPLEXITY
cursor-utils config api_keys --type GEMINI
cursor-utils config api_keys --type GITHUB
```

## Related Commands

- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils config paths` - View and manage configuration paths
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [INVALID_API_KEY (config-001)](config-001.md) - Invalid API key
- [API_KEY_SAVE_ERROR (config-002)](config-002.md) - Error saving API key
- [ENV_FILE_ERROR (config-004)](config-004.md) - Error with .env file
- [FILE_NOT_FOUND (install-002)](install-002.md) - File not found during installation

## Advanced Troubleshooting

### Check environment variables

Check if the API keys are defined as environment variables:

```bash
# Linux/macOS
env | grep -E 'PERPLEXITY_API_KEY|GEMINI_API_KEY|GITHUB_TOKEN'

# Windows (PowerShell)
Get-ChildItem Env: | Where-Object { $_.Name -match 'PERPLEXITY_API_KEY|GEMINI_API_KEY|GITHUB_TOKEN' }
```

### Check for conflicting .env files

Look for multiple .env files that might be causing conflicts:

```bash
# Linux/macOS
find ~/ -name ".env" -maxdepth 3

# Windows (PowerShell)
Get-ChildItem -Path $HOME -Filter .env -Recurse -Depth 3
```

### Check .env file encoding

Ensure the .env file has the correct encoding (UTF-8):

```bash
# Linux/macOS
file -i ~/.env

# Windows (PowerShell)
# Check through Notepad by opening the file and saving with UTF-8 encoding
```

### Manually inspect for invisible characters

Check for invisible characters that might affect parsing:

```bash
# Linux/macOS
hexdump -C ~/.env | head -20

# Windows (PowerShell)
Format-Hex -Path ~/.env | Select-Object -First 20
```

### Use direct environment variables

As a workaround, you can use environment variables directly:

```bash
# Linux/macOS
export PERPLEXITY_API_KEY="your-key-here"
export GEMINI_API_KEY="your-key-here"
export GITHUB_TOKEN="your-token-here"

# Windows (PowerShell)
$env:PERPLEXITY_API_KEY="your-key-here"
$env:GEMINI_API_KEY="your-key-here"
$env:GITHUB_TOKEN="your-token-here"
```

## Common .env File Issues

| Issue | Solution |
|-------|----------|
| Empty lines between entries | Remove empty lines |
| Spaces around equals sign | Remove spaces: `KEY=value` not `KEY = value` |
| Quoted values | Remove quotes unless they're part of the value |
| Comments | Comments should start with `#` |
| Line endings | Use Unix-style line endings (LF not CRLF) |
| BOM marker | Ensure file is saved without Byte Order Mark |

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug logging:
   ```bash
   cursor-utils config api_keys --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Create a completely new .env file in a different location:
   ```bash
   echo "PERPLEXITY_API_KEY=your-key-here" > ~/new-env-file
   cursor-utils config api_keys --env-file ~/new-env-file
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Your operating system and version
   - The output of any troubleshooting commands you've run
   - Steps you've taken to resolve the issue 