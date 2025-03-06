# VERSION_ERROR (version-001)

## Error Description

This error occurs when Cursor Utils encounters a general issue related to version handling, such as incompatible versions, version detection failures, or version-related conflicts that don't fall into more specific error categories.

## Example Error

```
× ERROR: Version-related error encountered
  Code: version-001
  
  Causes:
  - Version mismatch between components
  - Cannot determine installed version
  - Version incompatibility with system
  - Minimum version requirements not met
  
  Suggestion: Check installed versions and ensure compatibility
  
  For more information: https://gweidart.github.io/cursor-utils/errors/version-001.md
```

## Common Causes

1. **Component Version Mismatch**: Different components of Cursor Utils have incompatible versions.
2. **Version Detection Failure**: The system cannot determine the installed version.
3. **Dependency Version Conflicts**: Conflicts between Cursor Utils version and its dependencies.
4. **Minimum Requirements**: The current version doesn't meet minimum requirements for a feature.
5. **Inconsistent Installation**: Parts of the installation were updated but others weren't.
6. **Python Version Incompatibility**: The installed version is incompatible with your Python version.

## Solutions

### Check current version

Verify your currently installed version:

```bash
cursor-utils --version
pip show cursor-utils
```

### Update to the latest version

Update to the latest version to resolve version conflicts:

```bash
cursor-utils update
```

### Check Python version compatibility

Ensure your Python version is compatible:

```bash
python --version
```

Cursor Utils requires Python 3.7 or higher. If you're using an older version, you'll need to upgrade Python or use a compatible Cursor Utils version.

### Reinstall with a specific version

If needed, install a specific version:

```bash
pip uninstall -y cursor-utils
pip install cursor-utils==X.Y.Z
```

### Check component versions

Check the versions of all components:

```bash
cursor-utils components versions
```

### Force consistent versions

Force all components to use consistent versions:

```bash
cursor-utils install --force
```

## Related Commands

- `cursor-utils update` - Update to the latest version
- `cursor-utils --version` - Check the current version
- `cursor-utils install --force` - Force a fresh installation with consistent versions

## Related Error Codes

- [INVALID_VERSION (version-002)](version-002.md) - Invalid version format
- [UPDATE_FAILED (update-001)](update-001.md) - Update process failed
- [UNKNOWN_ERROR (update-999)](update-999.md) - Unknown error during update

## Advanced Troubleshooting

### Check version constraints

Examine version constraints in the package:

```bash
pip show cursor-utils
```

Look for the "Requires" section to see dependency version constraints.

### Check for conflicting packages

Identify packages that might conflict with Cursor Utils:

```bash
pip list | grep cursor
pip check
```

### Examine version information in detail

Get detailed version information:

```bash
cursor-utils --version --verbose
```

### Check for partial updates

If a previous update was interrupted, some components might have different versions:

```bash
find ~/.cursor-utils -name "version.txt" -exec cat {} \;
```

## Version Compatibility Matrix

Here's a quick reference for version compatibility:

| Cursor Utils Version | Python Version | Key Dependencies |
|----------------------|----------------|------------------|
| 0.1.x                | 3.7+           | click, rich, requests |
| 0.2.x                | 3.8+           | click, rich, requests, pyyaml |
| 0.3.x+               | 3.9+           | click, rich, requests, pyyaml, typing-extensions |

### Environment-specific considerations

#### Linux/macOS

On Linux/macOS, check for system Python vs. user Python:

```bash
which -a python
which -a pip
```

Make sure you're using the intended Python installation.

#### Windows

On Windows, check for multiple Python installations:

```powershell
where python
where pip
py --list
```

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug mode to get more detailed information:
   ```bash
   cursor-utils --version --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Try a complete reinstallation:
   ```bash
   pip uninstall -y cursor-utils
   rm -rf ~/.cursor-utils
   pip install cursor-utils
   cursor-utils install
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - Complete error message
   - Output of `cursor-utils --version`
   - Output of `python --version`
   - Output of `pip list`
   - Operating system and version
   - Installation method used 