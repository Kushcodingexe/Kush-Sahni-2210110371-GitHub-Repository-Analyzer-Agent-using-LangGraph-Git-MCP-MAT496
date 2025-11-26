# MAT496 Capstone Project - GitHub Repository Analyzer Agent

## Overview of MAT496

In this course, we learned about Langgraph, which is a really useful tool for building apps that can process unstructured text, find the information we need, and present it in whatever format we want. The main topics we covered were:

- Prompting
- Structured Output
- Semantic Search
- Retrieval Augmented Generation (RAG)
- Tool calling LLMs & MCP
- Langgraph: State, Nodes, Graph

We also learned that Langsmith is helpful for debugging Langgraph code.

---

## Capstone Project Objective

The capstone project gives us a chance to practice all the major topics from the course and also show some creativity. The idea is to think about problems that weren't solvable before but are now possible with what we learned. For example, LLMs can analyze different types of news, build legal assistants, or help with anything that requires a lot of reading.

---

## Project Report

### Title: GitHub Repository Analyzer Agent using LangGraph

### Overview

This project is an AI agent that analyzes GitHub repositories and issues. It can investigate codebases, research errors, answer questions about repositories, and provide fix recommendations. The agent uses LangGraph for orchestration and delegates tasks to specialized sub-agents (RepoInvestigator and ErrorResearcher) for focused research.

### Reason for Picking This Project

This project fits perfectly with the course content because it uses:
- **Prompting**: Custom prompts for main agent and sub-agents to guide their behavior
- **Structured Output**: Pydantic models for state management and tool inputs
- **RAG**: Fetching repository files and issue details to provide context for analysis
- **Tool Calling**: 16+ tools for GitHub API, web search, file system, and analysis
- **Langgraph**: State machine with nodes for agent reasoning, tool execution, and sub-agent delegation
- **MCP**: GitHub MCP for repository access, FileSystem MCP for local operations
- **Langsmith**: Used for debugging and tracing agent execution

Basically, it combines everything we learned into one project that solves a real problem - helping developers understand and debug code.

### Plan

- [DONE] **Step 1**: Set up project structure with dependencies (LangChain, LangGraph, PyGithub, Tavily)
- [DONE] **Step 2**: Create state management schema for agent conversations and context
- [DONE] **Step 3**: Implement 16 tools organized in 5 categories (GitHub, Search, File, Analysis, TODO)
- [DONE] **Step 4**: Design and implement sub-agent architecture with RepoInvestigator and ErrorResearcher
- [DONE] **Step 5**: Build main agent orchestration with task delegation system
- [DONE] **Step 6**: Create CLI interface with Click and Rich for user interaction
- [DONE] **Step 7**: Add enhanced error handling with helpful messages
- [DONE] **Step 8**: Test with real repositories and fix bugs (state validation, API compatibility)

### Conclusion

I planned to build a fully functional GitHub analysis agent using LangGraph, and I think I achieved it. The agent can successfully:
- Analyze GitHub issues and provide investigation reports
- Answer questions about repositories
- Delegate tasks to specialized sub-agents
- Handle errors gracefully with helpful messages

I'm satisfied because the agent actually works and uses all the course concepts. It was challenging to get the sub-agent delegation working (had to fix state validation issues), but debugging with Langsmith Traces helped a lot. The final product can genuinely help developers understand codebases faster.

---


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
## My Traces in LangSmith github-agent Project
![alt text](image.png)

list_repository_structure tool call:
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)

Relevent Output Testing Screenshots:
![alt text](image-5.png)
read_file_from_repo tool call:
![alt text](image-4.png)
![alt text](image-6.png)

Various Functionalities of the Agent:
![alt text](image-7.png)
Small production ready live demo of the agent using Streamlit clean frontend UI:
![alt text](image-8.png)
![alt text](image-9.png)
![alt text](image-10.png)
Detailed Analysis of the Github repositiry issue opened along with user included screenshots:
![alt text](image-11.png)
![alt text](image-12.png)
Generated Recommendation to MItigate the issue:
![alt text](image-13.png)

Example test repo:
![alt text](image-14.png)
![alt text](image-15.png)
![alt text](image-16.png)
![alt text](image-17.png)
![alt text](image-18.png)
![alt text](image-19.png)
![alt text](image-20.png)
![alt text](image-21.png)
![alt text](image-22.png)
![alt text](image-23.png)
Trace for the last one:
![alt text](image-24.png)
![alt text](image-25.png)
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
- ✅ Phase 2: Core Tool Development
- ✅ Phase 3: Sub-Agent Architecture
- ✅ Phase 4: Main Agent Orchestration
- ✅ Phase 5: Workflow Implementation
- ✅ Phase 6: CLI Interface
- ✅ Phase 7: Testing & Refinement
- ✅ Phase 8: Documentation

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

Made with ❤️ for the MAT496- Introduction to LLM Course Project

Unit test
![alt text](image.png)