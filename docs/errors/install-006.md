# ALREADY_INSTALLED (install-006)

## Error Description

This error occurs when you attempt to install Cursor Utils in a location where it is already installed. The installation process detects existing Cursor Utils files in the target location and prevents the reinstallation to avoid conflicts or overwriting customizations.

## Example Error

```
× ERROR: Cursor Utils is already installed in the specified location
  Code: install-006
  
  Causes:
  - Cursor Utils is already installed in the target directory
  - The installation directory contains existing Cursor Utils files
  - A previous installation was not properly uninstalled
  
  Suggestion: Use the update command instead, or specify a different installation path
  
  For more information: https://github.com/gweidart/cursor-utils/errors/install-006.md
```

## Common Causes

1. **Previous Installation**: Cursor Utils is already installed in the specified location.
2. **Partial Installation**: A previous installation attempt left files in the target directory.
3. **Shared Installation Path**: Multiple users sharing an installation path.
4. **Manual File Creation**: Files that match Cursor Utils patterns were manually created.
5. **Version Control System**: The repository was cloned or copied with existing Cursor Utils files.

## Solutions

### Use the update command

If you're trying to update an existing installation, use the update command instead:

```bash
cursor-utils update
```

### Specify a different installation path

Install to a different location:

```bash
cursor-utils install --path /different/path/
```

### Force reinstallation

If you want to reinstall over the existing installation, use the force flag:

```bash
cursor-utils install --force
```

This will overwrite the existing installation, but preserve your configuration and API keys.

### Check for existing installation

Verify if and where Cursor Utils is currently installed:

```bash
cursor-utils --version
which cursor-utils  # on Linux/macOS
where cursor-utils  # on Windows
```

### Uninstall first

Uninstall the existing installation before reinstalling:

```bash
# Remove using pip if installed that way
pip uninstall cursor-utils

# Or remove manually
rm -rf ~/.cursor-utils  # Use caution with rm -rf commands!
```

## Related Commands

- `cursor-utils update` - Update an existing installation
- `cursor-utils config show` - Display current configuration
- `cursor-utils --version` - Check the installed version

## Related Error Codes

- [INVALID_PATH (install-001)](install-001.md) - Invalid path specification
- [UPDATE_FAILED (update-001)](update-001.md) - Update process failed

## Advanced Troubleshooting

### Check for installation markers

Cursor Utils creates marker files to identify installations:

```bash
# Check for installation marker
ls -la ~/.cursor-utils/.installed

# Windows
Get-Item -Path "$HOME\.cursor-utils\.installed" -ErrorAction SilentlyContinue
```

### Clean partial installations

If you have a partial installation, you can clean it up:

```bash
# Be careful with these commands - they delete files
rm -rf ~/.cursor-utils/*
mkdir -p ~/.cursor-utils
touch ~/.cursor-utils/.clean
```

### Backup your configuration

Before reinstalling, back up your configuration:

```bash
# Backup config
cp ~/.cursor-utils/config.yaml ~/cursor-utils-config-backup.yaml

# Backup API keys
cp ~/.env ~/env-backup
```

### Check for multiple installations

You might have Cursor Utils installed in multiple locations:

```bash
# Find all cursor-utils executables
find / -name cursor-utils 2>/dev/null  # Linux/macOS

# Windows (PowerShell)
Get-ChildItem -Path C:\ -Filter cursor-utils.exe -Recurse -ErrorAction SilentlyContinue
```

## Installation Modes

Cursor Utils supports different installation modes:

### User Installation (Default)

Installs for the current user only:

```bash
cursor-utils install
```

### System-wide Installation

Installs for all users (requires admin/root):

```bash
sudo cursor-utils install --system
```

### Development Installation

Installs in development mode for contributing:

```bash
git clone https://github.com/gweidart/cursor-utils.git
cd cursor-utils
pip install -e .
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

3. Try a complete removal and fresh installation:
   ```bash
   # Remove config and installation
   rm -rf ~/.cursor-utils
   pip uninstall -y cursor-utils
   
   # Fresh install
   pip install cursor-utils
   cursor-utils install
   ```

4. [Submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - Your installation method (pip, git, etc.)
   - Complete error message
   - Output of `cursor-utils --version`
   - Output of `which cursor-utils` (Linux/macOS) or `where cursor-utils` (Windows) 