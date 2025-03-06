# REPO_TOO_LARGE (repo-002)

## Error Description

This error occurs when Cursor Utils attempts to clone or analyze a repository that exceeds the size limits. Repository size limits are in place to prevent excessive resource usage, long processing times, and potential system overload.

## Example Error

```
× ERROR: Repository size exceeds limits
  Code: repo-002
  
  Causes:
  - The repository is too large for analysis
  - Repository contains large binary files
  - Repository has many large assets
  - Repository has an extensive commit history
  
  Suggestion: Use a smaller repository or specify a subdirectory/specific files
  
  For more information: https://gweidart.github.io/cursor-utils/errors/repo-002.md
```

## Common Causes

1. **Large Repository**: The overall repository size exceeds the maximum allowed limit.
2. **Binary Files**: The repository contains large binary files like images, videos, or compiled binaries.
3. **Deep Git History**: The repository has an extensive commit history, making the `.git` directory very large.
4. **Large Assets**: The repository includes large asset files.
5. **LFS Content**: The repository uses Git LFS (Large File Storage) with many large files.
6. **Generated Content**: The repository contains generated content like build artifacts or node_modules.

## Solutions

### Use a shallow clone

Perform a shallow clone to get only the latest version without full history:

```bash
cursor-utils repo https://github.com/username/repo-name --depth 1
```

### Clone a specific branch

Clone only a specific branch to reduce size:

```bash
cursor-utils repo https://github.com/username/repo-name --branch main --single-branch
```

### Use a smaller repository

Try using a smaller repository:

```bash
cursor-utils repo https://github.com/username/smaller-repo
```

### Specify a subdirectory

Focus on a specific subdirectory of the repository:

```bash
cursor-utils repo https://github.com/username/repo-name --subdir src/
```

### Filter by file type

Process only specific file types:

```bash
cursor-utils repo https://github.com/username/repo-name --include "*.py" --exclude "*.png,*.jpg"
```

### Skip large files

Skip files that exceed a certain size:

```bash
cursor-utils repo https://github.com/username/repo-name --max-file-size 1MB
```

## Related Commands

- `cursor-utils repo --help` - Show help for the repo command
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [REPO_CLONE_ERROR (repo-001)](repo-001.md) - Error cloning repository
- [REPO_ANALYZE_ERROR (repo-003)](repo-003.md) - Error analyzing repository
- [PROJECT_TOO_LARGE (project-001)](project-001.md) - Project size exceeds limits

## Size Limitations

Cursor Utils has the following size limitations for repositories:

| Limit Type | Default Value | Description |
|------------|---------------|-------------|
| Total repository size | 2GB | Maximum total size of the repository |
| Individual file size | 20MB | Maximum size of any individual file |
| Maximum file count | 10,000 | Maximum number of files in the repository |
| Maximum processing depth | 10 | Maximum directory nesting level for processing |

## Advanced Troubleshooting

### Analyze repository size

Analyze the repository size to identify large files or directories:

```bash
# Clone the repository
git clone https://github.com/username/repo-name

# Analyze repository size
cd repo-name
du -h --max-depth=2 .
find . -type f -size +10M | sort -n
```

### Use Git sparse checkout

Use Git sparse checkout to get only specific directories:

```bash
mkdir repo-sparse
cd repo-sparse
git init
git remote add origin https://github.com/username/repo-name
git config core.sparseCheckout true
echo "path/to/specific/dir/" > .git/info/sparse-checkout
git pull origin main
```

### Use specific repo analysis tools

Use specialized tools to analyze repository content:

```bash
# Using git-sizer (if installed)
git-sizer --verbose

# Using GitHub's LFS migration tool
git lfs migrate info --everything --above=1MB
```

### Configure size limits

If you have control over Cursor Utils configuration, you can adjust size limits:

```bash
cursor-utils config set repo.max_size_gb 5
cursor-utils config set repo.max_file_size_mb 50
```

Note: Increasing limits may lead to higher resource usage and longer processing times.

## Managing Large Repositories

For effectively working with large repositories, consider these strategies:

### Repository Organization

- Split monolithic repositories into smaller, focused repositories
- Use submodules or package dependencies for larger projects
- Keep binary assets separate from code (use LFS or separate storage)

### Git Best Practices

- Use `.gitignore` to exclude build artifacts, dependencies, and generated content
- Periodically clean repository history if appropriate
- Use Git LFS for large binary files
- Consider shallow clones for CI/CD and temporary operations

### Analysis Strategies

- Focus analysis on specific directories or file types
- Process subdirectories individually
- Use targeted queries rather than whole-repository analysis

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug logging:
   ```bash
   cursor-utils repo https://github.com/username/repo-name --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Try with a known small repository:
   ```bash
   cursor-utils repo https://github.com/minimal-repo/example
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Information about the repository size (if known)
   - The repository URL
   - What solutions you've already tried 