"""File system tools for context offloading and state management.

Provides tools for managing the agent's virtual file system, allowing
storage and retrieval of detailed information without cluttering the
main conversation context.
"""
from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from src.state import GitHubAgentState


@tool
def ls(state: Annotated[GitHubAgentState, InjectedState]) -> str:
    """List all files in the agent's virtual file system.
    
    Shows all files that have been created during the current session,
    including search results, issue analyses, and research findings.
    
    Returns:
        List of filenames with sizes
    """
    files = state.get("files", {})
    
    if not files:
        return "📂 File system is empty. No files created yet."
    
    output = [f"📂 Virtual File System ({len(files)} files):\n"]
    
    for filename, content in sorted(files.items()):
        size_kb = len(content) / 1024
        output.append(f"  📄 {filename} ({size_kb:.1f} KB)")
    
    output.append(f"\n💡 Use read_file('filename') to view contents")
    
    return '\n'.join(output)


@tool
def read_file(
    filename: str,
    state: Annotated[GitHubAgentState, InjectedState]
) -> str:
    """Read contents of a file from the virtual file system.
    
    Retrieves the full contents of a previously created file. This is useful
    for accessing detailed search results, issue analyses, or research findings.
    
    Args:
        filename: Name of the file to read
    
    Returns:
        File contents or error message if file not found
    
    Example:
        read_file("issue_123_analysis.md")
    """
    files = state.get("files", {})
    
    if filename not in files:
        available = list(files.keys())
        return f"❌ File '{filename}' not found.\n\nAvailable files:\n" + '\n'.join(f"  - {f}" for f in available)
    
    content = files[filename]
    return f"📄 **{filename}**\n\n{content}"


@tool
def write_file(
    filename: str,
    content: str,
    state: Annotated[GitHubAgentState, InjectedState]
) -> str:
    """Write or update a file in the virtual file system.
    
    Creates a new file or updates an existing one with the provided content.
    Useful for saving analysis results, notes, or structured findings.
    
    Args:
        filename: Name of the file to write
        content: Content to write to the file
    
    Returns:
        Confirmation message
    
    Example:
        write_file("findings.md", "# Key Findings\\n- Error in oauth.py...")
    """
    files = state.get("files", {})
    
    is_new = filename not in files
    files[filename] = content
    
    size_kb = len(content) / 1024
    
    if is_new:
        return f"✅ Created new file: {filename} ({size_kb:.1f} KB)"
    else:
        return f"✅ Updated file: {filename} ({size_kb:.1f} KB)"


# Export all tools
__all__ = ['ls', 'read_file', 'write_file']
