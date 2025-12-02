"""GitHub Analyzer Agent for LangGraph Studio

Auto-generated from notebook. Load this file in LangGraph Studio.
"""
import os
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, add_messages
from langgraph.prebuilt import ToolNode
from github import Github
from langsmith import traceable
import base64
from datetime import datetime

load_dotenv(override=True)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "GitHub-Analyzer-Studio"

github_client = Github(os.getenv("GITHUB_TOKEN"))

class GitHubAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    files: dict[str, str]
    current_repo: str | None
    remaining_steps: int

@tool
@traceable
def get_repository_info(repo_name: str) -> str:
    """Get basic information about a GitHub repository."""
    try:
        repo = github_client.get_repo(repo_name)
        return (
            f"# {repo.full_name}\n"
            f"⭐ {repo.stargazers_count:,} stars | 🍴 {repo.forks_count:,} forks\n"
            f"{repo.description or 'No description'}\n"
            f"Language: {repo.language}\n"
            f"{repo.html_url}"
        )
    except Exception as e:
        return f"Error: {e}"

@tool
@traceable
def list_repository_structure(repo_name: str, path: str = "", max_depth: int = 2) -> str:
    """Get directory tree of a repository."""
    try:
        repo = github_client.get_repo(repo_name)
        contents = repo.get_contents(path)
        if isinstance(contents, list):
            items = [f"{'📁' if c.type=='dir' else '📄'} {c.name}" for c in contents[:20]]
            return f"Contents of {repo_name}/{path or 'root'}:\n" + "\n".join(items)
        return str(contents)
    except Exception as e:
        return f"Error: {e}"

@tool
@traceable
def read_file_from_repo(repo_name: str, file_path: str, ref: str = "main") -> str:
    """Read a file from a repository."""
    try:
        repo = github_client.get_repo(repo_name)
        try:
            file_content = repo.get_contents(file_path, ref=ref)
        except:
            file_content = repo.get_contents(file_path, ref="master")
        content = base64.b64decode(file_content.content).decode('utf-8')
        return f"# {file_path}\n{'='*60}\n{content}"
    except Exception as e:
        return f"Error: {e}"

# Initialize model and tools
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [get_repository_info, list_repository_structure, read_file_from_repo]

# Bind tools to the model
model_with_tools = model.bind_tools(tools)

# System prompt
SYSTEM_PROMPT = f"""GitHub Repository Analyzer Agent
Date: {datetime.now().strftime('%Y-%m-%d')}

Analyze GitHub repositories using available tools.
Be concise and use tools before answering.
"""

# Define the agent node
@traceable(name="agent_node")
def agent_node(state: GitHubAgentState) -> dict:
    """The agent node that calls the LLM."""
    messages = list(state["messages"])
    
    # Prepend system message if not already present
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

# Define the conditional edge function
def should_continue(state: GitHubAgentState) -> str:
    """Determine if we should continue to tools or end."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the LLM made tool calls, route to tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    # Otherwise, end
    return END

# Create the tool node
tool_node = ToolNode(tools)

# Build the graph manually
workflow = StateGraph(GitHubAgentState)

# Add nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Set entry point
workflow.set_entry_point("agent")

# Add conditional edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

# Tools always go back to agent
workflow.add_edge("tools", "agent")

# Compile the graph - this 'graph' variable will be detected by LangGraph Studio
graph = workflow.compile()
