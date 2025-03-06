# Data Models Reference

This reference provides detailed information about the data models used throughout Cursor Utils, including their implementation details and usage examples.

## Model Architecture

Cursor Utils uses TypedDict models and dataclasses for type-safe data handling across the application:

```
cursor_utils/
├── types.py             # TypedDict models for configuration and API responses
├── config.py            # Configuration dataclasses and enums
└── utils/
    └── file_rank_algo.py # File ranking TypedDict models
```

## Type Models

The `types.py` file defines several TypedDict models for configuration and API responses:

```python
from typing import Literal, TypedDict
from typing_extensions import NotRequired

# Model types
ModelType = Literal[
    "sonar",
    "sonar-pro",
    "sonar-reasoning",
    "sonar-pro-reasoning",
]

ModeType = Literal[
    "concise",
    "copilot",
]

SearchFocusType = Literal[
    "internet",
    "scholar",
    "writing",
    "wolfram",
    "youtube",
    "reddit",
]

# Configuration dictionary type
class SettingsDict(TypedDict):
    """Type definition for settings configuration."""
    debug: bool
    log_level: str

class WebConfig(TypedDict, total=True):
    """Type definition for web command configuration."""
    model: ModelType
    mode: ModeType
    search_focus: SearchFocusType

class GeminiConfig(TypedDict, total=True):
    """Type definition for Gemini command configuration."""
    model: str
    max_output_tokens: int
    temperature: float
    top_p: float
    top_k: int

class GitHubConfig(TypedDict, total=True):
    """Type definition for GitHub command configuration."""
    token_source: Literal["env", "config"]
    default_owner: str
    default_repo: str
    template_dir: str

class ConfigDict(TypedDict, total=True):
    """Type definition for configuration dictionary."""
    version: str
    settings: SettingsDict
    web: NotRequired[WebConfig]
    gemini: NotRequired[GeminiConfig]
    github: NotRequired[GitHubConfig]
    custom_options: NotRequired[dict[str, str]]

# Stream response type
class StreamResponse(TypedDict, total=True):
    """Type definition for stream response."""
    text: str
    done: bool
```

## Configuration Models

The `config.py` file defines several models for configuration management:

### APIKeyType Enum

```python
class APIKeyType(str, Enum):
    """Supported API key types."""

    GEMINI = "GEMINI_API_KEY"
    PERPLEXITY = "PERPLEXITY_API_KEY"
    GITHUB = "GITHUB_TOKEN"

    @property
    def description(self) -> str:
        """Get human-readable description of the API key."""
        return {
            self.GEMINI: "Google Gemini API Key",
            self.PERPLEXITY: "Perplexity AI API Key",
            self.GITHUB: "GitHub Personal Access Token",
        }[self]

    @property
    def feature_impact(self) -> str:
        """Get description of features impacted if key is missing."""
        return {
            self.GEMINI: "AI code generation and contextual analysis features will be limited",
            self.PERPLEXITY: "AI guided web search features will be unavailable",
            self.GITHUB: "GitHub integration features will be unavailable",
        }[self]
```

### APIKeyConfig Dataclass

```python
@dataclass
class APIKeyConfig:
    """Configuration for an API key."""

    key_type: APIKeyType
    value: Optional[str] = None
    is_set: bool = False
```

### Config Class

The `Config` class manages configuration and API keys:

```python
class Config:
    """Manages configuration and API keys."""

    def __init__(self) -> None:
        """Initialize configuration manager."""
        self.console = Console()
        self.env_file = Path.cwd() / ".env"
        self.config_dir = Path.cwd() / "config"
        self.yaml_config = Path.cwd() / "cursor-utils.yaml"
        self.config_path = self.yaml_config

        # Ensure required files and directories exist
        self._ensure_env_file()
        self._ensure_config_dir()
        self._load_env()

        # Load configuration
        self.config = self.load_config()
```

## File Ranking Models

The `file_rank_algo.py` file defines several TypedDict models for file information:

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

## Error Models

The `errors.py` file defines a hierarchy of error classes:

```python
class CursorUtilsError(DiagnosticError):
    """Base diagnostic error class for all Cursor Utils errors."""

    docs_index = "https://github.com/gweidart/cursor-utils/errors/{code}.md"
    style = DiagnosticStyle(
        name="error",
        color="red",
        ascii_symbol="x",
        unicode_symbol="✗",
    )

    def __init__(
        self,
        *,
        message: str,
        code: str,
        causes: list[str],
        hint_stmt: Optional[str] = None,
    ) -> None:
        """Initialize with documentation URL."""
        super().__init__(
            message=message,
            code=code,
            causes=causes,
            hint_stmt=hint_stmt,
        )
```

## Usage Examples

### Using Configuration Models

```python
from cursor_utils.config import Config, APIKeyType, APIKeyConfig

# Initialize configuration
config = Config()

# Access configuration values
debug_mode = config.config["settings"]["debug"]
log_level = config.config["settings"]["log_level"]

# Check if API key is set
gemini_key = config.get_api_key(APIKeyType.GEMINI)
if gemini_key:
    print(f"Gemini API key is set")
else:
    print(f"Gemini API key is not set")

# Set API key
config.set_api_key(APIKeyType.GEMINI, "your-api-key-here")
```

### Using Type Models

```python
from cursor_utils.types import ConfigDict, WebConfig, GeminiConfig

# Create configuration dictionary
config: ConfigDict = {
    "version": "1.0.0",
    "settings": {
        "debug": False,
        "log_level": "INFO",
    },
    "web": {
        "model": "sonar-pro",
        "mode": "copilot",
        "search_focus": "internet",
    },
    "gemini": {
        "model": "gemini-2.0-pro",
        "max_output_tokens": 1024,
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
    },
}

# Access configuration values with type safety
web_config: WebConfig = config["web"]
gemini_config: GeminiConfig = config["gemini"]

print(f"Web model: {web_config['model']}")
print(f"Gemini model: {gemini_config['model']}")
```

### Using File Ranking Models

```python
from cursor_utils.utils.file_rank_algo import FileRanker, FileInfo

# Create list of files
files: list[FileInfo] = [
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

# Process results
for file in ranked_files:
    print(f"{file['path']}: {file['importance_score']:.4f}")
```

## Best Practices for Using Models

1. **Use Type Annotations**: Always use type annotations with the provided models for better type safety.

2. **Validate Configuration**: Ensure configuration values are valid before using them.

3. **Handle Missing Values**: Check for optional fields in TypedDict models before accessing them.

4. **Use Enums for Constants**: Use the provided enums like `APIKeyType` for type-safe constants.

5. **Follow the Model Structure**: Adhere to the structure defined by the models when creating new instances.

6. **Use Default Values**: Provide sensible default values for optional fields.

7. **Document Model Extensions**: If you extend the models, document the new fields and their purpose. 