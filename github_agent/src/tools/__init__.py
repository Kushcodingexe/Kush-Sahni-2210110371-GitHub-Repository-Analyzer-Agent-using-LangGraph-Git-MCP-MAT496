"""Tools package - exports all available tools for the GitHub Agent.

Import all tools here for easy access by the agent.
"""
from src.tools.github_tools import (
    search_code_in_repo,
    read_file_from_repo,
    list_repository_structure,
    get_issue_details,
    get_repository_info,
)

from src.tools.search_tools import (
    search_error_solution,
    search_documentation,
)

from src.tools.file_tools import (
    ls,
    read_file,
    write_file,
)

from src.tools.analysis_tools import (
    extract_stack_trace,
    think_tool,
    parse_error_from_issue,
)

from src.tools.todo_tools import (
    write_todos,
    read_todos,
    mark_todo_done,
)


# GitHub tools
__all__ = [
    # GitHub tools
    "search_code_in_repo",
    "read_file_from_repo",
    "list_repository_structure",
    "get_issue_details",
    "get_repository_info",
    
    # Search tools
    "search_error_solution",
    "search_documentation",
    
    # File system tools
    "ls",
    "read_file",
    "write_file",
    
    # Analysis tools
    "extract_stack_trace",
    "think_tool",
    "parse_error_from_issue",
    
    # TODO tools
    "write_todos",
    "read_todos",
    "mark_todo_done",
]


# Organize tools by category
GITHUB_TOOLS = [
    search_code_in_repo,
    read_file_from_repo,
    list_repository_structure,
    get_issue_details,
    get_repository_info,
]

SEARCH_TOOLS = [
    search_error_solution,
    search_documentation,
]

FILE_TOOLS = [
    ls,
    read_file,
    write_file,
]

ANALYSIS_TOOLS = [
    extract_stack_trace,
    think_tool,
    parse_error_from_issue,
]

TODO_TOOLS = [
    write_todos,
    read_todos,
    mark_todo_done,
]

# All tools for agent
ALL_TOOLS = GITHUB_TOOLS + SEARCH_TOOLS + FILE_TOOLS + ANALYSIS_TOOLS + TODO_TOOLS
