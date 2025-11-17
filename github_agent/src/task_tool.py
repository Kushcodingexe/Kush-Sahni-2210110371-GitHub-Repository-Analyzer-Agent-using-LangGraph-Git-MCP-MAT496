"""Task delegation tool for sub-agent orchestration.

Based on the reference notebook's task delegation pattern.
"""
from typing import Annotated, Any
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent, InjectedState

from src.state import GitHubAgentState


def _create_task_tool(all_tools: list, sub_agents: list, model: Any, state_schema: type):
    """Create a task delegation tool for sub-agents.
    
    This follows the reference notebook pattern for delegating tasks to
    specialized sub-agents with isolated contexts.
    
    Args:
        all_tools: List of all available tools
        sub_agents: List of sub-agent configurations
        model: The LLM model to use
        state_schema: State schema class
    
    Returns:
        Task delegation tool
    """
    
    # Create mapping of sub-agent names to configurations
    sub_agent_map = {agent["name"]: agent for agent in sub_agents}
    
    # Create tool name to tool object mapping
    tool_map = {tool.name: tool for tool in all_tools}
    
    @tool(parse_docstring=True)
    def task(
        description: str,
        subagent_type: str,
        state: Annotated[GitHubAgentState, InjectedState]
    ) -> str:
        """Delegate a research task to a specialized sub-agent.
        
        Use this to offload focused investigations to sub-agents with
        isolated contexts. Each sub-agent is an expert in its domain.
        
        Available sub-agents:
        - "repo-investigator": Investigates repository structure and code
        - "error-researcher": Researches errors and finds solutions
        
        The sub-agent will conduct research independently and return findings.
        Results are saved to the shared file system for later access.
        
        Args:
            description: Clear, specific task description for the sub-agent.
                        Should be a standalone research question.
            subagent_type: Type of sub-agent to use ("repo-investigator" or 
                          "error-researcher")
        
        Returns:
            Summary of sub-agent's findings
        
        Examples:
            task("Find where the OAuth callback is handled in the code", 
                 "repo-investigator")
            
            task("Research solutions for KeyError: 'access_token' in OAuth2", 
                 "error-researcher")
        """
        # Validate sub-agent type
        if subagent_type not in sub_agent_map:
            available = ", ".join(sub_agent_map.keys())
            return f"❌ Unknown sub-agent type: {subagent_type}. Available: {available}"
        
        # Get sub-agent configuration
        agent_config = sub_agent_map[subagent_type]
        
        # Get tools for this sub-agent
        agent_tool_names = agent_config["tools"]
        agent_tools = [tool_map[name] for name in agent_tool_names if name in tool_map]
        
        if not agent_tools:
            return f"❌ No tools available for {subagent_type}"
        
        # Create sub-agent (with state schema for validation)
        try:
            sub_agent = create_react_agent(
                model,
                agent_tools,
                state_schema=state_schema
            )
        except Exception as e:
            return f"❌ Failed to create sub-agent: {str(e)}"
        
        # Prepare initial state for sub-agent (isolated context)
        # Must include ALL required fields from GitHubAgentState
        sub_agent_state = {
            "messages": [HumanMessage(content=description)],
            "files": state.get("files", {}).copy(),  # Share files for context
            "todos": [],  # Sub-agent gets its own TODOs
            "current_repo": state.get("current_repo", ""),
            "issue_url": state.get("issue_url", ""),
            "analysis_results": {},
            "remaining_steps": 10  # Limit sub-agent iterations
        }

        
        # Execute sub-agent
        try:
            result = sub_agent.invoke(sub_agent_state)
            
            # Merge files back to parent state (context offloading)
            state["files"].update(result.get("files", {}))
            
            # Extract final response from sub-agent
            if result.get("messages"):
                # Get last AI message
                for msg in reversed(result["messages"]):
                    if isinstance(msg, AIMessage):
                        findings = msg.content
                        break
                else:
                    findings = "Sub-agent completed but provided no response."
            else:
                findings = "Sub-agent completed but provided no response."
            
            # Format output
            output = [
                f"📋 Sub-Agent Report: {subagent_type}",
                f"Task: {description}",
                f"\n{findings}",
                f"\n💾 Files updated: {len(result.get('files', {}))} files in system"
            ]
            
            return "\n".join(output)
            
        except Exception as e:
            return f"❌ Sub-agent execution failed: {str(e)}"
    
    return task
