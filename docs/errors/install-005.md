# FILE_WRITE_ERROR (install-005)

## Error Description

This error occurs when Cursor Utils cannot write to a file during the installation process. This may be due to permission issues, disk space limitations, or file locking by another process.

## Example Error

```
× ERROR: Failed to write to file during installation
  Code: install-005
  
  Causes:
  - Insufficient permissions to write to the file
  - The file is locked by another process
  - Disk is full or write-protected
  - The file path is invalid
  
  Suggestion: Check file permissions and ensure sufficient disk space
  
  For more information: https://gweidart.github.io/cursor-utils/errors/install-005.md
```

## Common Causes

1. **Permission Issues**: You don't have write permissions for the file or its directory.
2. **File Locking**: The file is currently opened or locked by another application.
3. **Disk Space**: Insufficient disk space to write the file.
4. **Read-Only File System**: The target location is on a read-only file system.
5. **Path Issues**: The file path is invalid or contains characters not supported by the file system.
6. **File Already Exists**: The file exists and is marked as read-only or protected.

## Solutions

### Check and fix file permissions

Ensure you have the necessary permissions to write to the file location:

```bash
# Linux/macOS
# Check file permissions
ls -la /path/to/file
# Change permissions if needed
chmod 644 /path/to/file
# Change directory permissions if needed
chmod 755 /path/to/directory/

# Windows (PowerShell)
# Check file attributes
Get-Item -Path "C:\path\to\file" | Format-List *
# Remove read-only attribute if needed
Set-ItemProperty -Path "C:\path\to\file" -Name IsReadOnly -Value $false
```

### Check disk space

Ensure you have sufficient disk space:

```bash
# Linux/macOS
df -h

# Windows (PowerShell)
Get-PSDrive C
```

### Check for locked files

Determine if the file is locked by another process:

```bash
# Linux/macOS
lsof | grep "/path/to/file"

# Windows (PowerShell)
Get-Process | Where-Object {$_.Modules.FileName -like "*targetfile*"}
```

### Try an alternative location

Specify an alternative location for the installation:

```bash
cursor-utils install --path /different/path/
```

### Run with elevated privileges

If writing to a system location, try running with elevated privileges:

```bash
# Linux/macOS
sudo cursor-utils install

# Windows (run as Administrator)
```

### Close competing applications

Ensure no other applications are using the files being written:
- Close code editors that might have the file open
- Check for antivirus software that might be scanning the file
- Close backup software that might be accessing the file

## Related Commands

- `cursor-utils install --help` - Show help for the install command
- `cursor-utils config show` - Display current configuration
- `cursor-utils --version` - Check your current version

## Related Error Codes

- [INVALID_PATH (install-001)](install-001.md) - Invalid path specification
- [DIRECTORY_ERROR (install-004)](install-004.md) - Error creating or accessing directory
- [GENERAL_FILE_ERROR (general-002)](general-002.md) - General file error

## Advanced Troubleshooting

### Check write access with a test file

Test if you can create a simple file in the same location:

```bash
# Linux/macOS
touch /path/to/directory/test-file.txt
cat > /path/to/directory/test-file.txt << EOF
Test content
EOF

# Windows (PowerShell)
"Test content" | Out-File -FilePath "C:\path\to\directory\test-file.txt"
```

### Check file system type

Some file systems might have limitations:

```bash
# Linux/macOS
df -T /path/to/directory

# Windows
# Check using Disk Management
```

### Check for filesystem quota limits

```bash
# Linux/macOS
quota -v

# Windows
fsutil quota query C:
```

### Check for special file attributes

```bash
# Linux/macOS
lsattr /path/to/file

# Windows (PowerShell)
Get-Item "C:\path\to\file" | Format-List *
```

## Platform-Specific Issues

### Windows

- **File Path Length**: Windows has a 260-character path limit by default
- **UAC (User Account Control)**: May block writes to protected directories
- **Reserved File Names**: Avoid reserved names like CON, PRN, AUX, NUL
- **Hidden or System Files**: Check if installation is trying to modify system files

### Linux/macOS

- **File System Permissions**: Check user, group, and world permissions
- **File System Mounts**: Check if mounted as read-only
- **SELinux/AppArmor**: Security policies might restrict file operations
- **Symbolic Links**: Check if file is a symlink to a location with different permissions

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run the installation with debug logging:
   ```bash
   cursor-utils install --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Try creating the file manually:
   ```bash
   # Example for a config file
   touch ~/.cursor-utils/config.yaml
   ```

4. [Submit a bug report](https://github.com/gweidart/cursor-utils/issues) with details about:
   - The complete error message
   - Your operating system and version
   - File system type
   - Permissions of the parent directory
   - The output from the debug command 