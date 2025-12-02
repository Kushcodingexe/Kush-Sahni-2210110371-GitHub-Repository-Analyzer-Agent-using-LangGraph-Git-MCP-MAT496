# Quick Reference: Demo Commands

## 🚀 Commands to Copy-Paste During Demo

### 1. Configuration Check
```bash
python -c "from src.config import Config; Config.print_config()"
```

### 2. CLI - Analyze Issue
```bash
# Generic format
python -m src.main analyze-issue https://github.com/OWNER/REPO/issues/NUMBER

# Example with real repository (test this first!)
python -m src.main analyze-issue https://github.com/langchain-ai/langchain/issues/1234
```

### 3. CLI - Ask Repository
```bash
# Generic format
python -m src.main ask OWNER/REPO "Your question here"

# Example 1: Project structure
python -m src.main ask openai/openai-python "What is the project structure and main components?"

# Example 2: Authentication
python -m src.main ask fastapi/fastapi "How does dependency injection work?"

# Example 3: Specific feature
python -m src.main ask langchain-ai/langchain "Where is the ChatModel class defined?"
```

### 4. CLI - Interactive Mode
```bash
python -m src.main interactive
```

**Sample questions for interactive mode:**
- `What tools do you have available?`
- `Can you analyze a repository for me?`
- `How do I use the issue analysis feature?`
- `exit` (to quit)

### 5. Streamlit UI
```bash
cd github_agent
streamlit run streamlit_app.py
```

---

## 🧪 Test These Before Recording

### Good Test Repositories:
- `openai/openai-python` - Well-documented, clear structure
- `fastapi/fastapi` - Popular, good examples
- `langchain-ai/langchain` - Relevant to the project
- `streamlit/streamlit` - If you want to show meta-analysis
- Your own test repository with sample issues

### Sample Questions That Work Well:
1. "What is this repository about?"
2. "Explain the project structure"
3. "How does authentication work?"
4. "Where is the main entry point?"
5. "What dependencies does this project use?"
6. "How are errors handled?"
7. "Where is the [SpecificClass] defined?"

---

## 📋 Pre-Demo Setup Checklist

### Terminal Setup:
```bash
# 1. Navigate to project
cd "c:\Users\Kush\My Drive\LLM Project1\github_agent"

# 2. Clear terminal (optional)
clear  # or cls on Windows

# 3. Activate venv if needed
# .\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 4. Verify installation
pip list | grep langchain
pip list | grep langgraph
```

### Environment Variables Check:
```bash
# Create a test script to verify
python -c "import os; print('GitHub Token:', 'SET' if os.getenv('GITHUB_TOKEN') else 'NOT SET')"
python -c "import os; print('Tavily API:', 'SET' if os.getenv('TAVILY_API_KEY') else 'NOT SET')"
python -c "import os; print('LLM API:', 'SET' if (os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')) else 'NOT SET')"
```

---

## 🎬 During Recording - Command Flow

### Terminal 1: CLI Demo
```bash
# Command 1
python -c "from src.config import Config; Config.print_config()"

# Command 2
python -m src.main analyze-issue [YOUR_TESTED_ISSUE_URL]

# Command 3
python -m src.main ask openai/openai-python "What is the project structure?"

# Command 4 (optional)
python -m src.main interactive
```

### Terminal 2: Streamlit Demo
```bash
cd github_agent
streamlit run streamlit_app.py
```

**Then in browser:**
1. Show sidebar configuration
2. Tab 1: Analyze Issue - paste URL and click analyze
3. Tab 2: Ask Repository - enter repo and question
4. Tab 3: Examples - show use cases

---

## 💡 Time-Saving Tips

1. **Have two terminals open:**
   - Terminal 1: For CLI demos
   - Terminal 2: For Streamlit (keep running)

2. **Pre-type commands in a text file:**
   - Just copy-paste during recording
   - Saves time and prevents typos

3. **Browser bookmarks:**
   - Bookmark example repositories
   - Have issue URLs ready

4. **Test run everything:**
   - Make sure all commands work
   - Note approximate response times
   - Have backup examples ready

---

## ⚠️ Common Issues & Solutions

### Issue: "Module not found"
```bash
# Solution: Make sure you're in the right directory
cd github_agent
# Or use absolute imports
python -m src.main analyze-issue [URL]
```

### Issue: "API key not set"
```bash
# Solution: Check .env file exists
cat .env  # Mac/Linux
type .env  # Windows
# Or set temporarily
export GITHUB_TOKEN="your_token"  # Mac/Linux
$env:GITHUB_TOKEN="your_token"  # Windows PowerShell
```

### Issue: Streamlit won't open
```bash
# Solution: Specify port manually
streamlit run streamlit_app.py --server.port 8501

# Or check if port is in use
netstat -an | grep 8501  # Mac/Linux
netstat -an | findstr 8501  # Windows
```

### Issue: Agent takes too long
```bash
# Solution: Use simpler questions or smaller repos
# Or increase timeout in config.py
# Or edit the agent to use fewer iterations
```

---

## 🎯 Quick Demo Script (5-minute version)

If you need a shorter demo, use this flow:

```bash
# 1. Show config (10 seconds)
python -c "from src.config import Config; Config.print_config()"

# 2. CLI - one example (2 minutes)
python -m src.main ask fastapi/fastapi "What is this repository about?"

# 3. Streamlit - quick demo (2 minutes)
streamlit run streamlit_app.py
# - Show UI
# - Run one quick query

# 4. Wrap up (30 seconds)
```

---

## 📝 Backup Examples (If Something Fails)

Have these ready in case your primary examples don't work:

### Backup Issue URLs:
- Create your own test repository with sample issues
- Use well-known issues from popular repos
- Have 2-3 backup URLs ready

### Backup Questions:
- "What files are in this repository?"
- "What is the README about?"
- "List the main Python files"
- Simple questions that always work

### Backup Repositories:
- `pallets/flask` - Simple, well-documented
- `requests/requests` - Classic Python library
- `python/cpython` - If you want to show scalability
- Your own public repositories

---

## 🔧 Environment Setup Commands

### First-time Setup (Do Before Recording):
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installations
python -c "import langchain; print('LangChain version:', langchain.__version__)"
python -c "import langgraph; print('LangGraph installed')"
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"

# Test GitHub access
python -c "from src.tools.github_tools import get_github_client; print('GitHub client:', get_github_client())"

# Test Tavily
python -c "from src.config import Config; print('Tavily API:', 'Configured' if Config.TAVILY_API_KEY else 'Missing')"
```

---

Good luck with your demo! 🎬🚀
