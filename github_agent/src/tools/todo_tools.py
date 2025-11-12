"""TODO management tools for task tracking.

Based on reference deep agent pattern for tracking progress.
"""
from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.state import GitHubAgentState


@tool
def write_todos(
    todos_list: list[str],
    state: Annotated[GitHubAgentState, InjectedState]
) -> str:
    """Create or update the TODO list for the current task.
    
    Use this at the start of a user request to plan your approach.
    Break down the task into clear, actionable steps.
    
    Args:
        todos_list: List of TODO items (will replace existing TODOs)
    
    Returns:
        Confirmation message
    
    Examples:
        write_todos([
            "Fetch issue details",
            "Search for error in repository",
            "Research error solution online",
            "Compile findings into report"
        ])
    """
    if not isinstance(todos_list, list):
        return "❌ Error: todos_list must be a list of strings"
    
    # Update state todos
    state["todos"] = [str(todo) for todo in todos_list]
    
    output = [f"📋 Created {len(todos_list)} TODO items:\n"]
    for idx, todo in enumerate(todos_list, 1):
        output.append(f"  {idx}. [ ] {todo}")
    
    return "\n".join(output)


@tool
def read_todos(state: Annotated[GitHubAgentState, InjectedState]) -> str:
    """Read the current TODO list.
    
    Use this to:
    - Check what tasks remain
    - Remind yourself of the plan
    - Decide what to do next
    
    Returns:
        Formatted TODO list
    
    Examples:
        read_todos()  # Shows current plan
    """
    todos = state.get("todos", [])
    
    if not todos:
        return "📋 No TODOs set yet. Use write_todos() to create a plan."
    
    output = [f"📋 Current TODO List ({len(todos)} items):\n"]
    for idx, todo in enumerate(todos, 1):
        # Simple "done" marking if starts with [x] or ✓
        is_done = todo.strip().startswith(('[x]', '✓', '✅'))
        marker = "✅" if is_done else "[ ]"
        clean_todo = todo.strip().lstrip('[x]').lstrip('✓').lstrip('✅').strip()
        output.append(f"  {idx}. {marker} {clean_todo}")
    
    return "\n".join(output)


@tool
def mark_todo_done(
    todo_index: int,
    state: Annotated[GitHubAgentState, InjectedState]
) -> str:
    """Mark a TODO item as completed.
    
    Args:
        todo_index: 1-based index of the TODO item (as shown in read_todos)
    
    Returns:
        Confirmation message
    
    Examples:
        mark_todo_done(1)  # Marks first TODO as done
    """
    todos = state.get("todos", [])
    
    if not todos:
        return "❌ No TODOs exist. Use write_todos() first."
    
    if todo_index < 1 or todo_index > len(todos):
        return f"❌ Invalid index {todo_index}. Valid range: 1-{len(todos)}"
    
    # Mark as done
    idx = todo_index - 1
    todo = todos[idx].strip().lstrip('[x]').lstrip('✓').lstrip('✅').strip()
    todos[idx] = f"✅ {todo}"
    
    return f"✅ Marked TODO #{todo_index} as done: {todo}"
