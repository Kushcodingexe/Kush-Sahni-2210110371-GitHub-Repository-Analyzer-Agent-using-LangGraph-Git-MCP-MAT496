"""Tests for Phase 1: Project Setup & Foundation

Tests basic imports, configuration, and state management.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test that all core modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        from src import config
        print("  ✅ src.config imported")
    except ImportError as e:
        print(f"  ❌ Failed to import src.config: {e}")
        return False
    
    try:
        from src import state
        print("  ✅ src.state imported")
    except ImportError as e:
        print(f"  ❌ Failed to import src.state: {e}")
        return False
    
    try:
        from src.tools import __init__
        print("  ✅ src.tools package imported")
    except ImportError as e:
        print(f"  ❌ Failed to import src.tools: {e}")
        return False
    
    try:
        from src.agents import __init__
        print("  ✅ src.agents package imported")
    except ImportError as e:
        print(f"  ❌ Failed to import src.agents: {e}")
        return False
    
    return True


def test_config_class():
    """Test that Config class is properly defined."""
    print("\n🧪 Testing Config class...")
    
    try:
        from src.config import Config
        
        # Test that Config has expected attributes
        expected_attrs = [
            'OPENAI_API_KEY',
            'ANTHROPIC_API_KEY',
            'GITHUB_TOKEN',
            'TAVILY_API_KEY',
            'DEFAULT_MODEL',
            'MAX_CONCURRENT_RESEARCH_UNITS',
            'MAX_RESEARCHER_ITERATIONS',
        ]
        
        for attr in expected_attrs:
            if not hasattr(Config, attr):
                print(f"  ❌ Config missing attribute: {attr}")
                return False
            print(f"  ✅ Config.{attr} exists")
        
        # Test methods exist
        if not hasattr(Config, 'validate'):
            print("  ❌ Config missing validate() method")
            return False
        print("  ✅ Config.validate() method exists")
        
        if not hasattr(Config, 'print_config'):
            print("  ❌ Config missing print_config() method")
            return False
        print("  ✅ Config.print_config() method exists")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing Config: {e}")
        return False


def test_state_schema():
    """Test that GitHubAgentState schema is properly defined."""
    print("\n🧪 Testing GitHubAgentState schema...")
    
    try:
        from src.state import GitHubAgentState, get_initial_state
        
        # Test that schema has expected keys
        expected_keys = [
            'messages',
            'files',
            'todos',
            'current_repo',
            'issue_url',
            'analysis_results',
        ]
        
        # Get annotations from TypedDict
        annotations = GitHubAgentState.__annotations__
        
        for key in expected_keys:
            if key not in annotations:
                print(f"  ❌ GitHubAgentState missing key: {key}")
                return False
            print(f"  ✅ GitHubAgentState has '{key}' field")
        
        # Test get_initial_state
        initial = get_initial_state()
        if not isinstance(initial, dict):
            print("  ❌ get_initial_state() should return dict")
            return False
        
        print("  ✅ get_initial_state() returns dict")
        
        # Verify initial state has all keys
        for key in expected_keys:
            if key not in initial:
                print(f"  ❌ Initial state missing: {key}")
                return False
        
        print("  ✅ Initial state has all required keys")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing state: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_project_structure():
    """Test that project structure is correct."""
    print("\n🧪 Testing project structure...")
    
    project_root = Path(__file__).parent.parent
    
    required_paths = [
        'src/__init__.py',
        'src/config.py',
        'src/state.py',
        'src/tools/__init__.py',
        'src/agents/__init__.py',
        'requirements.txt',
        'README.md',
        '.env.example',
        '.gitignore',
    ]
    
    all_exist = True
    for path_str in required_paths:
        path = project_root / path_str
        if path.exists():
            print(f"  ✅ {path_str} exists")
        else:
            print(f"  ❌ {path_str} missing")
            all_exist = False
    
    return all_exist


def test_dependencies():
    """Test that key dependencies can be imported."""
    print("\n🧪 Testing dependencies...")
    
    dependencies = [
        ('langchain', 'langchain'),
        ('langchain_core', 'langchain-core'),
        ('langgraph', 'langgraph'),
        ('dotenv', 'python-dotenv'),
        ('pydantic', 'pydantic'),
    ]
    
    all_imported = True
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"  ✅ {package_name} installed")
        except ImportError:
            print(f"  ❌ {package_name} not installed (install with: pip install {package_name})")
            all_imported = False
    
    return all_imported


def run_all_tests():
    """Run all Phase 1 tests."""
    print("\n" + "="*60)
    print("  Phase 1 Testing - Project Setup & Foundation")
    print("="*60 + "\n")
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Dependencies", test_dependencies),
        ("Module Imports", test_imports),
        ("Config Class", test_config_class),
        ("State Schema", test_state_schema),
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
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print("\n" + "-"*60)
    print(f"  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("  🎉 All tests passed! Phase 1 is solid.")
    else:
        print(f"  ⚠️  {total - passed} test(s) failed.")
    
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
