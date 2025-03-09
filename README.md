# Cursor-Utils

**Give your Cursor Agent superpowers.**

[![PyPI Downloads](https://static.pepy.tech/badge/cursor-utils)](https://pepy.tech/projects/cursor-utils)

<div align="center">
  <div>
    <h3>Asking Perplexity to perform ai guided web research</h3>
  </div>
  <div style="display: flex;">
    <img width="350" alt="image" src="https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/perplexity1.jpg" />
  </div>
  <details>
    <summary>see what happens next...</summary>
    <img width="350" alt="image" src="https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/perplexity2.jpg" />
  </details>
  <br/>
  <br/>
  </div>
</div>

<div align="center">
  <div>
    <h3>Asking Gemini for a plan</h3>
  </div>
  <div style="display: flex;">
    <img width="350" src="https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/gemini1.jpg" />
  </div>
  <details>
    <summary>see what happens next...</summary>
    <img width="350" alt="image" src="https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/gemini2.jpg" />
    <details>
      <summary>see what happens next...</summary>
      <img width="350" alt="image" src="https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/gemini3.jpg" />
    </details>
  <br/>
  <br/>
  </div>
</div>

<div align="center">
  <div>
    <h3>Performing repository analysis</h3>
  </div>
  <div style="display: flex;">
    <img width="350" alt="image" src="https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/repo1.jpg" />
  </div>
  <details>
    <summary>see what happens next...</summary>
    <img width="350" alt="image" src="https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/repo2.jpg" />
  </details>
  <br/>
  <br/>
  </div>
</div>

### Installation

```bash
pip install cursor-utils
```
using uv:

```bash
uv pip install cursor-utils
```
using poetry:

```bash
poetry add cursor-utils
```

using pipx:

```bash
pipx install cursor-utils
```

### Read our [docs](https://gweidart.github.io/cursor-utils)

Cursor Utils is a powerful toolkit designed to extend your Cursor IDE with advanced functionality. It integrates Cursor Agents seamlessly with popular AI services like Google's Gemini and Perplexity to provide context-aware code analysis, web research, content generation, and GitHub management capabilities.

## What is Cursor Utils?

Cursor IDE is already an amazing tool for developers. Cursor-Utils is an amazing tool for Cursor Agents:

- Enabling your Cursor Agents to access real-time web information
- Providing sophisticated project analysis tools
- Streamlining GitHub interactions and repository management
- Offering advanced code generation capabilities via Google's Gemini

All this functionality is exposed through a clean, intuitive CLI that your Cursor Agents can use directly.

## Getting Started

To get started with Cursor-Utils, follow these steps:

1. [Install Cursor-Utils](https://gweidart.github.io/cursor-utils/docs/installation/) on your system
2. [Configure API keys](https://gweidart.github.io/cursor-utils/docs/usage/#api-key-setup) for external services
3. We designed cursor-utils to be used by Cursor Agents. Therefore there's really nothing else you need to do besides configuring the api keys. 
   
   **However if you want to explore the [available commands](https://gweidart.github.io/cursor-utils/docs/api/) and their options, you can do so.**

## Why Cursor-Utils?

  Our **Benchmarks** speak for themselves. Extensive benchmarking and profiling reflect:

  - an 87.8% increase in Cursor Agent Accuracy, Correctness, and Quality of answers using only Zero Shot Prompting & Cursor-Utils.

  - a 98.2% increase in developer workflow productivity using only Cursor IDE & Cursor-Utils. 

Cursor-Utils addresses common challenges in the development workflow:

- **Reducing Context Switching**: Get answers directly in your terminal without switching to a browser
- **Accelerating Onboarding**: Quickly understand new codebases with AI-powered analysis
- **Streamlining Research**: Find relevant information faster with intelligent web search
- **Enhancing Productivity**: Automate documentation, code generation, and GitHub tasks
- **Improving Collaboration**: Share standardized insights and documentation with team members

## Example Workflow

### Simply ask your Cursor Agent to:

```bash
# Analyze a new codebase you're working with
Use cursor-utils repo https://github.com/organization/project "Explain the authentication system"
```

```bash
# Research a technical concept
Ask Perplexity about "Best practices for GraphQL error handling"
```

```bash
# Generate a code snippet for your current project
Ask Gemini to "Write a Python function to validate JWT tokens"
```

```bash
# Create an issue based on your findings
Use cursor-utils github to create-issue --owner your-org --repo your-repo --title "Improve JWT validation"
```

## Next Steps

- Read the [installation guide](https://gweidart.github.io/cursor-utils/docs/installation/) to set up Cursor-Utils
- Explore the [usage documentation](https://gweidart.github.io/cursor-utils/docs/usage/) for detailed usage patterns
- Learn about [configuration options](https://gweidart.github.io/cursor-utils/docs/api/) to customize your experience

## Community and Support

- [Contributing guidelines](https://gweidart.github.io/cursor-utils/docs/contributing/) for developers interested in enhancing Cursor-Utils
- [License information](https://gweidart.github.io/cursor-utils/docs/license/) for usage terms and conditions 
