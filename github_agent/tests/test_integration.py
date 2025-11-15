"""Integration tests for Phases 1-3.

Tests configuration, tools, and basic functionality.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_config_validation():
    """Test that configuration is properly set up."""
    print("\n" + "="*60)
    print("🧪 Testing Configuration")
    print("="*60)
    
    from src.config import Config
    
    # Print config (will mask keys)
    Config.print_config()
    
    # Validate
    is_valid = Config.validate()
    
    if is_valid:
        print("✅ Configuration is valid!")
    else:
        print("❌ Configuration has issues. Please check .env file.")
        return False
    
    # Check model format
    if not Config.DEFAULT_MODEL.startswith(("openai:", "anthropic:")):
        print(f"\n⚠️  WARNING: DEFAULT_MODEL should include provider prefix")
        print(f"   Current: {Config.DEFAULT_MODEL}")
        print(f"   Should be: openai:{Config.DEFAULT_MODEL}")
        print(f"   Please update .env file!")
        return False
    
    return True


def test_state_schema():
    """Test state initialization."""
    print("\n" + "="*60)
    print("🧪 Testing State Schema")
    print("="*60)
    
    from src.state import get_initial_state
    
    state = get_initial_state()
    
    required_keys = ['messages', 'files', 'todos', 'current_repo', 'issue_url', 'analysis_results']
    
    for key in required_keys:
        if key in state:
            print(f"  ✅ State has '{key}' field")
        else:
            print(f"  ❌ State missing '{key}' field")
            return False
    
    print("\n✅ State schema is correct!")
    return True


def test_tool_imports():
    """Test that all tools can be imported."""
    print("\n" + "="*60)
    print("🧪 Testing Tool Imports")
    print("="*60)
    
    try:
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
            ls, read_file, write_file,
            # Analysis tools
            extract_stack_trace,
            think_tool,
            parse_error_from_issue,
            # TODO tools
            write_todos, read_todos, mark_todo_done,
        )
        
        print("  ✅ All 16 tools imported successfully!")
        
        # List them
        tools = [
            ("GitHub", ["search_code_in_repo", "read_file_from_repo", "list_repository_structure", "get_issue_details", "get_repository_info"]),
            ("Search", ["search_error_solution", "search_documentation"]),
            ("File", ["ls", "read_file", "write_file"]),
            ("Analysis", ["extract_stack_trace", "think_tool", "parse_error_from_issue"]),
            ("TODO", ["write_todos", "read_todos", "mark_todo_done"]),
        ]
        
        print("\n📦 Tool Categories:")
        for category, tool_list in tools:
            print(f"  {category} Tools: {len(tool_list)}")
            for tool_name in tool_list:
                print(f"    - {tool_name}")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Failed to import tools: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_github_client():
    """Test GitHub API connection."""
    print("\n" + "="*60)
    print("🧪 Testing GitHub API Connection")
    print("="*60)
    
    try:
        from src.tools.github_tools import github_client
        
        # Test connection by getting rate limit
        rate_limit = github_client.get_rate_limit()
        
        print(f"  ✅ Connected to GitHub API")
        print(f"  Core API Rate Limit: {rate_limit.core.remaining}/{rate_limit.core.limit}")
        print(f"  Search API Rate Limit: {rate_limit.search.remaining}/{rate_limit.search.limit}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ GitHub API connection failed: {e}")
        print("  Check your GITHUB_TOKEN in .env")
        return False


def test_model_initialization():
    """Test that the LLM model can be initialized."""
    print("\n" + "="*60)
    print("🧪 Testing Model Initialization")
    print("="*60)
    
    try:
        from langchain.chat_models import init_chat_model
        from src.config import Config
        
        print(f"  Initializing model: {Config.DEFAULT_MODEL}")
        
        model = init_chat_model(model=Config.DEFAULT_MODEL, temperature=0.0)
        
        print(f"  ✅ Model initialized successfully!")
        print(f"  Model type: {type(model).__name__}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Model initialization failed: {e}")
        print(f"\n  Common issues:")
        print(f"  1. DEFAULT_MODEL should be 'openai:gpt-4o-mini' not 'gpt-4o-mini'")
        print(f"  2. Check your OPENAI_API_KEY in .env")
        return False


def test_tool_functionality():
    """Test basic tool functionality."""
    print("\n" + "="*60)
    print("🧪 Testing Tool Functionality")
    print("="*60)
    
    from src.tools import think_tool, extract_stack_trace
    from src.state import get_initial_state
    
    # Test think tool
    try:
        result = think_tool.invoke({"reflection": "Testing the think tool"})
        print("  ✅ think_tool works")
    except Exception as e:
        print(f"  ❌ think_tool failed: {e}")
        return False
    
    # Test extract_stack_trace
    try:
        test_trace = """
        Traceback (most recent call last):
          File "test.py", line 10, in main
            result = process_data()
          File "test.py", line 5, in process_data
            return data['key']
        KeyError: 'key'
        """
        result = extract_stack_trace.invoke({"text": test_trace})
        print("  ✅ extract_stack_trace works")
    except Exception as e:
        print(f"  ❌ extract_stack_trace failed: {e}")
        return False
    
    return True


def run_all_integration_tests():
    """Run all integration tests."""
    print("\n" + "="*70)
    print("  PHASE 1-3 INTEGRATION TESTS")
    print("="*70)
    
    tests = [
        ("Configuration Validation", test_config_validation),
        ("State Schema", test_state_schema),
        ("Tool Imports", test_tool_imports),
        ("GitHub API Connection", test_github_client),
        ("Model Initialization", test_model_initialization),
        ("Tool Functionality", test_tool_functionality),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results[test_name] = False
    
    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print("\n" + "-"*70)
    print(f"  Total: {passed}/{total} tests passed ({passed*100//total}%)")
    
    if passed == total:
        print("\n  🎉 All integration tests passed!")
        print("  ✅ Phases 1-3 are fully functional!")
    else:
        print(f"\n  ⚠️  {total - passed} test(s) failed.")
        print("  Please review the failures above.")
    
    print("="*70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_integration_tests()
    sys.exit(0 if success else 1)
