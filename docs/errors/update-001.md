# UPDATE_FAILED (update-001)

## Error Description

This error occurs when Cursor Utils encounters an issue during the update process. The update may fail due to network issues, permission problems, dependency conflicts, or other update-related problems.

## Example Error

```
× ERROR: Failed to update Cursor Utils
  Code: update-001
  
  Causes:
  - Network connectivity issues
  - Insufficient permissions
  - Dependency conflicts
  - Corrupted installation
  - Package repository issues
  
  Suggestion: Check your internet connection and permissions, then try again
  
  For more information: https://gweidart.github.io/cursor-utils/errors/update-001.md
```

## Common Causes

1. **Network Issues**: Problems connecting to the package repository or GitHub.
2. **Permission Problems**: Insufficient permissions to update files.
3. **Dependency Conflicts**: Conflicts with other installed packages.
4. **Corrupted Installation**: The existing installation is in an inconsistent state.
5. **Version Problems**: Issues with version detection or compatibility.
6. **Disk Space**: Insufficient disk space for the updated files.

## Solutions

### Check internet connection

Ensure you have a stable internet connection:

```bash
# Test connection to GitHub
ping github.com

# Test connection to PyPI
ping pypi.org
```

### Run with elevated privileges

If updating in a system location, try running with elevated privileges:

```bash
# Linux/macOS
sudo cursor-utils update

# Windows (run as Administrator)
```

### Check disk space

Ensure you have sufficient disk space:

```bash
# Linux/macOS
df -h

# Windows (PowerShell)
Get-PSDrive C
```

### Try a specific version

If the latest version is causing problems, you can try updating to a specific version:

```bash
cursor-utils update --version X.Y.Z
```

### Clear cache and try again

Clear package caches and try updating again:

```bash
# Clear pip cache
pip cache purge

# For UV users (recommended)
uv cache clear
```

### Force reinstallation

Force a clean reinstallation:

```bash
pip uninstall -y cursor-utils
pip install --no-cache-dir cursor-utils
cursor-utils install --force
```

## Related Commands

- `cursor-utils install --help` - Show help for the install command
- `cursor-utils --version` - Check your current version
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [UNKNOWN_ERROR (update-999)](update-999.md) - Unknown error during update
- [VERSION_ERROR (version-001)](version-001.md) - General version error
- [INVALID_VERSION (version-002)](version-002.md) - Invalid version format

## Advanced Troubleshooting

### Check update logs

Check the update logs for more detailed information:

```bash
cat ~/.cursor-utils/logs/update.log
cat ~/.cursor-utils/logs/cursor-utils.log
```

### Check installed version

Verify your currently installed version:

```bash
cursor-utils --version
pip show cursor-utils
```

### Check for network proxy issues

If you're behind a proxy, ensure it's properly configured:

```bash
# Check proxy environment variables
echo $HTTP_PROXY
echo $HTTPS_PROXY

# Configure proxy for pip if needed
pip config set global.proxy http://user:password@proxy:port
```

### Try updating dependencies separately

Update dependencies separately before updating Cursor Utils:

```bash
pip install --upgrade pip setuptools wheel
```

### Check for conflicts with other packages

Look for package conflicts:

```bash
pip check
```

## Update Strategies

### Standard Update

The default update method:

```bash
cursor-utils update
```

### Clean Update

Performs a more thorough update by clearing caches:

```bash
cursor-utils update --clean
```

### Development Update

For development installations:

```bash
cd /path/to/cursor-utils
git pull
pip install -e .
```

### Manual Files Update

If the package update succeeds but file updates fail:

```bash
cursor-utils files update
```

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run the update with debug logging:
   ```bash
   cursor-utils update --debug
   ```

2. Try a complete removal and fresh installation:
   ```bash
   # Remove everything
   pip uninstall -y cursor-utils
   rm -rf ~/.cursor-utils
   
   # Fresh install
   pip install cursor-utils
   cursor-utils install
   ```

3. Check GitHub for known issues:
   [GitHub Issues](https://github.com/gweidart/cursor-utils/issues)

4. Submit a bug report with:
   - Your operating system and version
   - Your Cursor Utils version (`cursor-utils --version`)
   - Complete error message
   - Debug logs
   - Steps to reproduce the error 