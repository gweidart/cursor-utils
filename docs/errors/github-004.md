# GITHUB_PERMISSION_ERROR (github-004)

## Error Description

This error occurs when Cursor Utils attempts to perform an operation on a GitHub repository but lacks the necessary permissions. This could be due to insufficient token scopes, repository access restrictions, or organization-level permissions.

## Example Error

```
× ERROR: GitHub permission error
  Code: github-004
  
  Causes:
  - Your GitHub token lacks the required scopes
  - You don't have sufficient access to the repository
  - The repository has access restrictions
  - Organization policies prevent the requested action
  - The action requires admin permissions
  
  Suggestion: Check your GitHub token permissions and repository access
  
  For more information: https://github.com/gweidart/cursor-utils/errors/github-004.md
```

## Common Causes

1. **Insufficient Token Scopes**: Your GitHub token doesn't have the necessary scopes for the operation.
2. **Repository Access Level**: You have access to the repository but not at the level required (e.g., read-only vs. write).
3. **Protected Branches**: The operation involves a protected branch with restricted access.
4. **Organization Restrictions**: The organization has policies that restrict certain operations.
5. **Repository Settings**: The repository has settings that limit what actions can be performed.
6. **Two-Factor Authentication**: The account requires 2FA for certain operations.

## Solutions

### Check token scopes

Verify that your GitHub token has the necessary scopes:

```bash
# Check token info using curl
curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/user | grep -A 5 scopes
```

Common required scopes:
- `repo` - Full control of private repositories
- `public_repo` - Control of public repositories
- `read:org` - Read organization information
- `user` - Read user information
- `workflow` - Access to GitHub Actions workflows

### Generate a new token with proper scopes

Create a new GitHub token with the appropriate scopes:

1. Go to [GitHub Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select the necessary scopes (especially `repo` for full repository access)
4. Configure it in Cursor Utils:
   ```bash
   cursor-utils config api_keys --type GITHUB
   ```

### Check repository access level

Verify your access level to the repository:

1. Go to the repository on GitHub
2. Click on "Settings" (if you can see it)
3. Look for "Manage access" to check your role

Access levels:
- Read - Can view and clone the repository
- Triage - Can manage issues and pull requests
- Write - Can push to the repository
- Maintain - Can manage the repository without admin access
- Admin - Full control of the repository

### Check for protected branches

If working with branches, check if they're protected:

1. Go to the repository on GitHub
2. Click on "Settings" → "Branches"
3. Look for branch protection rules

### Ask for additional permissions

If you need more access:

1. Contact the repository owner or organization admin
2. Specify what operations you need to perform
3. Request the appropriate level of access

### Try a repository you own

If you're having permission issues, try with a repository you own:

```bash
cursor-utils github analyze YOUR_USERNAME/YOUR_REPO
```

## Related Commands

- `cursor-utils github --help` - Show help for the GitHub command
- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [GITHUB_AUTH_ERROR (github-001)](github-001.md) - GitHub authentication error
- [GITHUB_API_ERROR (github-002)](github-002.md) - GitHub API error
- [GITHUB_REPO_NOT_FOUND (github-003)](github-003.md) - GitHub repository not found
- [GITHUB_RATE_LIMIT (github-005)](github-005.md) - GitHub rate limit exceeded

## GitHub Permission Levels

GitHub has different permission levels for repositories:

| Permission Level | Description | Common Actions |
|------------------|-------------|----------------|
| Read | Can view and clone | Read code, issues, discussions |
| Triage | Can manage issues | Label issues, close inactive issues |
| Write | Can push changes | Push commits, create branches |
| Maintain | Can manage repo | Merge PRs, manage settings (except security) |
| Admin | Full control | Delete repo, add collaborators, change visibility |

## GitHub Token Scopes

Different operations require different token scopes:

| Scope | Description | Example Use Cases |
|-------|-------------|------------------|
| `repo` | Full access to private and public repositories | Clone, push, manage issues, webhooks |
| `public_repo` | Access to public repositories only | Public repo operations |
| `repo:status` | Access commit statuses | CI/CD integration |
| `repo_deployment` | Access deployment statuses | Deployment workflows |
| `read:org` | Read organization information | List organization repositories |
| `user` | Read user profile information | Get authenticated user info |
| `admin:org` | Organization administration | Manage organization settings |
| `admin:repo_hook` | Manage repository webhooks | Set up notifications |
| `workflow` | Access to Actions workflows | Work with GitHub Actions |

## Advanced Troubleshooting

### Test API calls with different scopes

Test API calls with different token scopes to identify what's needed:

```bash
# Create a test token with minimal scopes
# Then test specific API endpoints
curl -s -H "Authorization: token YOUR_TEST_TOKEN" https://api.github.com/repos/owner/repo
```

### Check for organization restrictions

Some organizations have additional restrictions:

1. Go to the organization page
2. Click on "Settings" → "Member privileges"
3. Check for restrictions on repository creation, deletion, etc.

### Look for two-factor authentication requirements

Some operations require 2FA to be enabled:

1. Go to your GitHub account settings
2. Click on "Password and authentication"
3. Check if 2FA is enabled

### Check for third-party access restrictions

Some organizations restrict third-party application access:

1. Go to the organization page
2. Click on "Settings" → "Third-party access"
3. Check for restrictions

## Permission Error Types

Common GitHub permission errors and their meanings:

| Error Message | Description | Solution |
|---------------|-------------|----------|
| Not Found | Resource exists but you don't have permission to see it | Request access |
| Resource not accessible by integration | OAuth App or GitHub App lacks access | Update App permissions |
| Organization has enabled OAuth App access restrictions | Third-party restrictions are active | Request organization approval |
| You need admin permissions | Operation requires administrator privileges | Request admin access |
| Repository is archived | Cannot modify archived repositories | Unarchive repository if allowed |
| Branch is protected | Cannot modify protected branches | Get write access to protected branches |

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

3. Test with a personal repository where you have full control:
   ```bash
   # Create a test repo on GitHub first
   cursor-utils github analyze YOUR_USERNAME/test-repo
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - The operation you were trying to perform
   - Your GitHub username
   - The repository you were trying to access
   - Output of debug logs (with sensitive information redacted) 