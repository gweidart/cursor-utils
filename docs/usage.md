# Usage Guide

This guide provides detailed information on how to use Cursor-Utils effectively for various development tasks.

However, **cursor-utils and its commands were designed to be used by your Cursor Agent's via terminal commands**. Nonetheless, i have included a fully featured, user friendly CLI interface. Therefore, you can run all cursor-utils commands manually yourself if you wish.


## Command-Line Interface

Cursor-Utils provides a consistent command-line interface with a focus on ease of use. You really only need to know a few phrases. Let your Cursor Agent worry about executing the commands and their arguments / options / parameters. while in an Agent Chat use the following phrases:

- `Ask Gemini`
- `Ask Perplexity`
- `Use cursor-utils <command>`

**Note:** core commands are:

- `repo`
- `gemini` (Ask Gemini)
- `project`
- `web` (Ask Perplexity)
- `github`
- `config`
- `update`

You will need to configure API keys for the commands that rely on external services before you can use them. We suggest you do this via the `config` command manually so that you dont expose your API key in your chat history.
## API Key Setup

To manually configure your API keys you can use the following workflow:

### Gemini API Key

```bash
cursor-utils config set gemini_api_key YOUR_GEMINI_API_KEY
```

### Perplexity API Key

```bash
cursor-utils config set perplexity_api_key YOUR_PERPLEXITY_API_KEY
```

### GitHub Token (Optional)

```bash
cursor-utils config set github_token YOUR_GITHUB_TOKEN
```

## Common Workflows


### Simply ask your Cursor Agent to:


```bash
Use cursor-utils repo https://github.com/user/repo to give me an overview of the repo then
Ask Gemini "Based on that repo analysis, how would I implement feature X?"
```

### Code Understanding

Quickly understand unfamiliar codebases:

```bash
# Analyze a local project
Use cursor-utils project /path/to/project "Explain the main components"

# Analyze a remote repository
Use cursor-utils repo https://github.com/organization/repo "How does the authentication system work?"
```

### Content Generation

Generate code, documentation, or explanations:

```bash
# Generate a Python function
Ask Gemini to "Write a Python function to calculate Fibonacci numbers"

# Create project documentation
Ask Gemini to "Generate API documentation for this endpoint: GET /api/users/:id"

# Explain complex concepts
Ask Gemini to "Explain OAuth 2.0 authorization flow"
```

### Technical Research

Find solutions and documentation:

```bash
# Research best practices
Ask Perplexity about "Best practices for React state management"

# Find documentation examples
Ask Perplexity about "How to implement pagination in GraphQL"

# Solve technical problems
Ask Perplexity about "Fix Docker container networking issues"
```

### GitHub Workflows

Manage GitHub repositories from the terminal:

```bash
# Get repository information
Use cursor-utils github repo --owner microsoft --repo vscode

# List open issues
Use cursor-utils github issues --owner microsoft --repo vscode

# Create an issue
Use cursor-utils github create-issue --owner your-username --repo your-repo --title "Bug: Application crashes"
```
## Combination workflows

Commands can be combined for powerful workflows:

simply ask your Cursor Agent to:

```bash
# Analyze a repository, then ask specific questions
Use cursor-utils repo https://github.com/user/repo to give me an overview of the repo then
Ask Gemini "Based on that repo analysis, how would I implement feature X?"
```

```bash
# Search for information, then apply to your project
Ask Perplexity to research best practices for API security then
use cursor-utils project to "audit my API endpoints for security issues"
```
### Command Specific Examples:

### Ask Gemini Command:

The `Ask Gemini` command allows your Cursor Agents to take full advantage of Gemini's industry leading *2 Million* token context window to query and collaborate back and forth allowing agents to iterate and refine thier answers before bringing you an even more polished result.

- Use the `--system` option to guide the model's behavior:
  ```bash
  Ask Gemini --system "You are a security expert" "Review this code for vulnerabilities"
  ```

- Adjust temperature for more or less creative outputs:
  ```bash
  Ask Gemini to --temperature 0.8 "Generate test cases for this function"
  ```

### Ask Perplexity Command:

- Use specific models for different types of queries:
  ```bash
  Ask Perplexity about --model sonar-reasoning "Compare serverless architectures"
  ```

### Project Command

- Limit the number of files for faster analysis:
  ```bash
  Use cursor-utils project . --max-files 20 "Find performance bottlenecks"
  ```

- Focus on specific directories:
  ```bash
  Use cursor-utils project ./src "Explain the data flow"
  ```

### Repo Command

- Limit the number of files for faster analysis:
  ```bash
  Use cursor-utils repo https://github.com/user/repo --max-files 20 "Find performance bottlenecks"
  ```

- Focus on specific directories:
  ```bash
  Use cursor-utils repo https://github.com/user/repo ./src "Explain the data flow"
  ```

- Use specific models for different types of queries:
  ```bash
  Use cursor-utils repo https://github.com/user/repo --model gemini-2.0-pro-exp "Find performance bottlenecks"
  ```

### GitHub Command

Collab with your Cursor Agents and let them take care of tasks you dont want to. Simply tell your Cursor Agent to use cursor-utils github to help you wwith pretty much anything & everything regarding GitHub repo mgmt:

```bash
Use cursor-utils github to help me create a new repo named "my-new-repo"
```

```bash
Use cursor-utils github to help me create a new issue in repo "my-repo"
```

```bash
Use cursor-utils github to help me create a new branch named "my-new-branch"
```

```bash
Use cursor-utils github to help me create a new pull request in repo "my-repo"
```

## Environment Variables

Cursor-Utils supports configuration via environment variables:

- `CURSOR_UTILS_GEMINI_API_KEY`: Google Gemini API key
- `CURSOR_UTILS_PERPLEXITY_API_KEY`: Perplexity API key
- `CURSOR_UTILS_GITHUB_TOKEN`: GitHub access token
- `CURSOR_UTILS_DEFAULT_FORMAT`: Default output format
- `CURSOR_UTILS_DEBUG`: Enable debug mode (set to 1)

Example:

```bash
export CURSOR_UTILS_DEFAULT_FORMAT=markdown
Ask Gemini to "Write a Python class for handling HTTP requests"
```

## Best Practices

1. **Be Specific with Queries**: More specific queries yield better results
   ```bash
   # Less effective
   Ask Perplexity "Docker"
   
   # More effective
   Ask Perplexity about "Docker multi-stage build optimization techniques"
   ```

2. **Choose the Right Model**: Different models have different strengths
   ```bash
   # For creative content
   Ask Gemini to --model gemini-2.0-pro-exp "Generate test scenarios"
   
   # For factual research
   Ask Perplexity about --model sonar-reasoning "Explain ACID properties"
   ```

3. **Use Output Redirection**: Save results to files when needed
   ```bash
   Ask Gemini to --format markdown "Write documentation for API endpoints" > api-docs.md
   ```

## Troubleshooting

### Rate Limiting

If you encounter rate limiting issues:

1. Check your API usage and limits
2. Implement delays between requests in scripts
3. Consider upgrading your API tier if available

### Slow Responses

For large repositories or complex queries:

1. Limit analysis scope with `--max-files`
2. Use more specific queries
3. Split complex queries into smaller, focused questions

### Authentication Issues

If experiencing authentication problems:

1. Verify API keys are correctly configured
2. Ensure keys haven't expired
3. Check your network connection and proxy settings

For persistent issues, refer to the [advanced documentation](https://gweidart.github.io/cursor-utils/) or check the GitHub repository for known issues and solutions. 