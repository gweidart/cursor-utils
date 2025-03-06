# Utilities Reference

This reference provides documentation on the utility modules used in Cursor Utils, focusing on the actual implementations present in the codebase.

## Utility Architecture

Cursor Utils has a focused utility architecture with a primary focus on file ranking:

```
cursor_utils/utils/
├── __init__.py         # Exports FileRanker
└── file_rank_algo.py   # Repository analysis algorithm
```

The `__init__.py` file is simple and only exports the `FileRanker` class:

```python
from cursor_utils.utils.file_rank_algo import FileRanker

__all__ = ["FileRanker"]
```

## File Ranking Algorithm

The file ranking algorithm (`cursor_utils/utils/file_rank_algo.py`) provides functionality to rank files based on their type, size, and creation time, while respecting `.gitignore` patterns.

### Core Data Types

The module defines several typed dictionaries for file information:

```python
class BaseFileInfo(TypedDict):
    """Base file information with just the path."""
    
    path: str


class ProcessedFileInfo(BaseFileInfo):
    """Processed file information with additional metadata."""
    
    type: str
    size: int
    creation_time: float
    importance_score: float


class FileInfo(TypedDict, total=False):
    """File information with optional fields."""
    
    path: str
    type: NotRequired[str]
    size: NotRequired[int]
    creation_time: NotRequired[float]
```

### FileRanker Class

The `FileRanker` class is the primary utility exported from the utils module:

```python
class FileRanker:
    """
    Ranks files based on a weighted score calculated from type frequency,
    file size, and creation time.
    
    Files matching .gitignore patterns are excluded by default.
    """
    
    def __init__(
        self,
        type_weight: float = 0.4,
        size_weight: float = 0.3,
        time_weight: float = 0.3,
        gitignore_path: Optional[str] = None,
        gitinclude_path: Optional[str] = None,
    ) -> None:
        """
        Initialize the file ranker with specified weights.
        
        Args:
            type_weight: Weight for file type in importance calculation
            size_weight: Weight for file size in importance calculation
            time_weight: Weight for creation time in importance calculation
            gitignore_path: Path to .gitignore file (optional)
            gitinclude_path: Path to .gitinclude file (optional)
        """
```

### Key Methods

The `FileRanker` class provides the following key methods:

#### rank_files

```python
def rank_files(self, files: list[FileInfo]) -> list[ProcessedFileInfo]:
    """
    Rank files based on their importance.
    
    Args:
        files: List of file information dictionaries
        
    Returns:
        List of processed file information dictionaries with importance scores,
        sorted in descending order of importance
    """
```

This method:
1. Filters files based on gitignore/gitinclude patterns
2. Computes type frequency across all files
3. Calculates normalized scores for type, size, and creation time
4. Computes a weighted importance score for each file
5. Returns files sorted by importance score

### Usage Example

The module includes a demonstration function showing how to use the `FileRanker`:

```python
def demo() -> None:
    """Demonstrate file ranking functionality."""
    # Initialize with sample files
    files = [
        {"path": "file1.py", "size": 1000, "creation_time": 1600000000},
        {"path": "file2.js", "size": 2000, "creation_time": 1600001000},
        {"path": "file3.md", "size": 500, "creation_time": 1600002000},
        {"path": "file4.py", "size": 1500, "creation_time": 1600003000},
    ]
    
    # Create ranker with custom weights
    ranker = FileRanker(
        type_weight=0.5,
        size_weight=0.3,
        time_weight=0.2,
    )
    
    # Rank files
    ranked_files = ranker.rank_files(files)
    
    # Print results
    for file in ranked_files:
        print(f"{file['path']}: {file['importance_score']:.4f}")
```

## Best Practices for Using Utilities

When working with the `FileRanker` utility:

1. **Customize weights** based on your specific use case:
   - Increase `type_weight` to prioritize certain file types
   - Increase `size_weight` to prioritize larger/smaller files
   - Increase `time_weight` to prioritize newer/older files

2. **Provide complete file information** when possible:
   - Always include the `path` (required)
   - Include `type`, `size`, and `creation_time` for accurate ranking

3. **Use gitignore/gitinclude paths** to filter files appropriately:
   - Point to your project's `.gitignore` to exclude irrelevant files
   - Create a `.gitinclude` file to explicitly include certain patterns

4. **Process the results** as needed for your specific use case:
   - Filter by minimum score threshold
   - Group by file type
   - Take only the top N results