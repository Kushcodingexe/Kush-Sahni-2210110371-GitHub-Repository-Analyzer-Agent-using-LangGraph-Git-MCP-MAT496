"""
Example: Analyze a GitHub Issue

This example shows how to use the agent to analyze a GitHub issue
and get investigation findings.
"""
from src.main import analyze_issue


def main():
    """Analyze a GitHub issue and print the results."""
    
    # Example issue URL
    # Replace with any real GitHub issue you want to analyze
    issue_url = "https://github.com/langchain-ai/langchain/issues/1"
    
    print(f"🔍 Analyzing issue: {issue_url}\n")
    
    # Analyze the issue
    # This will:
    # 1. Fetch issue details from GitHub
    # 2. Extract error information
    # 3. Search for relevant code
    # 4. Research potential solutions
    # 5. Generate a comprehensive report
    result = analyze_issue(issue_url)
    
    # Extract the final response
    if result and "messages" in result:
        # Get the last AI message
        messages = result["messages"]
        for msg in reversed(messages):
            if hasattr(msg, 'content'):
                print("📋 Analysis Results:")
                print("=" * 60)
                print(msg.content)
                break
    else:
        print("❌ Analysis failed or returned no results")
    
    # Print file system contents (context offloading)
    if "files" in result and result["files"]:
        print("\n" + "=" * 60)
        print(f"💾 Files created: {len(result['files'])}")
        for filename in result["files"].keys():
            print(f"  - {filename}")


if __name__ == "__main__":
    main()
