# GEMINI_API_ERROR (gemini-001)

## Error Description

This error occurs when Cursor Utils encounters an issue while communicating with the Google Gemini API. This could be due to problems with the API request, response, authentication, or other API-related issues.

## Example Error

```
× ERROR: Error communicating with Google Gemini API
  Code: gemini-001
  
  Causes:
  - API request or response format issues
  - Google Gemini API service error
  - Quota exceeded
  - Rate limits reached
  - API version incompatibility
  
  Suggestion: Check the error details and try again later
  
  For more information: https://gweidart.github.io/cursor-utils/errors/gemini-001.md
```

## Common Causes

1. **API Format Issues**: Problems with the request or response format.
2. **Service Error**: The Google Gemini API service is experiencing issues.
3. **Quota Exceeded**: You've exceeded your API usage quota.
4. **Rate Limiting**: You've hit rate limits for API requests.
5. **API Version Incompatibility**: Incompatibility between Cursor Utils and the Gemini API version.
6. **Invalid Request Parameters**: Incorrect or invalid parameters in the API request.

## Solutions

### Check API key validity

Verify that your Google Gemini API key is valid:

```bash
cursor-utils test api_key --type GEMINI
```

### Update your API key

If your API key is invalid or has issues, update it:

```bash
cursor-utils config api_keys --type GEMINI
```

### Check Google Gemini API status

Check if the Google Gemini API is experiencing issues:

- [Google Cloud Status Dashboard](https://status.cloud.google.com)

### Check quota and usage

Check if you've exceeded your API quota:

- [Google AI Studio Quota Page](https://makersuite.google.com/app/apikey/usage)

### Modify request parameters

Adjust parameters to stay within API limitations:

```bash
cursor-utils gemini "your prompt" --max-tokens 1000 --temperature 0.7
```

### Check for error details

Run with debug mode to get more detailed error information:

```bash
cursor-utils gemini "your prompt" --debug
```

## Related Commands

- `cursor-utils gemini --help` - Show help for the Gemini command
- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils test api_key` - Test API key validity

## Related Error Codes

- [GEMINI_MODEL_ERROR (gemini-002)](gemini-002.md) - Error with Gemini model
- [GEMINI_API_KEY_ERROR (gemini-003)](gemini-003.md) - Error with Gemini API key
- [INVALID_API_KEY (config-001)](config-001.md) - Invalid API key

## Advanced Troubleshooting

### Check API response details

Examine the API response for specific error details:

```bash
cursor-utils gemini "test prompt" --debug
```

Look for error codes and messages in the debug output.

### Test with minimal prompt

Try a simple prompt to isolate complex prompt issues:

```bash
cursor-utils gemini "Hello world"
```

### Check for API changes

The Google Gemini API may have changed. Check for updates:

```bash
cursor-utils update
```

### Examine request payload

Debug mode will show the request payload:

```bash
cursor-utils gemini "your prompt" --debug
```

Look for issues with the request format or parameters.

## Common API Errors and Solutions

| Error Code | Description | Solution |
|------------|-------------|----------|
| `INVALID_ARGUMENT` | Invalid request parameters | Check and fix parameters in your request |
| `PERMISSION_DENIED` | Authentication issues | Verify API key and permissions |
| `RESOURCE_EXHAUSTED` | Quota or rate limit reached | Wait and try again later, or request higher quota |
| `UNAVAILABLE` | Service temporarily unavailable | Wait and try again later |
| `UNIMPLEMENTED` | Requested feature not implemented | Check for supported features/models |
| `FAILED_PRECONDITION` | Request doesn't meet preconditions | Adjust request parameters |

## Google Gemini API Limitations

Be aware of these limitations when using the Google Gemini API:

- **Rate Limits**: Default quotas limit requests per minute/day
- **Token Limits**: Maximum tokens per request (input + output)
- **Content Filtering**: Some content may be filtered or flagged
- **Regional Availability**: Not all features available in all regions
- **Model Versioning**: Models are regularly updated, which may change behavior

## Optimizing Gemini Requests

To reduce API errors and improve reliability:

1. **Keep prompts concise**: Shorter prompts are less likely to trigger errors
2. **Set reasonable token limits**: Stay well below maximums
3. **Handle rate limiting**: Add delays between requests
4. **Implement retries**: Add automatic retries with backoff
5. **Monitor quota usage**: Track your usage to avoid exceeding limits

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Check the Google Gemini API documentation:
   - [Google Gemini API Documentation](https://ai.google.dev/docs)

2. Run with maximum debug information:
   ```bash
   cursor-utils gemini "test prompt" --debug
   ```

3. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Your prompt (if not confidential)
   - API response details from debug mode
   - Your Cursor Utils version (`cursor-utils --version`)
   - Steps you've taken to troubleshoot 