"""Test Phase 4: Sub-Agent Architecture

Tests the complete agent orchestration including sub-agents.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_prompts_import():
    """Test that prompts can be imported."""
    print("\n" + "="*60)
    print("🧪 Testing Prompts Import")
    print("="*60)
    
    try:
        from src.prompts import (
            REPO_INVESTIGATOR_PROMPT,
            ERROR_RESEARCHER_PROMPT,
            MAIN_AGENT_INSTRUCTIONS,
            get_today_str,
        )
        
        print("  ✅ All prompts imported successfully")
        print(f"  ✅ Today's date: {get_today_str()}")
        
        # Check prompts are not empty
        if len(REPO_INVESTIGATOR_PROMPT) > 100:
            print(f"  ✅ REPO_INVESTIGATOR_PROMPT: {len(REPO_INVESTIGATOR_PROMPT)} chars")
        
        if len(ERROR_RESEARCHER_PROMPT) > 100:
            print(f"  ✅ ERROR_RESEARCHER_PROMPT: {len(ERROR_RESEARCHER_PROMPT)} chars")
        
        if len(MAIN_AGENT_INSTRUCTIONS) > 100:
            print(f"  ✅ MAIN_AGENT_INSTRUCTIONS: {len(MAIN_AGENT_INSTRUCTIONS)} chars")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to import prompts: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_task_tool_creation():
    """Test that task delegation tool can be created."""
    print("\n" + "="*60)
    print("🧪 Testing Task Tool Creation")
    print("="*60)
    
    try:
        from src.task_tool import _create_task_tool
        from src.state import GitHubAgentState
        from src.tools import think_tool, search_code_in_repo
        from langchain.chat_models import init_chat_model
        
        # Create a simple model
        model = init_chat_model(model="openai:gpt-4o-mini", temperature=0.0)
        
        # Create simple sub-agent config
        sub_agents = [{
            "name": "test-agent",
            "prompt": "You are a test agent.",
            "tools": ["think_tool"],
        }]
        
        # Create task tool
        task_tool = _create_task_tool(
            all_tools=[think_tool, search_code_in_repo],
            sub_agents=sub_agents,
            model=model,
            state_schema=GitHubAgentState
        )
        
        print("  ✅ Task delegation tool created successfully")
        print(f"  ✅ Tool name: {task_tool.name}")
        print(f"  ✅ Tool has description: {bool(task_tool.description)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to create task tool: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_agent_creation():
    """Test that main agent can be created."""
    print("\n" + "="*60)
    print("🧪 Testing Main Agent Creation")
    print("="*60)
    
    try:
        from src.main import main_agent, sub_agents
        
        print("  ✅ Main agent created successfully")
        print(f"  ✅ Number of sub-agents: {len(sub_agents)}")
        
        for agent in sub_agents:
            print(f"     - {agent['name']}: {agent['description']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to create main agent: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cli_import():
    """Test that CLI can be imported."""
    print("\n" + "="*60)
    print("🧪 Testing CLI Import")
    print("="*60)
    
    try:
        from src.cli import cli
        
        print("  ✅ CLI imported successfully")
        print(f"  ✅ CLI is a Click command: {hasattr(cli, 'commands')}")
        
        # List available commands
        if hasattr(cli, 'commands'):
            commands = list(cli.commands.keys())
            print(f"  ✅ Available commands: {', '.join(commands)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to import CLI: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_helper_functions():
    """Test helper functions exist."""
    print("\n" + "="*60)
    print("🧪 Testing Helper Functions")
    print("="*60)
    
    try:
        from src.main import analyze_issue, ask_about_repository, interactive_session
        
        print("  ✅ analyze_issue function exists")
        print("  ✅ ask_about_repository function exists")
        print("  ✅ interactive_session function exists")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to import helper functions: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_phase4_tests():
    """Run all Phase 4 tests."""
    print("\n" + "="*70)
    print("  PHASE 4 ARCHITECTURE TESTS")
    print("="*70)
    
    tests = [
        ("Prompts Import", test_prompts_import),
        ("Task Tool Creation", test_task_tool_creation),
        ("Main Agent Creation", test_main_agent_creation),
        ("CLI Import", test_cli_import),
        ("Helper Functions", test_helper_functions),
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
        print("\n  🎉 All Phase 4 tests passed!")
        print("  ✅ Sub-agent architecture is ready!")
    else:
        print(f"\n  ⚠️  {total - passed} test(s) failed.")
    
    print("="*70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_phase4_tests()
    sys.exit(0 if success else 1)
