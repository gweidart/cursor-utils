# FILE_NOT_FOUND (install-002)

## Error Description

This error occurs when Cursor Utils cannot find a required file during the installation process. The file might be a template, configuration file, or another essential file needed for proper installation.

## Example Error

```
× ERROR: Required file not found during installation
  Code: install-002
  
  Causes:
  - The specified file does not exist
  - The file path is incorrect
  - The installation package might be corrupted
  
  Suggestion: Verify the file path or try reinstalling Cursor Utils
  
  For more information: https://github.com/gweidart/cursor-utils/errors/install-002.md
```

## Common Causes

1. **Missing Installation Files**: One or more files required for installation are missing.
2. **Incomplete Download**: The package download might have been interrupted or incomplete.
3. **Incorrect Path Reference**: The installation process is looking for a file in the wrong location.
4. **File Removal**: A required file was accidentally deleted after initial download.
5. **Permission Issues**: The file exists but cannot be accessed due to permission restrictions.

## Solutions

### Verify file existence

Check if the file exists at the expected location:

```bash
# Linux/macOS
ls -la /path/to/expected/file.ext

# Windows (PowerShell)
Get-ChildItem -Path C:\path\to\expected\file.ext -ErrorAction SilentlyContinue
```

### Re-download the installation package

If you suspect the package is corrupted or incomplete, try downloading it again:

```bash
# Using pip
pip uninstall cursor-utils
pip install cursor-utils

# Using UV (recommended)
uv pip uninstall cursor-utils
uv pip install cursor-utils
```

### Check installation source

If you installed from a specific source like GitHub, ensure the repository is complete:

```bash
# Clone the repository again
git clone https://github.com/gweidart/cursor-utils.git
cd cursor-utils
pip install -e .
```

### Check for custom templates

If you're using custom templates during installation, verify they exist:

```bash
# Linux/macOS
ls -la ~/.cursor-utils/templates/

# Windows (PowerShell)
Get-ChildItem -Path "$HOME\.cursor-utils\templates\" -ErrorAction SilentlyContinue
```

### Run with verbose output

Execute the installation with verbose output to see which file is missing:

```bash
cursor-utils install --debug
```

## Related Commands

- `cursor-utils install --help` - Show help for the install command
- `cursor-utils --version` - Check your current version
- `cursor-utils update` - Update to the latest version which might fix missing files

## Related Error Codes

- [INVALID_PATH (install-001)](install-001.md) - Invalid path specification
- [TEMPLATE_ERROR (install-003)](install-003.md) - Error processing template
- [GENERAL_FILE_ERROR (general-002)](general-002.md) - General file error

## Advanced Troubleshooting

### Check file integrity

If the file exists but might be corrupted, you can check its integrity:

```bash
# For text files, try to view them
cat /path/to/file.txt

# For binary files, check file size
ls -la /path/to/file.bin
```

### Recreate default files

Some configuration files can be recreated if missing:

```bash
cursor-utils config init
```

### Check installation logs

Installation logs might provide additional details:

```bash
cat ~/.cursor-utils/logs/install.log
```

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run the command with the `--debug` flag to get more detailed error information:
   ```bash
   cursor-utils install --debug
   ```

2. Check the full logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. [Submit a bug report](https://github.com/gweidart/cursor-utils/issues) with the detailed information. 