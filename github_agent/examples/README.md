# Example usage scripts for the GitHub Repository Analyzer Agent

## Analyze a GitHub Issue

```python
from src.main import analyze_issue

# Analyze a GitHub issue
result = analyze_issue("https://github.com/langchain-ai/langchain/issues/1234")

# Print the final response
for msg in reversed(result["messages"]):
    if hasattr(msg, 'content'):
        print(msg.content)
        break
```

## Ask About a Repository

```python
from src.main import ask_about_repository

# Ask a question
result = ask_about_repository(
    "langchain-ai/langchain",
    "How does the ChatOpenAI class work?"
)

# Print response
for msg in reversed(result["messages"]):
    if hasattr(msg, 'content'):
        print(msg.content)
        break
```

## Use Individual Tools

```python
from src.tools import search_code_in_repo, get_repository_info
from src.state import get_initial_state

# Search for code
result = search_code_in_repo.invoke({
    "repo_name": "langchain-ai/langchain",
    "query": "ChatOpenAI",
    "max_results": 5
})
print(result)

# Get repository info
info = get_repository_info.invoke({
    "repo_name": "langchain-ai/langchain"
})
print(info)
```

## Interactive Mode

```python
from src.main import interactive_session

# Start interactive session
interactive_session()
```

## Using Sub-Agents Directly

```python
from src.main import main_agent
from src.state import get_initial_state
from langchain_core.messages import HumanMessage

# Create initial state
state = get_initial_state()
state["messages"] = [
    HumanMessage(content="Investigate the authentication module in owner/repo")
]
state["current_repo"] = "owner/repo"

# Run the agent
result = main_agent.invoke(state)

# Agent will delegate to sub-agents automatically
print(result["messages"][-1].content)
```

## CLI Examples

```bash
# Install the package first
pip install -e .

# Analyze an issue
github-agent issue https://github.com/owner/repo/issues/123

# Ask about a repository
github-agent ask langchain-ai/langchain "How does ChatOpenAI work?"

# Interactive mode
github-agent interactive

# Check configuration
github-agent config

# Show agent info
github-agent info
```
