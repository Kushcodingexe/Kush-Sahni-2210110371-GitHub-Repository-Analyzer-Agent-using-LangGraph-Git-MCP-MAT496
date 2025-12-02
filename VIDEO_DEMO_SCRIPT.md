# Video Demo Script - GitHub Repository Analyzer Agent

## 📋 Video Overview
**Duration:** ~10 minutes  
**Requirements:** Face visible, clear audio, screen recording  
**Upload:** YouTube or Google Drive, link in README.md

---

## 🎬 SECTION 1: Introduction (1-2 minutes)

### On Camera (Face Visible)
**[Look at camera, smile, professional but friendly]**

> "Hello! I'm [Your Name], and today I'm presenting my MAT496 Capstone Project - a GitHub Repository Analyzer Agent built using LangGraph.
>
> This project is an AI-powered agent that can analyze GitHub repositories and issues, helping developers understand codebases, debug errors, and find solutions faster.
>
> Let me quickly explain what this agent does."

### What the Agent Does

**[Switch to screen share showing README or diagram]**

> "**Input:** The agent takes two types of input:
> 1. A GitHub issue URL - for investigating bugs and errors
> 2. A repository name and a question - for understanding code
>
> **Output:** The agent provides:
> - Detailed investigation reports for issues
> - Comprehensive answers about repository structure and code
> - Error solutions with recommendations
> - Context files for further analysis
>
> **How it works:** The agent uses a multi-agent architecture powered by LangGraph. The main orchestrator delegates tasks to specialized sub-agents:
> - **RepoInvestigator**: Searches code, reads files, and understands repository structure
> - **ErrorResearcher**: Searches the web for error solutions and documentation
>
> The agent has access to over 16 specialized tools including GitHub API access, web search via Tavily, file system operations, and code analysis capabilities."

---

## 🎬 SECTION 2: Architecture Quick Walkthrough (1-2 minutes)

### Show Project Structure

**[Open VS Code or File Explorer, show project structure]**

> "Let me quickly show you the project structure.
>
> The main components are:
> - **src/main.py** - The main orchestrator agent
> - **src/agents/** - Contains the RepoInvestigator and ErrorResearcher sub-agents
> - **src/tools/** - 16+ tools organized in categories: GitHub tools, search tools, file tools, and analysis tools
> - **src/state.py** - State management using Pydantic models for LangGraph
> - **src/cli.py** - Command-line interface using Click
> - **streamlit_app.py** - Beautiful web UI for the agent
>
> The agent uses:
> - **LangGraph** for orchestration and state management
> - **LangChain** for agent framework and tool calling
> - **PyGithub** for GitHub API access
> - **Tavily** for AI-powered web search
> - **Anthropic Claude** or **OpenAI GPT-4** as the LLM backend"

### Show LangSmith Traces (Optional)

**[Open LangSmith dashboard if you have it]**

> "Here you can see my LangSmith traces showing the agent in action - you can see the tool calls, reasoning steps, and sub-agent delegations."

---

## 🎬 SECTION 3: CLI Demo (3-4 minutes)

### Setup and Configuration

**[Open terminal/PowerShell]**

> "First, let me show you the CLI interface. The project is already set up with all dependencies installed.
>
> Let me verify the configuration:"

**[Type command]**
```bash
python -c "from src.config import Config; Config.print_config()"
```

> "As you can see, all API keys are configured - GitHub token, Tavily API, and the LLM API."

### Demo 1: Analyze a GitHub Issue

**[Type command]**
```bash
python -m src.main analyze-issue https://github.com/[owner]/[repo]/issues/[number]
```

**[Example - use a real issue you've tested]**
```bash
python -m src.main analyze-issue https://github.com/langchain-ai/langchain/issues/12345
```

> "I'm analyzing a real GitHub issue. Watch how the agent:
> 1. Fetches the issue details
> 2. Extracts error messages and stack traces
> 3. Searches the repository for relevant files
> 4. Researches solutions online
> 5. Generates a comprehensive investigation report"

**[Wait for output, then explain]**

> "As you can see, the agent has:
> - Identified the error type and location
> - Found relevant code files
> - Searched for similar issues and solutions
> - Provided actionable recommendations
> - Created context files for further investigation"

### Demo 2: Ask About a Repository

**[Type command]**
```bash
python -m src.main ask openai/openai-python "What is the project structure and main components?"
```

> "Now let's ask a question about the OpenAI Python SDK. The agent will:
> 1. Fetch repository information
> 2. Analyze the repository structure
> 3. Read relevant files like README and package structure
> 4. Provide a detailed answer"

**[Wait for output, show the response]**

> "The agent has analyzed the repository and given us a comprehensive overview of the project structure, main modules, and how they work together."

### Demo 3: Interactive Mode (Optional)

**[Type command]**
```bash
python -m src.main interactive
```

> "The agent also has an interactive mode where you can have a conversation. Let me ask a few questions..."

**[Type a question]**
```
What tools do you have available?
```

**[Type another question]**
```
Can you help me understand a Python error?
```

**[Exit with 'exit' or 'quit']**

---

## 🎬 SECTION 4: Streamlit UI Demo (3-4 minutes)

### Launch Streamlit

**[Open new terminal]**
```bash
cd github_agent
streamlit run streamlit_app.py
```

**[Wait for browser to open - should show the beautiful UI]**

> "Now let me show you the production-ready web interface I built using Streamlit.
>
> As you can see, it has a modern, beautiful design with:
> - A gradient header
> - Sidebar showing configuration status and agent info
> - Three main tabs: Analyze Issue, Ask Repository, and Examples"

### UI Walkthrough

**[Navigate through the UI]**

> "The sidebar shows:
> - API key configuration status (all green checkmarks)
> - The current LLM model being used
> - Maximum sub-agents allowed
> - Links to documentation"

### Demo 1: Analyze Issue in UI

**[Click on 'Analyze Issue' tab]**

> "Let's analyze a GitHub issue using the UI."

**[Enter issue URL]**
```
https://github.com/[owner]/[repo]/issues/[number]
```

**[Click 'Analyze' button]**

> "Watch the progress indicators - it shows:
> - Fetching issue details
> - Analyzing code and errors
> - Generating report
>
> The UI provides a much better user experience with progress tracking and structured output."

**[Show the results]**

> "Here's the investigation report formatted beautifully in markdown, and you can expand to see the context files that were created."

### Demo 2: Ask Repository in UI

**[Click on 'Ask Repository' tab]**

> "Now let's ask a question about a repository."

**[Enter repository and question]**
```
Repository: fastapi/fastapi
Question: How does dependency injection work in FastAPI?
```

**[Click 'Ask Agent' button]**

> "The agent is now researching the FastAPI repository..."

**[Show results]**

> "And here's a comprehensive answer about FastAPI's dependency injection system, pulled directly from analyzing the actual codebase."

### Demo 3: Examples Tab

**[Click on 'Examples' tab]**

> "The Examples tab provides sample use cases and quick test buttons to help users get started quickly."

---

## 🎬 SECTION 5: Key Features Highlight (1 minute)

**[Back to camera or screen with slides/notes]**

> "Let me highlight the key features that demonstrate what I learned in MAT496:
>
> **1. Prompting:** I created custom system prompts for the main agent and each sub-agent to guide their behavior and ensure they use the right tools.
>
> **2. Structured Output:** All state management uses Pydantic models, ensuring type safety and validation throughout the agent's execution.
>
> **3. RAG (Retrieval Augmented Generation):** The agent fetches repository files, issue details, and web search results to provide context for accurate analysis.
>
> **4. Tool Calling:** The agent has 16+ tools including GitHub API access, web search, file operations, and custom analysis tools.
>
> **5. LangGraph:** The heart of the system - a state machine with nodes for agent reasoning, tool execution, and sub-agent delegation.
>
> **6. Multi-Agent Architecture:** Specialized sub-agents handle specific tasks, making the system modular and efficient.
>
> **7. Error Handling:** Robust error handling with helpful messages and debugging support via LangSmith."

---

## 🎬 SECTION 6: Conclusion (30 seconds)

**[Back to camera, face visible]**

> "This project successfully combines all the concepts from MAT496 - prompting, structured output, RAG, tool calling, and LangGraph - into a practical application that solves a real problem for developers.
>
> The agent can genuinely help developers understand unfamiliar codebases, debug complex issues, and find solutions faster than manual investigation.
>
> Thank you for watching! The full code, documentation, and setup instructions are available in my GitHub repository. Feel free to try it out!"

**[Smile and wave]**

---

## 📝 Pre-Recording Checklist

### Before You Start Recording:

- [ ] **Test all demos beforehand** - Make sure everything works
- [ ] **Prepare example repositories and issues** - Have URLs ready to copy-paste
- [ ] **Clear your terminal history** - Keep it clean for the video
- [ ] **Close unnecessary tabs/applications** - Professional screen
- [ ] **Check your environment variables** - Make sure API keys work
- [ ] **Test your camera and microphone** - Good lighting and clear audio
- [ ] **Have notes visible** - But don't read them word-for-word
- [ ] **Prepare your workspace** - Clean background if recording face

### Good Testing Examples to Use:

**For Issue Analysis:**
- Any public repository with clear error issues
- Your own test repository with sample issues
- Popular repos like `langchain-ai/langchain`, `openai/openai-python`

**For Repository Questions:**
- `fastapi/fastapi` - "Explain the project structure"
- `openai/openai-python` - "How does authentication work?"
- `langchain-ai/langchain` - "What is the agent architecture?"

---

## 🎥 Recording Tips

1. **Speak clearly and at a moderate pace** - Don't rush
2. **Show enthusiasm** - You built something cool!
3. **Pause between sections** - Easier to edit later
4. **If you make a mistake** - Pause, then restart that section
5. **Keep it under 10 minutes** - Respect the time limit
6. **Show, don't just tell** - Demonstrate features live
7. **Point at the screen** - Use cursor to highlight important things
8. **Smile when on camera** - Be confident and friendly

---

## 🔗 After Recording

1. **Review the video** - Make sure audio and video are clear
2. **Edit if needed** - Cut out long pauses or mistakes
3. **Upload to YouTube** (unlisted) or Google Drive (anyone with link)
4. **Add to README.md** - Include the link prominently
5. **Test the link** - Make sure it works in incognito mode

---

## 📌 README.md Update

Add this section near the top of your README.md:

```markdown
## 🎥 Video Demo

**Watch the 10-minute demo video:** [YouTube Link](https://youtube.com/watch?v=YOUR_VIDEO_ID) or [Google Drive Link](https://drive.google.com/file/d/YOUR_FILE_ID/view)

In this video, I demonstrate:
- The overall agent architecture and how it works
- CLI interface with live examples
- Streamlit web UI with real-time analysis
- Analyzing GitHub issues and answering repository questions
```

---

## ⏱️ Suggested Time Breakdown

| Section | Duration | Content |
|---------|----------|---------|
| Introduction | 1-2 min | Who you are, what the agent does |
| Architecture | 1-2 min | Quick code walkthrough |
| CLI Demo | 3-4 min | Analyze issue + Ask repo |
| Streamlit Demo | 3-4 min | UI walkthrough + demos |
| Key Features | 1 min | Highlight MAT496 concepts |
| Conclusion | 30 sec | Wrap up and thank you |
| **Total** | **~10 min** | |

---

## 💡 Pro Tips

- **Practice first** - Do a few dry runs before recording
- **Use OBS Studio or similar** - For better quality screen recording
- **Record in 1080p** - Clear and professional
- **Use a decent microphone** - Built-in laptop mic is usually fine
- **Good lighting for face shots** - Natural light from window or lamp
- **Close notification popups** - Turn on Do Not Disturb
- **Have water nearby** - In case you need to clear your throat
- **Record in one take if possible** - But don't stress if you need multiple takes

Good luck with your recording! You've built an impressive project! 🚀
