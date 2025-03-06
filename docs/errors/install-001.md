# INVALID_PATH (install-001)

## Error Description

This error occurs when Cursor Utils encounters an invalid path during installation. The specified path may not exist, may not be accessible, or may not meet the requirements for installation.

## Example Error

```
× ERROR: Invalid path specified for installation
  Code: install-001
  
  Causes:
  - The specified path does not exist
  - The path points to a file instead of a directory
  - You don't have sufficient permissions to access the path
  
  Suggestion: Specify a valid directory path where you have write permissions
  
  For more information: https://gweidart.github.io/cursor-utils/errors/install-001.md
```

## Common Causes

1. **Non-existent path**: The directory path you specified doesn't exist on your system.
2. **Path is a file**: You specified a file path instead of a directory path.
3. **Permission issues**: You don't have sufficient permissions to access or write to the specified path.
4. **Path contains invalid characters**: The path contains characters that are not allowed in your operating system.
5. **Path is too long**: The path exceeds the maximum path length supported by your operating system.

## Solutions

### Check if the path exists

Verify that the path you're specifying exists:

```bash
# Linux/macOS
ls -la /path/to/directory
```

```bash
# Windows (PowerShell)
Get-ChildItem -Path C:\path\to\directory
```

### Create the directory if it doesn't exist

If the directory doesn't exist, create it before installation:

```bash
# Linux/macOS
mkdir -p /path/to/directory
```

```bash
# Windows (PowerShell)
New-Item -Path "C:\path\to\directory" -ItemType Directory
```

### Check and fix permissions

Ensure you have the necessary permissions for the directory:

```bash
# Linux/macOS
chmod 755 /path/to/directory
```

```bash
# Windows
# Right-click the folder, select Properties, then Security tab, and adjust permissions
```

### Use an absolute path

When specifying paths, use absolute paths rather than relative paths to avoid confusion:

```bash
# Good
cursor-utils install --path /home/username/projects/my-project

# Avoid
cursor-utils install --path ./my-project
```

### Run with elevated privileges if necessary

If you need to install in a system directory, you might need elevated privileges:

```bash
# Linux/macOS
sudo cursor-utils install --path /usr/local/bin

# Windows (run as Administrator)
```

## Related Commands

- `cursor-utils install --help` - Show help for the install command
- `cursor-utils config show` - Display current configuration
- `cursor-utils --version` - Check your current version

## Related Error Codes

- [DIRECTORY_ERROR (install-004)](install-004.md) - Error creating or accessing directory
- [FILE_WRITE_ERROR (install-005)](install-005.md) - Error writing to file
- [GENERAL_FILE_ERROR (general-002)](general-002.md) - General file error

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run the command with the `--debug` flag to get more detailed error information:
   ```bash
   cursor-utils install --path /path/to/directory --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. [Submit a bug report](https://github.com/gweidart/cursor-utils/issues) with the detailed information. 