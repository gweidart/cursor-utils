## Repo Command

The `repo` command analyzes and queries remote code repositories using Google's Gemini AI, allowing you to understand, explore, and extract insights from any public Git repository without cloning it manually.

### Syntax

```bash
cursor-utils repo [OPTIONS] REPO_URL QUERY
```

### Arguments

| Argument | Description | Required | Example |
|----------|-------------|----------|---------|
| `REPO_URL` | URL of the Git repository | Yes | `https://github.com/org/repo` |
| `QUERY` | The question or analysis request about the repository | Yes | "Explain the architecture" |

### Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--branch` | The branch to analyze | `main` or `master` | `--branch develop` |
| `--depth` | The clone depth (number of commits) | `1` | `--depth 10` |
| `--max-files` | Maximum number of files to include in analysis | `30` | `--max-files 50` |
| `--model` | The Gemini model to use | `gemini-1.5-pro` | `--model gemini-2.0-pro-exp` |
| `--ignore` | Patterns to ignore (comma-separated) | `.git,node_modules,dist` | `--ignore "build,*.log"` |
| `--format` | Output format (plain, markdown, json, rich) | `rich` | `--format markdown` |
| `--debug/--no-debug` | Enable/disable debug output | `--no-debug` | `--debug` |
| `--help` | Show command help | - | `--help` |

### Configuration

Before using the `repo` command, you need to set up your Google Gemini API key:

```bash
cursor-utils config set gemini_api_key YOUR_GEMINI_API_KEY
```

You can obtain an API key from [Google AI Studio](https://ai.google.dev/).

### Examples

### Basic Usage

Analyze a GitHub repository:

```bash
cursor-utils repo https://github.com/facebook/react "Explain the core architecture"
```

Analyze a GitLab repository:

```bash
cursor-utils repo https://gitlab.com/organization/project "How does error handling work?"
```

### Specifying Branches

Analyze a specific branch:

```bash
cursor-utils repo https://github.com/facebook/react --branch experimental "What are the new experimental features?"
```

### Clone Depth

Adjust clone depth for repositories with relevant history:

```bash
cursor-utils repo https://github.com/tensorflow/tensorflow --depth 5 "How has the API evolved recently?"
```

### Limiting Analysis Scope

Limit the number of files analyzed:

```bash
cursor-utils repo https://github.com/kubernetes/kubernetes --max-files 50 "Explain the core scheduling algorithm"
```

Ignore specific files or patterns:

```bash
cursor-utils repo https://github.com/django/django --ignore "docs,tests,*.md" "Explain the ORM implementation"
```

### Output Formats

Save analysis results as markdown:

```bash
cursor-utils repo https://github.com/expressjs/express --format markdown "Document the middleware system" > express-middleware.md
```

Get structured JSON output:

```bash
cursor-utils repo https://github.com/vuejs/vue --format json "List key components and their purposes"
```

### Using Different Models

Use a specific model for more complex analysis:

```bash
cursor-utils repo https://github.com/rust-lang/rust --model gemini-2.0-pro-exp "Explain the ownership system"
```

### Debug Mode

Enable debug output for troubleshooting:

```bash
cursor-utils repo https://github.com/pytorch/pytorch --debug "How does autograd work?"
```

### Use Cases

### Open Source Exploration

- Understand popular frameworks:
  ```bash
  cursor-utils repo https://github.com/angular/angular "Explain the dependency injection system"
  ```

- Explore new libraries before adopting:
  ```bash
  cursor-utils repo https://github.com/new-library/new-library "What are the main features and limitations?"
  ```

- Learn best practices from well-maintained projects:
  ```bash
  cursor-utils repo https://github.com/pallets/flask "Explain the extension system and patterns"
  ```

### Dependency Evaluation

- Evaluate dependencies before integration:
  ```bash
  cursor-utils repo https://github.com/dependency/project "What is the API stability commitment?"
  ```

- Assess security practices:
  ```bash
  cursor-utils repo https://github.com/auth-library/library "Review the security implementation"
  ```

- Check implementation quality:
  ```bash
  cursor-utils repo https://github.com/utility/library "Analyze code quality and test coverage"
  ```

### Learning and Research

- Study implementation techniques:
  ```bash
  cursor-utils repo https://github.com/redis/redis "How does the event loop work?"
  ```

- Understand algorithms:
  ```bash
  cursor-utils repo https://github.com/tensorflow/tensorflow "Explain the gradient descent implementation"
  ```

- Research architecture patterns:
  ```bash
  cursor-utils repo https://github.com/nestjs/nest "Explain the module system and architecture"
  ```

### Technical Decision Making

- Compare implementations:
  ```bash
  cursor-utils repo https://github.com/ORG1/implementation "How is feature X implemented?"
  cursor-utils repo https://github.com/ORG2/implementation "How is feature X implemented?"
  ```

- Evaluate migration paths:
  ```bash
  cursor-utils repo https://github.com/framework/next-version "What breaking changes are in this version?"
  ```

### Advanced Techniques

### Focused Analysis

Target specific directories for focused analysis:

```bash
# Analyze just the authentication module
cursor-utils repo https://github.com/org/repo --branch main "Analyze the code in src/auth directory"
```

### Comparative Analysis

Compare different repositories:

```bash
# Compare ORM implementations
cursor-utils repo https://github.com/sequelize/sequelize "Explain the query building system"
cursor-utils repo https://github.com/typeorm/typeorm "Explain the query building system"
```

Compare different versions or branches:

```bash
# Compare approaches in different branches
cursor-utils repo https://github.com/org/repo --branch main "How is feature X implemented?"
cursor-utils repo https://github.com/org/repo --branch experimental "How is feature X implemented?"
```

### Sequential Deep Dives

Build understanding through sequential queries:

```bash
# Start with architecture overview
cursor-utils repo https://github.com/nestjs/nest "Provide an architectural overview"

# Dive deeper into specific areas
cursor-utils repo https://github.com/nestjs/nest "Explain the dependency injection system in detail"
cursor-utils repo https://github.com/nestjs/nest "How does the middleware system work?"
```

### Integration with Development Workflow

Use for research during architectural decisions:

```bash
# Research pattern implementations before deciding approach
cursor-utils repo https://github.com/well-known/implementation "How is the repository pattern implemented?"
```

Use for learning before contribution:

```bash
# Understand contribution guidelines and patterns
cursor-utils repo https://github.com/project/to-contribute "Explain the contribution workflow and standards"
```

### Best Practices

1. **Be Specific with Your Queries**: More specific questions yield better results
   ```bash
   # Less effective
   cursor-utils repo https://github.com/org/repo "How does it work?"
   
   # More effective
   cursor-utils repo https://github.com/org/repo "How does the authentication system handle JWT validation?"
   ```

2. **Limit Analysis Scope**: For large repositories, focus on specific areas
   ```bash
   cursor-utils repo https://github.com/kubernetes/kubernetes --max-files 40 "Explain just the scheduler component"
   ```

3. **Choose Appropriate Branch**: Analyze the relevant branch for your needs
   ```bash
   # For stable code
   cursor-utils repo https://github.com/org/repo --branch main "Explain the core functionality"
   
   # For upcoming features
   cursor-utils repo https://github.com/org/repo --branch develop "What new features are being implemented?"
   ```

4. **Save Insights for Reference**: Save valuable analyses for future reference
   ```bash
   cursor-utils repo https://github.com/important/dependency --format markdown "Document the API" > dependency-api.md
   ```

5. **Follow Up with Specific Questions**: Start broad, then ask targeted questions
   ```bash
   # First query
   cursor-utils repo https://github.com/org/repo "What are the main components?"
   
   # Follow-up query
   cursor-utils repo https://github.com/org/repo "Explain how the caching system works in detail"
   ```

6. **Compare with Documentation**: Validate analysis against official documentation
   ```bash
   cursor-utils repo https://github.com/org/repo "What does the code actually do vs. what the documentation claims?"
   ```

### Performance Considerations

### Repository Size

For large repositories:

1. **Limit clone depth** to avoid downloading full history:
   ```bash
   cursor-utils repo https://github.com/large/repo --depth 1 "Analyze the core architecture"
   ```

2. **Limit the number of files** analyzed:
   ```bash
   cursor-utils repo https://github.com/large/repo --max-files 30 "Focus on the authentication system"
   ```

3. **Ignore irrelevant directories**:
   ```bash
   cursor-utils repo https://github.com/large/repo --ignore "docs,examples,tests,*.md" "Analyze core functionality"
   ```

### Network Considerations

1. **Enable debug mode** to monitor cloning progress:
   ```bash
   cursor-utils repo https://github.com/org/repo --debug "Your query"
   ```

2. **Consider caching** for repositories you analyze frequently:
   Repositories are temporarily cached, which speeds up subsequent analyses of the same repository.

### Troubleshooting

### Repository Access Issues

If you have trouble accessing a repository:

```
Error: Failed to clone repository
```

Verify:
1. The repository URL is correct
2. The repository is public or you have access
3. Your network connection can reach the Git server

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

### Context Size Limitations

If you receive an error about context size:

```
Error: Context size limit exceeded
```

Try reducing the number of files analyzed:

```bash
cursor-utils repo https://github.com/org/repo --max-files 15 "Your query"
```

### Branch Not Found

If the specified branch doesn't exist:

```
Error: Branch not found
```

Check available branches and use the correct name:

```bash
git ls-remote --heads https://github.com/org/repo
cursor-utils repo https://github.com/org/repo --branch correct-branch-name "Your query"
```

### Vague or Confusing Results

If the analysis results are vague or confusing:

1. Try being more specific with your query
2. Use debug mode to see what files are being analyzed:
   ```bash
   cursor-utils repo https://github.com/org/repo --debug "Your query"
   ```
3. Adjust the ignore patterns to focus on relevant files 