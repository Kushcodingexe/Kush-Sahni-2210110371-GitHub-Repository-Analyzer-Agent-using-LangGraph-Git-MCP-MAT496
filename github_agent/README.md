# GitHub Repository Analyzer Agent 🤖

An intelligent AI agent that analyzes GitHub repositories, investigates issues, answers questions about code, and proposes fixes using LangChain/LangGraph with specialized sub-agents.

## Features ✨

- **Issue Analysis**: Automatically analyze GitHub issues, extract stack traces, and find error origins
- **Repository Q&A**: Ask natural language questions about any GitHub repository
- **Error Research**: Search the web for known solutions and documentation
- **Code Investigation**: Navigate repository structure and trace dependencies
- **Multi-Agent Architecture**: Specialized sub-agents (RepoInvestigator, ErrorResearcher) for deep analysis

## Architecture 🏗️

```
Main Agent (Orchestrator)
├── RepoInvestigator → Analyzes code structure and locates files
├── ErrorResearcher → Searches for solutions and documentation
└── Context Files → Stores detailed findings for efficiency
```

## Installation 📦

### 1. Clone or navigate to project directory
```bash
cd github_agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API keys
Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Required API keys:
- **GitHub Token**: [Create personal access token](https://github.com/settings/tokens)
- **Tavily API Key**: [Get API key](https://tavily.com)
- **LLM API Key**: Either OpenAI or Anthropic
  - OpenAI: [Get API key](https://platform.openai.com/api-keys)
  - Anthropic: [Get API key](https://console.anthropic.com/)

### 4. Verify configuration
```bash
python -c "from src.config import Config; Config.print_config()"
```

## Usage 🚀

### Analyze a GitHub Issue
```bash
python -m src.main analyze-issue https://github.com/owner/repo/issues/123
```

### Ask about a Repository
```bash
python -m src.main ask owner/repo "How does the authentication work?"
```

### Interactive Mode
```bash
python -m src.main interactive
```

## Project Structure 📁

```
github_agent/
├── src/
│   ├── config.py              # Configuration management
│   ├── state.py               # Agent state schema
│   ├── tools/                 # Tool implementations
│   │   ├── github_tools.py    # GitHub API tools
│   │   ├── search_tools.py    # Web search tools
│   │   ├── file_tools.py      # File system tools
│   │   └── analysis_tools.py  # Code analysis tools
│   ├── agents/                # Sub-agent definitions
│   │   ├── repo_investigator.py
│   │   └── error_researcher.py
│   └── main.py                # Main orchestrator
├── tests/                     # Unit tests
├── examples/                  # Example scripts
├── requirements.txt           # Python dependencies
├── .env                       # Your API keys (not committed)
└── .env.example               # Template for API keys
```

## Configuration ⚙️

Edit `.env` to customize:

```bash
# Model Selection
DEFAULT_MODEL=anthropic:claude-sonnet-4-20250514
# or
DEFAULT_MODEL=openai:gpt-4o

# Agent Limits
MAX_CONCURRENT_RESEARCH_UNITS=3  # Parallel sub-agents
MAX_RESEARCHER_ITERATIONS=3      # Max search iterations
MAX_SEARCH_RESULTS=3             # Results per search
```

## Development Status 🚧

- ✅ Phase 1: Project Setup & Foundation
- ⏳ Phase 2: Core Tool Development
- ⏳ Phase 3: Sub-Agent Architecture
- ⏳ Phase 4: Main Agent Orchestration
- ⏳ Phase 5: Workflow Implementation
- ⏳ Phase 6: CLI Interface
- ⏳ Phase 7: Testing & Refinement
- ⏳ Phase 8: Documentation

## Example Output 📊

```markdown
# Investigation Report: Issue #123

## Issue Summary
Error in authentication module when using OAuth2 flow

## Stack Trace Analysis
- Error: KeyError: 'access_token'
- File: src/auth/oauth.py:45
- Function: process_callback()

## Code Investigation
Found 3 relevant files:
1. src/auth/oauth.py - Contains error location
2. src/config.py - OAuth configuration
3. tests/test_oauth.py - Related tests

## Research Findings
Similar issues found:
- Issue #87: Missing token validation
- StackOverflow solution for OAuth callbacks

## Proposed Fix
Add token validation before access...
```

## Contributing 🤝

This is a capstone project. Feel free to fork and extend!

## License 📄

MIT License

## Credits 🙏

Built with:
- [LangChain](https://github.com/langchain-ai/langchain) - Agent framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API wrapper
- [Tavily](https://tavily.com) - AI search API

---

Made with ❤️ for the LangChain community
