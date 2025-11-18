"""GitHub API tools for repository and issue analysis.

Provides tools for searching code, reading files, listing structure,
and analyzing GitHub issues.
"""
from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from github import Github, GithubException
import base64
import uuid

from src.config import Config
from src.errors import handle_github_error, validate_repo_name, retry_on_failure
from src.state import GitHubAgentState


# Initialize GitHub client
github_client = Github(Config.GITHUB_TOKEN)


@tool
def search_code_in_repo(
    repo_name: str,
    query: str,
    max_results: int = 10
) -> str:
    """Search for code patterns in a GitHub repository.
    
    Search uses GitHub's code search syntax. You can search for:
    - Specific strings: "error handling"
    - File types: "extension:py"
    - Path patterns: "path:src/auth"
    - Language: "language:python"
    
    Args:
        repo_name: Full repository name (e.g., "owner/repo")
        query: Search query using GitHub code search syntax
        max_results: Maximum number of results to return (default: 10)
    
    Returns:
        Formatted string with search results including file paths and snippets
    
    Examples:
        search_code_in_repo("langchain-ai/langchain", "ChatOpenAI")
        search_code_in_repo("owner/repo", "def authenticate", max_results=5)
    """
    try:
        # Add repo qualifier to query
        full_query = f"{query} repo:{repo_name}"
        
        # Perform search
        results = github_client.search_code(full_query)
        
        if results.totalCount == 0:
            return f"No results found for query: {query}"
        
        # Format results
        output = [f"Found {min(results.totalCount, max_results)} results for '{query}' in {repo_name}:\n"]
        
        for idx, item in enumerate(results[:max_results], 1):
            output.append(f"\n{idx}. **{item.path}**")
            output.append(f"   Repository: {item.repository.full_name}")
            output.append(f"   URL: {item.html_url}")
            
            # Add snippet if available
            if hasattr(item, 'text_matches') and item.text_matches:
                snippet = item.text_matches[0].get('fragment', '')[:200]
                output.append(f"   Snippet: {snippet}...")
        
        return "\n".join(output)
        
    except GithubException as e:
        return f"GitHub API error: {e.status} - {e.data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error searching code: {str(e)}"


@tool
def read_file_from_repo(
    repo_name: str,
    file_path: str,
    ref: str = "main"
) -> str:
    """Read a specific file from a GitHub repository.
    
    Args:
        repo_name: Full repository name (e.g., "owner/repo")
        file_path: Path to file in repository (e.g., "src/main.py")
        ref: Branch, tag, or commit SHA (default: "main")
    
    Returns:
        File contents as string, or error message
    
    Examples:
        read_file_from_repo("langchain-ai/langchain", "README.md")
        read_file_from_repo("owner/repo", "src/config.py", ref="develop")
    """
    try:
        repo = github_client.get_repo(repo_name)
        
        # Try to get file content
        try:
            file_content = repo.get_contents(file_path, ref=ref)
        except GithubException as e:
            if e.status == 404:
                # Try common alternative branch names
                alternative_refs = ["master", "main", "develop"]
                for alt_ref in alternative_refs:
                    if alt_ref != ref:
                        try:
                            file_content = repo.get_contents(file_path, ref=alt_ref)
                            ref = alt_ref  # Update ref for output
                            break
                        except:
                            continue
                else:
                    return f"File not found: {file_path} (tried ref: {ref})"
            else:
                raise
        
        # Decode content
        if isinstance(file_content, list):
            return f"Error: {file_path} is a directory, not a file"
        
        content = base64.b64decode(file_content.content).decode('utf-8')
        
        # Format output
        output = [
            f"# File: {file_path}",
            f"Repository: {repo_name}",
            f"Branch/Ref: {ref}",
            f"Size: {file_content.size} bytes",
            f"\n{'='*60}\n",
            content
        ]
        
        return "\n".join(output)
        
    except GithubException as e:
        return f"GitHub API error: {e.status} - {e.data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def list_repository_structure(
    repo_name: str,
    path: str = "",
    max_depth: int = 2
) -> str:
    """Get directory tree structure of a GitHub repository.
    
    Args:
        repo_name: Full repository name (e.g., "owner/repo")
        path: Starting path (empty string for root)
        max_depth: Maximum directory depth to explore (default: 2)
    
    Returns:
        Tree structure as formatted string
    
    Examples:
        list_repository_structure("langchain-ai/langchain")
        list_repository_structure("owner/repo", path="src", max_depth=3)
    """
    try:
        repo = github_client.get_repo(repo_name)
        
        def build_tree(current_path: str, depth: int = 0, prefix: str = "") -> list[str]:
            """Recursively build directory tree."""
            if depth > max_depth:
                return []
            
            output = []
            try:
                contents = repo.get_contents(current_path)
                
                # Sort: directories first, then files
                if isinstance(contents, list):
                    dirs = [c for c in contents if c.type == "dir"]
                    files = [c for c in contents if c.type == "file"]
                    contents = sorted(dirs, key=lambda x: x.name) + sorted(files, key=lambda x: x.name)
                else:
                    contents = [contents]
                
                for idx, item in enumerate(contents):
                    is_last = idx == len(contents) - 1
                    connector = "└── " if is_last else "├── "
                    
                    if item.type == "dir":
                        output.append(f"{prefix}{connector}📁 {item.name}/")
                        
                        # Recurse into directory
                        if depth < max_depth:
                            new_prefix = prefix + ("    " if is_last else "│   ")
                            output.extend(build_tree(item.path, depth + 1, new_prefix))
                    else:
                        # File
                        size_str = f"{item.size} bytes" if item.size else ""
                        output.append(f"{prefix}{connector}📄 {item.name} {size_str}")
                
            except GithubException:
                output.append(f"{prefix}└── ⚠️  (access denied or too large)")
            
            return output
        
        # Build and format tree
        header = [
            f"Repository Structure: {repo_name}",
            f"Path: /{path}" if path else "Path: / (root)",
            f"Max Depth: {max_depth}",
            "=" * 60,
            ""
        ]
        
        tree = build_tree(path)
        
        if not tree:
            return "\n".join(header + ["(empty or inaccessible)"])
        
        return "\n".join(header + tree)
        
    except GithubException as e:
        return f"GitHub API error: {e.status} - {e.data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error listing structure: {str(e)}"


@tool
def get_issue_details(
    issue_url: str,
    state: Annotated[GitHubAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """Fetch detailed information about a GitHub issue.
    
    Extracts and saves:
    - Issue title and description
    - Stack traces and error messages
    - Labels and metadata
    - Comments and discussion
    
    Saves detailed information to files for context offloading,
    returns only summary to agent.
    
    Args:
        issue_url: Full GitHub issue URL (e.g., "https://github.com/owner/repo/issues/123")
        state: Injected agent state
        tool_call_id: Injected tool call ID
    
    Returns:
        Command with file updates and summary message
    
    Examples:
        get_issue_details("https://github.com/langchain-ai/langchain/issues/1234")
    """
    try:
        # Parse issue URL
        # Format: https://github.com/owner/repo/issues/number
        parts = issue_url.rstrip('/').split('/')
        
        if 'github.com' not in issue_url or 'issues' not in parts:
            return Command(
                update={
                    "messages": [
                        ToolMessage(
                            f"Invalid GitHub issue URL: {issue_url}",
                            tool_call_id=tool_call_id
                        )
                    ]
                }
            )
        
        # Extract owner, repo, issue number
        issues_idx = parts.index('issues')
        owner = parts[issues_idx - 2]
        repo = parts[issues_idx - 1]
        issue_number = int(parts[issues_idx + 1])
        repo_name = f"{owner}/{repo}"
        
        # Get issue from GitHub
        repository = github_client.get_repo(repo_name)
        issue = repository.get_issue(issue_number)
        
        # Build detailed content
        file_content = [
            f"# GitHub Issue #{issue_number}: {issue.title}",
            f"\n**Repository:** {repo_name}",
            f"**URL:** {issue_url}",
            f"**State:** {issue.state}",
            f"**Created:** {issue.created_at}",
            f"**Author:** {issue.user.login}",
            f"\n## Labels\n",
            ", ".join([label.name for label in issue.labels]) if issue.labels else "No labels",
            f"\n## Description\n",
            issue.body or "(No description provided)",
        ]
        
        # Add comments
        comments = list(issue.get_comments())
        if comments:
            file_content.append(f"\n## Comments ({len(comments)})\n")
            for idx, comment in enumerate(comments[:10], 1):  # Limit to 10 comments
                file_content.append(f"\n### Comment {idx} by {comment.user.login}")
                file_content.append(f"*{comment.created_at}*\n")
                file_content.append(comment.body or "(empty)")
        
        # Save to files
        files = state.get("files", {})
        uid = base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b"=").decode("ascii")[:8]
        filename = f"issue_{issue_number}_{uid}.md"
        files[filename] = "\n".join(file_content)
        
        # Create summary
        summary = [
            f"📋 Issue #{issue_number}: {issue.title}",
            f"   State: {issue.state}",
            f"   Repository: {repo_name}",
            f"   Labels: {', '.join([l.name for l in issue.labels]) if issue.labels else 'None'}",
            f"   Comments: {len(comments)}",
            f"\n💾 Full details saved to: {filename}",
            f"💡 Use read_file('{filename}') to view complete issue details"
        ]
        
        return Command(
            update={
                "files": files,
                "issue_url": issue_url,
                "current_repo": repo_name,
                "messages": [
                    ToolMessage("\n".join(summary), tool_call_id=tool_call_id)
                ]
            }
        )
        
    except GithubException as e:
        error_msg = f"GitHub API error: {e.status} - {e.data.get('message', 'Unknown error')}"
        return Command(
            update={
                "messages": [
                    ToolMessage(error_msg, tool_call_id=tool_call_id)
                ]
            }
        )
    except Exception as e:
        error_msg = f"Error fetching issue: {str(e)}"
        return Command(
            update={
                "messages": [
                    ToolMessage(error_msg, tool_call_id=tool_call_id)
                ]
            }
        )


@tool
def get_repository_info(repo_name: str) -> str:
    """Get basic information about a GitHub repository.
    
    Fetches repository metadata including description, stars, forks,
    open issues, and last update time.
    
    Args:
        repo_name: Repository name in 'owner/repo' format
    
    Returns:
        Formatted repository information
    
    Examples:
        get_repository_info("openai/openai-python")
        get_repository_info("facebook/react")
    """
    # Validate input
    is_valid, error_msg = validate_repo_name(repo_name)
    if not is_valid:
        return f"❌ Invalid repository name\n\n{error_msg}"
    
    try:
        repo = github_client.get_repo(repo_name)
        
        info = f"""# Repository: {repo.full_name}

**Description:** {repo.description or 'No description provided'}
**Stars:** ⭐ {repo.stargazers_count:,}
**Forks:** 🍴 {repo.forks_count:,}
**Open Issues:** 🐛 {repo.open_issues_count}
**Default Branch:** {repo.default_branch}
**Created:** {repo.created_at}
**Last Updated:** {repo.updated_at}
**Size:** {repo.size} KB
**Topics:** {', '.join(repo.get_topics()[:10]) if repo.get_topics() else 'None'}
**License:** {repo.license.name if repo.license else 'Not specified'}
**Language:** {repo.language or 'Not specified'}
**URL:** {repo.html_url}
"""
        return info
        
    except GithubException as e:
        return handle_github_error(e, f"Fetching info for repository '{repo_name}'")
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}\n\n💡 Suggestion: Please report this error if it persists"
