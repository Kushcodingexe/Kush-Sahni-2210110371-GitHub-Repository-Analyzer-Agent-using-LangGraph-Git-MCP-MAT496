# API Reference

Complete reference for all tools and functions in the GitHub Repository Analyzer Agent.

---

## Main Functions

### `analyze_issue(issue_url: str) -> dict`

Analyze a GitHub issue and provide investigation report.

**Parameters:**
- `issue_url` (str): Full GitHub issue URL

**Returns:**
- dict: Agent execution result with analysis

**Example:**
```python
from src.main import analyze_issue

result = analyze_issue(
    "https://github.com/owner/repo/issues/123"
)
```

---

### `ask_about_repository(repo_name: str, question: str) -> dict`

Ask questions about a GitHub repository.

**Parameters:**
- `repo_name` (str): Repository in `owner/repo` format
- `question` (str): Natural language question

**Returns:**
- dict: Agent execution result with answer

**Example:**
```python
from src.main import ask_about_repository

result = ask_about_repository(
    "openai/openai-python",
    "How does authentication work?"
)
```

---

### `interactive_session()`

Start interactive CLI session.

**Example:**
```python
from src.main import interactive_session

interactive_session()
```

---

## GitHub Tools

### `search_code_in_repo(repo_name, query, max_results=10)`

Search for code patterns in a repository.

**Parameters:**
- `repo_name` (str): Repository name (owner/repo)
- `query` (str): Search query (GitHub code search syntax)
- `max_results` (int): Maximum results (default: 10)

**Returns:**
- str: Formatted search results with file paths and snippets

**Example:**
```python
search_code_in_repo(
    "langchain-ai/langchain",
    "ChatOpenAI",
    max_results=5
)
```

---

### `read_file_from_repo(repo_name, file_path, ref="main")`

Read a specific file from a repository.

**Parameters:**
- `repo_name` (str): Repository name
- `file_path` (str): Path to file in repo
- `ref` (str): Branch/tag/commit (default: "main")

**Returns:**
- str: File contents with metadata

**Example:**
```python
read_file_from_repo(
    "openai/openai-python",
    "README.md"
)
```

---

### `list_repository_structure(repo_name, path="", max_depth=2)`

Get directory tree structure.

**Parameters:**
- `repo_name` (str): Repository name
- `path` (str): Starting path (default: root)
- `max_depth` (int): Maximum depth (default: 2)

**Returns:**
- str: Tree structure

**Example:**
```python
list_repository_structure(
    "facebook/react",
    path="src",
    max_depth=3
)
```

---

### `get_issue_details(issue_url, state, tool_call_id)`

Fetch detailed issue information.

**Note:** This is an agent tool with injected state.

**Parameters:**
- `issue_url` (str): Full GitHub issue URL
- `state`: Agent state (injected)
- `tool_call_id`: Tool call ID (injected)

**Returns:**
- Command: State update with issue details

---

### `get_repository_info(repo_name)`

Get basic repository information.

**Parameters:**
- `repo_name` (str): Repository name

**Returns:**
- str: Formatted repository metadata

**Example:**
```python
get_repository_info("microsoft/vscode")
```

---

## Search Tools

### `search_error_solution(error_message, library_name, state, tool_call_id)`

Search web for error solutions.

**Parameters:**
- `error_message` (str): Error message to search for
- `library_name` (str): Related library/framework
- `state`: Agent state (injected)
- `tool_call_id`: Tool call ID (injected)

**Returns:**
- Command: State update with search results

---

### `search_documentation(query, library_name, state, tool_call_id)`

Search for official documentation.

**Parameters:**
- `query` (str): Documentation query
- `library_name` (str): Library/framework name
- `state`: Agent state (injected)
- `tool_call_id`: Tool call ID (injected)

**Returns:**
- Command: State update with documentation links

---

## File System Tools

### `ls(state)`

List files in virtual file system.

**Parameters:**
- `state`: Agent state (injected)

**Returns:**
- str: List of files with sizes

---

### `read_file(filename, state)`

Read file from virtual file system.

**Parameters:**
- `filename` (str): Name of file to read
- `state`: Agent state (injected)

**Returns:**
- str: File contents

---

### `write_file(filename, content, state)`

Write file to virtual file system.

**Parameters:**
- `filename` (str): Name of file to create
- `content` (str): Content to write
- `state`: Agent state (injected)

**Returns:**
- str: Confirmation message

---

## Analysis Tools

### `extract_stack_trace(text)`

Extract and parse stack traces from text.

**Parameters:**
- `text` (str): Text containing stack trace

**Returns:**
- str: Parsed stack trace information

**Example:**
```python
extract_stack_trace("""
Traceback (most recent call last):
  File "main.py", line 10, in <module>
    raise ValueError("error")
ValueError: error
""")
```

---

### `parse_error_from_issue(issue_body)`

Parse error information from issue body.

**Parameters:**
- `issue_body` (str): Issue description text

**Returns:**
- str: Extracted error details

---

### `think_tool(reflection, state)`

Agent reflection and planning tool.

**Parameters:**
- `reflection` (str): Agent's thoughts/observations
- `state`: Agent state (injected)

**Returns:**
- str: Acknowledgment

---

## TODO Management Tools

### `write_todos(todos_list, state)`

Create TODO list for task tracking.

**Parameters:**
- `todos_list` (list[str]): List of tasks
- `state`: Agent state (injected)

**Returns:**
- str: Confirmation with TODO list

**Example:**
```python
write_todos([
    "Fetch repository information",
    "Search for authentication code",
    "Analyze findings"
], state)
```

---

### `read_todos(state)`

Read current TODO list.

**Parameters:**
- `state`: Agent state (injected)

**Returns:**
- str: Formatted TODO list with status

---

### `mark_todo_done(todo_index, state)`

Mark a TODO as complete.

**Parameters:**
- `todo_index` (int): Index of TODO (1-based)
- `state`: Agent state (injected)

**Returns:**
- str: Updated TODO list

---

## Sub-Agent Task Delegation

### `task(description, subagent_type, state)`

Delegate task to specialized sub-agent.

**Parameters:**
- `description` (str): Clear task description
- `subagent_type` (str): "repo-investigator" or "error-researcher"
- `state`: Agent state (injected)

**Returns:**
- str: Sub-agent findings

**Example:**
```python
task(
    "Find where OAuth callback is handled",
    "repo-investigator",
    state
)
```

**Available Sub-Agents:**
- `repo-investigator`: Code structure and location
- `error-researcher`: Error solutions and documentation

---

## State Schema

### `GitHubAgentState`

TypedDict for agent state management.

**Fields:**
- `messages` (list[BaseMessage]): Conversation history
- `files` (dict[str, str]): Virtual file system
- `todos` (list[str]): Task list
- `current_repo` (str | None): Current repository
- `issue_url` (str | None): Current issue URL
- `analysis_results` (dict): Analysis findings
- `remaining_steps` (int): Iteration limit

---

## Configuration

### Environment Variables

- `GITHUB_TOKEN`: GitHub personal access token
- `TAVILY_API_KEY`: Tavily search API key
- `OPENAI_API_KEY`: OpenAI API key (or Anthropic)
- `ANTHROPIC_API_KEY`: Anthropic API key (or OpenAI)
- `DEFAULT_MODEL`: Model to use (e.g., "openai:gpt-4o-mini")
- `MAX_CONCURRENT_RESEARCH_UNITS`: Max parallel sub-agents (default: 3)
- `MAX_RESEARCHER_ITERATIONS`: Max research iterations (default: 3)
- `MAX_SEARCH_RESULTS`: Results per search (default: 3)

### `Config` Class

Access configuration values:

```python
from src.config import Config

print(Config.GITHUB_TOKEN)
print(Config.DEFAULT_MODEL)
Config.print_config()  # Display masked configuration
Config.validate()      # Validate all required keys
```

---

## Error Handling

### Custom Exceptions

- `AgentError`: Base exception with formatted messages
- `GitHubAPIError`: GitHub API specific errors
- `SearchError`: Search/research errors
- `ConfigurationError`: Configuration issues

### Error Utilities

- `handle_github_error(error, context)`: Format GitHub errors
- `handle_search_error(error, query)`: Format search errors
- `validate_repo_name(repo_name)`: Validate repository format
- `validate_issue_url(url)`: Validate issue URL format
- `retry_on_failure(max_retries, delay, backoff)`: Retry decorator

---

## CLI Commands

```bash
# Analyze issue
github-agent issue <issue_url>

# Ask about repository
github-agent ask <repo_name> <question>

# Interactive mode
github-agent interactive

# Show configuration
github-agent config

# Show information
github-agent info
```

---

## Type Hints

All functions use Python type hints. Import from `typing`:

```python
from typing import Annotated, TypedDict, Sequence
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import InjectedState
```

---

## Return Types

- **Tool functions**: Return `str` or `Command`
- **Main functions**: Return `dict` (agent state)
- **CLI functions**: Return `None` (print to stdout)

---

## Best Practices

1. **Always validate inputs** before making API calls
2. **Use context offloading** for large data (save to files)
3. **Create TODOs** at start of complex tasks
4. **Delegate to sub-agents** for focused research
5. **Handle errors gracefully** with helpful messages

---

For more examples, see:
- [examples/README.md](../examples/README.md)
- [GETTING_STARTED.md](GETTING_STARTED.md)
- [COMMON_TASKS.md](COMMON_TASKS.md)
