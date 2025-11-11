"""Search tools for web research and error investigation.

Provides tools for searching the web using Tavily API, with automatic
context offloading to files. Based on the deep research agent pattern.
"""
from typing import Annotated, Literal
import uuid
import base64
import os
from datetime import datetime

import httpx
from tavily import TavilyClient
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage, HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import InjectedState, InjectedToolCallId
from langgraph.types import Command
from markdownify import markdownify
from pydantic import BaseModel, Field

from src.config import Config
from src.state import GitHubAgentState


# Initialize clients
tavily_client = TavilyClient(api_key=Config.TAVILY_API_KEY)
summarization_model = init_chat_model(model="openai:gpt-4o-mini")


# Summarization schema
class Summary(BaseModel):
    """Schema for webpage content summarization."""
    filename: str = Field(description="Descriptive filename for this content")
    summary: str = Field(description="Key learnings from the webpage")


def get_today_str() -> str:
    """Get current date in human-readable format."""
    return datetime.now().strftime("%a %b %d, %Y")


SUMMARIZE_PROMPT = """You are analyzing web search results about programming errors and solutions.

**Your task:** Create a concise summary of the key information from this webpage.

**Content:**
{content}

**Your summary should include:**
1. Main topic or problem being addressed
2. Key takeaways or solutions mentioned
3. Any code examples or specific fixes
4. Relevant version information or library names

**Filename:** Choose a descriptive filename (lowercase, underscores, .md extension)
Example: oauth_token_error_fix.md, langchain_streaming_issue.md

**Date:** {date}

Keep the summary focused and actionable."""


def summarize_webpage_content(content: str) -> Summary:
    """Summarize webpage content using LLM.
    
    Args:
        content: Raw webpage content
        
    Returns:
        Summary object with filename and summary
    """
    try:
        structured_model = summarization_model.with_structured_output(Summary)
        
        result = structured_model.invoke([
            HumanMessage(content=SUMMARIZE_PROMPT.format(
                content=content[:4000],  # Limit content length
                date=get_today_str()
            ))
        ])
        
        return result
    except Exception:
        # Fallback summary
        return Summary(
            filename="search_result.md",
            summary=content[:500] + "..." if len(content) > 500 else content
        )


def process_search_results(results: dict) -> list[dict]:
    """Process Tavily search results and generate summaries.
    
    Args:
        results: Tavily search results dictionary
        
    Returns:
        List of processed results with summaries
    """
    processed = []
    httpx_client = httpx.Client(timeout=30.0)
    
    for result in results.get('results', []):
        url = result['url']
        
        try:
            response = httpx_client.get(url)
            
            if response.status_code == 200:
                # Convert HTML to markdown
                raw_content = markdownify(response.text)
                summary_obj = summarize_webpage_content(raw_content)
            else:
                # Use Tavily's summary
                raw_content = result.get('content', '')
                summary_obj = Summary(
                    filename="url_error.md",
                    summary=result.get('content', 'Error fetching URL')
                )
        except (httpx.TimeoutException, httpx.RequestError):
            raw_content = result.get('content', '')
            summary_obj = Summary(
                filename="connection_error.md",
                summary=result.get('content', 'Connection error')
            )
        
        # Add unique ID to filename
        uid = base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b"=").decode("ascii")[:8]
        name, ext = os.path.splitext(summary_obj.filename)
        summary_obj.filename = f"{name}_{uid}{ext}"
        
        processed.append({
            'url': url,
            'title': result.get('title', 'No title'),
            'summary': summary_obj.summary,
            'filename': summary_obj.filename,
            'raw_content': raw_content
        })
    
    return processed


@tool
def search_error_solution(
    error_message: str,
    state: Annotated[GitHubAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    library_name: str = "",
    max_results: Annotated[int, 3] = 3
) -> Command:
    """Search for solutions to programming errors and bugs.
    
    Performs web search for error messages, stack traces, and known issues.
    Saves full results to files for context offloading, returns summary.
    
    This is your primary tool for researching unknown errors and finding
    solutions from StackOverflow, GitHub issues, and documentation.
    
    Args:
        error_message: The error message, exception, or stack trace to search for
        library_name: Optional library/framework name for context (e.g., 'langchain', 'oauth2')
        max_results: Number of search results to retrieve (default: 3)
    
    Returns:
        Command with file updates and summary message
    
    Example:
        search_error_solution("KeyError: 'access_token' OAuth2", library_name="requests")
    """
    try:
        # Build search query
        if library_name:
            query = f"{library_name} {error_message}"
        else:
            query = error_message
        
        # Add programming context
        query += " programming error solution"
        
        # Execute search
        results = tavily_client.search(
            query,
            max_results=max_results,
            include_raw_content=True,
            topic="general"
        )
        
        # Process results
        processed_results = process_search_results(results)
        
        # Save to files
        files = state.get("files", {})
        saved_files = []
        summaries = []
        
        for result in processed_results:
            filename = result['filename']
            
            file_content = f"""# Search Result: {result['title']}

**URL:** {result['url']}
**Query:** {query}
**Date:** {get_today_str()}

## Summary
{result['summary']}

## Full Content
{result['raw_content'] if result['raw_content'] else 'No content available'}
"""
            
            files[filename] = file_content
            saved_files.append(filename)
            summaries.append(f"- **{filename}**: {result['summary'][:100]}...")
        
        # Create summary message
        summary_text = f"""🔍 Found {len(processed_results)} results for error: "{error_message[:50]}..."

{chr(10).join(summaries)}

**Files saved:** {', '.join(saved_files)}
💡 Use read_file('filename') to access full details when needed.
"""
        
        return Command(update={
            "files": files,
            "messages": [ToolMessage(summary_text, tool_call_id=tool_call_id)]
        })
        
    except Exception as e:
        error_msg = f"❌ Error performing search: {str(e)}"
        return Command(update={
            "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
        })


@tool
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.
    
    Use this tool to pause and think about your progress. This creates a
    deliberate pause in your workflow for quality decision-making.
    
    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?
    
    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples?
    4. Strategic decision - Should I continue searching or provide my answer?
    
    Args:
        reflection: Your detailed reflection on progress, findings, gaps, and next steps
    
    Returns:
        Confirmation that reflection was recorded
        
    Example:
        think_tool("Found 3 solutions for OAuth error. All mention missing token validation.
                   Have enough information to propose a fix. Ready to synthesize findings.")
    """
    return f"💭 Reflection recorded: {reflection}"


# Export all tools
__all__ = ['search_error_solution', 'think_tool']
