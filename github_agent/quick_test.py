"""Quick Test Runner - Automated testing for GitHub Agent

Run this to quickly verify the system is working.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_1_configuration():
    """Test 1: Configuration validation."""
    print_section("TEST 1: Configuration")
    
    try:
        from src.config import Config
        Config.print_config()
        
        if Config.validate():
            print("\n✅ Test 1 PASSED: Configuration is valid!")
            return True
        else:
            print("\n❌ Test 1 FAILED: Configuration has issues")
            return False
    except Exception as e:
        print(f"\n❌ Test 1 FAILED: {e}")
        return False


def test_2_tools_import():
    """Test 2: Import all tools."""
    print_section("TEST 2: Tools Import")
    
    try:
        from src.tools import (
            # GitHub
            search_code_in_repo, read_file_from_repo, list_repository_structure,
            get_issue_details, get_repository_info,
            # Search
            search_error_solution, search_documentation,
            # Files
            ls, read_file, write_file,
            # Analysis
            extract_stack_trace, think_tool, parse_error_from_issue,
            # TODO
            write_todos, read_todos, mark_todo_done,
        )
        
        print("✅ All 16 tools imported successfully!")
        print("\nTool categories:")
        print("  - GitHub tools: 5")
        print("  - Search tools: 2")
        print("  - File tools: 3")
        print("  - Analysis tools: 3")
        print("  - TODO tools: 3")
        
        print("\n✅ Test 2 PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Test 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_3_github_api():
    """Test 3: GitHub API connection."""
    print_section("TEST 3: GitHub API Connection")
    
    try:
        from src.tools.github_tools import github_client
        
        # Test with rate limit check
        rate_limit = github_client.get_rate_limit()
        
        print(f"✅ Connected to GitHub API")
        print(f"  Core API: {rate_limit.core.remaining}/{rate_limit.core.limit} requests")
        print(f"  Search API: {rate_limit.search.remaining}/{rate_limit.search.limit} requests")
        
        print("\n✅ Test 3 PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Test 3 FAILED: {e}")
        return False


def test_4_repository_info():
    """Test 4: Get repository info (real API call)."""
    print_section("TEST 4: Get Repository Info")
    
    try:
        from src.tools import get_repository_info
        
        print("Fetching info for 'openai/openai-python'...")
        result = get_repository_info.invoke({
            'repo_name': 'openai/openai-python'
        })
        
        if "openai-python" in result.lower() or "openai" in result.lower():
            print("\n" + "="*70)
            print(result[:300])  # First 300 chars
            print("="*70)
            print("\n✅ Test 4 PASSED: Repository info retrieved")
            return True
        else:
            print(f"\n❌ Test 4 FAILED: Unexpected response")
            return False
            
    except Exception as e:
        print(f"❌ Test 4 FAILED: {e}")
        return False


def test_5_file_system():
    """Test 5: Virtual file system."""
    print_section("TEST 5: Virtual File System")
    
    try:
        from src.tools import write_file, read_file, ls
        from src.state import get_initial_state
        
        state = get_initial_state()
        
        # Write
        write_result = write_file.invoke({
            'filename': 'test_note.txt',
            'content': 'This is a test note!',
            'state': state
        })
        print(f"Write: {write_result}")
        
        # List
        ls_result = ls.invoke({'state': state})
        print(f"\n{ls_result}")
        
        # Read
        read_result = read_file.invoke({
            'filename': 'test_note.txt',
            'state': state
        })
        print(f"\nRead: {read_result}")
        
        if "This is a test note!" in read_result:
            print("\n✅ Test 5 PASSED: File system works")
            return True
        else:
            print("\n❌ Test 5 FAILED: File content mismatch")
            return False
            
    except Exception as e:
        print(f"❌ Test 5 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_6_prompts():
    """Test 6: Agent prompts."""
    print_section("TEST 6: Agent Prompts")
    
    try:
        from src.prompts import (
            REPO_INVESTIGATOR_PROMPT,
            ERROR_RESEARCHER_PROMPT,
            MAIN_AGENT_INSTRUCTIONS,
            get_today_str,
        )
        
        print(f"✅ Today: {get_today_str()}")
        print(f"✅ REPO_INVESTIGATOR_PROMPT: {len(REPO_INVESTIGATOR_PROMPT)} characters")
        print(f"✅ ERROR_RESEARCHER_PROMPT: {len(ERROR_RESEARCHER_PROMPT)} characters")
        print(f"✅ MAIN_AGENT_INSTRUCTIONS: {len(MAIN_AGENT_INSTRUCTIONS)} characters")
        
        print("\n✅ Test 6 PASSED: All prompts loaded")
        return True
        
    except Exception as e:
        print(f"❌ Test 6 FAILED: {e}")
        return False


def test_7_main_agent():
    """Test 7: Main agent creation."""
    print_section("TEST 7: Main Agent")
    
    try:
        from src.main import main_agent, sub_agents
        
        print(f"✅ Main agent created successfully")
        print(f"✅ Sub-agents configured: {len(sub_agents)}")
        
        for agent in sub_agents:
            print(f"   - {agent['name']}: {agent['description']}")
        
        print("\n✅ Test 7 PASSED: Main agent ready")
        return True
        
    except Exception as e:
        print(f"❌ Test 7 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_quick_tests():
    """Run all quick tests."""
    print("\n" + "="*70)
    print("  QUICK TEST RUNNER - GitHub Repository Analyzer Agent")
    print("="*70)
    print("\nRunning automated tests...\n")
    
    tests = [
        ("Configuration", test_1_configuration),
        ("Tools Import", test_2_tools_import),
        ("GitHub API", test_3_github_api),
        ("Repository Info", test_4_repository_info),
        ("File System", test_5_file_system),
        ("Agent Prompts", test_6_prompts),
        ("Main Agent", test_7_main_agent),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70 + "\n")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print("\n" + "-"*70)
    percentage = (passed * 100) // total
    print(f"  Total: {passed}/{total} tests passed ({percentage}%)")
    
    if passed == total:
        print("\n  🎉 All tests passed! System is working perfectly!")
        print("  ✅ Ready for production use!")
    elif passed >= total * 0.7:
        print(f"\n  👍 Most tests passed! System is mostly functional.")
        print(f"  ⚠️  Review {total - passed} failure(s) above.")
    else:
        print(f"\n  ⚠️  Several tests failed.")
        print(f"  Please review configuration and setup.")
    
    print("="*70 + "\n")
    
    # Recommendations
    print("NEXT STEPS:")
    if passed == total:
        print("  1. Try the interactive mode: github-agent interactive")
        print("  2. Test with a real issue: github-agent issue <url>")
        print("  3. See TESTING_GUIDE.md for advanced tests")
    else:
        print("  1. Review failed tests above")
        print("  2. Check .env configuration")
        print("  3. Run: python verify_setup.py")
    
    print()
    
    return passed == total


if __name__ == "__main__":
    success = run_quick_tests()
    sys.exit(0 if success else 1)
