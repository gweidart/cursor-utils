# REPO_FILE_ERROR (repo-005)

## Error Description

This error occurs when Cursor Utils encounters an issue with a file while working with a repository. This could include problems reading, processing, or accessing specific files within the repository during analysis or other operations.

## Example Error

```
× ERROR: Error with file in repository
  Code: repo-005
  
  Causes:
  - Failed to read or process a file in the repository
  - The file has invalid encoding or format
  - The file is too large or complex
  - Permission issues when accessing the file
  - The file is binary or in an unsupported format
  
  Suggestion: Check the file format and encoding, or exclude problematic files
  
  For more information: https://gweidart.github.io/cursor-utils/errors/repo-005.md
```

## Common Causes

1. **File Access Issues**: Problems reading or accessing specific files in the repository.
2. **Encoding Problems**: Files with unusual or incompatible character encodings.
3. **Large Files**: Files that exceed size limits for processing.
4. **Unsupported Formats**: Binary files or other formats that can't be properly processed.
5. **Corrupt Files**: Files that are damaged or improperly formatted.
6. **Symlink Issues**: Problematic symbolic links or file references.

## Solutions

### Identify problematic files

Check logs to identify which files are causing issues:

```bash
cat ~/.cursor-utils/logs/cursor-utils.log | grep "file error"
```

### Exclude specific files

Use the exclude option to skip problematic files:

```bash
cursor-utils repo https://github.com/username/repo-name --exclude "path/to/problem/file.ext,*.bin"
```

### Filter by file type

Process only specific file types:

```bash
cursor-utils repo https://github.com/username/repo-name --include "*.py,*.js,*.md"
```

### Limit file size

Skip large files that might cause issues:

```bash
cursor-utils repo https://github.com/username/repo-name --max-file-size 1MB
```

### Check file encoding

If you have access to the repository, check the encoding of problematic files:

```bash
# Linux/macOS
file -i path/to/problem/file.ext

# Convert encoding if needed
iconv -f ISO-8859-1 -t UTF-8 path/to/problem/file.ext > path/to/problem/file.utf8.ext
```

### Try a different repository

If the current repository has persistent file issues, try a different one:

```bash
cursor-utils repo https://github.com/username/different-repo
```

## Related Commands

- `cursor-utils repo --help` - Show help for the repo command
- `cursor-utils config show` - Display current configuration

## Related Error Codes

- [REPO_CLONE_ERROR (repo-001)](repo-001.md) - Error cloning repository
- [REPO_ANALYZE_ERROR (repo-003)](repo-003.md) - Error analyzing repository
- [GEMINI_FILE_ERROR (gemini-005)](gemini-005.md) - Error with file in Gemini command
- [GENERAL_FILE_ERROR (general-002)](general-002.md) - General file error

## Advanced Troubleshooting

### Check file characteristics

If you have access to the repository, examine the characteristics of problematic files:

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

Identify potentially problematic files in the repository:

```bash
# Find very large files
find . -type f -size +10M

# Find files with unusual extensions
find . -type f | grep -v -E '\.(py|js|html|css|md|json|yaml|yml|txt|xml|csv|rst|ini|cfg|conf)$'

# Find files without extensions
find . -type f -not -path "*/\.*" | grep -v "\..*$"
```

### Check symlinks

Identify and check symbolic links:

```bash
# Find symbolic links
find . -type l

# Check if symlinks are valid
find . -type l -exec ls -la {} \;
```

### Verify file permissions

Check file permissions:

```bash
# Find files with unusual permissions
find . -type f -not -perm -644
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
   cursor-utils repo https://github.com/username/repo-name --debug
   ```

2. Check the logs for specific file errors:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log | grep -A 5 "file error"
   ```

3. Try limiting scope to a particular directory:
   ```bash
   cursor-utils repo https://github.com/username/repo-name --subdir docs/
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Information about the problematic file (if known)
   - The repository URL
   - What solutions you've already tried 