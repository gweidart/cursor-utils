## Config Command

The `config` command manages persistent configuration settings for Cursor-Utils, with a particular focus on storing and retrieving API keys securely.

### Syntax

```bash
cursor-utils config {SUBCOMMAND} [KEY] [VALUE] [OPTIONS]
```

### Subcommands

| Subcommand | Description | Syntax |
|------------|-------------|--------|
| `list` | List all configuration values | `cursor-utils config list [OPTIONS]` |
| `get` | Get a specific configuration value | `cursor-utils config get KEY [OPTIONS]` |
| `set` | Set a configuration value | `cursor-utils config set KEY VALUE [OPTIONS]` |
| `delete` | Delete a configuration value | `cursor-utils config delete KEY [OPTIONS]` |

### Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--format` | Output format (plain, markdown, json, rich) | `rich` | `--format json` |
| `--help` | Show command help | - | `--help` |

### Configuration Storage

By default, Cursor-Utils stores configuration in a JSON file located at:

- **Linux/macOS**: `~/.config/cursor-utils/config.json`
- **Windows**: `%APPDATA%\cursor-utils\config.json`

The configuration file is automatically created when you first use the `config set` command.

### Common Configuration Keys

| Key | Description | Used By Commands |
|-----|-------------|------------------|
| `gemini_api_key` | Google Gemini API key | `gemini`, `project`, `repo` |
| `perplexity_api_key` | Perplexity API key | `web` |
| `github_token` | GitHub personal access token | `github` |
| `default_format` | Default output format | All commands |
| `default_gemini_model` | Default Gemini model | `gemini`, `project`, `repo` |
| `default_perplexity_model` | Default Perplexity model | `web` |

### Examples

### Listing All Configuration Values

To see all currently configured values:

```bash
cursor-utils config list
```

This will display a table of all configuration keys and their values.

With JSON output:

```bash
cursor-utils config list --format json
```

### Getting a Specific Configuration Value

To retrieve a specific configuration value:

```bash
cursor-utils config get gemini_api_key
```

This will display just the value of the specified key.

### Setting Configuration Values

To set or update a configuration value:

```bash
cursor-utils config set gemini_api_key YOUR_API_KEY
```

For setting the default Gemini model:

```bash
cursor-utils config set default_gemini_model gemini-1.5-pro
```

For setting the default output format:

```bash
cursor-utils config set default_format markdown
```

### Deleting Configuration Values

To remove a configuration value:

```bash
cursor-utils config delete test_key
```

### Using Environment Variables

All configuration values can also be set using environment variables, which take precedence over values in the configuration file.

```bash
export GEMINI_API_KEY=your_api_key
export DEFAULT_FORMAT=markdown
export GITHUB_TOKEN=your_github_token
```

### API Key Setup

### Google Gemini API Key

To use the `gemini`, `project`, and `repo` commands, you need a Google Gemini API key:

1. Visit [Google AI Studio](https://ai.google.dev/) to create an API key
2. Configure the key in Cursor-Utils:

```bash
cursor-utils config set gemini_api_key YOUR_GEMINI_API_KEY
```

### Perplexity API Key

To use the `web` command, you need a Perplexity API key:

1. Visit [Perplexity API documentation](https://docs.perplexity.ai/) to create an API key
2. Configure the key in Cursor-Utils:

```bash
cursor-utils config set perplexity_api_key YOUR_PERPLEXITY_API_KEY
```

### GitHub Token

To use the `github` command, you need a GitHub personal access token:

1. Create a token at [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Configure the token in Cursor-Utils:

```bash
cursor-utils config set github_token YOUR_GITHUB_TOKEN
```

### Security Considerations

Configuration values, including API keys, are stored in plaintext in the configuration file. For enhanced security:

1. Ensure appropriate file permissions are set on the configuration file
2. Consider using environment variables for sensitive values in shared environments
3. On shared systems, use user-specific installations of Cursor-Utils

### Best Practices

1. **Regularly Rotate API Keys**: Periodically update your API keys for security
2. **Set Default Values**: Configure defaults for commonly used options:
   ```bash
   cursor-utils config set default_format markdown
   cursor-utils config set default_gemini_model gemini-1.5-pro
   ```
3. **Use Separate Keys**: For production vs. development environments
4. **Check Configuration**: Verify your configuration before troubleshooting:
   ```bash
   cursor-utils config list
   ``` 