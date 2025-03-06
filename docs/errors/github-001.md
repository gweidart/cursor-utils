# GITHUB_AUTH_ERROR (github-001)

## Error Description

This error occurs when Cursor Utils cannot authenticate with GitHub due to invalid, expired, or missing authentication credentials. This error prevents GitHub-related commands from functioning correctly.

## Example Error

```
× ERROR: GitHub authentication failed
  Code: github-001
  
  Causes:
  - Invalid or expired GitHub token
  - Missing GitHub token
  - Insufficient permissions for the requested operation
  - GitHub API rate limit exceeded
  
  Suggestion: Check your GitHub token and ensure it has the required permissions
  
  For more information: https://gweidart.github.io/cursor-utils/errors/github-001.md
```

## Common Causes

1. **Invalid Token**: Your GitHub token is incorrect or has been revoked.
2. **Expired Token**: Your GitHub token has expired.
3. **Missing Token**: You haven't set up a GitHub token.
4. **Insufficient Permissions**: Your token doesn't have the required scopes or permissions for the operation.
5. **Rate Limiting**: You have exceeded the GitHub API rate limits.
6. **2FA Requirements**: Your GitHub account requires two-factor authentication, but it's not properly configured.

## Solutions

### Check your GitHub token

Verify that your GitHub token is correctly set up:

```bash
cursor-utils config api_keys
```

If your token is not set or needs to be updated, you can set it with:

```bash
cursor-utils config api_keys --type GITHUB
```

### Create a new GitHub token

If your token has expired or been revoked, create a new one:

1. Go to [GitHub Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select the appropriate scopes:
   - For most cursor-utils operations, you need at least:
     - `repo` (Full control of private repositories)
     - `read:org` (Read organization membership)
     - `workflow` (For CI/CD workflows)
4. Generate the token and copy it
5. Set it in cursor-utils:
   ```bash
   cursor-utils config api_keys --type GITHUB
   ```

### Check token environment variable

Ensure the token is correctly set in your environment:

```bash
# Linux/macOS
grep GITHUB_TOKEN ~/.env

# Windows (PowerShell)
Get-Content ~/.env | Select-String GITHUB_TOKEN
```

### Check token permissions

Verify that your token has the required permissions:

1. Go to [GitHub Personal Access Tokens](https://github.com/settings/tokens)
2. Find your token and check its scopes
3. If needed, create a new token with the appropriate scopes

### Check rate limits

If you're hitting rate limits, you can check your current GitHub API rate limit status:

```bash
curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/rate_limit
```

### Run in debug mode

Execute the command with the debug flag to get more detailed error information:

```bash
cursor-utils github analyze owner/repo --debug
```

## Related Commands

- `cursor-utils github --help` - Show help for the GitHub command
- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [GITHUB_API_ERROR (github-002)](github-002.md) - GitHub API error
- [GITHUB_REPO_NOT_FOUND (github-003)](github-003.md) - GitHub repository not found
- [GITHUB_PERMISSION_ERROR (github-004)](github-004.md) - GitHub permission error
- [GITHUB_RATE_LIMIT (github-005)](github-005.md) - GitHub rate limit exceeded

## Token Security Best Practices

1. **Never commit tokens to version control**
2. **Set an expiration date** on your tokens
3. **Use the least privilege principle** - only grant the scopes you need
4. **Regularly rotate** your tokens
5. **Consider using GitHub Apps** instead of personal access tokens for organizational use
6. **Enable 2FA** on your GitHub account

## Advanced Troubleshooting

### Check token validity

Test if your GitHub token is valid:

```bash
curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/user
```

If the token is valid, this should return information about your GitHub user.

### Check for environment variable conflicts

Ensure there are no conflicting environment variables:

```bash
# Linux/macOS
env | grep -i github

# Windows (PowerShell)
Get-ChildItem Env: | Where-Object { $_.Name -match 'github' }
```

### Check GitHub API status

Check if the GitHub API is experiencing issues:

```bash
curl -s https://www.githubstatus.com/api/v2/status.json
```

### Use a different token temporarily

If you suspect your token has issues, create a new temporary token for testing:

1. Go to [GitHub Personal Access Tokens](https://github.com/settings/tokens)
2. Create a new token with minimal scopes
3. Use it directly in the command:
   ```bash
   GITHUB_TOKEN=your-temp-token cursor-utils github analyze owner/repo
   ```

## GitHub Token Scopes

Different operations require different token scopes:

| Operation | Required Scopes |
|-----------|----------------|
| Public repo operations | `public_repo` |
| Private repo operations | `repo` |
| Organization access | `read:org` |
| Workflow actions | `workflow` |
| GitHub packages | `packages:read` or `packages:write` |
| User information | `user` |
| GPG key management | `admin:gpg_key` |

## GitHub Authentication Errors

Common GitHub authentication errors and their solutions:

| Error | Description | Solution |
|-------|-------------|----------|
| Bad credentials | Invalid token | Create new token |
| Token revoked | Token was revoked | Create new token |
| Insufficient scopes | Token missing required scopes | Add necessary scopes |
| User not authenticated | Missing token | Provide token |
| Maximum number of login attempts | Too many failed attempts | Wait before retrying |

## GitHub API Configuration

You can configure GitHub settings in your `cursor-utils.yaml` file:

```yaml
github:
  token_source: "env"  # 'env' or 'config'
  default_owner: "username"
  default_repo: "repo-name"
  template_dir: "~/.cursor-utils/templates/github"
```

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Try with a fresh token with all required scopes.

2. Run with debug logging:
   ```bash
   cursor-utils github analyze owner/repo --debug
   ```

3. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - The command you were trying to run
   - Debug log output (with sensitive information redacted)
   - What solutions you've already tried 