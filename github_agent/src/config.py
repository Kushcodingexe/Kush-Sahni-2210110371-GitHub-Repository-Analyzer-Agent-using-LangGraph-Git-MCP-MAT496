"""Configuration module for GitHub Repository Analyzer Agent.

Loads environment variables and provides configuration access.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)


class Config:
    """Configuration class for the GitHub Agent."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    
    # LangSmith (optional)
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "github-agent")
    
    # Model Configuration
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "anthropic:claude-sonnet-4-20250514")
    
    # Agent Configuration
    MAX_CONCURRENT_RESEARCH_UNITS = int(os.getenv("MAX_CONCURRENT_RESEARCH_UNITS", "3"))
    MAX_RESEARCHER_ITERATIONS = int(os.getenv("MAX_RESEARCHER_ITERATIONS", "3"))
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "3"))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present.
        
        Returns:
            bool: True if all required config is present
        """
        required = [
            ("GITHUB_TOKEN", cls.GITHUB_TOKEN),
            ("TAVILY_API_KEY", cls.TAVILY_API_KEY),
        ]
        
        # At least one LLM API key required
        has_llm_key = bool(cls.OPENAI_API_KEY or cls.ANTHROPIC_API_KEY)
        
        missing = [name for name, value in required if not value]
        
        if missing:
            print(f"❌ Missing required configuration: {', '.join(missing)}")
            return False
        
        if not has_llm_key:
            print("❌ Missing required configuration: Need either OPENAI_API_KEY or ANTHROPIC_API_KEY")
            return False
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration (with masked keys)."""
        def mask_key(key: str) -> str:
            if not key or len(key) < 8:
                return "❌ Not set"
            return f"✅ {key[:4]}...{key[-4:]}"
        
        print("\n🔧 Configuration:")
        print(f"  OpenAI API Key: {mask_key(cls.OPENAI_API_KEY)}")
        print(f"  Anthropic API Key: {mask_key(cls.ANTHROPIC_API_KEY)}")
        print(f"  GitHub Token: {mask_key(cls.GITHUB_TOKEN)}")
        print(f"  Tavily API Key: {mask_key(cls.TAVILY_API_KEY)}")
        print(f"  Default Model: {cls.DEFAULT_MODEL}")
        print(f"  LangSmith Tracing: {'Enabled' if cls.LANGCHAIN_TRACING_V2 else 'Disabled'}")
        print()


# Validate configuration on import
if __name__ != "__main__":
    Config.validate()
