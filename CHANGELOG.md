# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New utility modules for common functionality:
  - `command_helpers.py`: Standardized error handling for commands
  - `api_helpers.py`: Centralized API key management
  - `config_helpers.py`: Simplified configuration handling
- Comprehensive documentation with examples for utility modules
- Protocol classes for better type safety and IDE support

### Changed
- Improved code organization and reduced duplication
- Simplified error handling across commands
- Refactored web, gemini, repo, project, github, install, and config commands to use the new utility modules
- Reduced cyclomatic complexity in command implementations
- Enhanced docstrings with detailed explanations and examples

### Fixed
- Fixed type annotations in web and gemini commands
- Added Protocol classes for better type safety with external libraries
- Improved async handling in Gemini client integration
- Fixed linter errors related to unknown attributes and types

## [0.1.2] - 2025-03-07

### Fixed
- Fixed `repo` command to properly send repository files to Gemini along with the ranking report
- Fixed `project` command to properly send project files to Gemini along with the ranking report
- Fixed type error in `project` command that was causing it to fail
- Added error handling for binary files in the `repo` and `project` commands
- Added file size limit (2GB) for individual files to prevent issues with very large files
- Added total context size limit (2GB) to comply with Gemini API limits
- Improved repository and project analysis by combining the ranking report with the actual source code files
- Maintained support for both local and repository .gitignore files
- Fixed configuration messages appearing in command output

## [0.1.1] - 2025-03-06

### Added
- Basic validation for API keys with helpful warnings
- Detailed error messages with actionable advice
- Improved documentation with troubleshooting guides
- Version-specific dependency requirements

### Changed
- Enhanced error handling for API calls
- Improved network error detection and recovery
- Better guidance for obtaining and configuring API keys
- More robust configuration validation and repair

### Fixed
- Fixed issues with missing or invalid configuration files
- Improved handling of API timeouts and connection issues
- Fixed dependency compatibility issues
- Added proper error handling for missing API keys
- Fixed validation of configuration values

## [0.1.0] - 2025-03-01

### Added
- Initial release
- Web command for querying Perplexity AI
- Gemini command for interacting with Google Gemini
- Repository analysis functionality
- GitHub automation tools
- Configuration management system 