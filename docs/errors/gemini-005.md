# GEMINI_FILE_ERROR (gemini-005)

## Error Description

This error occurs when Cursor Utils encounters an issue with a file while using the Gemini command. This could be due to problems with reading, processing, or accessing a file that was specified as context for the Gemini API request.

## Example Error

```
× ERROR: Error with file in Gemini command
  Code: gemini-005
  
  Causes:
  - The specified file does not exist
  - Insufficient permissions to read the file
  - The file format is not supported
  - The file is too large for processing
  - File path is invalid
  
  Suggestion: Check that the file exists and is accessible
  
  For more information: https://github.com/gweidart/cursor-utils/errors/gemini-005.md
```

## Common Causes

1. **File Not Found**: The specified file doesn't exist at the given path.
2. **Permission Issues**: The user doesn't have permission to read the file.
3. **Invalid File Format**: The file format is not supported or cannot be processed.
4. **File Size Limits**: The file exceeds size limits for Gemini API requests.
5. **Path Issues**: The file path is invalid or malformed.
6. **File Encoding**: The file has an encoding that cannot be properly processed.

## Solutions

### Check file existence

Verify that the file exists at the specified path:

```bash
# Linux/macOS
ls -la /path/to/your/file

# Windows (PowerShell)
Test-Path -Path "C:\path\to\your\file"
```

### Check file permissions

Ensure you have read permissions for the file:

```bash
# Linux/macOS
ls -la /path/to/your/file
chmod 644 /path/to/your/file  # If needed

# Windows (PowerShell)
Get-Acl -Path "C:\path\to\your\file"
```

### Verify file format and size

Check if the file is in a supported format and within size limits:

```bash
# Linux/macOS
file /path/to/your/file  # Check file type
du -h /path/to/your/file  # Check file size

# Windows (PowerShell)
Get-Item -Path "C:\path\to\your\file" | Select-Object Length
```

Note: Gemini typically works best with text files. Very large files may need to be split or summarized before sending to the API.

### Use absolute paths

When specifying file paths, use absolute paths instead of relative ones:

```bash
cursor-utils gemini "Analyze this code" --append /absolute/path/to/file.py
```

### Fix file encoding issues

If the file has encoding issues, convert it to UTF-8:

```bash
# Linux/macOS
iconv -f ORIGINAL_ENCODING -t UTF-8 /path/to/file > /path/to/file.utf8

# Windows (PowerShell)
Get-Content -Path "C:\path\to\file" -Encoding ORIGINAL_ENCODING | Set-Content -Path "C:\path\to\file.utf8" -Encoding UTF8
```

### Try a different file

If one file is causing issues, try with a different file:

```bash
cursor-utils gemini "your prompt" --append /path/to/different/file.txt
```

## Related Commands

- `cursor-utils gemini --help` - Show help for the Gemini command
- `cursor-utils gemini "prompt" --append FILE` - Use a file as context for the prompt

## Related Error Codes

- [GEMINI_API_ERROR (gemini-001)](gemini-001.md) - Error with Gemini API
- [FILE_NOT_FOUND (install-002)](install-002.md) - File not found during installation
- [GENERAL_FILE_ERROR (general-002)](general-002.md) - General file error

## Advanced Troubleshooting

### Check file content

Examine the content of the file to ensure it's valid:

```bash
# Linux/macOS
cat /path/to/your/file | head -20  # View first 20 lines

# Windows (PowerShell)
Get-Content -Path "C:\path\to\your\file" -TotalCount 20
```

### Check for hidden characters

Look for hidden or non-printable characters that might cause issues:

```bash
# Linux/macOS
xxd /path/to/your/file | head

# Windows (PowerShell)
Format-Hex -Path "C:\path\to\your\file" -Count 100
```

### Try preprocessing the file

For large or complex files, try preprocessing them:

```bash
# Extract only text content
grep -v "^$" /path/to/your/file | grep -v "^#" > /path/to/simplified.txt

# Or limit to the most relevant section
sed -n '100,200p' /path/to/your/file > /path/to/section.txt
```

### Debug file processing

Run with debug mode to see how the file is being processed:

```bash
cursor-utils gemini "your prompt" --append /path/to/your/file --debug
```

## File Limitations for Gemini API

When using files with the Gemini API, be aware of these limitations:

### File Size

- The Gemini API has token limits for inputs
- Large files may be truncated or rejected
- Consider splitting large files into smaller chunks

### File Types

Files that work best:
- Plain text (`.txt`)
- Source code (`.py`, `.js`, etc.)
- Markdown (`.md`)
- JSON (`.json`)
- YAML (`.yaml`, `.yml`)

Files that may cause issues:
- Binary files
- Very large files
- Files with unusual encodings
- Files with complex formatting

### Context Window Limitations

The Gemini API has a maximum context window size:
- Total tokens (input + output) must be within limits
- Model-specific limits apply (e.g., 32K tokens for Gemini Pro)
- Consider summarizing or focusing on relevant parts of large files

## Still Having Issues?

If you've tried the solutions above and still encounter the error, please:

1. Run with debug logging:
   ```bash
   cursor-utils gemini "your prompt" --append /path/to/your/file --debug
   ```

2. Check the logs:
   ```bash
   cat ~/.cursor-utils/logs/cursor-utils.log
   ```

3. Try with a simple text file:
   ```bash
   echo "Test content" > ~/test.txt
   cursor-utils gemini "Analyze this" --append ~/test.txt
   ```

4. If the issue persists, please [submit a bug report](https://github.com/gweidart/cursor-utils/issues) with:
   - The complete error message
   - Information about the file (type, size, encoding if known)
   - The command you were trying to run
   - Output of debug logs 