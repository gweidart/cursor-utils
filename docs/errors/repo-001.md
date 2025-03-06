# REPO_CLONE_ERROR (repo-001)

## Error Description

This error occurs when Cursor Utils fails to clone a repository. This could be due to network issues, authentication problems, invalid repository URLs, or other Git-related issues.

## Example Error

```
× ERROR: Failed to clone repository
  Code: repo-001
  
  Causes:
  - Network connectivity issues
  - Repository URL is invalid or inaccessible
  - Authentication failed for private repository
  - Git is not installed or misconfigured
  - Insufficient permissions for the destination directory
  
  Suggestion: Check the repository URL and your network connection
  
  For more information: https://github.com/gweidart/cursor-utils/errors/repo-001.md
```

## Common Causes

1. **Network Issues**: Problems connecting to the repository host (GitHub, GitLab, etc.).
2. **Invalid URL**: The repository URL is incorrect or malformed.
3. **Authentication**: Missing or invalid credentials for a private repository.
4. **Git Installation**: Git is not installed or not in the PATH.
5. **Permission Issues**: Insufficient permissions to write to the destination directory.
6. **Repository Doesn't Exist**: The specified repository doesn't exist or has been deleted.

## Solutions

### Check repository URL

Verify that the repository URL is correct:

```bash
# Use the full URL format
cursor-utils repo https://github.com/username/repo-name

# Or the shorthand format
cursor-utils repo username/repo-name
```

### Test manual cloning

Try cloning the repository manually to check if it works:

```bash
git clone https://github.com/username/repo-name test-clone
```

### Check network connectivity

Ensure you can connect to the repository host:

```bash
ping github.com
curl -I https://github.com
```

### Verify Git installation

Make sure Git is installed and in your PATH:

```bash
git --version
which git  # Linux/macOS
where git  # Windows
```

### Check authentication for private repositories

For private repositories, ensure you have the necessary credentials:

```bash
# Set GitHub token if needed
cursor-utils config api_keys --type GITHUB
```

### Try with a different repository

If one repository is causing issues, try with a different one:

```bash
cursor-utils repo https://github.com/torvalds/linux
```

## Related Commands

- `cursor-utils repo --help` - Show help for the repo command
- `cursor-utils config api_keys` - Manage API keys including GitHub tokens
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [REPO_INVALID_URL (repo-004)](repo-004.md) - Invalid repository URL
- [GITHUB_AUTH_ERROR (github-001)](github-001.md) - GitHub authentication error
- [GITHUB_REPO_NOT_FOUND (github-003)](github-003.md) - GitHub repository not found

## Advanced Troubleshooting

### Check Git configuration

Verify your Git configuration:

```bash
git config --list
```

### Check SSH keys (if using SSH URLs)

If you're using SSH URLs, check your SSH keys:

```bash
# Check SSH keys
ls -la ~/.ssh

# Test SSH connection
ssh -T git@github.com
```

### Use HTTPS instead of SSH

Try using HTTPS URLs instead of SSH:

```bash
# Instead of
cursor-utils repo git@github.com:username/repo-name.git

# Use
cursor-utils repo https://github.com/username/repo-name
```

### Check proxy settings

If you're behind a proxy, check your proxy settings:

```bash
# Check environment variables
echo $HTTP_PROXY
echo $HTTPS_PROXY

# Check Git proxy settings
git config --global http.proxy
```

### Enable verbose output

Run with debug mode for more detailed information:

```bash
cursor-utils repo https://github.com/username/repo-name --debug
```

## Common Repository URL Formats

### GitHub

```
https://github.com/username/repo-name
github.com/username/repo-name
username/repo-name (shorthand for GitHub)
```

### GitLab

```
https://gitlab.com/username/repo-name
gitlab.com/username/repo-name
```

### Bitbucket

```
https://bitbucket.org/username/repo-name
bitbucket.org/username/repo-name
```

## Git Error Messages and Solutions

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| `Repository not found` | Repo doesn't exist or is private | Check URL or authenticate |
| `Authentication failed` | Invalid or missing credentials | Update GitHub token |
| `Permission denied` | Insufficient access rights | Check your permissions |
| `Could not resolve host` | Network or DNS issues | Check network connection |
| `fatal: destination path already exists` | Destination directory exists | Use a different directory |

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

3. Try cloning manually with verbose output:
   ```bash
   GIT_TRACE=1 git clone https://github.com/username/repo-name test-repo
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - The repository URL you're trying to clone
   - Output of `git --version`
   - Output of debug logs
   - Your operating system and network configuration 