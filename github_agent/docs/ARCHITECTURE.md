# System Architecture

Detailed architecture documentation for the GitHub Repository Analyzer Agent.

---

## Overview

The GitHub Repository Analyzer Agent is a multi-agent AI system built with LangGraph that analyzes GitHub repositories, investigates issues, and answers questions about code. It uses specialized sub-agents for focused research and employs context offloading to manage token limits.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   CLI    │  │  Python  │  │  Docker  │  │  Future  │   │
│  │Commands  │  │   API    │  │Container │  │   API    │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────────┘   │
└───────┼─────────────┼─────────────┼────────────────────────┘
        │             │             │
        └─────────────┴─────────────┘
                      │
┌─────────────────────▼─────────────────────────────────────┐
│                   Main Agent Layer                         │
│  ┌──────────────────────────────────────────────────────┐ │
│  │            Main Orchestrator Agent                    │ │
│  │  • Creates research plans (TODOs)                    │ │
│  │  • Delegates to sub-agents                           │ │
│  │  • Manages virtual file system                       │ │
│  │  • Synthesizes findings                              │ │
│  └──┬───────────────────────────────────────────────┬───┘ │
└─────┼───────────────────────────────────────────────┼─────┘
      │                                               │
      ├─────────────────┬─────────────────┬──────────┤
      │                 │                 │          │
┌─────▼─────┐    ┌─────▼─────┐    ┌─────▼─────┐   │
│   Repo    │    │   Error   │    │  Future   │   │
│Investigator│    │ Researcher│    │Sub-Agents │   │
│           │    │           │    │           │   │
│• Code     │    │• Search   │    │• Security │   │
│  search   │    │  errors   │    │  analyzer │   │
│• File     │    │• Find     │    │• PR       │   │
│  reading  │    │  solutions│    │  reviewer │   │
│• Structure│    │• Research │    │           │   │
│  analysis │    │  docs     │    │           │   │
└─────┬─────┘    └─────┬─────┘    └───────────┘   │
      │                │                           │
      └────────────────┴───────────────────────────┘
                       │
┌──────────────────────▼─────────────────────────────────────┐
│                   Tools Layer                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ GitHub   │ │ Search   │ │   File   │ │ Analysis │     │
│  │  Tools   │ │  Tools   │ │  System  │ │  Tools   │     │
│  │          │ │          │ │  Tools   │ │          │     │
│  │• Search  │ │• Tavily  │ │• ls      │ │• Extract │     │
│  │• Read    │ │• Error   │ │• read    │ │  trace   │     │
│  │• List    │ │• Docs    │ │• write   │ │• Parse   │     │
│  │• Issues  │ │          │ │          │ │• Think   │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
└───────┼────────────┼────────────┼────────────┼───────────┘
        │            │            │            │
┌───────▼────────────▼────────────▼────────────▼───────────┐
│                External Services Layer                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ GitHub   │ │  Tavily  │ │  OpenAI  │ │Anthropic │    │
│  │   API    │ │   API    │ │   API    │ │   API    │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │
└────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Main Orchestrator Agent

**Responsibility:** Coordinates all activities and delegates to specialists

**Key Features:**
- **Planning:** Creates TODO lists for complex tasks
- **Delegation:** Spawns sub-agents for focused research
- **Synthesis:** Combines findings from multiple sources
- **State Management:** Maintains conversation context and file system

**Tools Available:**
- All 16+ built-in tools
- Task delegation tool for sub-agents

### 2. Sub-Agents

#### RepoInvestigator

**Purpose:** Deep repository analysis

**Capabilities:**
- Navigate repository structure
- Search for code patterns
- Read specific files
- Trace dependencies
- Follow stack traces to source

**Tools:**
- `search_code_in_repo`
- `read_file_from_repo`
- `list_repository_structure`
- `think_tool`
- `read_file`

**Hard Limits:**
- Max 5 tool calls per task
- Isolated context from main agent

#### ErrorResearcher

**Purpose:** Research programming errors and solutions

**Capabilities:**
- Web search for error solutions
- Find official documentation
- Analyze error patterns
- Synthesize findings from multiple sources

**Tools:**
- `search_error_solution`
- `search_documentation`
- `think_tool`
- `read_file`

**Hard Limits:**
- Max 3 searches per task
- Stops when solution found

---

## Key Design Patterns

### Context Offloading

**Problem:** LLM context windows are limited

**Solution:** Save detailed content to virtual file system

**How it works:**
1. Tool fetches large content (e.g., GitHub issue)
2. Full content saved to `state.files` as markdown
3. Only summary returned to agent
4. Agent can later `read_file()` to see details

**Benefits:**
- Prevents context overflow
- Enables long-running investigations
- Allows parallel research

**Example:**
```python
# Tool saves full content
state["files"]["issue_123.md"] = full_issue_details

# Returns only summary
return "Issue saved to issue_123.md. Main error: KeyError on line 45"
```

### Sub-Agent Delegation

**Problem:** Single agent can't specialize in everything

**Solution:** Delegate focused tasks to specialist sub-agents

**How it works:**
1. Main agent creates task description
2. Sub-agent spawned with isolated context
3. Sub-agent uses specialized tools
4. Results merged back to main agent
5. Main agent continues with enriched knowledge

**Benefits:**
- Specialization (repo vs error research)
- Parallel execution (multiple sub-agents)
- Clear separation of concerns

**Example:**
```python
# Main agent delegates
task(
    "Find where OAuth callback is handled",
    "repo-investigator"
)

# Sub-agent executes independently
# Returns findings summary
```

### State Management

**State Schema:**
```python
class GitHubAgentState(TypedDict):
    messages: list[BaseMessage]      # Conversation history
    files: dict[str, str]            # Virtual file system
    todos: list[str]                 # Task tracking
    current_repo: str | None         # Active repository
    issue_url: str | None            # Active issue
    analysis_results: dict           # Findings
    remaining_steps: int             # Iteration limit
```

**State Flow:**
```
User Input → Main Agent → Sub-Agent (isolated) → Back to Main → Response
              ↓                                      ↑
         state.files (shared)                  state.files (merged)
```

---

## Tool Categories

### GitHub Tools (5 tools)
- `search_code_in_repo` - Search for code patterns
- `read_file_from_repo` - Read specific files
- `list_repository_structure` - Directory trees
- `get_issue_details` - Fetch issue information
- `get_repository_info` - Basic repo metadata

### Search Tools (2 tools)
- `search_error_solution` - Web search for errors
- `search_documentation` - Find official docs

### File System Tools (3 tools)
- `ls` - List virtual files
- `read_file` - Read virtual file
- `write_file` - Write virtual file

### Analysis Tools (3 tools)
- `extract_stack_trace` - Parse error traces
- `parse_error_from_issue` - Extract error info
- `think_tool` - Agent reflection

### TODO Tools (3 tools)
- `write_todos` - Create task list
- `read_todos` - View tasks
- `mark_todo_done` - Complete task

### Task Delegation (1 tool)
- `task` - Delegate to sub-agent

---

## Execution Flow

### Example: Analyze GitHub Issue

```
1. User: "Analyze https://github.com/owner/repo/issues/123"
   ↓
2. Main Agent:
   - Creates TODO list
   - Calls get_issue_details()
   ↓
3. get_issue_details:
   - Fetches full issue from GitHub API
   - Saves to files["issue_123.md"]
   - Returns summary: "KeyError in oauth.py:45"
   ↓
4. Main Agent:
   - Delegates: "Find oauth.py and locate line 45"
   - task("...", "repo-investigator")
   ↓
5. RepoInvestigator sub-agent:
   - search_code_in_repo("oauth")
   - read_file_from_repo("src/auth/oauth.py")
   - Analyzes code
   - Returns: "Found error at access_token access"
   ↓
6. Main Agent:
   - Delegates: "Research KeyError solutions"
   - task("...", "error-researcher")
   ↓
7. ErrorResearcher sub-agent:
   - search_error_solution("KeyError access_token")
   - Finds StackOverflow answers
   - Returns: "Add validation before access"
   ↓
8. Main Agent:
   - Synthesizes all findings
   - Creates comprehensive report
   - Returns to user
```

---

## Technology Stack

### Core Framework
- **LangGraph** - Agent orchestration and state management
- **LangChain** - LLM abstractions and tools

### LLM Providers
- **OpenAI** - GPT-4o, GPT-4o-mini
- **Anthropic** - Claude Sonnet 4

### External APIs
- **GitHub API** - Repository and issue access
- **Tavily API** - Web search for solutions

### Deployment
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
- **PyPI** - Package distribution

---

## Security & Best Practices

### Security
- ✅ Non-root user in Docker
- ✅ Environment variables for secrets
- ✅ No hardcoded credentials
- ✅ API key validation
- ✅ Input validation for repo names and URLs

### Performance
- ✅ Context offloading for large data
- ✅ Parallel sub-agent execution
- ✅ Iteration limits to prevent runaway
- ✅ Caching GitHub API responses

### Reliability
- ✅ Error handling with helpful messages
- ✅ Retry logic for API failures
- ✅ Graceful degradation
- ✅ Comprehensive testing

---

## Scalability

### Current Limits
- Max 3 concurrent sub-agents (configurable)
- Max 25 iterations per main agent
- Max 10 iterations per sub-agent
- Max 3 searches per research task

### Future Improvements
- Queue system for batch processing
- Caching layer for repeated queries
- Database for persistent storage
- Load balancing for multiple agents

---

## Extension Points

### Adding New Sub-Agents
1. Create prompt in `src/prompts.py`
2. Define tool list in `src/main.py` SUB_AGENTS
3. Sub-agent automatically available via `task()` tool

### Adding New Tools
1. Create tool function in appropriate file
2. Add `@tool` decorator
3. Import in `src/tools/__init__.py`
4. Tool automatically available to agents

### Adding New Commands
1. Add Click command in `src/cli.py`
2. Command automatically available in CLI

---

## Testing Architecture

### Test Layers
1. **Unit Tests** - Individual tool testing
2. **Integration Tests** - Tool combinations
3. **End-to-End Tests** - Full workflows
4. **Performance Tests** - Speed benchmarks

### CI/CD Pipeline
```
PR Created
  ↓
Run Tests (Python 3.10, 3.11, 3.12)
  ↓
Check Code Quality (Black, Flake8)
  ↓
Build Docker Image
  ↓
Test Docker Image
  ↓
Merge if Passing
```

---

## Deployment Architecture

### Local
```
User Machine → Python Install → Agent
```

### Docker
```
User Machine → Docker Container → Agent → APIs
```

### Cloud
```
User → Load Balancer → Container(s) → APIs
                           ↓
                    Shared Storage (optional)
```

---

## Monitoring & Observability

### Logging
- LangSmith traces for debugging
- Standard Python logging
- Docker logs

### Metrics
- API call counts
- Token usage
- Response times
- Error rates

---

For implementation details, see:
- [API.md](API.md) - Complete API reference
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [GETTING_STARTED.md](GETTING_STARTED.md) - Quick start
