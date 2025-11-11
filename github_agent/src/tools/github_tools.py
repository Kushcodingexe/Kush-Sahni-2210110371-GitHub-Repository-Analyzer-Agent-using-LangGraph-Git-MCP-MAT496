"""GitHub tools for repository access and analysis.

Provides tools for searching code, reading files, analyzing issues,
and exploring repository structure using the GitHub API.
"""
from typing import Annotated
import base64
from github import Github, GithubException
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import InjectedState, InjectedToolCallId
from langgraph.types import Command

from src.config import Config
from src.state import GitHubAgentState


# Initialize GitHub client
github_client = Github(Config.GITHUB_TOKEN)


@tool
def search_code_in_repo(
    repo_name: str,
    query: str,
    max_results: int = 5
) -> str:
    """Search for code patterns in a GitHub repository.
    
    This tool searches through all code files in a repository using GitHub's
    code search API. It's useful for finding specific functions, classes,
    error messages, or code patterns.
    
    Args:
        repo_name: Full repository name in format 'owner/repo' (e.g., 'langchain-ai/langchain')
        query: Search query. Can include:
            - Plain text: 'def process_callback'
            - Language filter: 'oauth language:python'
            - Path filter: 'error path:src/auth'
            - Extension: 'token extension:py'
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        Formatted search results with file paths, line numbers, and code snippets
    
    Example:
        search_code_in_repo("langchain-ai/langchain", "ChatOpenAI class", 3)
    """
    try:
        # Add repository qualifier to query
        full_query = f"{query} repo:{repo_name}"
        
        # Perform search
        results = github_client.search_code(full_query)
        
        # Format results
        output = []
        output.append(f"🔍 Found {results.totalCount} results for '{query}' in {repo_name}\n")
        output.append(f"Showing top {max_results} results:\n")
        
        for i, result in enumerate(results[:max_results], 1):
            output.append(f"\n{i}. **{result.path}**")
            output.append(f"   Repository: {result.repository.full_name}")
            output.append(f"   URL: {result.html_url}")
            
            # Try to get a snippet
            try:
                content = result.decoded_content.decode('utf-8')
                lines = content.split('\n')
                # Find lines containing query terms
                query_terms = query.lower().split()
                matching_lines = [
                    (idx, line) for idx, line in enumerate(lines, 1)
                    if any(term in line.lower() for term in query_terms)
                ]
                
                if matching_lines:
                    output.append(f"   Preview (line {matching_lines[0][0]}):")
                    output.append(f"   ```\n   {matching_lines[0][1][:100]}...\n   ```")
            except:
                output.append("   (Preview unavailable)")
        
        if results.totalCount == 0:
            output.append(f"\n💡 Try different search terms or check the repository name.")
        
        return "\n".join(output)
        
    except GithubException as e:
        return f"❌ GitHub API Error: {e.data.get('message', str(e))}"
    except Exception as e:
        return f"❌ Error searching repository: {str(e)}"


@tool
def read_file_from_repo(
    repo_name: str,
    file_path: str,
    ref: str = "main"
) -> str:
    """Read a specific file from a GitHub repository.
    
    Retrieves the complete contents of a file from a repository. Useful after
    using search_code_in_repo to investigate specific files.
    
    Args:
        repo_name: Full repository name in format 'owner/repo'
        file_path: Path to the file within the repository (e.g., 'src/auth/oauth.py')
        ref: Branch, tag, or commit SHA (default: 'main')
    
    Returns:
        File contents with line numbers for easier reference
    
    Example:
        read_file_from_repo("langchain-ai/langchain", "src/chat_models/openai.py")
    """
    try:
        repo = github_client.get_repo(repo_name)
        
        # Get file contents
        file_content = repo.get_contents(file_path, ref=ref)
        
        if file_content.type != "file":
            return f"❌ Path '{file_path}' is a directory, not a file."
        
        # Decode content
        content = base64.b64decode(file_content.content).decode('utf-8')
        
        # Add line numbers
        lines = content.split('\n')
        numbered_lines = [f"{i:4d} | {line}" for i, line in enumerate(lines, 1)]
        
        output = []
        output.append(f"📄 File: {file_path}")
        output.append(f"📦 Repository: {repo_name}")
        output.append(f"🌿 Branch/Ref: {ref}")
        output.append(f"📏 Lines: {len(lines)}")
        output.append(f"🔗 URL: {file_content.html_url}")
        output.append(f"\n{'='*60}\n")
        output.append('\n'.join(numbered_lines[:100]))  # First 100 lines
        
        if len(lines) > 100:
            output.append(f"\n... ({len(lines) - 100} more lines)")
            output.append(f"\n💡 Use specific line ranges if you need to see more")
        
        return '\n'.join(output)
        
    except GithubException as e:
        if e.status == 404:
            return f"❌ File '{file_path}' not found in {repo_name} (ref: {ref}). Check the path and branch name."
        return f"❌ GitHub API Error: {e.data.get('message', str(e))}"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"


@tool
def list_repository_structure(
    repo_name: str,
    path: str = "",
    max_depth: int = 2
) -> str:
    """Get directory tree structure of a GitHub repository.
    
    Explores the repository structure to understand organization.
    Useful for initial repository investigation.
    
    Args:
        repo_name: Full repository name in format 'owner/repo'
        path: Starting path within repository (empty string for root)
        max_depth: Maximum directory depth to explore (default: 2)
    
    Returns:
        Tree structure showing directories and files
    
    Example:
        list_repository_structure("langchain-ai/langchain", "src", 2)
    """
    try:
        repo = github_client.get_repo(repo_name)
        
        def explore_contents(current_path, depth=0, prefix=""):
            if depth > max_depth:
                return []
            
            contents = repo.get_contents(current_path)
            if not isinstance(contents, list):
                contents = [contents]
            
            output = []
            # Sort: directories first, then files
            dirs = [c for c in contents if c.type == "dir"]
            files = [c for c in contents if c.type == "file"]
            
            for item in dirs + files:
                is_last = item == (dirs + files)[-1]
                connector = "└── " if is_last else "├── "
                
                if item.type == "dir":
                    output.append(f"{prefix}{connector}📁 {item.name}/")
                    
                    # Recurse into directory
                    if depth < max_depth:
                        extension = "    " if is_last else "│   "
                        output.extend(explore_contents(item.path, depth + 1, prefix + extension))
                else:
                    size_kb = item.size / 1024
                    output.append(f"{prefix}{connector}📄 {item.name} ({size_kb:.1f} KB)")
            
            return output
        
        output = []
        output.append(f"📂 Repository: {repo_name}")
        output.append(f"🌿 Default Branch: {repo.default_branch}")
        output.append(f"📍 Path: /{path if path else 'root'}")
        output.append(f"🔍 Depth: {max_depth}")
        output.append(f"\n{'='*60}\n")
        
        tree = explore_contents(path)
        output.extend(tree)
        
        if not tree:
            output.append(f"(Empty directory or path not found)")
        
        return '\n'.join(output)
        
    except GithubException as e:
        if e.status == 404:
            return f"❌ Repository '{repo_name}' or path '{path}' not found."
        return f"❌ GitHub API Error: {e.data.get('message', str(e))}"
    except Exception as e:
        return f"❌ Error listing repository: {str(e)}"


@tool
def get_issue_details(
    issue_url: str,
    state: Annotated[GitHubAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """Fetch detailed information about a GitHub issue.
    
    Retrieves issue title, description, labels, and extracts important details like
    stack traces and error messages. Saves full details to files for context offloading.
    
    Args:
        issue_url: Full GitHub issue URL (e.g., 'https://github.com/owner/repo/issues/123')
        state: Injected agent state
        tool_call_id: Injected tool call ID
    
    Returns:
        Command with updated files and summary message
    
    Example:
        get_issue_details("https://github.com/langchain-ai/langchain/issues/1234")
    """
    try:
        # Parse issue URL
        # Format: https://github.com/owner/repo/issues/123
        parts = issue_url.rstrip('/').split('/')
        
        if 'github.com' not in issue_url or 'issues' not in parts:
            return Command(update={
                "messages": [ToolMessage(
                    f"❌ Invalid issue URL format. Expected: https://github.com/owner/repo/issues/123",
                    tool_call_id=tool_call_id
                )]
            })
        
        owner = parts[-4]
        repo_name = parts[-3]
        issue_number = int(parts[-1])
        
        repo = github_client.get_repo(f"{owner}/{repo_name}")
        issue = repo.get_issue(issue_number)
        
        # Extract information
        title = issue.title
        body = issue.body or "(No description provided)"
        labels = [label.name for label in issue.labels]
        state_str = issue.state
        created = issue.created_at.strftime("%Y-%m-%d %H:%M")
        comments_count = issue.comments
        
        # Build detailed report
        report = []
        report.append(f"# GitHub Issue Analysis: #{issue_number}")
        report.append(f"\n**Repository:** {owner}/{repo_name}")
        report.append(f"**Title:** {title}")
        report.append(f"**Status:** {state_str}")
        report.append(f"**Created:** {created}")
        report.append(f"**Labels:** {', '.join(labels) if labels else 'None'}")
        report.append(f"**Comments:** {comments_count}")
        report.append(f"**URL:** {issue_url}")
        
        report.append(f"\n## Description\n")
        report.append(body)
        
        # Extract stack traces and error messages
        potential_errors = []
        for line in body.split('\n'):
            if any(keyword in line.lower() for keyword in ['error', 'exception', 'traceback', 'failed']):
                potential_errors.append(line)
        
        if potential_errors:
            report.append(f"\n## Potential Error Lines\n")
            for error_line in potential_errors[:10]:  # First 10
                report.append(f"- {error_line.strip()}")
        
        # Get comments
        if comments_count > 0:
            report.append(f"\n## Comments\n")
            for idx, comment in enumerate(issue.get_comments()[:5], 1):  # First 5 comments
                report.append(f"\n### Comment {idx} by @{comment.user.login}")
                report.append(f"{comment.body[:500]}...")  # First 500 chars
        
        # Save to files
        files = state.get("files", {})
        filename = f"issue_{issue_number}_analysis.md"
        files[filename] = '\n'.join(report)
        
        # Create summary
        summary = f"""📋 Fetched Issue #{issue_number}: {title}
        
**Status:** {state_str}
**Labels:** {', '.join(labels) if labels else 'None'}
**Repository:** {owner}/{repo_name}

Saved detailed analysis to: {filename}
💡 Use read_file('{filename}') to access full details.
"""
        
        return Command(update={
            "files": files,
            "issue_url": issue_url,
            "current_repo": f"{owner}/{repo_name}",
            "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
        })
        
    except GithubException as e:
        error_msg = f"❌ GitHub API Error: {e.data.get('message', str(e))}"
        return Command(update={
            "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
        })
    except Exception as e:
        error_msg = f"❌ Error fetching issue: {str(e)}"
        return Command(update={
            "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
        })


# Export all tools
__all__ = [
    'search_code_in_repo',
    'read_file_from_repo',
    'list_repository_structure',
    'get_issue_details'
]
