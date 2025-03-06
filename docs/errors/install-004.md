# DIRECTORY_ERROR (install-004)

## Error Description

This error occurs when Cursor Utils encounters an issue with directory operations during installation. This can include problems creating, accessing, or modifying directories required for installation.

## Example Error

```
× ERROR: Directory operation failed during installation
  Code: install-004
  
  Causes:
  - Cannot create directory due to permission issues
  - The specified directory already exists but cannot be accessed
  - The directory path is invalid or too long
  - The parent directory does not exist
  
  Suggestion: Check directory permissions and ensure the path is valid
  
  For more information: https://github.com/gweidart/cursor-utils/errors/install-004.md
```

## Common Causes

1. **Permission Issues**: Insufficient permissions to create or access the directory.
2. **Path Validity**: The directory path contains invalid characters or is malformed.
3. **Path Length**: The directory path exceeds the maximum length allowed by the operating system.
4. **Parent Directory**: The parent directory in the path doesn't exist.
5. **Disk Space**: Insufficient disk space to create the directory.
6. **File System Issues**: Underlying file system problems or limitations.

## Solutions

### Check and fix permissions

Ensure you have the necessary permissions to create and access directories:

```bash
# Linux/macOS
# Check permissions of parent directory
ls -la /path/to/parent/
# Change permissions if needed
chmod 755 /path/to/parent/

# Windows (PowerShell Admin)
# Check directory access
Get-Acl C:\path\to\parent\
# Grant yourself full control if needed through File Explorer properties
```

### Create parent directories

Make sure all parent directories exist:

```bash
# Linux/macOS
mkdir -p /path/to/parent/directory/

# Windows (PowerShell)
New-Item -Path "C:\path\to\parent\directory" -ItemType Directory -Force
```

### Check path validity

Verify that the path doesn't contain invalid characters or exceed path length limits:

```bash
# For Windows, paths should be less than 260 characters
# For Linux/macOS, keep paths reasonable (under 4096 characters)
# Avoid special characters like ?, *, :, |, ", <, >, etc.
```

### Check disk space

Ensure you have sufficient disk space:

```bash
# Linux/macOS
df -h

# Windows (PowerShell)
Get-PSDrive C
```

### Run with elevated privileges

If installing in a system location, try running with elevated privileges:

```bash
# Linux/macOS
sudo cursor-utils install

# Windows (run as Administrator)
```

### Specify an alternative directory

Use a different directory location:

```bash
cursor-utils install --path /different/path/
```

## Related Commands

- `cursor-utils install --help` - Show help for the install command
- `cursor-utils config show` - Display current configuration, including paths

## Related Error Codes

- [INVALID_PATH (install-001)](install-001.md) - Invalid path specification
- [FILE_WRITE_ERROR (install-005)](install-005.md) - Error writing to file
- [GENERAL_FILE_ERROR (general-002)](general-002.md) - General file error

## Advanced Troubleshooting

### Check for existing directories with similar names

Sometimes issues occur due to case sensitivity differences:

```bash
# Linux/macOS (case sensitive)
ls -la /path/to/Directory/
ls -la /path/to/directory/

# Windows (case insensitive, but check anyway)
Get-ChildItem -Path "C:\path\to\" -Directory
```

### Check for directory locks

Ensure the directory is not locked by another process:

```bash
# Linux/macOS
lsof | grep "/path/to/directory"

# Windows (PowerShell)
Get-Process | ForEach-Object { $_.Modules } | Where-Object { $_.FileName -like "C:\path\to\directory*" }
```

### Test with a simple directory

Test if you can create a simple directory in the same location:

```bash
# Linux/macOS
mkdir -p /path/to/test-directory

# Windows (PowerShell)
New-Item -Path "C:\path\to\test-directory" -ItemType Directory
```

## Special Considerations

### Windows Long Path Support

On Windows, if you're dealing with paths longer than 260 characters:

1. Enable long path support in Windows 10/11:
   - Open Group Policy Editor (gpedit.msc)
   - Navigate to: Computer Configuration > Administrative Templates > System > Filesystem
   - Enable "Enable Win32 long paths"

2. Or use the registry editor:
   ```
   reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v "LongPathsEnabled" /t REG_DWORD /d 1 /f
   ```

3. Use UNC path format for very long paths:
   ```
   \\?\C:\very\long\path\that\exceeds\normal\limits
   ```

### Hidden Directories

Some directories might be hidden:

```bash
# Linux/macOS
ls -la  # Shows hidden files/directories starting with .

# Windows (PowerShell)
Get-ChildItem -Path "C:\path\to" -Hidden
```

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug mode:
   ```bash
   cursor-utils install --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Try installing in a simple, accessible location:
   ```bash
   cursor-utils install --path ~/cursor-utils-test
   ```

4. [Submit a bug report](https://github.com/gweidart/cursor-utils/issues) with details about your operating system, file system, and the full error message. 