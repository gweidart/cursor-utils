# CONFIG_FILE_ERROR (config-005)

## Error Description

This error occurs when Cursor Utils encounters an issue with its main configuration file (`cursor-utils.yaml` or similar). This could be due to problems with the file format, missing required fields, permission issues, or other configuration-related problems.

## Example Error

```
× ERROR: Problem with configuration file
  Code: config-005
  
  Causes:
  - The configuration file has invalid YAML syntax
  - Required configuration fields are missing
  - The configuration file cannot be accessed
  - The configuration contains invalid values
  
  Suggestion: Check the configuration file format and ensure all required fields are present
  
  For more information: https://gweidart.github.io/cursor-utils/errors/config-005.md
```

## Common Causes

1. **Invalid YAML**: The configuration file contains invalid YAML syntax.
2. **Missing Fields**: Required configuration fields are missing from the file.
3. **Permission Issues**: The user doesn't have sufficient permissions to read or write the configuration file.
4. **Invalid Values**: The configuration contains values that are not allowed or are of the wrong type.
5. **File Location**: The configuration file is not in the expected location.
6. **File Corruption**: The configuration file is corrupted or incomplete.

## Solutions

### Check the configuration file location

Verify that the configuration file exists in the expected location:

```bash
# Linux/macOS
ls -la ~/cursor-utils.yaml
ls -la ~/.cursor-utils/config.yaml  # Alternative location

# Windows (PowerShell)
Test-Path ~/cursor-utils.yaml
Test-Path ~/.cursor-utils/config.yaml  # Alternative location
```

### Check configuration file format

Ensure the configuration file has valid YAML syntax:

```bash
# Linux/macOS
cat ~/cursor-utils.yaml

# Windows (PowerShell)
Get-Content ~/cursor-utils.yaml
```

### Validate YAML syntax

You can use online YAML validators or tools to check syntax:

```bash
# If you have Python installed
python -c "import yaml, sys; yaml.safe_load(open('~/cursor-utils.yaml'))"

# If you have yamllint installed
yamllint ~/cursor-utils.yaml
```

### Reset to default configuration

Generate a new configuration file with default settings:

```bash
cursor-utils config init
```

### Show current configuration

View your current configuration to identify issues:

```bash
cursor-utils config show
```

### Set specific configuration values

If specific values are causing issues, set them individually:

```bash
cursor-utils config set key.subkey value
```

For example:
```bash
cursor-utils config set web.model sonar-pro
cursor-utils config set settings.debug true
```

### Fix file permissions

Ensure proper permissions for the configuration file:

```bash
# Linux/macOS
chmod 644 ~/cursor-utils.yaml

# Windows
# Check permissions through File Explorer's Properties > Security tab
```

## Related Commands

- `cursor-utils config show` - Display current configuration
- `cursor-utils config set` - Set a specific configuration value
- `cursor-utils config init` - Initialize a new configuration file
- `cursor-utils config paths` - View configuration file paths

## Related Error Codes

- [ENV_FILE_ERROR (config-004)](config-004.md) - Error with .env file
- [API_KEY_READ_ERROR (config-003)](config-003.md) - Error reading API key
- [FILE_NOT_FOUND (install-002)](install-002.md) - File not found during installation
- [FILE_WRITE_ERROR (install-005)](install-005.md) - Error writing to file

## Configuration File Structure

The Cursor Utils configuration file uses YAML format with the following structure:

```yaml
version: "1.0.0"
settings:
  debug: false
  log_level: "INFO"
web:
  model: "sonar-pro"
  mode: "copilot"
  search_focus: "internet"
gemini:
  model: "gemini-2.0-pro-exp-02-05"
  max_output_tokens: 8000
  temperature: 0.7
  top_p: 0.95
  top_k: 40
github:
  token_source: "env"
  default_owner: "username"
  default_repo: "repo-name"
  template_dir: "~/.cursor-utils/templates/github"
```

## Advanced Troubleshooting

### Check for syntax errors

Common YAML syntax errors include:
- Incorrect indentation
- Missing colons
- Unquoted strings with special characters
- Missing quotes around strings that start with special characters
- Using tabs instead of spaces for indentation

### Create a minimal configuration

Create a minimal working configuration to start with:

```bash
# Linux/macOS
cat > ~/cursor-utils.yaml << EOF
version: "1.0.0"
settings:
  debug: false
  log_level: "INFO"
EOF

# Windows (PowerShell)
@"
version: "1.0.0"
settings:
  debug: false
  log_level: "INFO"
"@ | Set-Content -Path "$HOME\cursor-utils.yaml"
```

### Check for specific syntax errors

Use a YAML linter or parser to find specific syntax errors:

```bash
# Using Python (if available)
python -c "import yaml, sys; print(yaml.safe_load(open('~/cursor-utils.yaml')));"
```

### Check file encoding

Ensure the configuration file has the correct encoding (UTF-8):

```bash
# Linux/macOS
file -i ~/cursor-utils.yaml

# Windows (PowerShell)
# Check through Notepad by opening and saving with UTF-8 encoding
```

## Configuration Reference

### Required Fields

The following fields are required in the configuration:

```yaml
version: "1.0.0"  # Configuration version
settings:
  debug: false    # Debug mode (true/false)
  log_level: "INFO"  # Log level (DEBUG, INFO, WARNING, ERROR)
```

### Web Command Settings

```yaml
web:
  model: "sonar-pro"  # sonar, sonar-pro, sonar-reasoning, sonar-pro-reasoning
  mode: "copilot"     # copilot, concise
  search_focus: "internet"  # internet, scholar, writing, wolfram, youtube, reddit
```

### Gemini Command Settings

```yaml
gemini:
  model: "gemini-2.0-pro-exp-02-05"  # Gemini model name
  max_output_tokens: 8000             # Maximum output tokens
  temperature: 0.7                    # Temperature (0.0-1.0)
  top_p: 0.95                         # Top-p sampling
  top_k: 40                           # Top-k sampling
```

### GitHub Command Settings

```yaml
github:
  token_source: "env"  # Where to get the token (env or config)
  default_owner: "username"  # Default GitHub owner/organization
  default_repo: "repo-name"  # Default repository
  template_dir: "~/.cursor-utils/templates/github"  # Template directory
```

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug logging:
   ```bash
   cursor-utils config show --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Create a completely new minimal configuration:
   ```bash
   mv ~/cursor-utils.yaml ~/cursor-utils.yaml.backup
   cursor-utils config init
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Your operating system and version
   - The content of your configuration file (with sensitive information redacted)
   - Steps you've taken to resolve the issue 