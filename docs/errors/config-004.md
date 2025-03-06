# ENV_FILE_ERROR (config-004)

## Error Description

This error occurs when Cursor Utils encounters a general issue with the .env file that is used to store API keys and other sensitive information. This could include problems with the file's format, location, or processing that don't fit into more specific error categories.

## Example Error

```
× ERROR: Problem with environment file
  Code: config-004
  
  Causes:
  - The .env file has invalid syntax
  - The .env file is corrupted
  - The .env file contains invalid entries
  - Cannot locate the .env file in the expected paths
  
  Suggestion: Check the .env file format and ensure it exists in the correct location
  
  For more information: https://gweidart.github.io/cursor-utils/errors/config-004.md
```

## Common Causes

1. **Format Issues**: The .env file has an invalid format or syntax errors.
2. **Location Problems**: The .env file is not in the expected location or path.
3. **Parsing Errors**: Issues when parsing the .env file contents.
4. **File Corruption**: The .env file is corrupted or has been partially written.
5. **Concurrent Access**: Multiple processes trying to access the .env file simultaneously.
6. **Encoding Issues**: The .env file has an incorrect character encoding.

## Solutions

### Check .env file location

Verify that the .env file is in the expected location:

```bash
# Linux/macOS
ls -la ~/.env

# Windows (PowerShell)
Test-Path ~/.env
```

### Check .env file format

Ensure the .env file has the correct format:

```bash
# Linux/macOS
cat ~/.env

# Windows (PowerShell)
Get-Content ~/.env
```

The file should contain simple key-value pairs like:
```
PERPLEXITY_API_KEY=your-key-here
GEMINI_API_KEY=your-key-here
GITHUB_TOKEN=your-token-here
```

### Create or fix the .env file

If the .env file is missing or has issues, create a new one:

```bash
# Linux/macOS
touch ~/.env
chmod 600 ~/.env  # Set secure permissions

# Windows (PowerShell)
"" | Out-File -FilePath "$HOME\.env"
```

### Check for specific format issues

Common format issues include:
- Spaces around the equals sign (should be `KEY=value` not `KEY = value`)
- Quotes around values (not needed unless part of the value)
- Special characters in values
- Missing or extra newlines

### Use the configuration tool to set up keys

Let Cursor Utils manage the .env file for you:

```bash
cursor-utils config api_keys --type PERPLEXITY
cursor-utils config api_keys --type GEMINI
cursor-utils config api_keys --type GITHUB
```

### Specify an alternative .env file

You can specify an alternative location for the .env file:

```bash
cursor-utils config api_keys --type [KEY_TYPE] --env-file /path/to/alternative/.env
```

## Related Commands

- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils config paths` - View and manage configuration paths
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [API_KEY_SAVE_ERROR (config-002)](config-002.md) - Error saving API key
- [API_KEY_READ_ERROR (config-003)](config-003.md) - Error reading API key
- [CONFIG_FILE_ERROR (config-005)](config-005.md) - Error with configuration file
- [FILE_NOT_FOUND (install-002)](install-002.md) - File not found during installation

## Advanced Troubleshooting

### Check file encoding

Ensure the .env file has the correct encoding (UTF-8 without BOM):

```bash
# Linux/macOS
file -i ~/.env

# Windows (PowerShell)
# Check using Notepad by opening and saving with "UTF-8" encoding (not "UTF-8 with BOM")
```

### Check for invisible characters

Look for invisible characters that might be causing issues:

```bash
# Linux/macOS
cat -A ~/.env

# Windows (PowerShell)
$content = Get-Content ~/.env -Raw
[System.Text.Encoding]::ASCII.GetString([System.Text.Encoding]::ASCII.GetBytes($content))
```

### Check for line ending issues

Different line endings can cause parsing problems:

```bash
# Linux/macOS
dos2unix ~/.env  # Convert DOS/Windows line endings to Unix

# Windows (PowerShell)
(Get-Content ~/.env -Raw).Replace("`r`n", "`n") | Set-Content ~/.env -NoNewLine
```

### Recreate with proper formatting

Create a new .env file with proper formatting:

```bash
# Linux/macOS
cat > ~/.env << EOF
PERPLEXITY_API_KEY=your-key-here
GEMINI_API_KEY=your-key-here
GITHUB_TOKEN=your-token-here
EOF
chmod 600 ~/.env

# Windows (PowerShell)
@"
PERPLEXITY_API_KEY=your-key-here
GEMINI_API_KEY=your-key-here
GITHUB_TOKEN=your-token-here
"@ | Set-Content -Path "$HOME\.env" -NoNewline
```

### Use environment variables directly

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

## Common .env Issues and Solutions

| Issue | Solution |
|-------|----------|
| Inconsistent line endings | Convert to Unix line endings (LF, not CRLF) |
| Empty lines | Remove extra blank lines |
| Comments | Comments should start with `#` |
| Spaces in keys | Keys should not have spaces |
| Quotes around values | Quotes not needed unless part of the value |
| Hidden characters | Check for and remove hidden/control characters |
| Multiple .env files | Identify which one is being used |
| Permissions | Ensure proper file permissions (600 recommended) |

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

3. Create a simple test .env file:
   ```bash
   echo "TEST_KEY=test_value" > ~/test.env
   cursor-utils config api_keys --type PERPLEXITY --env-file ~/test.env
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Your operating system and version
   - The content of your .env file (with actual API keys redacted)
   - Steps you've taken to resolve the issue 