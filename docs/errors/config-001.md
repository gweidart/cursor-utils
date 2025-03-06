# INVALID_API_KEY (config-001)

## Error Description

This error occurs when Cursor Utils encounters an invalid API key. This can happen when an API key has an incorrect format, is expired, or is otherwise rejected by the associated service (like Perplexity AI, Google Gemini, or GitHub).

## Example Error

```
× ERROR: Invalid API key
  Code: config-001
  
  Causes:
  - The API key format is incorrect
  - The API key has expired
  - The API key has been revoked
  - The API key has insufficient permissions
  
  Suggestion: Check and update your API key in the configuration
  
  For more information: https://gweidart.github.io/cursor-utils/errors/config-001.md
```

## Common Causes

1. **Incorrect Format**: The API key doesn't match the expected format for the service.
2. **Expired Key**: The API key has expired or been revoked by the service provider.
3. **Quota Exceeded**: The API key has exceeded its usage quota or rate limits.
4. **Insufficient Permissions**: The API key doesn't have the necessary permissions for the requested operation.
5. **Incorrect API Key Type**: You're using the wrong type of API key for the service.
6. **Misconfiguration**: The API key is configured incorrectly in your settings.

## Solutions

### Check your API keys

View your current API key configuration:

```bash
cursor-utils config api_keys
```

### Set up or update API keys

Configure a new API key:

```bash
cursor-utils config api_keys --type [KEY_TYPE]
```

Where `[KEY_TYPE]` is one of:
- `PERPLEXITY` - For Perplexity AI (web search)
- `GEMINI` - For Google Gemini (code generation)
- `GITHUB` - For GitHub API access

### Verify keys in environment file

Check if your keys are correctly set in the environment file:

```bash
# Linux/macOS
cat ~/.env | grep API_KEY

# Windows (PowerShell)
Get-Content ~/.env | Select-String API_KEY
```

### Test API key validity

Test if your API key is valid:

```bash
cursor-utils test api_key --type [KEY_TYPE]
```

### Get a new API key

If your key is invalid or expired, get a new one from the service provider:

- [Perplexity AI API](https://www.perplexity.ai/settings/api) - For web search features
- [Google AI Studio](https://makersuite.google.com/app/apikey) - For Gemini features
- [GitHub Personal Access Tokens](https://github.com/settings/tokens) - For GitHub features

## Related Commands

- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils config show` - Display current configuration
- `cursor-utils test api_key` - Test API key validity

## Related Error Codes

- [API_KEY_SAVE_ERROR (config-002)](config-002.md) - Error saving API key
- [API_KEY_READ_ERROR (config-003)](config-003.md) - Error reading API key
- [WEB_API_ERROR (web-001)](web-001.md) - Error with Perplexity API
- [GEMINI_API_KEY_ERROR (gemini-003)](gemini-003.md) - Error with Gemini API key

## API Key Formats

### Perplexity AI

Perplexity API keys typically:
- Start with "pplx-"
- Followed by a string of characters
- Example: `pplx-abc123def456...`

### Google Gemini

Google Gemini API keys typically:
- Are 39 characters long
- Begin with "AI"
- Example: `AIzaSyC1a2b3c4d5e...`

### GitHub

GitHub Personal Access Tokens typically:
- Are 40 characters long
- Contain only hexadecimal characters (0-9, a-f)
- Example: `ghp_123abc...`

## Advanced Troubleshooting

### Check for invisible characters

Sometimes API keys might contain invisible characters or line breaks:

```bash
# Display hidden characters
cat -A ~/.env | grep API_KEY
```

### Regenerate API keys

If you suspect your key is compromised or invalid, regenerate it:

1. Go to the service provider's website
2. Find the API key management section
3. Revoke the existing key
4. Generate a new key
5. Update it in Cursor Utils:
   ```bash
   cursor-utils config api_keys --type [KEY_TYPE]
   ```

### Use environment variables directly

You can set API keys as environment variables before running commands:

```bash
# Linux/macOS
export PERPLEXITY_API_KEY="your-key-here"
cursor-utils web "your query"

# Windows (PowerShell)
$env:PERPLEXITY_API_KEY="your-key-here"
cursor-utils web "your query"
```

### Move .env file to correct location

Ensure your .env file is in the correct location:

```bash
# Check where Cursor Utils is looking for the .env file
cursor-utils config paths

# Move your .env file to the correct location if needed
cp /path/to/your/.env ~/.env
```

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Check if the service is experiencing issues:
   - [Perplexity AI Status](https://status.perplexity.ai)
   - [Google Gemini Status](https://status.cloud.google.com)
   - [GitHub Status](https://www.githubstatus.com)

2. Try creating a new API key from scratch.

3. Run with debug mode:
   ```bash
   cursor-utils config api_keys --type [KEY_TYPE] --debug
   ```

4. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

5. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The service you're having trouble with (Perplexity, Gemini, GitHub)
   - Complete error message (without including the actual API key)
   - Steps you've taken to resolve the issue 