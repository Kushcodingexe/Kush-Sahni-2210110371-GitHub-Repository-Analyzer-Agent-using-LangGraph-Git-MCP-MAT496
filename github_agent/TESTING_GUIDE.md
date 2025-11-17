# Testing Guide for GitHub Repository Analyzer Agent

Comprehensive testing guide to verify all components work correctly.

---

## Quick Testing Checklist

- [ ] Level 1: Configuration & Setup
- [ ] Level 2: Individual Tools
- [ ] Level 3: Agent Components
- [ ] Level 4: CLI Commands
- [ ] Level 5: End-to-End Workflows
- [ ] Level 6: Integration Tests

---

## Level 1: Configuration & Setup Tests

### Test 1: Verify Setup
```bash
python verify_setup.py
```

**Expected Output:**
```
✅ Configuration valid! You're ready to start development.
```

**What it checks:**
- All API keys are set
- Model configuration is correct
- No missing required variables

---

### Test 2: Run Integration Tests
```bash
python tests/test_integration.py
```

**Expected Output:**
```
Total: 6/6 tests passed (100%)
🎉 All integration tests passed!
✅ Phases 1-3 are fully functional!
```

**What it checks:**
- Configuration validation
- State schema
- All 16 tools import
- GitHub API connection
- Model initialization
- Tool functionality

---

## Level 2: Individual Tool Tests

### Test 3: GitHub API Tools

#### 3a. Get Repository Info
```bash
python -c "
from src.tools import get_repository_info

result = get_repository_info.invoke({'repo_name': 'openai/openai-python'})
print(result)
"
```

**Expected:** Repository information with stars, forks, description

#### 3b. Search Code
```bash
python -c "
from src.tools import search_code_in_repo

result = search_code_in_repo.invoke({
    'repo_name': 'openai/openai-python',
    'query': 'class ChatCompletion',
    'max_results': 3
})
print(result)
"
```

**Expected:** List of files containing the search term

#### 3c. List Repository Structure
```bash
python -c "
from src.tools import list_repository_structure

result = list_repository_structure.invoke({
    'repo_name': 'openai/openai-python',
    'path': '',
    'max_depth': 1
})
print(result)
"
```

**Expected:** Tree structure of the repository

---

### Test 4: File System Tools

```bash
python -c "
from src.tools import write_file, read_file, ls
from src.state import get_initial_state

state = get_initial_state()

# Test write
write_result = write_file.invoke({
    'filename': 'test.txt',
    'content': 'Hello, World!',
    'state': state
})
print('Write:', write_result)

# Test list
ls_result = ls.invoke({'state': state})
print('List:', ls_result)

# Test read
read_result = read_file.invoke({
    'filename': 'test.txt',
    'state': state
})
print('Read:', read_result)
"
```

**Expected:**
- Write: ✅ Created file: test.txt
- List: 📁 Virtual File System (1 files)
- Read: Hello, World!

---

### Test 5: Analysis Tools

```bash
python -c "
from src.tools import extract_stack_trace

error_text = '''
Traceback (most recent call last):
  File \"test.py\", line 10, in main
    result = process_data()
  File \"test.py\", line 5, in process_data
    return data[\"key\"]
KeyError: \"key\"
'''

result = extract_stack_trace.invoke({'text': error_text})
print(result)
"
```

**Expected:** Structured stack trace analysis with error type, files, and line numbers

---

### Test 6: Search Tools (Requires API Credits)

```bash
python -c "
from src.tools import search_error_solution
from src.state import get_initial_state

state = get_initial_state()

result = search_error_solution.invoke({
    'error_message': 'ModuleNotFoundError: No module named requests',
    'library_name': 'Python',
    'state': state,
    'tool_call_id': 'test-123'
})

# This returns a Command object, access update
print('Search completed')
print('Files created:', len(state.get('files', {})))
"
```

**Expected:** 
- Search completed
- Files created: 2-3

---

## Level 3: Agent Component Tests

### Test 7: Prompts Import
```bash
python -c "
from src.prompts import (
    REPO_INVESTIGATOR_PROMPT,
    ERROR_RESEARCHER_PROMPT,
    MAIN_AGENT_INSTRUCTIONS,
    get_today_str
)

print('✅ All prompts imported')
print(f'Today: {get_today_str()}')
print(f'Repo prompt length: {len(REPO_INVESTIGATOR_PROMPT)} chars')
print(f'Error prompt length: {len(ERROR_RESEARCHER_PROMPT)} chars')
print(f'Main prompt length: {len(MAIN_AGENT_INSTRUCTIONS)} chars')
"
```

**Expected:**
- All prompts imported successfully
- Prompt lengths > 100 characters each

---

### Test 8: Main Agent Import
```bash
python -c "
from src.main import main_agent, sub_agents

print('✅ Main agent created')
print(f'Sub-agents: {len(sub_agents)}')
for agent in sub_agents:
    print(f'  - {agent[\"name\"]}: {agent[\"description\"]}')
"
```

**Expected:**
```
✅ Main agent created
Sub-agents: 2
  - repo-investigator: Investigates repository structure and locates code
  - error-researcher: Researches errors and finds solutions online
```

---

## Level 4: CLI Command Tests

### Test 9: CLI Info Command
```bash
github-agent info
```

**Expected:** Display agent information and capabilities

---

### Test 10: CLI Config Command
```bash
github-agent config
```

**Expected:**
```
✅ Configuration is valid!
You're ready to use the GitHub Repository Analyzer.
```

---

### Test 11: CLI Help
```bash
github-agent --help
```

**Expected:** List of all available commands

---

### Test 12: Interactive Mode (Quick Test)
```bash
github-agent interactive
```

**Test Steps:**
1. Type: "Hello"
2. Wait for response
3. Type: "exit"

**Expected:** Agent responds and exits cleanly

---

## Level 5: End-to-End Workflow Tests

### Test 13: Simple Repository Question (Recommended - Low Cost)

```bash
python -c "
from src.main import ask_about_repository

result = ask_about_repository(
    'openai/openai-python',
    'What is this repository about?'
)

# Print last AI message
for msg in reversed(result['messages']):
    if hasattr(msg, 'content') and msg.content:
        print('=== AGENT RESPONSE ===')
        print(msg.content)
        break
"
```

**Expected:**
- Agent provides description of the repository
- Uses `get_repository_info` tool directly
- Response within 10-30 seconds

---

### Test 14: Code Search Question (Moderate Cost)

```bash
python -c "
from src.main import ask_about_repository

result = ask_about_repository(
    'openai/openai-python',
    'Find the ChatCompletion class implementation'
)

for msg in reversed(result['messages']):
    if hasattr(msg, 'content') and msg.content:
        print('=== AGENT RESPONSE ===')
        print(msg.content)
        break
"
```

**Expected:**
- Agent searches code and finds the class
- May delegate to repo-investigator
- Provides file paths and code locations

---

### Test 15: GitHub Issue Analysis (Higher Cost - Real Use Case)

**Pick a real issue from a public repository**, for example:
```bash
github-agent issue https://github.com/langchain-ai/langchain/issues/12345
```

Or programmatically:
```bash
python -c "
from src.main import analyze_issue

# Use a real, simple issue URL
result = analyze_issue('https://github.com/openai/openai-python/issues/1')

for msg in reversed(result['messages']):
    if hasattr(msg, 'content') and msg.content:
        print('=== INVESTIGATION REPORT ===')
        print(msg.content[:500])  # First 500 chars
        break
"
```

**Expected:**
- Agent creates TODO plan
- Fetches issue details
- May delegate to both sub-agents
- Produces investigation report
- Takes 30-90 seconds

---

## Level 6: Integration Testing Scenarios

### Test 16: Virtual File System Persistence

```python
# Save as test_file_persistence.py
from src.main import main_agent
from src.state import get_initial_state
from langchain_core.messages import HumanMessage

# First interaction
state = get_initial_state()
state["messages"] = [
    HumanMessage(content="Save a note: Testing file system")
]

result = main_agent.invoke(state)

# Check files were created
print(f"Files after first interaction: {len(result.get('files', {}))}")

# Second interaction - agent should remember files
state["messages"].append(HumanMessage(content="List all files"))
result = main_agent.invoke(state)

print(f"Files after second interaction: {len(result.get('files', {}))}")
```

**Expected:** Files persist across interactions

---

### Test 17: TODO Management

```python
# Save as test_todo_management.py
from src.tools import write_todos, read_todos, mark_todo_done
from src.state import get_initial_state

state = get_initial_state()

# Create TODOs
write_result = write_todos.invoke({
    'todos_list': [
        'Fetch repository info',
        'Search for code',
        'Analyze findings'
    ],
    'state': state
})
print(write_result)

# Read TODOs
read_result = read_todos.invoke({'state': state})
print('\n' + read_result)

# Mark one done
mark_result = mark_todo_done.invoke({
    'todo_index': 1,
    'state': state
})
print('\n' + mark_result)

# Read again
read_result2 = read_todos.invoke({'state': state})
print('\n' + read_result2)
```

**Expected:** TODOs created, read, and marked complete successfully

---

## Test Results Tracking

Create a test results file to track your progress:

```markdown
# Test Results

Date: [DATE]

## Level 1: Configuration ✅/❌
- [ ] Test 1: Verify Setup
- [ ] Test 2: Integration Tests

## Level 2: Individual Tools ✅/❌
- [ ] Test 3a: Get Repository Info
- [ ] Test 3b: Search Code
- [ ] Test 3c: List Structure
- [ ] Test 4: File System Tools
- [ ] Test 5: Analysis Tools
- [ ] Test 6: Search Tools

## Level 3: Agent Components ✅/❌
- [ ] Test 7: Prompts Import
- [ ] Test 8: Main Agent Import

## Level 4: CLI Commands ✅/❌
- [ ] Test 9: CLI Info
- [ ] Test 10: CLI Config
- [ ] Test 11: CLI Help
- [ ] Test 12: Interactive Mode

## Level 5: End-to-End ✅/❌
- [ ] Test 13: Simple Repository Question
- [ ] Test 14: Code Search Question
- [ ] Test 15: Issue Analysis

## Level 6: Integration ✅/❌
- [ ] Test 16: File Persistence
- [ ] Test 17: TODO Management

Notes:
- [Add any issues or observations here]
```

---

## Recommended Testing Order

### Quick Smoke Test (5 minutes)
1. Test 1: Verify Setup
2. Test 2: Integration Tests
3. Test 7: Prompts Import
4. Test 10: CLI Config

### Medium Test Suite (15 minutes)
Above + 
5. Test 3a-c: GitHub API Tools
6. Test 4: File System Tools
7. Test 13: Simple Repository Question

### Full Test Suite (30-45 minutes)
All tests above +
8. Test 14: Code Search
9. Test 15: Issue Analysis (real use case)

---

## Troubleshooting Common Issues

### Issue: "Cannot import name 'create_agent'"
**Solution:** Already fixed! Using `create_react_agent` from `langgraph.prebuilt`

### Issue: "API rate limit exceeded"
**Solution:** Wait a Few minutes or use a different repository for testing

### Issue: "Model initialization failed"
**Solution:** Check `.env` has `DEFAULT_MODEL=openai:gpt-4o-mini` (with provider prefix)

### Issue: "github-agent command not found"
**Solution:** 
```bash
cd github_agent
pip install -e .
```

---

## Cost Estimation (OpenAI GPT-4o-mini)

**Individual Tool Tests:** ~$0.00 (minimal tokens)
**Simple Queries (Test 13):** ~$0.01-0.02
**Code Search (Test 14):** ~$0.02-0.05
**Issue Analysis (Test 15):** ~$0.05-0.15 (with sub-agents)

**Total for Full Test Suite:** ~$0.25-0.50 USD

---

## Success Criteria

**Minimum to Pass:**
- ✅ All Level 1 tests pass
- ✅ At least 3 tools work in Level 2
- ✅ Agent imports successfully (Level 3)

**Good to Go:**
- ✅ All tools in Level 2 work
- ✅ CLI commands respond correctly
- ✅ One end-to-end test completes successfully

**Production Ready:**
- ✅ All tests pass
- ✅ Issue analysis produces coherent reports
- ✅ No errors in any component

---

## Next Steps After Testing

1. **All Pass:** Ready for real-world usage!
2. **Some Fail:** Review failures, fix issues, re-test
3. **Integration Issues:** May need minor adjustments to agent prompts or tool configurations

**Good luck with testing!** 🚀
