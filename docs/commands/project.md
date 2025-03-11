## Project Command

The `project` command analyzes local project code using Google's Gemini AI to provide insights, context, and answers about your codebase directly from the terminal.

### Syntax

```bash
cursor-utils project [OPTIONS] PROJECT_PATH QUERY
```

### Arguments

| Argument | Description | Required | Example |
|----------|-------------|----------|---------|
| `PROJECT_PATH` | Path to the project directory | Yes | `./` or `/path/to/project` |
| `QUERY` | The question or analysis request about the project | Yes | "Explain the main components" |

### Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--model` | The Gemini model to use | `gemini-1.5-pro` | `--model gemini-2.0-pro-exp` |
| `--max-files` | Maximum number of files to include in analysis | `30` | `--max-files 50` |
| `--ignore` | Patterns to ignore (comma-separated) | `.git,node_modules,dist` | `--ignore "build,*.log"` |
| `--format` | Output format (plain, markdown, json, rich) | `rich` | `--format markdown` |
| `--debug/--no-debug` | Enable/disable debug output | `--no-debug` | `--debug` |
| `--help` | Show command help | - | `--help` |

### Configuration

Before using the `project` command, you need to set up your Google Gemini API key:

```bash
cursor-utils config set gemini_api_key YOUR_GEMINI_API_KEY
```

You can obtain an API key from [Google AI Studio](https://ai.google.dev/).

### Examples

### Basic Usage

Analyze the current project:

```bash
cursor-utils project . "Explain the main architecture"
```

Analyze a specific project directory:

```bash
cursor-utils project /path/to/project "How does error handling work?"
```

### Using Different Models

Use a specific model for more complex analysis:

```bash
cursor-utils project . --model gemini-2.0-pro-exp "Identify potential security vulnerabilities"
```

### Limiting Analysis Scope

Limit the number of files analyzed:

```bash
cursor-utils project . --max-files 20 "Explain the authentication system"
```

Ignore specific paths or patterns:

```bash
cursor-utils project . --ignore "tests,*.spec.js,dist" "Analyze the core business logic"
```

### Output Formats

Save analysis results as markdown:

```bash
cursor-utils project . --format markdown "Document the API endpoints" > api-documentation.md
```

Get structured JSON output:

```bash
cursor-utils project . --format json "List all React components"
```

### Debug Mode

Enable debug output for troubleshooting:

```bash
cursor-utils project . --debug "Why is the application crashing on startup?"
```

### Use Cases

### Code Understanding

- Get a high-level overview of an unfamiliar codebase:
  ```bash
  cursor-utils project /path/to/new-project "Explain the main components and how they interact"
  ```

- Understand specific parts of a codebase:
  ```bash
  cursor-utils project . "How does the authentication system work?"
  ```

- Analyze data flow:
  ```bash
  cursor-utils project . "Trace the data flow from API request to database"
  ```

### Architecture Analysis

- Identify architectural patterns:
  ```bash
  cursor-utils project . "What design patterns are used in this codebase?"
  ```

- Analyze dependency structure:
  ```bash
  cursor-utils project . "Map out the dependency graph between modules"
  ```

- Review system architecture:
  ```bash
  cursor-utils project . "Evaluate the microservice architecture and suggest improvements"
  ```

### Code Quality and Improvements

- Identify potential issues:
  ```bash
  cursor-utils project . "Find potential performance bottlenecks"
  ```

- Suggest improvements:
  ```bash
  cursor-utils project . "How can error handling be improved?"
  ```

- Review security:
  ```bash
  cursor-utils project . "Identify security vulnerabilities in the authentication system"
  ```

### Documentation

- Generate documentation:
  ```bash
  cursor-utils project . --format markdown "Document the public API endpoints" > api-docs.md
  ```

- Create architecture diagrams:
  ```bash
  cursor-utils project . "Create a component diagram for the frontend"
  ```

- Document workflows:
  ```bash
  cursor-utils project . "Document the user registration flow"
  ```

### Advanced Techniques

### Focused Analysis

Focus on specific directories or components:

```bash
# Analyze just the backend code
cursor-utils project ./backend "Explain the database schema and relationships"

# Focus on a specific feature
cursor-utils project ./src/features/authentication "Review the authentication implementation"
```

### Comparative Analysis

Compare different parts of the codebase:

```bash
cursor-utils project . "Compare the user and admin authentication flows"
```

### Sequential Analysis

Build up understanding through sequential queries:

```bash
# Start with high-level overview
cursor-utils project . "Provide an overview of the main components"

# Then dig deeper into specific areas
cursor-utils project . "Explain the data access layer in detail"
cursor-utils project . "How is caching implemented in the data access layer?"
```

### Integration with Development Workflow

Use during code reviews:

```bash
git diff main... | cursor-utils project . "Review these changes and suggest improvements"
```

Use for onboarding:

```bash
cursor-utils project . "Create an onboarding guide for new developers" > onboarding.md
```

### Best Practices

1. **Start with Broad Questions**: Get a high-level overview before diving into details
   ```bash
   cursor-utils project . "What are the main components and their responsibilities?"
   ```

2. **Be Specific with Follow-ups**: Ask targeted questions for deeper understanding
   ```bash
   cursor-utils project . "How does the JWT authentication validation work?"
   ```

3. **Limit Scope When Necessary**: For large projects, focus on specific areas
   ```bash
   cursor-utils project ./src/core --max-files 15 "Explain the core business logic"
   ```

4. **Use for Documentation**: Generate documentation as you explore the codebase
   ```bash
   cursor-utils project . --format markdown "Document the state management approach" > state-management.md
   ```

5. **Combine with Manual Review**: Use AI analysis as a complement to manual code review
   ```bash
   # AI overview first
   cursor-utils project ./src/auth "Explain the authentication system"
   
   # Then manual review of key files identified by the AI
   ```

6. **Save Analysis Results**: Preserve insights for future reference
   ```bash
   cursor-utils project . --format markdown "Architectural overview" > architecture.md
   ```

### Performance Considerations

### Large Codebases

For large codebases, consider:

1. **Increasing max-files limit** for broader coverage:
   ```bash
   cursor-utils project . --max-files 100 "Provide a comprehensive overview"
   ```

2. **Focusing on specific directories** for targeted analysis:
   ```bash
   cursor-utils project ./src/core "Analyze the core modules"
   ```

3. **Using ignore patterns** to exclude irrelevant files:
   ```bash
   cursor-utils project . --ignore "tests,*.test.js,node_modules,build,dist" "Analyze business logic"
   ```

### Troubleshooting

### API Key Issues

If you receive authentication errors:

```
Error: Invalid API key
```

Verify your API key is correctly set:

```bash
cursor-utils config get gemini_api_key
```

If it's missing or incorrect, set it:

```bash
cursor-utils config set gemini_api_key YOUR_GEMINI_API_KEY
```

### Project Path Issues

If the project path is not found:

```
Error: Project path not found
```

Verify the path exists and is accessible:

```bash
ls -la /path/to/project
```

### Context Size Limitations

If you receive an error about context size:

```
Error: Context size limit exceeded
```

Try reducing the number of files analyzed:

```bash
cursor-utils project . --max-files 10 "Your query"
```

Or focus on a specific subdirectory:

```bash
cursor-utils project ./src/specific-feature "Your query"
```

### Vague or Confusing Results

If the analysis results are vague or confusing:

1. Try being more specific with your query
2. Use debug mode to see what files are being analyzed:
   ```bash
   cursor-utils project . --debug "Your query"
   ```
3. Adjust the ignore patterns to focus on relevant files 