# Cursor-Utils

### **_Give your Cursor Agents superpowers._**

[Install Cursor Utils :simple-pypi:](installation.md#){ .md-button .copy-js data-clipboard-text="pip install cursor-utils" }


## What is Cursor Utils?

[Cursor](https://www.cursor.com/) is already an amazing tool for developers. [Cursor-Utils](https://github.com/gweidart/cursor-utils) extends your existing agents with new skills and advanced features via:

<div class="grid cards" markdown>

-   :simple-googlegemini:{ .lg .middle } __Google Gemini__

    ---

    2M token ENTIRE codebase contextual memory. 
    Grounding & reasoning.

    [:octicons-arrow-right-24: Gemini](#)

-   :simple-perplexity:{ .lg .middle } __Perplexity__

    ---

    AI guided deep web research, without the 
    risk of hallucinations.

    [:octicons-arrow-right-24: Perplexity](#)

-   :material-source-repository-multiple:{ .lg .middle } __Local & Remote Repo Analysis__

    ---

    Complex & Context aware agent codebase analysis
    and dev workflow.

    [:octicons-arrow-right-24: Repo](#)

-   :simple-github:{ .lg .middle } __GitHub__

    ---

    Agentic & autonomous Github repository mgmt.
    and maint.

    [:octicons-arrow-right-24: GitHub](#)

</div>


All of this functionality is exposed through a clean, intuitive CLI __*designed to be used by your existing Cursor Agents*__.

### Asking Perplexity to perform ai guided web research

???+ example
    ![image](https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/perplexity1.jpg)

### _*See what happens next...*_

??? example
    ![image](https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/perplexity2.jpg)

### Asking Gemini for a plan

??? example
    ![image](https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/gemini1.jpg)

    ![image](https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/gemini2.jpg)

    ![image](https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/gemini3.jpg)

### Performing repository analysis

??? example
    ![image](https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/repo1.jpg)

    ![image](https://raw.githubusercontent.com/gweidart/cursor-utils/refs/heads/main/assets/repo2.jpg)

## Getting Started

To get started with Cursor-Utils, follow these steps:

???+ note

    We designed cursor-utils to be used by Cursor Agents. Therefore there's really nothing else you need to do besides configuring the api keys. 
   
    **However if you want to explore the [available commands](api/index.md) and their options, you can do so.**

1. Read the [installation guide](installation.md) to set up Cursor-Utils
2. Explore the [usage documentation](usage.md) for detailed usage patterns
3. Learn about [configuration options](commands/config.md) to customize your experience

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

## Community and Support

- [Contributing guidelines](contributing.md) for developers interested in enhancing Cursor-Utils
- [License information](license.md) for usage terms and conditions 