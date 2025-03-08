import os
from collections import Counter
from typing import Optional, TypedDict

import pathspec
from pathspec import PathSpec


class BaseFileInfo(TypedDict):
    """
    Base typed dict with the required path key.
    """

    path: str


class ProcessedFileInfo(BaseFileInfo):
    """
    TypedDict for files that have been processed and have all required fields.
    """

    type: str
    size: int
    creation_time: float
    importance_score: float


class FileInfo(BaseFileInfo, total=False):
    """
    Typed dict for our file info. The path key is mandatory
    (from BaseFileInfo). The remaining fields can optionally
    be provided by the user. We fill them if missing.
    """

    type: str
    size: int
    time: float
    creation_time: float
    importance_score: float


# Common ignore patterns used across commands
COMMON_IGNORE_PATTERNS = [
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "node_modules",
    "build",
    "dist",
    ".idea",
    ".vscode",
]


def build_file_list(base_path: str) -> list[FileInfo]:
    """
    Build a list of FileInfo dictionaries for a given base path.

    Args:
        base_path: The base path to scan for files

    Returns:
        A list of FileInfo dictionaries with path keys

    """
    files: list[FileInfo] = []

    for root, dirs, filenames in os.walk(base_path):
        # Skip common ignored directories
        dirs[:] = [d for d in dirs if d not in COMMON_IGNORE_PATTERNS]

        for filename in filenames:
            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, base_path)

            # Skip files that are too large (>2GB)
            try:
                size = os.path.getsize(file_path)
                if size > 2 * (1024**3):
                    continue
            except OSError:
                continue

            # Create file info dictionary with just the path
            file_info: FileInfo = {"path": rel_path}
            files.append(file_info)

    return files


class FileRanker:
    """
    Ranks files by a weighted score.

        score = (type_frequency * type_weight)
              + (file_size      * size_weight)
              + (creation_time  * time_weight)

    Also excludes files matching .gitignore patterns (if any),
    unless they match .gitinclude patterns (which re-include them).

    This version uses:
      - Python's TypedDict for type safety (FileInfo).
      - pathspec for robust .gitignore matching.
    """

    def __init__(
        self,
        type_weight: float = 1.0,
        size_weight: float = 1.0,
        time_weight: float = 1.0,
        gitignore_path: Optional[str] = None,
        gitinclude_path: Optional[str] = None,
    ) -> None:
        """
        :param type_weight: Influence of file-type frequency in the final score
        :param size_weight: Influence of file size in the final score
        :param time_weight: Influence of file creation time in the final score
        :param gitignore_path: Path to a .gitignore-like file with exclusion patterns
        :param gitinclude_path: Path to a .gitinclude-like file with inclusion patterns
        """
        self.type_weight = type_weight
        self.size_weight = size_weight
        self.time_weight = time_weight

        self.ignore_spec: Optional[PathSpec] = self._compile_pathspec(gitignore_path)
        self.include_spec: Optional[PathSpec] = self._compile_pathspec(gitinclude_path)

    def rank_files(self, files: list[FileInfo]) -> list[ProcessedFileInfo]:
        """
        Filters out unwanted files based on .gitignore / .gitinclude,
        then computes a weighted importance score for each included file,
        and returns them sorted (descending) by that score.

        :param files: List of FileInfo typed dictionaries. Must have at least 'path'.
        :return: A new list of ProcessedFileInfo (with all fields set) in descending order of importance.
        """
        if not files:
            return []

        # 1) Filter via .gitignore / .gitinclude
        included_files: list[FileInfo] = [
            f for f in files if self._include_file(f["path"])
        ]

        if not included_files:
            return []

        # 2) Preprocess each file so it has guaranteed 'type', 'size', 'creation_time'
        preprocessed: list[ProcessedFileInfo] = [
            self._preprocess_file_info(file_dict) for file_dict in included_files
        ]

        # 3) Calculate type frequencies
        type_counts: Counter[str] = self._compute_type_frequencies(preprocessed)

        # 4) Compute importance score for each file
        for file_dict in preprocessed:
            file_dict["importance_score"] = self._compute_importance_score(
                file_dict, type_counts
            )

        # 5) Sort in descending order by importance score
        ranked: list[ProcessedFileInfo] = sorted(
            preprocessed, key=lambda x: x["importance_score"], reverse=True
        )
        return ranked

    # ------------------------------------------------------------------
    # .gitignore / .gitinclude logic
    # ------------------------------------------------------------------
    def _compile_pathspec(self, path: Optional[str]) -> Optional[PathSpec]:
        """
        Reads patterns from a file (e.g., .gitignore or .gitinclude),
        then compiles them into a PathSpec for matching.

        :param path: Path to a gitignore-like file
        :return: Compiled PathSpec object, or None if file doesn't exist or is empty.
        """
        if path is None:
            return None

        lines: list[str] = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line_stripped = line.strip()
                    if not line_stripped or line_stripped.startswith("#"):
                        continue
                    lines.append(line_stripped)
        except OSError:
            # If file is missing or unreadable, skip
            return None

        if lines:
            # "gitwildmatch" mimics Git's wildcard rules
            return pathspec.PathSpec.from_lines("gitwildmatch", lines)
        return None

    def _include_file(self, filepath: str) -> bool:
        """
        Determines if the file should be included in ranking:
         - If it matches .gitinclude => include
         - Else if it matches .gitignore => exclude
         - Otherwise => include.
        """
        if self.include_spec and self.include_spec.match_file(filepath):
            return True
        if self.ignore_spec and self.ignore_spec.match_file(filepath):
            return False
        return True

    # ------------------------------------------------------------------
    # Preprocessing & metadata
    # ------------------------------------------------------------------
    def _preprocess_file_info(self, file_info: FileInfo) -> ProcessedFileInfo:
        """
        Ensures a FileInfo dictionary has all required fields:
          - 'type' (file extension, or 'unknown' if none)
          - 'size' (in bytes, 0 if inaccessible)
          - 'creation_time' (epoch float, 0 if inaccessible)
          - 'importance_score' (initialized to 0.0, set later).

        :param file_info: A FileInfo typed dict with at least 'path'.
        :return: A ProcessedFileInfo with all required fields set.
        """
        # Create a new dict with required fields
        new_info: ProcessedFileInfo = {
            "path": file_info["path"],
            "type": file_info.get("type", "")
            or self._get_file_extension(file_info["path"]),
            "size": file_info.get("size", 0) or self._get_file_size(file_info["path"]),
            "creation_time": file_info.get("creation_time", 0)
            or self._get_file_creation_time(file_info["path"]),
            "importance_score": 0.0,  # Will be set later
        }
        return new_info

    @staticmethod
    def _get_file_extension(path: str) -> str:
        """
        Returns the lowercase file extension without the leading dot,
        or 'unknown' if none is found.
        """
        _, ext = os.path.splitext(path)
        return ext.lower().lstrip(".") if ext else "unknown"

    @staticmethod
    def _get_file_size(path: str) -> int:
        """Returns file size in bytes, or 0 if inaccessible."""
        try:
            return os.path.getsize(path)
        except OSError:
            return 0

    @staticmethod
    def _get_file_creation_time(path: str) -> float:
        """
        Returns the file's creation time (epoch).
        On Unix-like systems, getctime() can be the inode change time
        if true creation time is unavailable. Returns 0 if inaccessible.
        """
        try:
            return os.path.getctime(path)
        except OSError:
            return 0

    # ------------------------------------------------------------------
    # EXAMPLE IMPLEMENTATION
    # ------------------------------------------------------------------
    @staticmethod
    def _compute_type_frequencies(files: list[ProcessedFileInfo]) -> Counter[str]:
        """
        Counts how many times each file type appears in `files`.
        """
        file_types = [f["type"] for f in files]  # Safe now since type is required
        return Counter(file_types)

    def _compute_importance_score(
        self, file_info: ProcessedFileInfo, type_counts: Counter[str]
    ) -> float:
        """
        Computes the weighted importance score for a single file.

          score = (type_freq * self.type_weight)
                 + (size      * self.size_weight)
                 + (ctime     * self.time_weight)

        Note: For large files or recent creation times, the size or time component
        might dominate. Consider normalizing values for balanced scoring.
        """
        # All fields are guaranteed to exist in ProcessedFileInfo
        type_freq = type_counts[file_info["type"]]

        # Prevent division by zero in empty type counts
        if type_freq == 0:
            type_freq = 1

        return (
            type_freq * self.type_weight
            + file_info["size"] * self.size_weight
            + file_info["creation_time"] * self.time_weight
        )


def demo() -> None:
    """
    Simple usage demonstration. In real code, replace or remove this.
    """
    files: list[FileInfo] = [
        {"path": "docs/readme.md"},
        {"path": "src/main.py"},
        {"path": "src/old_helper.py"},
        {"path": "assets/image.png"},
        # Example with explicit metadata:
        # {"path": "logs/debug.log", "type": "log", "size": 1234, "creation_time": 1693000000.0}
    ]

    ranker = FileRanker(
        type_weight=2.0,
        size_weight=1.0,
        time_weight=0.5,
        gitignore_path="./.gitignore",
        gitinclude_path="./.gitinclude",
    )

    ranked_files: list[ProcessedFileInfo] = ranker.rank_files(files)

    for f in ranked_files:
        # All fields are guaranteed to exist in ProcessedFileInfo
        print(f"{f['path']} => Score: {f['importance_score']:.2f}")


if __name__ == "__main__":
    demo()
