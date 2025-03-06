# REPO_INVALID_URL (repo-004)

## Error Description

This error occurs when Cursor Utils encounters an invalid repository URL. This could be due to a malformed URL, a non-existent repository, or a URL that doesn't point to a valid Git repository.

## Example Error

```
× ERROR: Invalid repository URL
  Code: repo-004
  
  Causes:
  - The URL format is incorrect
  - The repository does not exist
  - The URL does not point to a valid Git repository
  - Typo in repository owner or name
  
  Suggestion: Check the URL format and ensure the repository exists
  
  For more information: https://gweidart.github.io/cursor-utils/errors/repo-004.md
```

## Common Causes

1. **Malformed URL**: The URL structure doesn't follow the required format.
2. **Non-existent Repository**: The repository doesn't exist at the specified URL.
3. **Typos**: Typos in the repository owner or name.
4. **Private Repository**: The repository exists but is private and not accessible.
5. **Not a Git Repository**: The URL points to a resource that is not a Git repository.
6. **Incorrect Protocol**: Using the wrong protocol (e.g., HTTP instead of HTTPS or SSH).

## Solutions

### Check URL format

Ensure the repository URL follows the correct format:

```bash
# GitHub URLs
cursor-utils repo https://github.com/username/repo-name
cursor-utils repo github.com/username/repo-name
cursor-utils repo username/repo-name  # Short form for GitHub

# GitLab URLs
cursor-utils repo https://gitlab.com/username/repo-name

# Bitbucket URLs
cursor-utils repo https://bitbucket.org/username/repo-name
```

### Verify repository existence

Check if the repository exists and is accessible:

```bash
# Open in browser to check
open https://github.com/username/repo-name

# Or try cloning manually
git clone https://github.com/username/repo-name test-clone
```

### Check for typos

Double-check the repository owner and name for typos:

```bash
# Example of incorrect URL with typo
cursor-utils repo https://github.com/usrename/repo-name  # 'usrename' instead of 'username'

# Correct URL
cursor-utils repo https://github.com/username/repo-name
```

### Try different URL formats

If one URL format doesn't work, try another:

```bash
# Instead of
cursor-utils repo git@github.com:username/repo-name.git

# Try
cursor-utils repo https://github.com/username/repo-name
```

### Check authentication for private repositories

For private repositories, ensure you have the necessary authentication:

```bash
# Set GitHub token
cursor-utils config api_keys --type GITHUB
```

## Related Commands

- `cursor-utils repo --help` - Show help for the repo command
- `cursor-utils config api_keys` - Manage API keys including GitHub tokens
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [REPO_CLONE_ERROR (repo-001)](repo-001.md) - Error cloning repository
- [GITHUB_REPO_NOT_FOUND (github-003)](github-003.md) - GitHub repository not found
- [GENERAL_INVALID_URL (general-006)](general-006.md) - General invalid URL

## Valid Repository URL Formats

### GitHub

```
https://github.com/username/repo-name
https://github.com/username/repo-name.git
github.com/username/repo-name
username/repo-name (shorthand notation)
git@github.com:username/repo-name.git (SSH format, requires SSH setup)
```

### GitLab

```
https://gitlab.com/username/repo-name
https://gitlab.com/username/repo-name.git
gitlab.com/username/repo-name
git@gitlab.com:username/repo-name.git (SSH format)
```

### Bitbucket

```
https://bitbucket.org/username/repo-name
https://bitbucket.org/username/repo-name.git
bitbucket.org/username/repo-name
git@bitbucket.org:username/repo-name.git (SSH format)
```

## Advanced Troubleshooting

### Test URL resolution

Check if the domain can be resolved:

```bash
# Using ping
ping github.com

# Using nslookup
nslookup github.com

# Using curl
curl -I https://github.com/username/repo-name
```

### Check Git configuration

Verify your Git configuration:

```bash
git config --list
```

### Test SSH connectivity (for SSH URLs)

If using SSH URLs, test SSH connectivity:

```bash
ssh -T git@github.com
```

### Check for URL encoding issues

Some special characters in URLs need to be properly encoded:

```bash
# URL with space (incorrect)
cursor-utils repo https://github.com/username/repo name

# URL with space (correct)
cursor-utils repo https://github.com/username/repo%20name
```

## Common URL Errors and Solutions

| Error | Description | Solution |
|-------|-------------|----------|
| 404 Not Found | Repository doesn't exist | Check URL, verify existence |
| 403 Forbidden | No access to repository | Check authentication, permissions |
| Host unreachable | Cannot connect to host | Check internet connection, DNS |
| Invalid username | Username doesn't exist | Check for typos in owner name |
| SSL certificate error | SSL verification failed | Check system certificates |

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug logging:
   ```bash
   cursor-utils repo https://github.com/username/repo-name --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Try testing the URL with external tools:
   ```bash
   # Using curl to check URL status
   curl -I https://github.com/username/repo-name
   
   # Using wget to check URL
   wget --spider https://github.com/username/repo-name
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - The repository URL you're trying to use
   - The output of any tests you've run
   - What solutions you've already tried 