"""Search tools using Tavily AI for web research.

Based on the deep research agent pattern with context offloading.
"""
from typing import Annotated, Literal
from langchain_core.tools import tool, InjectedToolArg, InjectedToolCallId
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from tavily import TavilyClient
import httpx
from markdownify import markdownify
import base64
import uuid
import os
from datetime import datetime

from src.config import Config
from src.state import GitHubAgentState


# Initialize clients
tavily_client = TavilyClient(api_key=Config.TAVILY_API_KEY)
summarization_model = init_chat_model(model="openai:gpt-4o-mini")


class Summary(BaseModel):
    """Schema for webpage content summarization."""
    filename: str = Field(description="Name of the file to store.")
    summary: str = Field(description="Key learnings from the webpage.")


def get_today_str() -> str:
    """Get current date in a human-readable format."""
    return datetime.now().strftime("%a %b %d, %Y")


SUMMARIZE_WEB_SEARCH = """You are summarizing a webpage from a search result.

Today's date: {date}

Webpage content:
{webpage_content}

Create a concise summary focusing on:
1. Main technical points
2. Relevant code examples or solutions
3. Key takeaways for developers

Also generate a descriptive filename (lowercase, underscores, .md extension).
"""


def run_tavily_search(
    search_query: str,
    max_results: int = 3,
    topic: Literal["general", "news"] = "general",
    include_raw_content: bool = True,
) -> dict:
    """Perform search using Tavily API.
    
    Args:
        search_query: Search query to execute
        max_results: Maximum number of results per query  
        topic: Topic filter for search results
        include_raw_content: Whether to include raw webpage content
    
    Returns:
        Search results dictionary
    """
    result = tavily_client.search(
        search_query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic
    )
    return result


def summarize_webpage_content(webpage_content: str) -> Summary:
    """Summarize webpage content using GPT-4o-mini.
    
    Args:
        webpage_content: Raw webpage content to summarize
    
    Returns:
        Summary object with filename and summary
    """
    try:
        structured_model = summarization_model.with_structured_output(Summary)
        
        summary_and_filename = structured_model.invoke([
            HumanMessage(content=SUMMARIZE_WEB_SEARCH.format(
                webpage_content=webpage_content,
                date=get_today_str()
            ))
        ])
        
        return summary_and_filename
        
    except Exception:
        # Return basic summary on failure
        return Summary(
            filename="search_result.md",
            summary=webpage_content[:1000] + "..." if len(webpage_content) > 1000 else webpage_content
        )


def process_search_results(results: dict) -> list[dict]:
    """Process search results by fetching and summarizing content.
    
    Args:
        results: Tavily search results dictionary
    
    Returns:
        List of processed results with summaries
    """
    processed_results = []
    
    # Create HTTP client with timeout
    httpx_client = httpx.Client(timeout=30.0)
    
    for result in results.get('results', []):
        url = result['url']
        
        # Try to read URL
        try:
            response = httpx_client.get(url)
            
            if response.status_code == 200:
                # Convert HTML to markdown
                raw_content = markdownify(response.text)
                summary_obj = summarize_webpage_content(raw_content)
            else:
                # Use Tavily's summary
                raw_content = result.get('raw_content', '')
                summary_obj = Summary(
                    filename="url_error.md",
                    summary=result.get('content', 'Error reading URL; try another search.')
                )
        except (httpx.TimeoutException, httpx.RequestError):
            # Handle errors gracefully
            raw_content = result.get('raw_content', '')
            summary_obj = Summary(
                filename="connection_error.md",
                summary=result.get('content', 'Could not fetch URL. Try another search.')
            )
        
        # Uniquify filenames
        uid = base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b"=").decode("ascii")[:8]
        name, ext = os.path.splitext(summary_obj.filename)
        summary_obj.filename = f"{name}_{uid}{ext}"
        
        processed_results.append({
            'url': result['url'],
            'title': result['title'],
            'summary': summary_obj.summary,
            'filename': summary_obj.filename,
            'raw_content': raw_content,
        })
    
    httpx_client.close()
    return processed_results


@tool(parse_docstring=True)
def search_error_solution(
    error_message: str,
    library_name: str = "",
    state: Annotated[GitHubAgentState, InjectedState] = None,
    tool_call_id: Annotated[str, InjectedToolCallId] = None,
    max_results: Annotated[int, InjectedToolArg] = 3,
) -> Command:
    """Search for solutions to programming errors and bugs.
    
    Performs web search for error messages, stack traces, and solutions.
    Saves full results to files (context offloading) and returns summary.
    
    Use this when:
    - Investigating error messages from issues
    - Looking for known solutions to bugs
    - Researching library-specific problems
    
    Args:
        error_message: The error message or stack trace
        library_name: Optional library/framework name for context
        max_results: Maximum search results (default: 3)
    
    Returns:
        Command with file updates and summary message
    
    Examples:
        search_error_solution("KeyError: 'access_token'", "oauth2")
        search_error_solution("TypeError: 'NoneType' object is not subscriptable")
    """
    # Build search query
    query_parts = [error_message]
    if library_name:
        query_parts.append(library_name)
    query_parts.append("solution fix")
    
    search_query = " ".join(query_parts)
    
    # Execute search
    search_results = run_tavily_search(
        search_query,
        max_results=max_results,
        topic="general",
        include_raw_content=True
    )
    
    # Process and summarize results
    processed_results = process_search_results(search_results)
    
    # Save to files
    files = state.get("files", {})
    saved_files = []
    summaries = []
    
    for i, result in enumerate(processed_results):
        filename = result['filename']
        
        # Create file content
        file_content = f"""# Search Result: {result['title']}

**URL:** {result['url']}
**Query:** {search_query}
**Date:** {get_today_str()}

## Summary
{result['summary']}

## Raw Content
{result['raw_content'] if result['raw_content'] else 'No raw content available'}
"""
        
        files[filename] = file_content
        saved_files.append(filename)
        summaries.append(f"- {filename}: {result['summary'][:100]}...")
    
    # Create summary for tool message  
    summary_text = f"""🔍 Found {len(processed_results)} result(s) for error: "{error_message[:50]}..."

{chr(10).join(summaries)}

Files: {', '.join(saved_files)}
💡 Use read_file() to access full details when needed."""
    
    return Command(
        update={
            "files": files,
            "messages": [
                ToolMessage(summary_text, tool_call_id=tool_call_id)
            ],
        }
    )


@tool(parse_docstring=True)
def search_documentation(
    topic: str,
    library_name: str = "",
    state: Annotated[GitHubAgentState, InjectedState] = None,
    tool_call_id: Annotated[str, InjectedToolCallId] = None,
    max_results: Annotated[int, InjectedToolArg] = 2,
) -> Command:
    """Search for official documentation and guides.
    
    Use this to find:
    - API documentation
    - Usage guides
    - Best practices
    - Official tutorials
    
    Args:
        topic: What to search for
        library_name: Library/framework name
        max_results: Maximum results (default: 2)
    
    Returns:
        Command with file updates and summary
    
    Examples:
        search_documentation("authentication flow", "OAuth2")
        search_documentation("async/await usage", "Python asyncio")
    """
    # Build search query
    query_parts = [topic]
    if library_name:
        query_parts.append(library_name)
    query_parts.append("documentation official guide")
    
    search_query = " ".join(query_parts)
    
    # Execute search
    search_results = run_tavily_search(
        search_query,
        max_results=max_results,
        topic="general",
        include_raw_content=True
    )
    
    # Process results
    processed_results = process_search_results(search_results)
    
    # Save to files
    files = state.get("files", {})
    saved_files = []
    summaries = []
    
    for result in processed_results:
        filename = result['filename']
        
        file_content = f"""# Documentation: {result['title']}

**URL:** {result['url']}
**Topic:** {topic}
**Date:** {get_today_str()}

## Summary
{result['summary']}

## Content
{result['raw_content'] if result['raw_content'] else 'No content available'}
"""
        
        files[filename] = file_content
        saved_files.append(filename)
        summaries.append(f"- {filename}: {result['summary'][:100]}...")
    
    summary_text = f"""📚 Found {len(processed_results)} documentation result(s) for "{topic}"

{chr(10).join(summaries)}

Files: {', '.join(saved_files)}
💡 Use read_file() to view full documentation."""
    
    return Command(
        update={
            "files": files,
            "messages": [
                ToolMessage(summary_text, tool_call_id=tool_call_id)
            ],
        }
    )
