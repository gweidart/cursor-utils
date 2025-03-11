## Gemini Command

The `gemini` command generates content using Google's Gemini AI models, providing powerful AI-assisted capabilities for code generation, explanations, and more.

### Syntax

```bash
cursor-utils gemini [OPTIONS] PROMPT
```

### Arguments

| Argument | Description | Required | Example |
|----------|-------------|----------|---------|
| `PROMPT` | The text prompt for Gemini to respond to | Yes | "Explain how promises work in JavaScript" |

### Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--model` | The Gemini model to use | `gemini-1.5-pro` | `--model gemini-2.0-flash` |
| `--temperature` | Sampling temperature (0.0-1.0) | `0.7` | `--temperature 0.9` |
| `--max-tokens` | Maximum tokens to generate | Based on model | `--max-tokens 1000` |
| `--system` | System instruction for guiding model behavior | None | `--system "You are a Python expert"` |
| `--format` | Output format (plain, markdown, json, rich) | `rich` | `--format markdown` |
| `--help` | Show command help | - | `--help` |

### Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `gemini-1.5-pro` | Powerful general-purpose model | Default for most use cases |
| `gemini-2.0-pro-exp` | Experimental pro model | Complex reasoning, cutting-edge |
| `gemini-2.0-flash` | Faster, more efficient model | Quick responses, simpler tasks |
| `gemini-2.0-flash-exp` | Experimental flash model | Testing latest capabilities |
| `gemini-2.0-flash-thinking-exp` | Enhanced thinking capabilities | Step-by-step reasoning |

### Configuration

Before using the `gemini` command, you need to set up your Google Gemini API key:

```bash
cursor-utils config set gemini_api_key YOUR_GEMINI_API_KEY
```

You can obtain an API key from [Google AI Studio](https://ai.google.dev/).

### Examples

### Basic Usage

Generate a simple response:

```bash
cursor-utils gemini "Explain quantum computing in simple terms"
```

### Code Generation

Generate a Python function:

```bash
cursor-utils gemini "Write a Python function to check if a string is a palindrome"
```

### Using Different Models

Use a specific model:

```bash
cursor-utils gemini --model gemini-2.0-flash "Write a JavaScript function to sort an array"
```

### Controlling Temperature

Lower temperature for more focused, deterministic responses:

```bash
cursor-utils gemini --temperature 0.2 "List 5 best practices for RESTful API design"
```

Higher temperature for more creative, varied responses:

```bash
cursor-utils gemini --temperature 0.9 "Generate unique names for a fantasy game"
```

### Using System Instructions

Guide the model's behavior with system instructions:

```bash
cursor-utils gemini --system "You are a security expert specialized in code review" "Review this code for vulnerabilities: ..."
```

```bash
cursor-utils gemini --system "You are a technical writer who explains complex concepts clearly" "Explain OAuth 2.0 authorization flow"
```

### Different Output Formats

Output in markdown format:

```bash
cursor-utils gemini --format markdown "Create documentation for a REST API endpoint"
```

Output in JSON format:

```bash
cursor-utils gemini --format json "List common HTTP status codes with descriptions"
```

### Limiting Output Length

Specify maximum token generation:

```bash
cursor-utils gemini --max-tokens 500 "Summarize the history of artificial intelligence"
```

## Use Cases

### Code Development

- Generate function implementations
  ```bash
  cursor-utils gemini "Write a Python function to paginate API results"
  ```

- Write test cases
  ```bash
  cursor-utils gemini "Create unit tests for this function: def add(a, b): return a + b"
  ```

- Debug code
  ```bash
  cursor-utils gemini "Debug this code: for i in range(10): print(i[0])"
  ```

### Documentation

- Generate technical documentation
  ```bash
  cursor-utils gemini --format markdown "Write documentation for a database connection class"
  ```

- Create usage examples
  ```bash
  cursor-utils gemini "Show examples of using the requests library in Python"
  ```

### Learning

- Explain concepts
  ```bash
  cursor-utils gemini "Explain CORS and why it's important for web security"
  ```

- Compare technologies
  ```bash
  cursor-utils gemini "Compare MongoDB and PostgreSQL for web applications"
  ```

### Advanced Techniques

### Chaining Prompts

Building on previous responses for iterative development:

```bash
# First, generate a basic implementation
cursor-utils gemini "Write a Python function to convert Celsius to Fahrenheit" > temperature.py

# Then, improve the implementation
cursor-utils gemini "Improve this function to include error handling and type checking: $(cat temperature.py)" > temperature_improved.py
```

### Structured Output

Request structured data for programmatic use:

```bash
cursor-utils gemini --format json "Convert this email to JSON with fields for sender, date, subject, and body: ..."
```

### Redirecting Output

Save output to files:

```bash
cursor-utils gemini --format markdown "Write documentation for GraphQL mutations" > graphql-mutations.md
```

### Best Practices

1. **Be Specific**: More specific prompts yield better results
   ```bash
   # Less effective
   cursor-utils gemini "Write a function"
   
   # More effective
   cursor-utils gemini "Write a Python function that validates email addresses using regex"
   ```

2. **Consider Model Selection**: Choose the appropriate model for your task
   - Use `gemini-1.5-pro` for complex reasoning, detailed responses
   - Use `gemini-2.0-flash` for quick, simple tasks

3. **Tune Temperature**: Adjust based on your need for creativity vs. determinism
   - Lower temperature (0.1-0.4) for factual, consistent responses
   - Higher temperature (0.7-0.9) for creative, varied responses

4. **Use System Instructions**: Guide the model's behavior using system instructions
   ```bash
   cursor-utils gemini --system "You are a Python expert who writes well-documented, PEP 8 compliant code" "..."
   ```

5. **Format for Readability**: Use markdown for documentation, rich for interactive use
   ```bash
   cursor-utils gemini --format markdown "Generate a tutorial on async/await in JavaScript"
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

### Model Availability

If you receive an error about model availability:

```
Error: Model [model_name] is not available
```

Try using a different model:

```bash
cursor-utils gemini --model gemini-1.5-pro "Your prompt"
```

### Rate Limiting

If you encounter rate limiting:

```
Error: Rate limit exceeded
```

Wait a few minutes and try again, or check your API usage limits.

### Timeout Issues

For complex prompts that time out:

```
Error: Request timed out
```

Try simplifying your prompt or breaking it into smaller parts. 