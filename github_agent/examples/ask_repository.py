"""
Example: Ask Questions About a Repository

This example shows how to query information about any GitHub repository.
"""
from src.main import ask_about_repository


def main():
    """Ask questions about a repository and print answers."""
    
    # Example repository
    repo_name = "openai/openai-python"
    
    # Example questions to ask
    questions = [
        "What is this repository about?",
        "How is the project structured?",
        "Where is the ChatCompletion class defined?",
    ]
    
    print(f"🔍 Querying repository: {repo_name}\n")
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"Question {i}: {question}")
        print('='*60)
        
        # Ask the question
        result = ask_about_repository(repo_name, question)
        
        # Extract the answer
        if result and "messages" in result:
            for msg in reversed(result["messages"]):
                if hasattr(msg, 'content'):
                    print(f"\n{msg.content}")
                    break
        else:
            print("❌ Query failed or returned no results")
    
    print("\n" + "="*60)
    print("✅ All queries complete!")


if __name__ == "__main__":
    main()
