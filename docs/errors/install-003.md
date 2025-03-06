# TEMPLATE_ERROR (install-003)

## Error Description

This error occurs when Cursor Utils encounters an issue while processing a template during installation. Template processing errors can happen when a template file is malformed, contains invalid syntax, or when there are issues with variable substitution.

## Example Error

```
× ERROR: Failed to process template during installation
  Code: install-003
  
  Causes:
  - The template file contains invalid syntax
  - A required template variable is missing
  - The template engine encountered an unexpected format
  - Template file is corrupted
  
  Suggestion: Check the template file for errors or use a default template
  
  For more information: https://gweidart.github.io/cursor-utils/errors/install-003.md
```

## Common Causes

1. **Invalid Template Syntax**: The template contains syntax errors or invalid formatting.
2. **Missing Variables**: Required template variables are not provided during processing.
3. **Template File Corruption**: The template file is corrupted or incomplete.
4. **Template Engine Issues**: There's a problem with the template engine itself.
5. **Incompatible Template Version**: The template version is incompatible with your Cursor Utils version.

## Solutions

### Check template syntax

Verify that the template file has the correct syntax:

```bash
# View the template file
cat ~/.cursor-utils/templates/your-template-file.yml
```

Look for:
- Missing or unmatched brackets, braces, or quotes
- Invalid YAML or JSON syntax if applicable
- Correct indentation

### Use a default template

If you're using a custom template that's causing issues, try using the default template instead:

```bash
cursor-utils install --use-default-templates
```

### Validate template variables

Ensure all required variables are provided:

```bash
# Check which variables are expected
cursor-utils template list-variables --template your-template-file.yml
```

### Regenerate templates

You can regenerate the default templates:

```bash
cursor-utils template reset
```

### Check for template errors with debug mode

Run the installation with debug mode to see detailed template processing:

```bash
cursor-utils install --debug
```

## Related Commands

- `cursor-utils install --help` - Show help for the install command
- `cursor-utils template --help` - Show help for template management
- `cursor-utils template list` - List available templates

## Related Error Codes

- [FILE_NOT_FOUND (install-002)](install-002.md) - File not found during installation
- [FILE_WRITE_ERROR (install-005)](install-005.md) - Error writing to file
- [CONFIG_FILE_ERROR (config-005)](config-005.md) - Error with configuration file

## Template Format Guide

Cursor Utils templates follow a specific format:

```yaml
# Example template format
name: "Project Template"
version: "1.0.0"
description: "A template for new projects"

variables:
  project_name:
    description: "Name of the project"
    default: "my-project"
  author_name:
    description: "Author of the project"
    required: true

files:
  - source: "templates/readme.md.tmpl"
    destination: "{{ project_name }}/README.md"
  - source: "templates/setup.py.tmpl"
    destination: "{{ project_name }}/setup.py"
```

When creating or modifying templates, ensure they follow this structure.

## Advanced Troubleshooting

### Manually process templates

For advanced users, you can try manually processing a template to identify issues:

```bash
# Export template variables to a file
cursor-utils template export-variables --output variables.json

# Manually process a template
cursor-utils template process --template your-template.yml --variables variables.json --output processed-output
```

### Check template engine logs

Template processing logs may provide more details:

```bash
cat ~/.cursor-utils/logs/template.log
```

### Validate template schema

Ensure your template follows the correct schema:

```bash
cursor-utils template validate --template your-template.yml
```

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Try with the latest version of Cursor Utils:
   ```bash
   cursor-utils update
   ```

2. Check the detailed logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. [Submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The template file that's causing the issue (if it's not confidential)
   - The complete error message
   - Steps to reproduce the error 