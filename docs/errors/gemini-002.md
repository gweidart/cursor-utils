# GEMINI_MODEL_ERROR (gemini-002)

## Error Description

This error occurs when Cursor Utils encounters an issue with the specified Google Gemini model. This could be due to an invalid model name, a model that's unavailable or deprecated, or other model-related issues.

## Example Error

```
× ERROR: Error with Google Gemini model
  Code: gemini-002
  
  Causes:
  - Invalid model name specified
  - The requested model is unavailable
  - The model is deprecated
  - The model requires additional permissions
  - The model is currently overloaded
  
  Suggestion: Check the model name and try a different model
  
  For more information: https://gweidart.github.io/cursor-utils/errors/gemini-002.md
```

## Common Causes

1. **Invalid Model Name**: The specified model name is not valid or contains typos.
2. **Unavailable Model**: The requested model is not available to your API key or in your region.
3. **Deprecated Model**: The model has been deprecated and is no longer supported.
4. **Permission Issues**: Your API key doesn't have permission to use the requested model.
5. **Model Overload**: The model is temporarily overloaded and cannot accept new requests.
6. **Regional Restrictions**: The model is not available in your region.

## Solutions

### Check available models

Verify which models are available:

```bash
cursor-utils gemini models list
```

### Use a default model

If you're unsure which model to use, let Cursor Utils use the default model:

```bash
cursor-utils gemini "your prompt"  # Without specifying a model
```

### Try a different model

If one model is not working, try another supported model:

```bash
cursor-utils gemini "your prompt" --model gemini-2.0-flash  # Faster model
cursor-utils gemini "your prompt" --model gemini-2.0-pro  # Standard model
```

### Check model name spelling

Ensure the model name is spelled correctly:

```bash
# Correct
cursor-utils gemini "your prompt" --model gemini-2.0-pro

# Incorrect
cursor-utils gemini "your prompt" --model Gemini2.0Pro  # Wrong format
cursor-utils gemini "your prompt" --model gemini-2-pro  # Wrong format
```

### Update your configuration

Update your Gemini configuration with a valid model:

```bash
cursor-utils config set gemini.model gemini-2.0-pro
```

### Update Cursor Utils

Make sure you're using the latest version:

```bash
cursor-utils update
```

## Valid Gemini Models

| Model | Description | Notes |
|-------|-------------|-------|
| `gemini-2.0-pro` | Standard Gemini 2.0 Pro model | Good general purpose model |
| `gemini-2.0-flash` | Faster, more efficient model | Good for quicker responses |
| `gemini-2.0-pro-exp-02-05` | Experimental Pro model | Enhanced for code-related tasks |
| `gemini-2.0-flash-thinking-exp` | Experimental thinking model | Better for step-by-step reasoning |

Note: Available models may change as Google updates the Gemini API.

## Related Commands

- `cursor-utils gemini --help` - Show help for the Gemini command
- `cursor-utils gemini models list` - List available models
- `cursor-utils config show` - Display current configuration
- `cursor-utils config set gemini.model [MODEL]` - Set the default model

## Related Error Codes

- [GEMINI_API_ERROR (gemini-001)](gemini-001.md) - Error with Gemini API
- [GEMINI_API_KEY_ERROR (gemini-003)](gemini-003.md) - Error with Gemini API key
- [INVALID_API_KEY (config-001)](config-001.md) - Invalid API key

## Advanced Troubleshooting

### Check API documentation

Refer to the Google Gemini API documentation for the latest information on supported models:
- [Google Gemini API Documentation](https://ai.google.dev/docs/gemini_api_overview)

### Debug model selection

Run with debug mode to see model selection details:

```bash
cursor-utils gemini "your prompt" --model gemini-2.0-pro --debug
```

### Check for API updates

The Google Gemini API might have changed since your version of Cursor Utils was released:

```bash
# Check your Cursor Utils version
cursor-utils --version

# Update to the latest version
cursor-utils update
```

### Check API key capabilities

Some API keys might be restricted to certain models. Check your API key's capabilities:

```bash
cursor-utils test api_key --type GEMINI
```

## Model Selection Considerations

### Performance vs Quality

Different models offer different trade-offs:
- **Flash models** (gemini-2.0-flash): Faster responses, lower resource usage, less detailed answers
- **Pro models** (gemini-2.0-pro): More detailed responses, higher resource usage, might be slower

### Task Appropriateness

Choose models based on your task:
- **Factual questions**: Any model should work well
- **Code generation**: Pro models usually work better
- **Simple instructions**: Flash models are faster and efficient
- **Complex reasoning**: Pro models with experimental features may be better

### API Costs

Different models may have different costs associated with them:
- Higher-tier models might use more tokens or cost more per request
- Check your Google AI Studio account for specific pricing details

## Regional Availability

Google Gemini models may have different availability in different regions:
- Some models might not be available in all countries
- Certain features might be region-restricted
- Check the [Google Gemini API Documentation](https://ai.google.dev/docs/gemini_api_overview) for regional availability details

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Check the current status of the Google Cloud:
   - [Google Cloud Status Dashboard](https://status.cloud.google.com)

2. Run with debug logging:
   ```bash
   cursor-utils gemini "test prompt" --model gemini-2.0-pro --debug
   ```

3. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - The model you tried to use
   - Other models you've tested (and whether they worked)
   - Your Cursor Utils version (`cursor-utils --version`)
   - Debug log output 