# GITHUB_RATE_LIMIT (github-005)

## Error Description

This error occurs when Cursor Utils has exceeded the GitHub API rate limits. GitHub limits the number of API requests that can be made within a certain time period to ensure service stability and fair usage. When these limits are reached, API requests will be rejected until the rate limit resets.

## Example Error

```
× ERROR: GitHub API rate limit exceeded
  Code: github-005
  
  Causes:
  - You've exceeded the GitHub API request limit
  - Multiple applications using the same token
  - Running commands in rapid succession
  - Token has lower rate limits (unauthenticated or OAuth App)
  - Rate limits differ across GitHub API endpoints
  
  Suggestion: Wait for the rate limit to reset or use a token with higher limits
  
  For more information: https://gweidart.github.io/cursor-utils/errors/github-005.md
```

## Common Causes

1. **Exceeded Request Limit**: You've made too many API requests within the rate limit window.
2. **Shared Token Usage**: Multiple applications or scripts are using the same GitHub token.
3. **Batch Operations**: Running commands that make multiple API calls in rapid succession.
4. **Unauthenticated Requests**: Making requests without authentication, which have much lower limits.
5. **Search API Usage**: The Search API has stricter rate limits than other GitHub APIs.
6. **Secondary Rate Limits**: Triggered by making too many requests in a short time period.

## Solutions

### Check your current rate limit status

View your current GitHub API rate limit status:

```bash
# Replace YOUR_GITHUB_TOKEN with your actual token
curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/rate_limit
```

This will show:
- Your current remaining requests
- The total limit
- When the rate limit will reset

### Wait for the rate limit to reset

Rate limits typically reset hourly. You can wait until the reset time shown in the rate limit response:

```bash
# Extract reset time from rate limit response
reset_time=$(curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/rate_limit | grep "reset" | head -1 | awk '{print $2}' | tr -d ',')
echo "Rate limit resets at: $(date -d @$reset_time)"
```

### Use conditional requests

Implement conditional requests using ETags to avoid consuming rate limits for unchanged resources:

```bash
# First request to get ETag
response=$(curl -i -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/repos/owner/repo)
etag=$(echo "$response" | grep ETag | awk '{print $2}')

# Second request using ETag
curl -i -H "Authorization: token YOUR_GITHUB_TOKEN" -H "If-None-Match: $etag" https://api.github.com/repos/owner/repo
```

### Use a personal access token

Ensure you're using authentication, as authenticated requests have higher rate limits:

```bash
cursor-utils config api_keys --type GITHUB
```

### Use a GitHub App token

GitHub Apps have higher rate limits than personal access tokens. Consider using a GitHub App if you need higher limits.

### Implement request throttling

Add delays between commands or implement exponential backoff:

```bash
# Wait 5 seconds between commands
cursor-utils github analyze owner/repo1
sleep 5
cursor-utils github analyze owner/repo2
```

## Related Commands

- `cursor-utils github --help` - Show help for the GitHub command
- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [GITHUB_AUTH_ERROR (github-001)](github-001.md) - GitHub authentication error
- [GITHUB_API_ERROR (github-002)](github-002.md) - GitHub API error
- [GITHUB_REPO_NOT_FOUND (github-003)](github-003.md) - GitHub repository not found
- [GITHUB_PERMISSION_ERROR (github-004)](github-004.md) - GitHub permission error

## GitHub API Rate Limits

GitHub has different rate limits based on authentication status and API endpoints:

| Authentication Type | Core API Limit | Search API Limit | GraphQL API Limit |
|---------------------|---------------|-----------------|-------------------|
| Unauthenticated     | 60 per hour   | 10 per minute   | N/A (requires auth) |
| Personal Access Token | 5,000 per hour | 30 per minute | 5,000 points per hour |
| GitHub App | 5,000 per hour per installation | 30 per minute | 5,000 points per hour |
| GitHub Enterprise | 15,000+ per hour | 60+ per minute | 15,000+ points per hour |

## Understanding Rate Limit Headers

GitHub API responses include rate limit headers:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | The maximum number of requests allowed in the rate limit window |
| `X-RateLimit-Remaining` | The number of requests remaining in the current rate limit window |
| `X-RateLimit-Reset` | The time (in Unix epoch seconds) when the rate limit window resets |
| `X-RateLimit-Used` | The number of requests used in the current rate limit window |
| `X-RateLimit-Resource` | The rate limit grouping this request counts against |

## Secondary Rate Limits

GitHub also implements secondary rate limits to prevent abuse:

- Triggered by making too many requests in a short time period
- Not publicly documented with specific thresholds
- Results in HTTP 403 responses with a "secondary rate limit" message
- May require exponential backoff strategies

## Advanced Troubleshooting

### Monitor rate limit consumption

Track your rate limit usage over time:

```bash
# Create a simple monitoring script
while true; do
  curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/rate_limit | jq .rate
  sleep 300  # Check every 5 minutes
done
```

### Implement exponential backoff

For automated scripts, implement exponential backoff when rate limits are hit:

```python
# Python example
import time
import random

def backoff(attempt):
    # Exponential backoff with jitter
    return (2 ** attempt) + random.uniform(0, 1)

# Usage
attempt = 0
while True:
    try:
        # Make API request
        break  # Success
    except RateLimitError:
        wait_time = backoff(attempt)
        print(f"Rate limit hit. Waiting {wait_time}s")
        time.sleep(wait_time)
        attempt += 1
```

### Use GraphQL for multiple requests

Consider using GitHub's GraphQL API to reduce the number of requests needed:

```bash
curl -s -H "Authorization: token YOUR_GITHUB_TOKEN" -X POST -d '{"query": "query { viewer { login repositories(first: 100) { nodes { name } } } }"}' https://api.github.com/graphql
```

### Distribute workloads

If possible, distribute your GitHub API requests:
- Use multiple tokens across different applications
- Implement request queuing
- Schedule non-urgent operations during off-peak times

## Rate Limit Best Practices

1. **Cache responses** when possible to reduce repeated requests
2. **Use conditional requests** with ETags to avoid counting unchanged resources against limits
3. **Implement proper pagination** to efficiently process large result sets
4. **Use GraphQL** for complex queries that would otherwise require multiple REST API calls
5. **Log rate limit headers** to track usage patterns and anticipate limits
6. **Add timeouts and retries** with exponential backoff for handling rate limit errors
7. **Prioritize requests** based on importance for your application

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

3. Consider upgrading to GitHub Enterprise if you consistently hit limits with normal usage.

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - The rate limit information (from the API response)
   - A description of how many commands you were running
   - Output of debug logs 