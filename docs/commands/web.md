## Web Command

The `web` command performs intelligent web research using Perplexity AI, providing curated, up-to-date information from across the internet without requiring you to leave the terminal.

### Syntax

```bash
cursor-utils web [OPTIONS] QUERY
```

### Arguments

| Argument | Description | Required | Example |
|----------|-------------|----------|---------|
| `QUERY` | The search query to research | Yes | "How to implement JWT authentication in Express" |

### Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--model` | The Perplexity model to use | `sonar` | `--model sonar-reasoning` |
| `--format` | Output format (plain, markdown, json, rich) | `rich` | `--format markdown` |
| `--help` | Show command help | - | `--help` |

### Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `sonar` | Standard search model | General queries, basic information |
| `sonar-pro` | Enhanced search model | More comprehensive results |
| `sonar-reasoning` | Model with reasoning capabilities | Technical queries requiring analysis |
| `sonar-reasoning-pro` | Advanced reasoning model | Complex technical questions, in-depth analysis |

### Configuration

Before using the `web` command, you need to set up your Perplexity API key:

```bash
cursor-utils config set perplexity_api_key YOUR_PERPLEXITY_API_KEY
```

You can obtain an API key from [Perplexity API documentation](https://docs.perplexity.ai/).

### Examples

### Basic Usage

Simple web search:

```bash
cursor-utils web "What is Docker containerization?"
```

### Using Different Models

Use a specific model for more technical queries:

```bash
cursor-utils web --model sonar-reasoning "Compare microservices vs. monolithic architecture"
```

For complex topics requiring in-depth analysis:

```bash
cursor-utils web --model sonar-reasoning-pro "Explain OAuth 2.0 security considerations"
```

### Different Output Formats

Output in markdown format for documentation:

```bash
cursor-utils web --format markdown "Best practices for React state management"
```

Output in JSON format for programmatic use:

```bash
cursor-utils web --format json "List HTTP status codes and meanings"
```

### Use Cases

### Technical Research

- Researching programming concepts:
  ```bash
  cursor-utils web "How does Redux middleware work?"
  ```

- Finding best practices:
  ```bash
  cursor-utils web --model sonar-reasoning "Best practices for securing Node.js applications"
  ```

- Comparing technologies:
  ```bash
  cursor-utils web "Compare PostgreSQL vs. MongoDB for web applications"
  ```

### Problem Solving

- Debugging errors:
  ```bash
  cursor-utils web "Fix React useEffect infinite loop"
  ```

- Finding solutions to common issues:
  ```bash
  cursor-utils web "Resolve Docker networking between containers"
  ```

### Learning

- Understanding new technologies:
  ```bash
  cursor-utils web --model sonar-reasoning "Explain WebAssembly and its use cases"
  ```

- Following development trends:
  ```bash
  cursor-utils web "Latest developments in frontend frameworks 2023"
  ```

### Documentation and Examples

- Finding code examples:
  ```bash
  cursor-utils web "Example of using React context API with TypeScript"
  ```

- Looking up API documentation:
  ```bash
  cursor-utils web "How to use fetch API with async/await"
  ```

### Advanced Techniques

### Focused Queries

For more precise results, craft specific queries:

```bash
# Less effective
cursor-utils web "React"

# More effective
cursor-utils web "React custom hooks for form validation best practices"
```

### Combining with Other Tools

Pipe results to other commands for further processing:

```bash
# Extract code examples from the results
cursor-utils web --format plain "Python pandas dataframe filtering examples" | grep -A 20 "```python" | grep -B 20 "```"
```

Save results to a file for later reference:

```bash
cursor-utils web --format markdown "GraphQL schema design best practices" > graphql-best-practices.md
```

### Iterative Research

Build on previous research with follow-up queries:

```bash
# Start with a general topic
cursor-utils web "What is WebRTC?"

# Follow up with more specific questions
cursor-utils web "WebRTC NAT traversal techniques"
cursor-utils web "Implementing WebRTC signaling server in Node.js"
```

### Best Practices

1. **Be Specific**: Frame your query with specific details for better results
   ```bash
   # Less effective
   cursor-utils web "JavaScript testing"
   
   # More effective
   cursor-utils web "Unit testing React components with Jest and React Testing Library"
   ```

2. **Choose the Right Model**: Select the appropriate model for your query type
   - Use `sonar` for general information
   - Use `sonar-reasoning` or `sonar-reasoning-pro` for technical topics requiring analysis

3. **Consider Output Format**: Choose the format that best suits your needs
   - Use `markdown` for documentation
   - Use `rich` for interactive terminal viewing
   - Use `json` for programmatic processing

4. **Check Information Freshness**: Web information can become outdated
   ```bash
   cursor-utils web "Latest version of Node.js and its features"
   ```

5. **Verify Technical Solutions**: Always validate solutions in your specific context
   ```bash
   cursor-utils web "How to fix memory leaks in React applications"
   ```

### Troubleshooting

### API Key Issues

If you receive authentication errors:

```
Error: Invalid API key
```

Verify your API key is correctly set:

```bash
cursor-utils config get perplexity_api_key
```

If it's missing or incorrect, set it:

```bash
cursor-utils config set perplexity_api_key YOUR_PERPLEXITY_API_KEY
```

### Model Availability

If you receive an error about model availability:

```
Error: Model [model_name] is not available
```

Try using a different model:

```bash
cursor-utils web --model sonar "Your query"
```

### Rate Limiting

If you encounter rate limiting:

```
Error: Rate limit exceeded
```

Wait a few minutes and try again, or check your API usage limits.

### No Results Found

If your query returns limited or no results:

```
No relevant information found for your query
```

Try reformulating your query to be more specific or using different keywords. 