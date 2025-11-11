"""State management for GitHub Repository Analyzer Agent.

Defines the state schema used across the agent system.
"""
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class GitHubAgentState(TypedDict):
    """State schema for the GitHub analyzer agent.
    
    This state is passed between agent nodes and maintains context
    throughout the execution.
    
    Attributes:
        messages: Conversation history with add_messages reducer
        files: Virtual file system for context offloading (filename -> content)
        todos: List of tasks to track progress
        current_repo: Currently analyzed repository (owner/repo format)
        issue_url: GitHub issue URL being analyzed
        analysis_results: Structured results from investigations
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    files: dict[str, str]
    todos: list[str]
    current_repo: str | None
    issue_url: str | None
    analysis_results: dict


def get_initial_state() -> GitHubAgentState:
    """Create an initial empty state.
    
    Returns:
        GitHubAgentState: Fresh state with empty collections
    """
    return {
        "messages": [],
        "files": {},
        "todos": [],
        "current_repo": None,
        "issue_url": None,
        "analysis_results": {}
    }
