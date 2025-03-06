# INVALID_VERSION (version-002)

## Error Description

This error occurs when Cursor Utils encounters an invalid version format or specification. This typically happens when an incorrect version string is provided to commands that require version information, or when the version string in the configuration is malformed.

## Example Error

```
× ERROR: Invalid version format
  Code: version-002
  
  Causes:
  - The specified version string does not follow semantic versioning
  - The version contains invalid characters
  - The version format is incompatible with Cursor Utils
  - The version string is empty or malformed
  
  Suggestion: Use a valid version format (e.g., 1.2.3 or 1.2.3-beta.1)
  
  For more information: https://github.com/gweidart/cursor-utils/errors/version-002.md
```

## Common Causes

1. **Invalid Format**: The version string doesn't follow semantic versioning (SemVer) standards.
2. **Invalid Characters**: The version string contains characters that aren't allowed.
3. **Empty Version**: The version string is empty or only contains whitespace.
4. **Incorrect Prefix**: The version string has an incorrect prefix (e.g., "v1.0.0" instead of "1.0.0").
5. **Too Many/Few Components**: The version has too many or too few components (e.g., "1.2.3.4").
6. **Corrupted Version File**: The version information in the installation is corrupted.

## Solutions

### Use the correct version format

Cursor Utils follows Semantic Versioning (SemVer). Valid version formats include:

```
1.0.0
1.2.3
0.1.0
2.0.0-alpha
1.0.0-beta.1
1.0.0-rc.2
```

When specifying a version, use one of these formats:

```bash
cursor-utils update --version 1.2.3
```

### Check current version

Verify the currently installed version format:

```bash
cursor-utils --version
```

### Reinstall with a valid version

If you're trying to install a specific version, make sure to use a valid version string:

```bash
pip uninstall -y cursor-utils
pip install cursor-utils==1.2.3
```

### Fix version file

If the version file is corrupted, you can try fixing it:

```bash
# Find the version file
find ~/.cursor-utils -name "version.txt"

# Fix the version file (replace X.Y.Z with a valid version)
echo "X.Y.Z" > ~/.cursor-utils/version.txt
```

### Update to the latest version

If you're unsure about version numbers, simply update to the latest version:

```bash
cursor-utils update
```

## Related Commands

- `cursor-utils --version` - Check the current version
- `cursor-utils update` - Update to the latest version
- `cursor-utils update --version X.Y.Z` - Update to a specific version

## Related Error Codes

- [VERSION_ERROR (version-001)](version-001.md) - General version error
- [UPDATE_FAILED (update-001)](update-001.md) - Update process failed

## Advanced Troubleshooting

### Understanding Semantic Versioning

Semantic Versioning (SemVer) uses a three-part version number: MAJOR.MINOR.PATCH

1. **MAJOR** version increments when incompatible API changes are made
2. **MINOR** version increments when functionality is added in a backward-compatible manner
3. **PATCH** version increments when backward-compatible bug fixes are made

Pre-release versions can be denoted by appending a hyphen and identifiers:
- `1.0.0-alpha`
- `1.0.0-beta.1`
- `1.0.0-rc.1`

### Check version constraints

Examine version constraints in the package:

```bash
pip show cursor-utils
```

### Check Git tags

If you're working with a Git repository, check available version tags:

```bash
git tag
```

### Manually set version for development

For development installations, you can set the version manually:

```bash
# In your cursor-utils directory
bump-my-version set X.Y.Z
```

## Common Version Format Errors

| Invalid Format | Issue | Correct Format |
|----------------|-------|----------------|
| `v1.0.0`       | Includes "v" prefix | `1.0.0` |
| `1.0`          | Missing patch version | `1.0.0` |
| `1`            | Missing minor and patch | `1.0.0` |
| `1.0.0.0`      | Too many components | `1.0.0` |
| `1.0.0alpha`   | Missing hyphen for pre-release | `1.0.0-alpha` |
| `latest`       | Not a version number | Specify an actual version |
| `1.0.0+build.1` | Build metadata not supported | `1.0.0` |

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Try a complete reinstallation with a specific, known-good version:
   ```bash
   pip uninstall -y cursor-utils
   pip install cursor-utils==0.1.0  # Adjust with a known good version
   cursor-utils install
   ```

2. Check the logs for more details:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - The version string you were trying to use
   - Output of `cursor-utils --version`
   - Commands you were running when the error occurred 