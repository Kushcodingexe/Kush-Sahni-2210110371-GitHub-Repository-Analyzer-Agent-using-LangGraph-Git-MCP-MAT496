# Testing Recommendations Summary

## Quick Start Testing (Recommended First Steps)

### 1. Run the Quick Test Suite (5 minutes)

```bash
cd "C:/Users/Kush/My Drive/LLM Project1/github_agent"
python quick_test.py
```

**This automated script tests:**
- ✅ Configuration validation
- ✅ All 16 tools import correctly
- ✅ GitHub API connection
- ✅ Real API call to get repository info
- ✅ Virtual file system
- ✅ Agent prompts loading
- ✅ Main agent creation

**Expected Output:**
```
Total: 7/7 tests passed (100%)
🎉 All tests passed! System is working perfectly!
```

---

### 2. Run Existing Integration Tests (1 minute)

```bash
python tests/test_integration.py
```

**Tests:**
- Configuration
- State schema
- Tool imports
- GitHub API
- Model initialization
- Tool functionality

**Expected:** 6/6 tests passing

---

### 3. Test CLI Commands (2 minutes)

```bash
# Check configuration
github-agent config

# Show system info
github-agent info

# Try interactive mode (type 'exit' to quit)
github-agent interactive
```

---

## Medium-Level Testing (Recommended Next)

### 4. Test Individual Tools (10 minutes)

Pick a few tools to test manually:

**GitHub Tools:**
```bash
python -c "
from src.tools import get_repository_info
result = get_repository_info.invoke({'repo_name': 'openai/openai-python'})
print(result)
"
```

**File System:**
```bash
python -c "
from src.tools import write_file, ls, read_file
from src.state import get_initial_state
state = get_initial_state()
write_file.invoke({'filename': 'test.md', 'content': '# Test', 'state': state})
print(ls.invoke({'state': state}))
print(read_file.invoke({'filename': 'test.md', 'state': state}))
"
```

**Analysis:**
```bash
python -c "
from src.tools import extract_stack_trace
result = extract_stack_trace.invoke({'text': 'KeyError: access_token at line 42 in auth.py'})
print(result)
"
```

---

## Advanced Testing (Optional - Uses API Credits)

### 5. Test Simple Agent Query (~$0.01)

```bash
python -c "
from src.main import ask_about_repository

result = ask_about_repository(
    'openai/openai-python',
    'What is this repository?'
)

for msg in reversed(result['messages']):
    if hasattr(msg, 'content') and msg.content:
        print(msg.content)
        break
"
```

**What to check:**
- Agent responds with repository description
- Uses tools appropriately
- Provides coherent answer

---

### 6. Test Code Search (~$0.02-0.05)

```bash
python -c "
from src.main import ask_about_repository

result = ask_about_repository(
    'openai/openai-python',
    'Find the ChatCompletion class'
)

for msg in reversed(result['messages']):
    if hasattr(msg, 'content') and msg.content:
        print(msg.content[:500])  # First 500 chars
        break
"
```

**What to check:**
- Agent searches code successfully
- May delegate to repo-investigator
- Provides file locations

---

### 7. Test Issue Analysis (~$0.05-0.15)

Use a real GitHub issue:

```bash
github-agent issue https://github.com/openai/openai-python/issues/1
```

Or programmatically:
```bash
python -c "
from src.main import analyze_issue

result = analyze_issue('https://github.com/openai/openai-python/issues/1')

for msg in reversed(result['messages']):
    if hasattr(msg, 'content') and msg.content:
        print('=== REPORT ===')
        print(msg.content[:800])
        break
"
```

**What to check:**
- Agent creates investigation plan
- Fetches issue details
- May delegate to sub-agents
- Produces structured report

---

## Testing Priority Order

### Priority 1 (Must Do - 10-15 minutes)
1. ✅ Run `quick_test.py` 
2. ✅ Run `tests/test_integration.py`
3. ✅ Test CLI commands (`github-agent config`, `github-agent info`)

**If all pass:** Your system is verified and ready! ✅

### Priority 2 (Should Do - 10 minutes)
4. Test 2-3 individual tools manually
5. Test file system persistence
6. Try interactive mode briefly

**If successful:** Ready for real-world testing

### Priority 3 (Nice to Have - Uses credits)
7. Simple agent query (cheap ~$0.01)
8. Code search query (moderate ~$0.02-0.05)

**If successful:** Confident in agent capabilities

### Priority 4 (Production Validation) 
9. Full issue analysis with real GitHub issue (~$0.05-0.15)

**If successful:** Production-ready! 🎉

---

## Troubleshooting Guide

### Common Issues & Fixes

**Issue:** Tests fail with "cannot import create_agent"  
**Fix:** Already resolved - using `create_react_agent`

**Issue:** "DEFAULT_MODEL format error"  
**Fix:** Ensure `.env` has `DEFAULT_MODEL=openai:gpt-4o-mini` (with `openai:` prefix)

**Issue:** "GitHub API rate limit"  
**Fix:** Wait a few minutes or test with different repositories

**Issue:** "github-agent command not found"  
**Fix:** 
```bash
cd github_agent
pip install -e .
```

**Issue:** Agent doesn't respond or hangs  
**Fix:** 
- Check API keys are valid
- Check internet connection
- Try with `verbose` flag in CLI

---

## Cost Estimates (OpenAI GPT-4o-mini)

| Test Level | Estimated Cost |
|-----------|----------------|
| Priority 1 (automated tests) | $0.00 (no LLM calls) |
| Priority 2 (manual tool tests) | $0.00 (no LLM calls) |  
| Priority 3 (simple queries) | $0.01-0.05 |
| Priority 4 (full issue analysis) | $0.05-0.15 |
| **Complete test suite** | **~$0.10-0.25** |

---

## Success Criteria

### ✅ Minimum (Ready to Continue)
- All Priority 1 tests pass
- Configuration valid
- Tools import correctly
- GitHub API connected

### ✅ Good (Ready for Testing)
- Priority 1 + Priority 2 tests pass
- Individual tools work
- CLI commands respond
- File system functional

### ✅ Excellent (Production Ready)
- All priority levels pass
- Agent queries work
- Issue analysis produces reports
- No critical errors

---

## Recommended Testing Approach

**For Quick Verification (10 minutes):**
```bash
# 1. Run automated tests
python quick_test.py

# 2. Run integration tests  
python tests/test_integration.py

# 3. Check CLI
github-agent config
github-agent info
```

**For Thorough Validation (30 minutes):**
```bash
# Above + manual tool tests
python -c "from src.tools import get_repository_info; ..."

# Above + simple agent query
python -c "from src.main import ask_about_repository; ..."
```

**For Production Confidence (45 minutes):**
```bash
# All above + real issue analysis
github-agent issue <real-github-issue-url>
```

---

## What Each Test Validates

| Test | What It Proves |
|------|---------------|
| quick_test.py | Foundation is solid |
| test_integration.py | Components integrate correctly |
| Individual tools | Each tool works independently |
| Simple query | Basic agent reasoning works |
| Code search | Agent can delegate and search |
| Issue analysis | Full workflow end-to-end |

---

## Next Steps After Testing

**All Tests Pass:**
- 🎉 Congratulations! System is fully functional
- Ready for real-world usage
- Can proceed to deploy or use in projects

**Some Tests Fail:**
- 📋 Document which tests failed
- 🔍 Check error messages
- 🛠️ Fix issues based on error type
- 🔄 Re-run tests

**Need Help:**
- See TESTING_GUIDE.md for detailed troubleshooting
- Review CONFIGURATION_REVIEW.md for setup issues
- Check FINAL_SUCCESS_REPORT.md for known issues

---

## Quick Reference Commands

```bash
# Automated tests
python quick_test.py                   # 7 automated tests
python tests/test_integration.py        # 6 integration tests

# CLI commands
github-agent config                     # Check configuration
github-agent info                       # Show capabilities
github-agent interactive                # Interactive mode
github-agent issue <url>                # Analyze issue
github-agent ask <repo> <question>      # Ask about repo

# Manual testing
python verify_setup.py                  # Verify setup
python -m src.main interactive          # Interactive Python mode
```

---

**Start Here:** Run `python quick_test.py` right now! 🚀
