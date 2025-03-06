# GITHUB_API_ERROR (github-002)

## Error Description

This error occurs when Cursor Utils encounters an issue while communicating with the GitHub API. This could be due to problems with the API request, response format, server errors, or other API-related issues.

## Example Error

```
× ERROR: GitHub API error
  Code: github-002
  
  Causes:
  - GitHub API service is unavailable
  - API request contains invalid parameters
  - Response from GitHub API is malformed
  - Network connectivity issues
  - API version incompatibility
  
  Suggestion: Check the error details and try again later
  
  For more information: https://github.com/gweidart/cursor-utils/errors/github-002.md
```

## Common Causes

1. **API Service Issues**: The GitHub API service is experiencing problems or downtime.
2. **Invalid Request**: The request to the GitHub API contains invalid parameters or formatting.
3. **Rate Limiting**: You've hit rate limits for API requests.
4. **Network Issues**: Problems with network connectivity to GitHub's servers.
5. **Response Format**: The API response is unexpected or malformed.
6. **GitHub Changes**: Changes to the GitHub API that are incompatible with Cursor Utils.

## Solutions

### Check GitHub status

Verify if GitHub and its API are experiencing issues:

```bash
curl -s https://www.githubstatus.com/api/v2/status.json
```

You can also visit the [GitHub Status Page](https://www.githubstatus.com/) to check for reported outages.

### Check your internet connection

Ensure you have a stable internet connection:

```bash
ping api.github.com
curl -I https://api.github.com
```

### Check rate limits

Verify your current GitHub API rate limit status:

```bash
# Replace YOUR_GITHUB_TOKEN with your actual token
curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/rate_limit
```

### Update Cursor Utils

Make sure you're using the latest version of Cursor Utils:

```bash
cursor-utils update
```

### Run with debug mode

Execute the command with debug mode to get more detailed error information:

```bash
cursor-utils github analyze owner/repo --debug
```

### Try a simpler command

If a complex command is failing, try a simpler one to isolate the issue:

```bash
cursor-utils github user info
```

## Related Commands

- `cursor-utils github --help` - Show help for the GitHub command
- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [GITHUB_AUTH_ERROR (github-001)](github-001.md) - GitHub authentication error
- [GITHUB_REPO_NOT_FOUND (github-003)](github-003.md) - GitHub repository not found
- [GITHUB_PERMISSION_ERROR (github-004)](github-004.md) - GitHub permission error
- [GITHUB_RATE_LIMIT (github-005)](github-005.md) - GitHub rate limit exceeded

## Advanced Troubleshooting

### Check API request details

Examine the API request that's causing issues:

```bash
# Run with debug and verbose logging
cursor-utils github analyze owner/repo --debug --verbose
```

### Test API endpoint directly

Try accessing the GitHub API endpoint directly:

```bash
# Replace YOUR_GITHUB_TOKEN with your actual token
curl -v -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/repos/owner/repo
```

### Check for API changes

Check the [GitHub API Changelog](https://docs.github.com/en/rest/overview/changelog) for recent changes that might affect your usage.

### Check proxy settings

If you're behind a proxy, ensure it's correctly configured:

```bash
# Check proxy environment variables
echo $HTTP_PROXY
echo $HTTPS_PROXY

# Set proxy if needed
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

## GitHub API Error Codes

Common GitHub API error codes and their meanings:

| HTTP Status | Description | Common Cause |
|-------------|-------------|--------------|
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication issue |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | GitHub server issue |
| 503 | Service Unavailable | GitHub service down |

## GitHub API Limitations

Be aware of these GitHub API limitations:

- **Rate Limits**: GitHub has different rate limits based on authentication and API endpoints.
- **Pagination**: Large result sets are paginated and may require multiple requests.
- **Payload Size**: There are limits to the size of data you can send in requests.
- **Concurrent Requests**: Too many concurrent requests may be throttled.
- **Preview Features**: Some API features might be in preview and subject to change.

## GitHub API Configuration

You can configure GitHub API settings in your `cursor-utils.yaml` file:

```yaml
github:
  api_version: "2022-11-28"  # API version to use
  accept_header: "application/vnd.github.v3+json"  # Accept header for requests
  timeout: 30  # Timeout in seconds
  retries: 3  # Number of retry attempts
```

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Check the GitHub API documentation:
   - [GitHub REST API Documentation](https://docs.github.com/en/rest)

2. Run with maximum debug information:
   ```bash
   cursor-utils github analyze owner/repo --debug --verbose
   ```

3. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - The exact command you were trying to run
   - Output of the debug logs
   - Your Cursor Utils version (`cursor-utils --version`)
   - Steps you've taken to troubleshoot 