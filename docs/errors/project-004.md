# PROJECT_FILE_ERROR (project-004)

## Error Description

This error occurs when Cursor Utils encounters an issue with a file while working with a project. This could include problems reading, processing, or accessing specific files within the project during analysis or other operations.

## Example Error

```
× ERROR: Error with file in project
  Code: project-004
  
  Causes:
  - Failed to read or process a file in the project
  - The file has invalid encoding or format
  - The file is too large or complex
  - Permission issues when accessing the file
  - The file is binary or in an unsupported format
  
  Suggestion: Check the file format and encoding, or exclude problematic files
  
  For more information: https://gweidart.github.io/cursor-utils/errors/project-004.md
```

## Common Causes

1. **File Access Issues**: Problems reading or accessing specific files in the project.
2. **Encoding Problems**: Files with unusual or incompatible character encodings.
3. **Large Files**: Files that exceed size limits for processing.
4. **Unsupported Formats**: Binary files or other formats that can't be properly processed.
5. **Corrupt Files**: Files that are damaged or improperly formatted.
6. **Permission Issues**: Insufficient permissions to read certain files.

## Solutions

### Identify problematic files

Check logs to identify which files are causing issues:

```bash
cat ~/.cursor-utils/logs/cursor-utils.log | grep "file error"
```

### Exclude specific files

Use the exclude option to skip problematic files:

```bash
cursor-utils project analyze --exclude "path/to/problem/file.ext,*.bin"
```

### Filter by file type

Process only specific file types:

```bash
cursor-utils project analyze --include "*.py,*.js,*.md"
```

### Limit file size

Skip large files that might cause issues:

```bash
cursor-utils project analyze --max-file-size 1MB
```

### Check file encoding

Check the encoding of problematic files:

```bash
# Linux/macOS
file -i path/to/problem/file.ext

# Convert encoding if needed
iconv -f ISO-8859-1 -t UTF-8 path/to/problem/file.ext > path/to/problem/file.utf8.ext
```

### Fix file permissions

Ensure you have read permissions for all project files:

```bash
# Linux/macOS
find . -type f -not -readable -exec chmod +r {} \;

# Windows PowerShell
Get-ChildItem -Recurse | Where-Object { -not $_.PSIsContainer } | ForEach-Object { $_.IsReadOnly = $false }
```

## Related Commands

- `cursor-utils project --help` - Show help for the project command
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [PROJECT_TOO_LARGE (project-001)](project-001.md) - Project size exceeds limits
- [PROJECT_ANALYZE_ERROR (project-002)](project-002.md) - Error analyzing project
- [REPO_FILE_ERROR (repo-005)](repo-005.md) - Error with file in repository
- [GEMINI_FILE_ERROR (gemini-005)](gemini-005.md) - Error with file in Gemini command

## Advanced Troubleshooting

### Check file characteristics

Examine the characteristics of problematic files:

```bash
# Check file type
file path/to/problem/file.ext

# Check file size
du -h path/to/problem/file.ext

# Check file encoding
chardet path/to/problem/file.ext  # If you have chardet installed

# Check for binary content
grep -I "^" path/to/problem/file.ext > /dev/null || echo "Binary file"
```

### Look for unusual files

Identify potentially problematic files in the project:

```bash
# Find very large files
find . -type f -size +10M

# Find files with unusual extensions
find . -type f | grep -v -E '\.(py|js|html|css|md|json|yaml|yml|txt|xml|csv|rst|ini|cfg|conf)$'

# Find files without extensions
find . -type f -not -path "*/\.*" | grep -v "\..*$"
```

### Check for hidden files

Identify hidden files that might cause issues:

```bash
# Linux/macOS
find . -type f -name ".*" | grep -v ".git"

# Windows PowerShell
Get-ChildItem -Hidden -Recurse | Where-Object { -not $_.PSIsContainer }
```

### Verify line endings

Check for mixed line endings that might cause issues:

```bash
# Find files with mixed line endings
find . -type f -name "*.py" -exec file {} \; | grep "with CRLF, LF line terminators"
```

## File Type Considerations

Different types of files have different considerations for processing:

| File Type | Considerations |
|-----------|----------------|
| Text files | Usually process well, but may have encoding issues |
| Source code | Generally well-supported, but very large files may cause issues |
| Markdown/documentation | Usually process well |
| Binary files | May cause processing errors; often should be excluded |
| Generated files | May be large or have unusual formats; consider excluding |
| Configuration files | Usually small and process well |
| Data files | May be very large or have complex formats |

## Common Problematic File Types

These file types often cause issues and should generally be excluded:

| File Type | Description | Recommendation |
|-----------|-------------|----------------|
| `.pyc` | Python compiled bytecode | Exclude with `--exclude "*.pyc"` |
| `.class` | Java compiled bytecode | Exclude with `--exclude "*.class"` |
| `.o`, `.obj` | Compiled object files | Exclude with `--exclude "*.o,*.obj"` |
| `.bin`, `.exe` | Binary executables | Exclude with `--exclude "*.bin,*.exe"` |
| `.so`, `.dll` | Shared libraries | Exclude with `--exclude "*.so,*.dll"` |
| Large media files | Images, videos, audio | Exclude with `--exclude "*.jpg,*.png,*.mp4"` |
| Log files | Application logs | Exclude with `--exclude "*.log"` |
| Database files | Database data files | Exclude with `--exclude "*.db,*.sqlite"` |

## Tips for Handling Problematic Files

### For Large Files

- Split large files into smaller ones if possible
- Process only the most relevant sections
- Use summarization tools before processing

### For Binary Files

- Exclude binary files from processing
- Use specific tools designed for the binary format
- Convert to text representation if possible

### For Encoding Issues

- Convert files to UTF-8 encoding
- Add proper encoding declarations to source files
- Use encoding detection tools

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug logging:
   ```bash
   cursor-utils project analyze --debug
   ```

2. Check the logs for specific file errors:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log | grep -A 5 "file error"
   ```

3. Try limiting scope to a particular directory:
   ```bash
   cursor-utils project analyze --subdir docs/
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Information about the problematic file (if known)
   - The command you were trying to run
   - What solutions you've already tried 