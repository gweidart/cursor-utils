# GEMINI_API_KEY_ERROR (gemini-003)

## Error Description

This error occurs when Cursor Utils encounters an issue with the Google Gemini API key. This could be due to an invalid, expired, or missing API key, or problems with API key permissions or configuration.

## Example Error

```
× ERROR: Google Gemini API key error
  Code: gemini-003
  
  Causes:
  - API key is missing or not configured
  - API key is invalid or malformed
  - API key has expired
  - API key lacks required permissions
  - API key has been revoked
  
  Suggestion: Check and update your Gemini API key
  
  For more information: https://github.com/gweidart/cursor-utils/errors/gemini-003.md
```

## Common Causes

1. **Missing API Key**: No Gemini API key has been configured in Cursor Utils.
2. **Invalid API Key**: The configured API key is not valid or is malformed.
3. **Expired API Key**: The API key has expired or been revoked.
4. **Permission Issues**: The API key doesn't have the necessary permissions for Gemini operations.
5. **Configuration Problems**: The API key is not properly configured in the environment file.
6. **Quota Exceeded**: The API key has reached its quota or usage limits.

## Solutions

### Check if API key is configured

Verify that a Gemini API key is configured:

```bash
cursor-utils config api_keys
```

### Configure or update API key

Set up or update your Gemini API key:

```bash
cursor-utils config api_keys --type GEMINI
```

### Test API key validity

Check if your API key is valid:

```bash
cursor-utils test api_key --type GEMINI
```

### Verify API key format

Google Gemini API keys typically:
- Are 39 characters long
- Begin with "AI"
- Example: `AIzaSyC1a2b3c4d5e...`

### Create a new API key

If your current key is invalid or has issues, create a new one:

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click on "Create API Key"
3. Copy the new API key
4. Configure it in Cursor Utils:
   ```bash
   cursor-utils config api_keys --type GEMINI
   ```

### Check for environment variables

Ensure no conflicting environment variables are set:

```bash
# Linux/macOS
env | grep GEMINI

# Windows (PowerShell)
Get-ChildItem Env: | Where-Object { $_.Name -match 'GEMINI' }
```

## Related Commands

- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils test api_key` - Test API key validity
- `cursor-utils gemini --help` - Show help for the Gemini command

## Related Error Codes

- [GEMINI_API_ERROR (gemini-001)](gemini-001.md) - Error with Gemini API
- [GEMINI_MODEL_ERROR (gemini-002)](gemini-002.md) - Error with Gemini model
- [INVALID_API_KEY (config-001)](config-001.md) - Invalid API key
- [API_KEY_READ_ERROR (config-003)](config-003.md) - Error reading API key

## Advanced Troubleshooting

### Check .env file directly

Examine your .env file to ensure the API key is correctly stored:

```bash
# Linux/macOS
cat ~/.env | grep GEMINI

# Windows (PowerShell)
Get-Content ~/.env | Select-String GEMINI
```

The key should be stored in this format:
```
GEMINI_API_KEY=your-key-here
```

### Check for API key restrictions

Some API keys might have usage restrictions:
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to check your key's limitations
- Look for restrictions on models, usage quotas, or regional availability

### Clear cached credentials

Clear any cached credentials that might be interfering:

```bash
# Linux/macOS
rm -f ~/.cursor-utils/cache/credentials*

# Windows (PowerShell)
Remove-Item -Path "$HOME\.cursor-utils\cache\credentials*" -Force -ErrorAction SilentlyContinue
```

### Use API key directly for testing

For testing purposes, you can use the API key directly:

```bash
GEMINI_API_KEY=your-key-here cursor-utils gemini "test prompt"
```

## API Key Management Best Practices

1. **Regularly rotate keys**: Create new keys and retire old ones periodically
2. **Secure storage**: Store API keys securely and never share them
3. **Monitor usage**: Keep track of your API usage to avoid hitting limits
4. **Use environment variables**: Set keys as environment variables for security
5. **Don't embed in code**: Never hardcode API keys in your code
6. **Set usage alerts**: Configure alerts for unusual usage patterns

## Google AI API Key Considerations

### Usage Limits

Google Gemini API keys have usage limits:
- Requests per minute
- Requests per day
- Total tokens per month

### Rate Limiting

If you exceed rate limits, requests may fail with:
- 429 (Too Many Requests) status codes
- RESOURCE_EXHAUSTED error messages

### Regional Availability

API keys may have regional restrictions:
- Some features may not be available in all regions
- Models may have different regional availability

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug mode:
   ```bash
   cursor-utils gemini "test prompt" --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Verify Google service status:
   - [Google Cloud Status Dashboard](https://status.cloud.google.com)

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Debug log output
   - Steps you've taken to troubleshoot
   - Your operating system and Cursor Utils version 