"""File system tools for context offloading.

Virtual file system for storing agent research and findings.
Based on the reference deep agent pattern.
"""
from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.state import GitHubAgentState


@tool
def ls(state: Annotated[GitHubAgentState, InjectedState]) -> str:
    """List all files in the agent's virtual file system.
    
    Use this to see what research and findings have been saved.
    
    Returns:
        List of filenames with sizes
    
    Examples:
        ls()  # Shows all saved files
    """
    files = state.get("files", {})
    
    if not files:
        return "📁 No files saved yet. Use search or investigation tools to gather information."
    
    output = [f"📁 Virtual File System ({len(files)} files):\n"]
    
    for filename, content in sorted(files.items()):
        size = len(content)
        size_str = f"{size:,} bytes"
        output.append(f"  📄 {filename} ({size_str})")
    
    return "\n".join(output)


@tool
def read_file(
    filename: str,
    state: Annotated[GitHubAgentState, InjectedState]
) -> str:
    """Read a file from the agent's virtual file system.
    
    Use this to access detailed research findings, search results,
    or issue details that were previously saved.
    
    Args:
        filename: Name of the file to read
    
    Returns:
        File contents or error message
    
    Examples:
        read_file("issue_123_abc.md")
        read_file("error_solution_xyz.md")
    """
    files = state.get("files", {})
    
    if filename not in files:
        available = ", ".join(sorted(files.keys()))
        return f"❌ File not found: {filename}\n\nAvailable files: {available or '(none)'}"
    
    return files[filename]


@tool
def write_file(
    filename: str,
    content: str,
    state: Annotated[GitHubAgentState, InjectedState]
) -> str:
    """Write content to a file in the virtual file system.
    
    Use this to:
    - Save analysis results
    - Store investigation findings
    - Keep notes for later reference
    
    Args:
        filename: Name of file to create/overwrite
        content: Content to write
    
    Returns:
        Confirmation message
    
    Examples:
        write_file("my_analysis.md", "## Analysis Results\\n...")
        write_file("notes.txt", "Important findings: ...")
    """
    # Get or create files dict
    if "files" not in state:
        state["files"] = {}
    
    # Check if file exists before writing
    is_update = filename in state["files"]
    
    # Write to state
    state["files"][filename] = content
    
    size = len(content)
    action = "Updated" if is_update else "Created"
    
    return f"✅ {action} file: {filename} ({size:,} bytes)"
