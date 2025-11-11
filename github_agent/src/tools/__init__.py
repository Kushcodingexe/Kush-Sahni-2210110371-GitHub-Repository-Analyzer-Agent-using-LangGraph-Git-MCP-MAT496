"""Tools package initialization.

Exports all available tools for the GitHub Repository Analyzer Agent.
"""
from src.tools.github_tools import (
    search_code_in_repo,
    read_file_from_repo,
    list_repository_structure,
    get_issue_details
)

from src.tools.file_tools import (
    ls,
    read_file,
    write_file
)

from src.tools.search_tools import (
    search_error_solution,
    think_tool
)

from src.tools.analysis_tools import (
    extract_stack_trace,
    find_code_dependencies
)

from src.tools.todo_tools import (
    write_todos,
    read_todos
)


# All available tools
ALL_TOOLS = [
    # GitHub tools
    search_code_in_repo,
    read_file_from_repo,
    list_repository_structure,
    get_issue_details,
    
    # File system tools
    ls,
    read_file,
    write_file,
    
    # Search tools
    search_error_solution,
    think_tool,
    
    # Analysis tools
    extract_stack_trace,
    find_code_dependencies,
    
    # TODO tools
    write_todos,
    read_todos
]


# Tool categories for sub-agents
REPO_INVESTIGATOR_TOOLS = [
    search_code_in_repo,
    read_file_from_repo,
    list_repository_structure,
    find_code_dependencies,
    think_tool
]

ERROR_RESEARCHER_TOOLS = [
    search_error_solution,
    read_file,
    think_tool
]


__all__ = [
    'ALL_TOOLS',
    'REPO_INVESTIGATOR_TOOLS',
    'ERROR_RESEARCHER_TOOLS',
    # Individual tools
    'search_code_in_repo',
    'read_file_from_repo',
    'list_repository_structure',
    'get_issue_details',
    'ls',
    'read_file',
    'write_file',
    'search_error_solution',
    'think_tool',
    'extract_stack_trace',
    'find_code_dependencies',
    'write_todos',
    'read_todos'
]
