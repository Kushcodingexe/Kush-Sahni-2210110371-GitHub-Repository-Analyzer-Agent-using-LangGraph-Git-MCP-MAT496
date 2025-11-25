"""
Example: Custom Workflow with Direct Tool Usage

This example shows how to use the agent's tools directly for custom workflows.
"""
from src.state import get_initial_state
from src.tools import (
    get_repository_info,
    search_code_in_repo,
    read_file_from_repo,
    write_todos,
    read_todos,
)


def custom_research_workflow(repo_name: str, search_term: str):
    """
    Custom workflow that demonstrates direct tool usage.
    
    This workflow:
    1. Gets repository information
    2. Creates a TODO list
    3. Searches for code
    4. Reads relevant files
    5. Summarizes findings
    """
    print(f"🔬 Starting custom research on: {repo_name}\n")
    
    # Initialize state
    state = get_initial_state()
    state["current_repo"] = repo_name
    
    # Step 1: Get repository information
    print("📊 Step 1: Fetching repository info...")
    repo_info = get_repository_info(repo_name)
    print(repo_info[:200] + "...\n")  # Print first 200 chars
    
    # Step 2: Create TODO list
    print("📝 Step 2: Creating research plan...")
    todos = [
        f"Search for '{search_term}' in the codebase",
        "Identify relevant files",
        "Analyze code patterns",
        "Document findings"
    ]
    
    todos_result = write_todos.invoke({
        "todos_list": todos,
        "state": state
    })
    print(todos_result + "\n")
    
    # Step 3: Search for code
    print(f"🔍 Step 3: Searching for '{search_term}'...")
    search_results = search_code_in_repo(repo_name, search_term, max_results=3)
    print(search_results + "\n")
    
    # Step 4: Read a file (if search found results)
    # Note: In real usage, you'd parse search results to get actual file path
    print("📄 Step 4: Reading example file (README.md)...")
    try:
        file_content = read_file_from_repo(repo_name, "README.md")
        print(file_content[:300] + "...\n")  # Print first 300 chars
    except Exception as e:
        print(f"Could not read file: {e}\n")
    
    # Step 5: Check TODOs
    print("✅ Step 5: Checking TODO progress...")
    current_todos = read_todos.invoke({"state": state})
    print(current_todos)
    
    print("\n" + "="*60)
    print("🎉 Custom workflow complete!")
    print("="*60)


def main():
    """Run custom workflow examples."""
    
    # Example 1: Research authentication implementation
    print("Example 1: Research authentication\n")
    custom_research_workflow(
        repo_name="openai/openai-python",
        search_term="authentication"
    )
    
    print("\n\n")
    
    # Example 2: Research error handling
    print("Example 2: Research error handling\n")
    custom_research_workflow(
        repo_name="langchain-ai/langchain",
        search_term="error handling"
    )


if __name__ == "__main__":
    main()
