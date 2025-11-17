"""Main agent orchestration for GitHub Repository Analyzer.

This module creates the main coordinating agent that delegates to sub-agents.
"""
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

from src.config import Config
from src.state import GitHubAgentState
from src.prompts import (
    REPO_INVESTIGATOR_PROMPT,
    ERROR_RESEARCHER_PROMPT,
    MAIN_AGENT_INSTRUCTIONS,
    TODO_USAGE_INSTRUCTIONS,
    FILE_USAGE_INSTRUCTIONS,
    SUBAGENT_USAGE_INSTRUCTIONS,
    get_today_str,
)
from src.task_tool import _create_task_tool

# Import all tools
from src.tools import (
    # GitHub tools
    search_code_in_repo,
    read_file_from_repo,
    list_repository_structure,
    get_issue_details,
    get_repository_info,
    # Search tools
    search_error_solution,
    search_documentation,
    # File tools
    ls,
    read_file,
    write_file,
    # Analysis tools
    extract_stack_trace,
    think_tool,
    parse_error_from_issue,
    # TODO tools
    write_todos,
    read_todos,
    mark_todo_done,
)


# Initialize model
model = init_chat_model(
    model=Config.DEFAULT_MODEL,
    temperature=0.0
)

# Agent limits from config
MAX_CONCURRENT_RESEARCH_UNITS = Config.MAX_CONCURRENT_RESEARCH_UNITS
MAX_RESEARCHER_ITERATIONS = Config.MAX_RESEARCHER_ITERATIONS

# ============================================================================
# TOOLS ORGANIZATION
# ============================================================================

# Tools for sub-agents
sub_agent_tools = [
    search_code_in_repo,
    read_file_from_repo,
    list_repository_structure,
    search_error_solution,
    search_documentation,
    think_tool,
    read_file,  # Sub-agents can read from shared file system
]

# Tools available to main agent directly
built_in_tools = [
    # GitHub tools (direct access)
    search_code_in_repo,
    read_file_from_repo,
    list_repository_structure,
    get_issue_details,
    get_repository_info,
    # File system
    ls,
    read_file,
    write_file,
    # Analysis
    extract_stack_trace,
    parse_error_from_issue,
    # TODO management
    write_todos,
    read_todos,
    mark_todo_done,
    # Reflection
    think_tool,
]

# ============================================================================
# SUB-AGENT CONFIGURATIONS
# ============================================================================

repo_investigator_agent = {
    "name": "repo-investigator",
    "description": "Investigates repository structure and locates code",
    "prompt": REPO_INVESTIGATOR_PROMPT.format(date=get_today_str()),
    "tools": [
        "search_code_in_repo",
        "read_file_from_repo",
        "list_repository_structure",
        "think_tool",
        "read_file",
    ],
}

error_researcher_agent = {
    "name": "error-researcher",
    "description": "Researches errors and finds solutions online",
    "prompt": ERROR_RESEARCHER_PROMPT.format(date=get_today_str()),
    "tools": [
        "search_error_solution",
        "search_documentation",
        "think_tool",
        "read_file",
    ],
}

sub_agents = [repo_investigator_agent, error_researcher_agent]

# ============================================================================
# CREATE TASK DELEGATION TOOL
# ============================================================================

task_tool = _create_task_tool(
    all_tools=sub_agent_tools,
    sub_agents=sub_agents,
    model=model,
    state_schema=GitHubAgentState
)

# ============================================================================
# MAIN AGENT
# ============================================================================

delegation_tools = [task_tool]
all_main_agent_tools = built_in_tools + delegation_tools

# Build main agent prompt
FULL_MAIN_PROMPT = (
    MAIN_AGENT_INSTRUCTIONS.format(date=get_today_str())
    + "\n\n"
    + "="*80
    + "\n\n"
    + "# TODO MANAGEMENT\n"
    + TODO_USAGE_INSTRUCTIONS
    + "\n\n"
    + "="*80
    + "\n\n"
    + "# FILE SYSTEM USAGE\n"
    + FILE_USAGE_INSTRUCTIONS
    + "\n\n"
    + "="*80
    + "\n\n"
    + "# SUB-AGENT DELEGATION\n"
    + SUBAGENT_USAGE_INSTRUCTIONS.format(
        max_concurrent_research_units=MAX_CONCURRENT_RESEARCH_UNITS,
        max_researcher_iterations=MAX_RESEARCHER_ITERATIONS,
    )
)

# Create main agent (with state schema for proper validation)
main_agent = create_react_agent(
    model,
    all_main_agent_tools,
    state_schema=GitHubAgentState
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def analyze_issue(issue_url: str) -> dict:
    """Analyze a GitHub issue.
    
    Args:
        issue_url: Full GitHub issue URL
    
    Returns:
        Agent execution result
    """
    from src.state import get_initial_state
    from langchain_core.messages import HumanMessage
    
    initial_state = get_initial_state()
    initial_state["messages"] = [
        HumanMessage(content=f"Analyze this GitHub issue and provide a comprehensive investigation report: {issue_url}")
    ]
    initial_state["issue_url"] = issue_url
    
    result = main_agent.invoke(initial_state)
    return result


def ask_about_repository(repo_name: str, question: str) -> dict:
    """Ask a question about a GitHub repository.
    
    Args:
        repo_name: Repository name (owner/repo format)
        question: Question to ask
    
    Returns:
        Agent execution result
    """
    from src.state import get_initial_state
    from langchain_core.messages import HumanMessage
    
    initial_state = get_initial_state()
    initial_state["messages"] = [
        HumanMessage(content=f"Repository: {repo_name}\n\nQuestion: {question}")
    ]
    initial_state["current_repo"] = repo_name
    
    result = main_agent.invoke(initial_state)
    return result


def interactive_session():
    """Start an interactive session with the agent."""
    from src.state import get_initial_state
    from langchain_core.messages import HumanMessage
    
    print("\n" + "="*70)
    print("  GitHub Repository Analyzer - Interactive Mode")
    print("="*70)
    print("\nType 'exit' or 'quit' to end the session.\n")
    
    state = get_initial_state()
    
    while True:
        try:
            user_input = input("\n🧑 You: ")
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            if not user_input.strip():
                continue
            
            # Add user message to state
            state["messages"].append(HumanMessage(content=user_input))
            
            # Get agent response
            print("\n🤖 Agent: ", end="", flush=True)
            result = main_agent.invoke(state)
            
            # Update state with result
            state = result
            
            # Print last AI message
            for msg in reversed(result.get("messages", [])):
                if hasattr(msg, 'content') and msg.content:
                    print(msg.content)
                    break
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "issue" and len(sys.argv) > 2:
            # Analyze issue
            issue_url = sys.argv[2]
            print(f"\n🔍 Analyzing issue: {issue_url}\n")
            result = analyze_issue(issue_url)
            print("\n✅ Analysis complete!")
            
        elif command == "ask" and len(sys.argv) > 3:
            # Ask about repository
            repo_name = sys.argv[2]
            question = " ".join(sys.argv[3:])
            print(f"\n🔍 Asking about {repo_name}: {question}\n")
            result = ask_about_repository(repo_name, question)
            print("\n✅ Analysis complete!")
            
        elif command == "interactive":
            interactive_session()
            
        else:
            print("Usage:")
            print("  python -m src.main issue <issue_url>")
            print("  python -m src.main ask <repo_name> <question>")
            print("  python -m src.main interactive")
    else:
        # Default: interactive mode
        interactive_session()
