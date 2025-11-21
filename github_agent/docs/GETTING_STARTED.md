# Getting Started with GitHub Repository Analyzer Agent

A quick guide to get you up and running with the agent in 5 minutes.

---

## Prerequisites

- Python 3.10 or higher
- Git installed
- GitHub account (for API token)
- OpenAI or Anthropic API key
- Tavily API key (free tier available)

---

## Quick Setup

### 1. Install Dependencies

```bash
cd github_agent
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your keys:
```bash
# Required
GITHUB_TOKEN=ghp_your_github_token_here
TAVILY_API_KEY=tvly-your_tavily_key_here

# Choose one LLM provider
OPENAI_API_KEY=sk-your_openai_key_here
# OR
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here

# Set your preferred model
DEFAULT_MODEL=openai:gpt-4o-mini
```

**Getting API Keys:**
- [GitHub Token](https://github.com/settings/tokens) - Select "repo" scope
- [Tavily API](https://tavily.com) - Free tier: 1000 searches/month
- [OpenAI API](https://platform.openai.com/api-keys) - Pay-per-use
- [Anthropic API](https://console.anthropic.com/) - Alternative to OpenAI

### 3. Install CLI (Optional)

```bash
pip install -e .
```

This makes `github-agent` command available globally.

### 4. Verify Setup

```bash
python -c "from src.config import Config; Config.print_config()"
```

Expected output:
```
🔧 Configuration:
  OpenAI API Key: ✅ sk-p...
  GitHub Token: ✅ ghp_...
  Tavily API Key: ✅ tvly...
  ...
✅ Configuration is valid!
```

---

## First Steps

### Try Interactive Mode

```bash
github-agent interactive
```

Or without installation:
```bash
python -m src.main interactive
```

**Try these commands:**
```
> What is the openai/openai-python repository?
> Find the ChatCompletion class in openai/openai-python
> exit
```

### Analyze a Repository

```bash
github-agent ask openai/openai-python "How does the authentication work?"
```

### Analyze an Issue

```bash
github-agent issue https://github.com/owner/repo/issues/123
```

---

## Common Use Cases

### 1. Understanding a New Codebase

```python
from src.main import ask_about_repository

result = ask_about_repository(
    "fastapi/fastapi",
    "Explain the project structure"
)
```

### 2. Debugging an Issue

```python
from src.main import analyze_issue

result = analyze_issue(
    "https://github.com/langchain-ai/langchain/issues/1234"
)
```

### 3. Finding Specific Code

```bash
github-agent ask langchain-ai/langchain "Where is the ChatOpenAI class defined?"
```

---

## How It Works

The agent uses a multi-agent architecture:

1. **Main Agent** - Coordinates the analysis
2. **RepoInvestigator** - Searches code and repository structure
3. **ErrorResearcher** - Finds solutions online
4. **Context Files** - Stores detailed findings

When you ask a question:
1. Agent creates a research plan (TODOs)
2. Delegates to specialized sub-agents
3. Gathers and synthesizes findings
4. Provides comprehensive answer

---

## Configuration Tips

### Use a Different Model

Edit `.env`:
```bash
# GPT-4o (more capable, more expensive)
DEFAULT_MODEL=openai:gpt-4o

# Claude Sonnet (good balance)
DEFAULT_MODEL=anthropic:claude-sonnet-4-20250514

# GPT-4o-mini (faster, cheaper)  
DEFAULT_MODEL=openai:gpt-4o-mini
```

### Adjust Agent Limits

Control how thorough the research is:
```bash
MAX_CONCURRENT_RESEARCH_UNITS=3  # Run 3 sub-agents in parallel
MAX_RESEARCHER_ITERATIONS=3      # Max search attempts
MAX_SEARCH_RESULTS=5             # Results per search
```

Higher values = more thorough but slower and more expensive.

---

## Troubleshooting

### "GitHub API rate limit exceeded"

Wait a few minutes or:
- Use a GitHub Personal Access Token (higher limits)
- Reduce `MAX_SEARCH_RESULTS` in `.env`

### "Invalid repository name"

Use format: `owner/repo`
- ✅ `openai/openai-python`
- ❌ `openai-python`
- ❌ `https://github.com/openai/openai-python`

### "Agent not responding"

- Check internet connection
- Verify API keys are valid
- Check LangSmith traces for errors (if enabled)

### "Command not found: github-agent"

Run installation:
```bash
pip install -e .
```

Or use Python module directly:
```bash
python -m src.main [command]
```

---

## Next Steps

- [API Reference](API.md) - All available tools
- [Common Tasks](COMMON_TASKS.md) - Example workflows
- [Troubleshooting](TROUBLESHOOTING.md) - Detailed solutions
- [Architecture](ARCHITECTURE.md) - How it works

---

## Need Help?

- Check [examples/](../examples/) for code samples
- See existing [tests/](../tests/) for usage patterns
- Review [TESTING_GUIDE.md](../TESTING_GUIDE.md) for testing

**Happy analyzing!** 🚀
