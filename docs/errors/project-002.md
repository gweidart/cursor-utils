# PROJECT_ANALYZE_ERROR (project-002)

## Error Description

This error occurs when Cursor Utils encounters an issue while analyzing a project. Project analysis problems can happen when processing project contents, extracting information, or generating insights from the project structure or code.

## Example Error

```
× ERROR: Failed to analyze project
  Code: project-002
  
  Causes:
  - Error processing project files
  - Analysis timeout due to project complexity
  - Insufficient memory for analysis
  - Unsupported file types or structures
  - API service error during analysis
  
  Suggestion: Try with a simpler project or focus on specific subdirectories
  
  For more information: https://gweidart.github.io/cursor-utils/errors/project-002.md
```

## Common Causes

1. **Processing Errors**: Issues encountered when processing project files.
2. **Project Complexity**: The project is too complex or large for effective analysis.
3. **Resource Limitations**: Insufficient memory or CPU resources for the analysis.
4. **Unsupported Content**: The project contains file types or structures that aren't supported.
5. **API Service Issues**: Problems with the underlying AI service used for project analysis.
6. **Timeout**: The analysis took too long and timed out.

## Solutions

### Limit analysis scope

Focus the analysis on a specific part of the project:

```bash
cursor-utils project analyze --subdir src/
```

### Filter by file type

Analyze only specific file types:

```bash
cursor-utils project analyze --include "*.py,*.md" --exclude "*.json,*.yaml"
```

### Increase timeout

Allow more time for the analysis:

```bash
cursor-utils project analyze --timeout 300
```

### Check API key

Ensure your API key for the analysis service is valid:

```bash
cursor-utils config api_keys --type GEMINI
```

### Update Cursor Utils

Make sure you're using the latest version:

```bash
cursor-utils update
```

### Exclude problem files

If specific files are causing issues, exclude them:

```bash
cursor-utils project analyze --exclude "path/to/problem/file.ext,*.problematic"
```

## Related Commands

- `cursor-utils project --help` - Show help for the project command
- `cursor-utils config api_keys` - Manage API keys
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [PROJECT_TOO_LARGE (project-001)](project-001.md) - Project size exceeds limits
- [PROJECT_INVALID_URL (project-003)](project-003.md) - Invalid project URL
- [PROJECT_FILE_ERROR (project-004)](project-004.md) - Error with file in project
- [GEMINI_API_ERROR (gemini-001)](gemini-001.md) - Error with Gemini API

## Advanced Troubleshooting

### Check analysis logs

Review the analysis logs for specific error information:

```bash
cat ~/.cursor-utils/logs/cursor-utils.log
```

### Run with debug mode

Enable debug mode for more detailed logging:

```bash
cursor-utils project analyze --debug
```

### Check project structure

Examine the project structure for potential issues:

```bash
# Count files by type
find . -type f | grep -v "^./.git/" | rev | cut -d. -f1 | rev | sort | uniq -c | sort -nr

# Check directory structure
find . -type d -not -path "*/\.*" | sort
```

### Test with a simpler project

Try the analysis with a simpler project to determine if the issue is project-specific:

```bash
# Create a minimal test project
mkdir -p test-project/src
echo 'print("Hello, world!")' > test-project/src/main.py
cursor-utils project analyze test-project
```

### Check system resources

Make sure your system has sufficient resources:

```bash
# Check available memory
free -h

# Check CPU usage
top -n 1
```

## Analysis Limitations

Cursor Utils has several limitations for project analysis:

| Limitation | Description |
|------------|-------------|
| File types | Some binary or proprietary file formats may not be analyzed properly |
| Project structure | Unusual or non-standard project structures may cause issues |
| Analysis depth | There may be limits to how deeply code relationships are analyzed |
| Language support | Some programming languages may have better support than others |
| Framework recognition | Specialized frameworks may not be recognized or analyzed correctly |

## Optimization Strategies

To optimize project analysis:

### Project Structure

- Use standard project layouts
- Keep directory nesting to a reasonable depth
- Follow conventional code organization patterns
- Separate code from data and assets

### Modular Analysis

- Analyze one module or component at a time
- Focus on the most important parts of the project first
- Use targeted queries for specific functionality
- Break large projects into logical subsystems

### File Selection

- Prioritize key source files
- Exclude generated code and third-party libraries
- Focus on one language or framework at a time
- Include relevant documentation and configuration files

## Common Issues by Project Type

Different project types may encounter specific issues:

| Project Type | Common Issues | Recommendations |
|--------------|--------------|-----------------|
| Web applications | Large node_modules, bundled assets | Exclude node_modules, build directories |
| Data science | Large datasets, notebook outputs | Exclude data files, clear notebook outputs |
| Mobile apps | Large asset files, generated code | Focus on core source files |
| Monorepos | Overall size, many dependencies | Analyze one package at a time |
| Legacy systems | Unusual structures, mixed languages | Start with core modules |

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with extensive debug information:
   ```bash
   cursor-utils project analyze --debug --verbose
   ```

2. Check service status:
   - [Google Cloud Status Dashboard](https://status.cloud.google.com) (for Gemini API)

3. Try a different API key:
   ```bash
   # Set a different Gemini API key temporarily
   GEMINI_API_KEY=your-alternate-key cursor-utils project analyze
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Project type and structure (without sharing sensitive code)
   - Command you were trying to run
   - Debug log output
   - Your operating system and Cursor Utils version 