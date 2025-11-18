"""Enhanced error handling utilities for GitHub Agent.

Provides consistent error handling, helpful error messages, and recovery strategies.
"""
from typing import Callable, Any, Optional
import time
from functools import wraps


class AgentError(Exception):
    """Base exception for agent errors with helpful messages."""
    
    def __init__(self, message: str, suggestion: str = "", details: str = ""):
        self.message = message
        self.suggestion = suggestion
        self.details = details
        super().__init__(self.format_error())
    
    def format_error(self) -> str:
        """Format error with helpful information."""
        parts = [f"❌ {self.message}"]
        
        if self.details:
            parts.append(f"\n📋 Details: {self.details}")
        
        if self.suggestion:
            parts.append(f"\n💡 Suggestion: {self.suggestion}")
        
        return "\n".join(parts)


class GitHubAPIError(AgentError):
    """GitHub API related errors."""
    pass


class SearchError(AgentError):
    """Search/research related errors."""
    pass


class ConfigurationError(AgentError):
    """Configuration and setup errors."""
    pass


def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator to retry function on failure with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
    
    Example:
        @retry_on_failure(max_retries=3, delay=1.0, backoff=2.0)
        def fetch_data():
            # If this fails, it will retry up to 3 times
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_retries - 1:
                        # Not the last attempt, wait and retry
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        # Last attempt failed, raise with context
                        raise AgentError(
                            f"Failed after {max_retries} attempts: {str(e)}",
                            suggestion="Check your network connection and API credentials",
                            details=f"Last error: {type(e).__name__}"
                        ) from e
            
            # Should never reach here, but just in case
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def handle_github_error(error: Exception, context: str = "") -> str:
    """Convert GitHub API errors to helpful messages.
    
    Args:
        error: The exception that was raised
        context: Additional context about what was being attempted
    
    Returns:
        User-friendly error message with suggestions
    """
    error_str = str(error).lower()
    
    # Rate limit errors
    if "rate limit" in error_str or "403" in error_str:
        return f"""❌ GitHub API Rate Limit Exceeded
        
📋 Details: {context if context else 'API request failed'}

💡 Suggestions:
   1. Wait a few minutes before trying again
   2. Check your rate limit: https://github.com/settings/tokens
   3. Consider using a GitHub Personal Access Token with higher limits
   
Current error: {str(error)}"""
    
    # Authentication errors
    if "401" in error_str or "authentication" in error_str:
        return f"""❌ GitHub Authentication Failed
        
📋 Details: {context if context else 'Credentials invalid or missing'}

💡 Suggestions:
   1. Check GITHUB_TOKEN in your .env file
   2. Ensure token has required permissions (repo, read:org)
   3. Generate a new token: https://github.com/settings/tokens
   
Current error: {str(error)}"""
    
    # Not found errors
    if "404" in error_str or "not found" in error_str:
        return f"""❌ Resource Not Found
        
📋 Details: {context if context else 'Repository or resource not found'}

💡 Suggestions:
   1. Check the repository name (format: owner/repo)
   2. Verify the repository is public or you have access
   3. Check for typos in the URL or name
   
Current error: {str(error)}"""
    
    # Network errors
    if "timeout" in error_str or "connection" in error_str:
        return f"""❌ Network Connection Issue
        
📋 Details: {context if context else 'Network request failed'}

💡 Suggestions:
   1. Check your internet connection
   2. Try again in a moment
   3. Check if GitHub is accessible: https://www.githubstatus.com/
   
Current error: {str(error)}"""
    
    # Generic error with helpful format
    return f"""❌ GitHub API Error
    
📋 Details: {context if context else 'Request failed'}

💡 Suggestion: Check the error message below for more details

Error: {str(error)}"""


def handle_search_error(error: Exception, query: str = "") -> str:
    """Convert search API errors to helpful messages.
    
    Args:
        error: The exception that was raised
        query: The search query that failed
    
    Returns:
        User-friendly error message with suggestions
    """
    error_str = str(error).lower()
    
    # API key errors
    if "api key" in error_str or "unauthorized" in error_str:
        return f"""❌ Search API Authentication Failed
        
📋 Details: Tavily API key is missing or invalid

💡 Suggestions:
   1. Check TAVILY_API_KEY in your .env file
   2. Sign up for a free API key: https://tavily.com
   3. Ensure no extra spaces or quotes in the key
   
Query attempted: {query}"""
    
    # Rate limit
    if "rate limit" in error_str or "quota" in error_str:
        return f"""❌ Search API Rate Limit Reached
        
📋 Details: Daily search quota exceeded

💡 Suggestions:
   1. Wait until tomorrow for quota reset
   2. Upgrade to a higher tier at https://tavily.com
   3. Use a different search strategy with fewer queries
   
Query attempted: {query}"""
    
    # Generic search error
    return f"""❌ Search Failed
    
📋 Details: Web search could not be completed

💡 Suggestions:
   1. Try simplifying your query
   2. Check your internet connection
   3. Try again in a moment
   
Query: {query}
Error: {str(error)}"""


def validate_repo_name(repo_name: str) -> tuple[bool, str]:
    """Validate GitHub repository name format.
    
    Args:
        repo_name: Repository name to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not repo_name:
        return False, "Repository name cannot be empty"
    
    if "/" not in repo_name:
        return False, f"""Invalid repository format: '{repo_name}'

💡 Expected format: owner/repository
   Examples: 
   - openai/openai-python
   - facebook/react
   - microsoft/vscode"""
    
    parts = repo_name.split("/")
    if len(parts) != 2:
        return False, f"""Invalid repository format: '{repo_name}'

💡 Should contain exactly one '/' separating owner and repository name"""
    
    owner, repo = parts
    if not owner or not repo:
        return False, f"""Invalid repository format: '{repo_name}'

💡 Both owner and repository name must be non-empty"""
    
    return True, ""


def validate_issue_url(url: str) -> tuple[bool, str]:
    """Validate GitHub issue URL format.
    
    Args:
        url: Issue URL to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not url:
        return False, "Issue URL cannot be empty"
    
    if "github.com" not in url:
        return False, f"""Invalid GitHub URL: '{url}'

💡 Must be a GitHub URL
   Example: https://github.com/owner/repo/issues/123"""
    
    if "/issues/" not in url and "/pull/" not in url:
        return False, f"""URL doesn't appear to be a GitHub issue or PR: '{url}'

💡 Expected formats:
   - https://github.com/owner/repo/issues/123
   - https://github.com/owner/repo/pull/456"""
    
    return True, ""
