# PROJECT_TOO_LARGE (project-001)

## Error Description

This error occurs when Cursor Utils attempts to analyze a project that exceeds the size limits. Project size limits are in place to prevent excessive resource usage, long processing times, and potential system overload when analyzing local or remote projects.

## Example Error

```
× ERROR: Project size exceeds limits
  Code: project-001
  
  Causes:
  - The project is too large for analysis
  - Project contains large binary files
  - Too many files in the project
  - Node modules, cache files, or build artifacts are included
  - Deep directory structure exceeding parsing limits
  
  Suggestion: Use a smaller project or exclude large directories/files
  
  For more information: https://github.com/gweidart/cursor-utils/errors/project-001.md
```

## Common Causes

1. **Large Project**: The overall project size exceeds the maximum allowed limit.
2. **Binary Files**: The project contains large binary files like images, videos, or compiled binaries.
3. **Dependency Directories**: Inclusion of large directories like `node_modules`, `.venv`, or `build`.
4. **Too Many Files**: The project contains more files than the analyzer can process efficiently.
5. **Generated Content**: The project contains generated content like build artifacts, cache files, or logs.
6. **Deep Directory Structure**: The project has an excessively deep directory structure.

## Solutions

### Exclude large directories

Exclude large directories that aren't needed for analysis:

```bash
cursor-utils project analyze --exclude node_modules,dist,build,.venv
```

### Focus on specific directories

Analyze only the most relevant parts of the project:

```bash
cursor-utils project analyze --include src,docs,tests
```

### Filter by file type

Process only specific file types:

```bash
cursor-utils project analyze --include "*.py,*.md,*.json" --exclude "*.png,*.jpg,*.log"
```

### Use a smaller project

If possible, use a smaller project or a subset of your current project.

### Ignore large files

Skip files that exceed a certain size:

```bash
cursor-utils project analyze --max-file-size 1MB
```

### Clean the project before analysis

Remove build artifacts, caches, and temporary files:

```bash
# Example for Python project
rm -rf __pycache__ .pytest_cache build dist *.egg-info
```

## Related Commands

- `cursor-utils project --help` - Show help for the project command
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [PROJECT_ANALYZE_ERROR (project-002)](project-002.md) - Error analyzing project
- [PROJECT_FILE_ERROR (project-004)](project-004.md) - Error with file in project
- [REPO_TOO_LARGE (repo-002)](repo-002.md) - Repository size exceeds limits

## Project Size Limitations

Cursor Utils has the following size limitations for projects:

| Limit Type | Default Value | Description |
|------------|---------------|-------------|
| Total project size | 2GB | Maximum total size of the project |
| Individual file size | 20MB | Maximum size of any individual file |
| Maximum file count | 10,000 | Maximum number of files in the project |
| Maximum directory depth | 10 | Maximum directory nesting level for processing |

## Advanced Troubleshooting

### Analyze project size

Analyze the project size to identify large files or directories:

```bash
# Find large directories
du -h --max-depth=2 . | sort -hr

# Find large files
find . -type f -size +5M | sort -n

# Count files by type
find . -type f | grep -v "node_modules\|\.git" | rev | cut -d. -f1 | rev | sort | uniq -c | sort -nr
```

### Create a project-specific .gitignore

Create or update the `.gitignore` file to exclude large or unnecessary files and directories:

```bash
# Example .gitignore for common large directories
node_modules/
.venv/
__pycache__/
dist/
build/
*.log
```

### Use symbolic links

For complex project structures, consider using symbolic links to create a simplified view of your project:

```bash
mkdir -p simplified_project/src
ln -s ../actual_project/src simplified_project/src
ln -s ../actual_project/docs simplified_project/docs
```

### Configure project analysis settings

If you have control over Cursor Utils configuration, you can adjust size limits:

```bash
cursor-utils config set project.max_size_gb 5
cursor-utils config set project.max_file_size_mb 50
```

Note: Increasing limits may lead to higher resource usage and longer processing times.

## Optimizing Large Projects

For effectively working with large projects, consider these strategies:

### Project Organization

- Separate source code from data files and assets
- Use modular architecture with clear boundaries
- Keep generated files in separate directories
- Implement proper `.gitignore` files

### Analysis Strategies

- Start with core modules and gradually expand analysis
- Focus on one component or feature at a time
- Use targeted queries rather than whole-project analysis
- Create documentation for complex subsystems

### Development Best Practices

- Regularly clean build artifacts and caches
- Remove unused dependencies
- Archive old or deprecated code
- Split monolithic projects into smaller, focused ones

## Common Large Directories to Exclude

| Directory | Description | Typical Size |
|-----------|-------------|--------------|
| `node_modules` | JavaScript dependencies | 200MB-1GB+ |
| `.venv` / `env` | Python virtual environments | 50-500MB |
| `build` / `dist` | Compiled/bundled output | 10-500MB |
| `.git` | Git history | 10MB-1GB+ |
| `__pycache__` | Python bytecode cache | 1-100MB |
| `.cache` | Various cache files | 10-500MB |
| `logs` | Log files | 1MB-1GB+ |
| `data` | Data files | Varies |

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug logging:
   ```bash
   cursor-utils project analyze --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Try analyzing a subset of the project:
   ```bash
   # Create a temporary subset of your project
   mkdir -p /tmp/project-subset/src
   cp -r path/to/your/project/src/main /tmp/project-subset/src/
   cursor-utils project analyze /tmp/project-subset
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Information about your project size (total size, number of files, etc.)
   - The command you were trying to run
   - Output of debug logs 