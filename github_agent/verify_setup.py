"""Quick setup verification script.

Run this to verify that your environment is configured correctly.
"""
from src.config import Config


def main():
    print("\n" + "="*60)
    print("  GitHub Repository Analyzer Agent - Setup Verification")
    print("="*60)
    
    Config.print_config()
    
    if Config.validate():
        print("✅ Configuration valid! You're ready to start development.")
        print("\nNext steps:")
        print("  1. Review implementation_plan.md for development roadmap")
        print("  2. Start implementing Phase 2 (Core Tool Development)")
        print("  3. Test with: python -m src.main")
    else:
        print("❌ Configuration incomplete. Please update your .env file.")
        print("\nRequired:")
        print("  - GITHUB_TOKEN")
        print("  - TAVILY_API_KEY")
        print("  - Either OPENAI_API_KEY or ANTHROPIC_API_KEY")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
