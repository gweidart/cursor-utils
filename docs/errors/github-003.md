# GITHUB_REPO_NOT_FOUND (github-003)

## Error Description

This error occurs when Cursor Utils attempts to access a GitHub repository that cannot be found. This could be due to the repository not existing, being private with insufficient access permissions, or having been renamed or deleted.

## Example Error

```
× ERROR: GitHub repository not found
  Code: github-003
  
  Causes:
  - The repository does not exist
  - The repository is private and you don't have access
  - The repository has been renamed or moved
  - There is a typo in the repository name or owner
  - The repository has been deleted
  
  Suggestion: Check the repository name and ensure it exists
  
  For more information: https://github.com/gweidart/cursor-utils/errors/github-003.md
```

## Common Causes

1. **Non-existent Repository**: The specified repository doesn't exist on GitHub.
2. **Private Repository**: The repository exists but is private, and you don't have permission to access it.
3. **Renamed Repository**: The repository has been renamed or transferred to a different owner.
4. **Typos**: There's a typo in the repository name or owner.
5. **Deleted Repository**: The repository has been deleted from GitHub.
6. **GitHub Account Issues**: The GitHub account that owns the repository has been suspended or deleted.

## Solutions

### Check repository existence

Verify that the repository exists by navigating to it in a web browser:

```
https://github.com/owner/repo
```

Where `owner` is the username or organization name, and `repo` is the repository name.

### Check for typos

Ensure there are no typos in the repository name or owner:

```bash
# Example of correct usage
cursor-utils github analyze owner/repo

# Common typo (incorrect)
cursor-utils github analyze onwer/repo  # Typo in 'owner'
```

### Check access permissions

If the repository is private, ensure you have access to it:

1. Try accessing the repository in a web browser while logged into GitHub
2. Check if you've been invited to the repository
3. Request access from the repository owner

### Check for repository changes

If the repository previously existed but now returns a 404, check if it has been:
- Renamed
- Transferred to a different owner
- Made private
- Deleted

### Use a different repository

If you're unable to access the repository, try using a different one:

```bash
cursor-utils github analyze different-owner/different-repo
```

### Update GitHub token

Ensure your GitHub token has the necessary permissions:

```bash
cursor-utils config api_keys --type GITHUB
```

## Related Commands

- `cursor-utils github --help` - Show help for the GitHub command
- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [GITHUB_AUTH_ERROR (github-001)](github-001.md) - GitHub authentication error
- [GITHUB_API_ERROR (github-002)](github-002.md) - GitHub API error
- [GITHUB_PERMISSION_ERROR (github-004)](github-004.md) - GitHub permission error
- [REPO_INVALID_URL (repo-004)](repo-004.md) - Invalid repository URL

## Advanced Troubleshooting

### Test repository access via API

Check if the repository is accessible via the GitHub API:

```bash
# Replace YOUR_GITHUB_TOKEN with your actual token
curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/repos/owner/repo
```

If this returns a 404 error, the repository doesn't exist or you don't have access to it.

### Check repository visibility

If you own the repository, check its visibility settings:

1. Go to the repository on GitHub
2. Click on "Settings"
3. Scroll down to the "Danger Zone"
4. Check the "Change repository visibility" section

### Check organization access

If the repository belongs to an organization:

1. Ensure you're a member of the organization
2. Check your access level within the organization
3. Contact the organization administrators if necessary

### Try a different GitHub account

If possible, try accessing the repository with a different GitHub account to determine if it's an issue with your specific account.

## GitHub Repository URL Formats

Valid GitHub repository URL formats:

```
github.com/owner/repo
https://github.com/owner/repo
owner/repo (shorthand format)
```

## GitHub Repository Status Codes

Common HTTP status codes for repository access:

| Status Code | Description | Common Cause |
|-------------|-------------|--------------|
| 200 | OK | Repository exists and is accessible |
| 301 | Moved Permanently | Repository has been renamed or transferred |
| 404 | Not Found | Repository doesn't exist or you don't have access |
| 403 | Forbidden | Repository exists but you don't have permission |
| 410 | Gone | Repository has been deleted |

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug logging:
   ```bash
   cursor-utils github analyze owner/repo --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Try a known public repository:
   ```bash
   cursor-utils github analyze octocat/Spoon-Knife
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - The repository you're trying to access
   - The output of the debug logs
   - What solutions you've already tried 