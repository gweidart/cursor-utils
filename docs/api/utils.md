# Utilities API

Cursor-Utils provides a collection of utility modules that handle common operations for filesystem access, Git operations, text processing, and file ranking. These utilities are used throughout the application to provide consistent behavior and error handling.

## Overview

The utilities are organized into the following modules:

| Module | Description | Primary Functions |
|--------|-------------|-------------------|
| [Filesystem (fs)](#filesystem-utilities) | File and directory operations | Reading/writing files, directory management |
| [Git Operations (git)](#git-utilities) | Git repository interactions | Clone, checkout, analyze repositories |
| [Text Processing (text)](#text-utilities) | Text manipulation functions | Text formatting, ANSI handling, code highlighting |
| [File Ranking (file_rank_algo)](#file-ranking-utilities) | Algorithms for ranking files | File ranking based on multiple factors |

## Filesystem Utilities

The `fs` module provides functions for file and directory operations with consistent error handling.

### Core Functions

#### `ensure_directory(path)`

Ensure a directory exists, creating it if necessary.

**Parameters**:
- `path` (Union[str, Path]): The directory path

**Returns**:
- `Path`: The directory path as a Path object

**Raises**:
- `FilesystemError`: If the directory cannot be created

**Example**:
```python
from cursor_utils.utils.fs import ensure_directory

# Create a directory if it doesn't exist
config_dir = ensure_directory("~/.config/my-app")
```

#### `get_temp_dir(prefix="cursor_utils_")`

Get a temporary directory with the specified prefix.

**Parameters**:
- `prefix` (str): The prefix for the directory name

**Returns**:
- `Path`: The temporary directory path

**Raises**:
- `FilesystemError`: If the temporary directory cannot be created

**Example**:
```python
from cursor_utils.utils.fs import get_temp_dir

# Create a temporary directory
temp_dir = get_temp_dir("my_app_")
try:
    # Use the temporary directory
    print(f"Using temporary directory: {temp_dir}")
finally:
    # Clean up (optional, depends on your needs)
    import shutil
    shutil.rmtree(temp_dir)
```

#### `read_file(path, binary=False)`

Read a file, optionally in binary mode.

**Parameters**:
- `path` (Union[str, Path]): The file path
- `binary` (bool): Whether to read the file in binary mode

**Returns**:
- `Union[str, bytes]`: The file contents

**Raises**:
- `FilesystemError`: If the file cannot be read

**Example**:
```python
from cursor_utils.utils.fs import read_file

# Read a text file
content = read_file("config.json")

# Read a binary file
binary_content = read_file("image.png", binary=True)
```

#### `write_file(path, content, binary=False)`

Write content to a file, optionally in binary mode.

**Parameters**:
- `path` (Union[str, Path]): The file path
- `content` (Union[str, bytes]): The file contents
- `binary` (bool): Whether to write the file in binary mode

**Raises**:
- `FilesystemError`: If the file cannot be written

**Example**:
```python
from cursor_utils.utils.fs import write_file

# Write a text file
write_file("output.txt", "Hello, world!")

# Write a binary file
write_file("output.bin", b"\x00\x01\x02\x03", binary=True)
```

#### `list_files(directory, pattern="*", recursive=False)`

List files in a directory matching a glob pattern.

**Parameters**:
- `directory` (Union[str, Path]): The directory path
- `pattern` (str): The glob pattern to match
- `recursive` (bool): Whether to search recursively

**Returns**:
- `list[Path]`: The list of file paths

**Raises**:
- `FilesystemError`: If the directory cannot be read

**Example**:
```python
from cursor_utils.utils.fs import list_files

# List all Python files in the current directory
py_files = list_files(".", "*.py")

# List all JSON files recursively
json_files = list_files(".", "*.json", recursive=True)
```

#### `is_binary_file(path)`

Check if a file is binary.

**Parameters**:
- `path` (Union[str, Path]): The file path

**Returns**:
- `bool`: True if the file is binary, False otherwise

**Raises**:
- `FilesystemError`: If the file cannot be read

**Example**:
```python
from cursor_utils.utils.fs import is_binary_file

# Check if a file is binary
if is_binary_file("unknown_file"):
    print("This is a binary file")
else:
    print("This is a text file")
```

### Error Handling

The `fs` module defines a `FilesystemError` class that provides context-specific error messages for filesystem operations.

```python
try:
    content = read_file("non_existent_file.txt")
except FilesystemError as e:
    print(f"Filesystem error: {e.message}")
    print(f"Path: {e.path}")
    if e.help_text:
        print(f"Help: {e.help_text}")
```

## Git Utilities

The `git` module provides functions for working with Git repositories.

### Core Functions

#### `_run_git_command(args, cwd=None, capture_output=True)`

Internal function to run a Git command.

**Parameters**:
- `args` (list[str]): The Git command arguments
- `cwd` (Optional[Union[str, Path]]): The working directory
- `capture_output` (bool): Whether to capture the command output

**Returns**:
- `str`: The command output

**Raises**:
- `GitError`: If the command fails

#### `is_git_repository(path)`

Check if a directory is a Git repository.

**Parameters**:
- `path` (Union[str, Path]): The directory path

**Returns**:
- `bool`: True if the directory is a Git repository, False otherwise

**Example**:
```python
from cursor_utils.utils.git import is_git_repository

# Check if the current directory is a Git repository
if is_git_repository("."):
    print("This is a Git repository")
else:
    print("This is not a Git repository")
```

#### `get_repository_root(path)`

Get the root directory of a Git repository.

**Parameters**:
- `path` (Union[str, Path]): A path within the repository

**Returns**:
- `Path`: The repository root path

**Raises**:
- `GitError`: If the path is not within a Git repository

**Example**:
```python
from cursor_utils.utils.git import get_repository_root

# Get the root directory of the Git repository
repo_root = get_repository_root(".")
print(f"Repository root: {repo_root}")
```

#### `get_default_branch(path)`

Get the default branch of a repository.

**Parameters**:
- `path` (Union[str, Path]): A path within the repository

**Returns**:
- `str`: The default branch name

**Raises**:
- `GitError`: If the default branch cannot be determined

**Example**:
```python
from cursor_utils.utils.git import get_default_branch

# Get the default branch of a repository
branch = get_default_branch("my-repo")
print(f"Default branch: {branch}")
```

#### `clone_repository(url, target_dir, branch=None, depth=None)`

Clone a Git repository.

**Parameters**:
- `url` (str): The repository URL
- `target_dir` (Union[str, Path]): The target directory
- `branch` (Optional[str]): The branch to checkout
- `depth` (Optional[int]): The clone depth (for shallow clones)

**Returns**:
- `Path`: The repository directory path

**Raises**:
- `GitError`: If the repository cannot be cloned

**Example**:
```python
from cursor_utils.utils.git import clone_repository

# Clone a repository
repo_dir = clone_repository(
    "https://github.com/gweidart/cursor-utils.git",
    "cursor-utils-clone",
    branch="main",
    depth=1
)
```

### Error Handling

The `git` module defines a `GitError` class for Git-related errors:

```python
try:
    repo_root = get_repository_root("not-a-git-repo")
except GitError as e:
    print(f"Git error: {e.message}")
    if e.help_text:
        print(f"Help: {e.help_text}")
```

## Text Utilities

The `text` module provides functions for text processing and formatting.

### Core Functions

#### `truncate_text(text, max_length, suffix="...")`

Truncate text to a maximum length.

**Parameters**:
- `text` (str): The text to truncate
- `max_length` (int): The maximum length
- `suffix` (str): The suffix to append if truncated

**Returns**:
- `str`: The truncated text

**Example**:
```python
from cursor_utils.utils.text import truncate_text

# Truncate a long string
long_text = "This is a very long text that needs to be truncated"
short_text = truncate_text(long_text, 20)
print(short_text)  # "This is a very long..."
```

#### `wrap_text(text, width=80)`

Wrap text to a maximum width.

**Parameters**:
- `text` (str): The text to wrap
- `width` (int): The maximum width

**Returns**:
- `str`: The wrapped text

**Example**:
```python
from cursor_utils.utils.text import wrap_text

# Wrap text to a specific width
long_text = "This is a long text that will be wrapped to fit within the specified width"
wrapped_text = wrap_text(long_text, width=40)
print(wrapped_text)
```

#### `strip_ansi(text)`

Strip ANSI escape sequences from text.

**Parameters**:
- `text` (str): The text to strip

**Returns**:
- `str`: The stripped text

**Example**:
```python
from cursor_utils.utils.text import strip_ansi

# Strip ANSI escape sequences from text
ansi_text = "\033[31mRed text\033[0m"
plain_text = strip_ansi(ansi_text)
print(plain_text)  # "Red text"
```

#### `highlight_code(code, rich_theme, language=None, line_numbers=False, use_rich=False)`

Highlight code syntax.

**Parameters**:
- `code` (str): The code to highlight
- `rich_theme` (str | SyntaxTheme): The Rich theme to use
- `language` (Optional[str]): The language for syntax highlighting
- `line_numbers` (bool): Whether to include line numbers
- `use_rich` (bool): Whether to use Rich for highlighting

**Returns**:
- `str`: The highlighted code

**Example**:
```python
from cursor_utils.utils.text import highlight_code

# Highlight Python code
code = "def hello():\n    print('Hello, world!')"
highlighted = highlight_code(code, "monokai", language="python", line_numbers=True)
print(highlighted)
```

## File Ranking Utilities

The `file_rank_algo` module provides algorithms for ranking files by relevance and importance.

### Core Types

#### `BaseFileInfo`

Base TypedDict with the required path key.

```python
class BaseFileInfo(TypedDict):
    path: str
```

#### `ProcessedFileInfo`

TypedDict for files that have been processed with all required fields.

```python
class ProcessedFileInfo(BaseFileInfo):
    type: str
    size: int
    creation_time: float
    importance_score: float
```

#### `FileInfo`

TypedDict for file info with optional fields.

```python
class FileInfo(BaseFileInfo, total=False):
    type: str
    size: int
    time: float
    creation_time: float
    importance_score: float
```

### Core Functions

#### `build_file_list(base_path)`

Build a list of FileInfo dictionaries for a given base path.

**Parameters**:
- `base_path` (str): The base path to scan for files

**Returns**:
- `list[FileInfo]`: A list of FileInfo dictionaries with path keys

**Example**:
```python
from cursor_utils.utils.file_rank_algo import build_file_list

# Get a list of files in a directory
files = build_file_list("./my-project")
print(f"Found {len(files)} files")
```

### FileRanker Class

The `FileRanker` class provides file ranking functionality based on multiple factors.

#### `FileRanker(type_weight=1.0, size_weight=1.0, time_weight=1.0, gitignore_path=None, gitinclude_path=None)`

Create a new FileRanker instance.

**Parameters**:
- `type_weight` (float): Influence of file-type frequency in the final score
- `size_weight` (float): Influence of file size in the final score
- `time_weight` (float): Influence of file creation time in the final score
- `gitignore_path` (Optional[str]): Path to a .gitignore-like file with exclusion patterns
- `gitinclude_path` (Optional[str]): Path to a .gitinclude-like file with inclusion patterns

**Example**:
```python
from cursor_utils.utils.file_rank_algo import FileRanker, build_file_list

# Create a ranker with custom weights
ranker = FileRanker(
    type_weight=1.5,  # Prefer common file types
    size_weight=0.8,  # Slightly prefer smaller files
    time_weight=1.2,  # Prefer newer files
    gitignore_path=".gitignore"  # Use .gitignore patterns
)

# Rank files
files = build_file_list("./my-project")
ranked_files = ranker.rank_files(files)

# Print top 5 most important files
for file_info in ranked_files[:5]:
    print(f"{file_info['path']} (score: {file_info['importance_score']:.2f})")
```

#### `rank_files(files)`

Rank files by importance score.

**Parameters**:
- `files` (list[FileInfo]): List of FileInfo dictionaries

**Returns**:
- `list[ProcessedFileInfo]`: List of ranked files with all fields set

**Example**:
```python
from cursor_utils.utils.file_rank_algo import FileRanker, build_file_list

# Create a ranker and rank files
ranker = FileRanker()
files = build_file_list("./my-project")
ranked_files = ranker.rank_files(files)
```

## Best Practices

1. **Handle Errors Properly**: All utility functions raise specific exceptions with helpful error messages
   ```python
   try:
       clone_repository("https://github.com/invalid/repo.git", "target")
   except GitError as e:
       print(f"Git error: {e.message}")
       if e.help_text:
           print(f"Help: {e.help_text}")
   ```

2. **Clean Up Temporary Resources**: When using functions that create temporary resources, ensure proper cleanup
   ```python
   temp_dir = get_temp_dir()
   try:
       # Use temporary directory
   finally:
       import shutil
       shutil.rmtree(temp_dir)
   ```

3. **Prefer Path Objects**: Most functions accept both strings and Path objects, but using Path objects provides more flexibility
   ```python
   from pathlib import Path
   config_dir = ensure_directory(Path.home() / ".config" / "my-app")
   ```

4. **Use Safe Operations**: Utility functions handle common edge cases and provide safe defaults
   ```python
   # Safely read a file that might not exist
   try:
       content = read_file("config.json")
   except FilesystemError:
       content = "{}"  # Default content
   ``` 