"""TODO management tools for task tracking.

Provides tools for creating and managing TODO lists to track
the agent's progress through complex tasks.
"""
from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.state import GitHubAgentState


@tool
def write_todos(
    todos: list[str],
    state: Annotated[GitHubAgentState, InjectedState]
) -> str:
    """Create or update the TODO list for the current task.
    
    Use this at the start of a complex task to break it down into
    manageable steps. Update as you complete tasks.
    
    Mark completed tasks with [x], in-progress with [/], pending with [ ].
    
    Args:
        todos: List of TODO items
    
    Returns:
        Confirmation with TODO count
    
    Example:
        write_todos([
            "[x] Fetch issue details",
            "[/] Search for error in repository",
            "[ ] Research error solutions",
            "[ ] Synthesize findings"
        ])
    """
    if not todos:
        return "⚠️ No TODOs provided. Please provide a list of tasks."
    
    # Count status
    completed = sum(1 for t in todos if t.strip().startswith("[x]"))
    in_progress = sum(1 for t in todos if t.strip().startswith("[/]"))
    pending = sum(1 for t in todos if t.strip().startswith("[ ]"))
    
    return f"""✅ TODO list updated
    
**Total tasks:** {len(todos)}
- ✅ Completed: {completed}
- ⏳ In Progress: {in_progress}
- 📋 Pending: {pending}

Use read_todos() to review your progress."""


@tool
def read_todos(state: Annotated[GitHubAgentState, InjectedState]) -> str:
    """Read the current TODO list.
    
    Use this to remind yourself of the task breakdown and track progress.
    
    Returns:
        Current TODO list with status counts
    """
    todos = state.get("todos", [])
    
    if not todos:
        return "📋 No TODOs set. Use write_todos() to create a task breakdown."
    
    # Count status
    completed = sum(1 for t in todos if t.strip().startswith("[x]"))
    in_progress = sum(1 for t in todos if t.strip().startswith("[/]"))
    pending = sum(1 for t in todos if t.strip().startswith("[ ]"))
    
    result = ["📋 Current TODO List\n"]
    
    for i, todo in enumerate(todos, 1):
        # Add emoji based on status
        if todo.strip().startswith("[x]"):
            result.append(f"{i}. ✅ {todo.replace('[x]', '').strip()}")
        elif todo.strip().startswith("[/]"):
            result.append(f"{i}. ⏳ {todo.replace('[/]', '').strip()}")
        else:
            result.append(f"{i}. 📋 {todo.replace('[ ]', '').strip()}")
    
    result.append(f"\n**Progress:** {completed}/{len(todos)} completed")
    
    if in_progress > 0:
        result.append(f"**In Progress:** {in_progress} task(s)")
    
    if pending > 0:
        result.append(f"**Remaining:** {pending} task(s)")
    
    return '\n'.join(result)


# Export all tools
__all__ = ['write_todos', 'read_todos']
