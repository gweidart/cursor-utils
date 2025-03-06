# GEMINI_API_KEY_SAVE_ERROR (gemini-004)

## Error Description

This error occurs when Cursor Utils fails to save the Google Gemini API key to its configuration or environment file. This could be due to permission issues, file system problems, or other issues with storing the API key.

## Example Error

```
× ERROR: Failed to save Google Gemini API key
  Code: gemini-004
  
  Causes:
  - Insufficient permissions to write to the .env file
  - The .env file or directory is locked by another process
  - The file system is read-only
  - Disk space issues
  
  Suggestion: Check file permissions and ensure you have write access
  
  For more information: https://github.com/gweidart/cursor-utils/errors/gemini-004.md
```

## Common Causes

1. **Permission Issues**: The user doesn't have write permissions for the .env file.
2. **File Locking**: The .env file is being used by another process.
3. **Read-Only File System**: The file system where the .env file is located is mounted as read-only.
4. **Disk Space**: There isn't enough disk space to write the updated file.
5. **Path Issues**: The path to the .env file is incorrect or doesn't exist.
6. **Invalid API Key Format**: The provided API key has an invalid format.

## Solutions

### Check file permissions

Ensure you have write permissions for the .env file:

```bash
# Linux/macOS
ls -la ~/.env
chmod 600 ~/.env  # Make it writable only by you for security

# Windows (PowerShell)
Get-Acl ~/.env
# Then check through Windows Explorer if needed
```

### Ensure .env directory exists

Make sure the directory for the .env file exists:

```bash
# Linux/macOS
mkdir -p $(dirname ~/.env)

# Windows (PowerShell)
$envPath = "$HOME\.env"
$envDir = Split-Path -Path $envPath -Parent
if (-not (Test-Path $envDir)) { New-Item -ItemType Directory -Path $envDir }
```

### Close other processes

Ensure no other applications or processes are using the .env file:
- Close any text editors or IDEs that might have the file open
- Check for other instances of Cursor Utils that might be running

### Run with elevated privileges

If you're trying to save to a system location, try running with elevated privileges:

```bash
# Linux/macOS
sudo cursor-utils config api_keys --type GEMINI

# Windows (run as Administrator)
```

### Specify an alternative location

You can specify an alternative location for the .env file:

```bash
cursor-utils config api_keys --type GEMINI --env-file /path/to/alternative/.env
```

### Verify API key format

Ensure the API key has the correct format before saving:
- Google Gemini API keys are typically 39 characters long
- They usually begin with "AI"
- Example: `AIzaSyC1a2b3c4d5e...`

## Related Commands

- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils test api_key` - Test API key validity
- `cursor-utils config paths` - View configuration file paths

## Related Error Codes

- [GEMINI_API_KEY_ERROR (gemini-003)](gemini-003.md) - Error with Gemini API key
- [API_KEY_SAVE_ERROR (config-002)](config-002.md) - Error saving API key
- [ENV_FILE_ERROR (config-004)](config-004.md) - Error with .env file
- [FILE_WRITE_ERROR (install-005)](install-005.md) - Error writing to file

## Advanced Troubleshooting

### Test file writing

Test if you can write to the .env file location:

```bash
# Linux/macOS
touch ~/.env.test
echo "TEST=value" > ~/.env.test
cat ~/.env.test
rm ~/.env.test

# Windows (PowerShell)
"TEST=value" | Out-File -FilePath "$HOME\.env.test"
Get-Content "$HOME\.env.test"
Remove-Item "$HOME\.env.test"
```

### Check for hidden .env file

Sometimes there might be a hidden .env file with different permissions:

```bash
# Linux/macOS
ls -la ~ | grep "\.env"

# Windows (PowerShell)
Get-ChildItem -Path $HOME -Hidden -Filter .env
```

### Manually create or edit the .env file

If automatic saving fails, you can manually create or edit the .env file:

```bash
# Linux/macOS
echo "GEMINI_API_KEY=your-key-here" >> ~/.env
chmod 600 ~/.env  # Set secure permissions

# Windows (PowerShell)
"GEMINI_API_KEY=your-key-here" | Out-File -FilePath "$HOME\.env" -Append
```

### Use environment variables directly

As a workaround, you can use environment variables directly:

```bash
# Linux/macOS
export GEMINI_API_KEY="your-key-here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-key-here"
```

## Security Considerations

When saving API keys, keep these security considerations in mind:

1. **File Permissions**: Ensure the .env file has secure permissions (readable only by you)
2. **Location**: Store the .env file in a secure location, not in public directories
3. **Backup**: Keep a secure backup of your API keys
4. **Never Commit**: Never commit the .env file to version control
5. **Key Rotation**: Regularly rotate your API keys for improved security

## .env File Format

The .env file should contain key-value pairs like:

```
GEMINI_API_KEY=your-key-here
PERPLEXITY_API_KEY=your-key-here
GITHUB_TOKEN=your-token-here
```

Each key-value pair should be on a separate line with no extra spaces around the equals sign.

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug logging:
   ```bash
   cursor-utils config api_keys --type GEMINI --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Try using a completely different location for the .env file:
   ```bash
   cursor-utils config api_keys --type GEMINI --env-file ~/gemini-key.env
   ```

4. Check for any file system issues or disk corruption.

5. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Your operating system and version
   - File system details (if known)
   - Steps you've taken to troubleshoot 