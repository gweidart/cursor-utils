# PROJECT_INVALID_URL (project-003)

## Error Description

This error occurs when Cursor Utils encounters an invalid URL while trying to access a remote project. This could be due to a malformed URL, a non-existent project, or a URL that doesn't point to a valid project or repository.

## Example Error

```
× ERROR: Invalid project URL
  Code: project-003
  
  Causes:
  - The URL format is incorrect
  - The project does not exist at the provided URL
  - The URL is not accessible (private or requires authentication)
  - The URL points to a resource that is not a valid project
  - Typo in the project URL
  
  Suggestion: Check the URL format and ensure the project exists
  
  For more information: https://gweidart.github.io/cursor-utils/errors/project-003.md
```

## Common Causes

1. **Malformed URL**: The URL structure doesn't follow the required format.
2. **Non-existent Project**: The project doesn't exist at the specified URL.
3. **Typos**: Typos in the project URL or path.
4. **Private Project**: The project exists but is private and not accessible.
5. **Not a Project**: The URL points to a resource that is not a valid project.
6. **Incorrect Protocol**: Using the wrong protocol (e.g., HTTP instead of HTTPS).

## Solutions

### Check URL format

Ensure the project URL follows the correct format:

```bash
# Example of correct URL formats
cursor-utils project analyze https://github.com/username/project-name
cursor-utils project analyze https://gitlab.com/username/project-name
cursor-utils project analyze https://bitbucket.org/username/project-name
```

### Verify project existence

Check if the project exists and is accessible by opening the URL in a web browser.

### Check for typos

Double-check the project URL for typos:

```bash
# Example of incorrect URL with typo
cursor-utils project analyze https://github.com/usrename/project-name  # 'usrename' instead of 'username'

# Correct URL
cursor-utils project analyze https://github.com/username/project-name
```

### Try different URL formats

If one URL format doesn't work, try another:

```bash
# Instead of
cursor-utils project analyze git@github.com:username/project-name.git

# Try
cursor-utils project analyze https://github.com/username/project-name
```

### Check authentication for private projects

For private projects, ensure you have the necessary authentication:

```bash
# Set up authentication
cursor-utils config api_keys --type GITHUB
```

### Test with a public project

If you're having issues with a specific project, try with a known public project:

```bash
cursor-utils project analyze https://github.com/python/cpython
```

## Related Commands

- `cursor-utils project --help` - Show help for the project command
- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [PROJECT_TOO_LARGE (project-001)](project-001.md) - Project size exceeds limits
- [PROJECT_ANALYZE_ERROR (project-002)](project-002.md) - Error analyzing project
- [REPO_INVALID_URL (repo-004)](repo-004.md) - Invalid repository URL
- [GITHUB_REPO_NOT_FOUND (github-003)](github-003.md) - GitHub repository not found

## Valid Project URL Formats

### GitHub

```
https://github.com/username/project-name
https://github.com/username/project-name.git
github.com/username/project-name
git@github.com:username/project-name.git (SSH format)
```

### GitLab

```
https://gitlab.com/username/project-name
https://gitlab.com/username/project-name.git
gitlab.com/username/project-name
git@gitlab.com:username/project-name.git (SSH format)
```

### Bitbucket

```
https://bitbucket.org/username/project-name
https://bitbucket.org/username/project-name.git
bitbucket.org/username/project-name
git@bitbucket.org:username/project-name.git (SSH format)
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
curl -I https://github.com/username/project-name
```

### Check Git configuration

If using Git URLs, verify your Git configuration:

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
cursor-utils project analyze https://github.com/username/project name

# URL with space (correct)
cursor-utils project analyze https://github.com/username/project%20name
```

## Common URL Errors and Solutions

| Error | Description | Solution |
|-------|-------------|----------|
| 404 Not Found | Project doesn't exist | Check URL, verify existence |
| 403 Forbidden | No access to project | Check authentication, permissions |
| Host unreachable | Cannot connect to host | Check internet connection, DNS |
| Invalid username | Username doesn't exist | Check for typos in owner name |
| SSL certificate error | SSL verification failed | Check system certificates |

## Project URL Best Practices

1. **Use HTTPS**: Prefer HTTPS URLs over SSH or Git protocol for better compatibility
2. **Complete URLs**: Always use complete URLs including the protocol (https://)
3. **Check accessibility**: Ensure you have access to the project before analyzing
4. **Verify URLs**: Double-check URLs for typos and errors
5. **Try alternatives**: If one URL format fails, try another

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug logging:
   ```bash
   cursor-utils project analyze https://github.com/username/project-name --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Try testing the URL with external tools:
   ```bash
   # Using curl to check URL status
   curl -I https://github.com/username/project-name
   
   # Using wget to check URL
   wget --spider https://github.com/username/project-name
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - The project URL you're trying to use
   - The output of any tests you've run
   - What solutions you've already tried 