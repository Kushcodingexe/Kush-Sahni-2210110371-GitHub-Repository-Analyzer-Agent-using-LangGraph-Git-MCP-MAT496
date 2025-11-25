"""
Streamlit UI for GitHub Repository Analyzer Agent

A beautiful, modern interface for analyzing GitHub repositories and issues.
"""
import streamlit as st
from src.main import analyze_issue, ask_about_repository
from src.config import Config
import time

# Page configuration
st.set_page_config(
    page_title="GitHub Repository Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, beautiful UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Card styling */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.1);
        transform: translateY(-2px);
    }
    
    /* Result container */
    .result-container {
        background: linear-gradient(to bottom, #f9fafb, #ffffff);
        padding: 2rem;
        border-radius: 1rem;
        border: 2px solid #e5e7eb;
        margin-top: 2rem;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .status-success {
        background-color: #d1fae5;
        color: #065f46;
    }
    
    .status-processing {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f9fafb 0%, #ffffff 100%);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        border-radius: 0.5rem;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 GitHub Repository Analyzer</h1>
    <p>AI-powered code analysis using LangGraph multi-agent system</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 About")
    st.markdown("""
    This agent uses **LangGraph** to:
    - 🔍 Analyze GitHub issues
    - 💬 Answer repository questions
    - 🔎 Research error solutions
    - 📊 Investigate code structure
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Configuration")
    
    # Check API keys
    config_status = []
    if Config.GITHUB_TOKEN:
        config_status.append("✅ GitHub Token")
    else:
        config_status.append("❌ GitHub Token")
    
    if Config.TAVILY_API_KEY:
        config_status.append("✅ Tavily API")
    else:
        config_status.append("❌ Tavily API")
    
    if Config.OPENAI_API_KEY or Config.ANTHROPIC_API_KEY:
        config_status.append("✅ LLM API")
    else:
        config_status.append("❌ LLM API")
    
    for status in config_status:
        st.markdown(status)
    
    st.markdown("---")
    
    st.markdown("### 🤖 Agent Status")
    st.markdown(f"**Model:** {Config.DEFAULT_MODEL}")
    st.markdown(f"**Max Sub-Agents:** {Config.MAX_CONCURRENT_RESEARCH_UNITS}")
    
    st.markdown("---")
    
    st.markdown("""
    ### 📚 Documentation
    - [Getting Started](docs/GETTING_STARTED.md)
    - [API Reference](docs/API.md)
    - [Architecture](docs/ARCHITECTURE.md)
    """)

# Main content - Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Analyze Issue", "💬 Ask Repository", "📊 Examples"])

# Tab 1: Analyze Issue
with tab1:
    st.markdown("### Analyze a GitHub Issue")
    st.markdown("Investigate bugs, extract stack traces, and find solutions")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        issue_url = st.text_input(
            "GitHub Issue URL",
            placeholder="https://github.com/owner/repo/issues/123",
            key="issue_url"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("🔍 Analyze", key="analyze_btn", use_container_width=True)
    
    if analyze_button and issue_url:
        with st.spinner("🤖 Agent is investigating the issue..."):
            # Progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("📥 Fetching issue details...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            status_text.text("🔎 Analyzing code and errors...")
            progress_bar.progress(50)
            
            try:
                # Run analysis
                result = analyze_issue(issue_url)
                
                progress_bar.progress(80)
                status_text.text("📝 Generating report...")
                time.sleep(0.3)
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                time.sleep(0.5)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Display results
                st.success("Analysis Completed Successfully!")
                
                # Extract response
                if result and "messages" in result:
                    for msg in reversed(result["messages"]):
                        if hasattr(msg, 'content'):
                            st.markdown("### 📋 Investigation Report")
                            st.markdown(msg.content)
                            break
                
                # Show files created
                if "files" in result and result["files"]:
                    with st.expander(f"💾 Context Files Created ({len(result['files'])})"):
                        for filename in result["files"].keys():
                            st.code(filename, language="text")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure your API keys are configured correctly in `.env`")

# Tab 2: Ask Repository
with tab2:
    st.markdown("### Ask Questions About a Repository")
    st.markdown("Get insights about any GitHub repository using natural language")
    
    col1, col2 = st.columns(2)
    
    with col1:
        repo_name = st.text_input(
            "Repository (owner/repo)",
            placeholder="openai/openai-python",
            key="repo_name"
        )
    
    with col2:
        question = st.text_input(
            "Your Question",
            placeholder="How does authentication work?",
            key="question"
        )
    
    ask_button = st.button("💬 Ask Agent", key="ask_btn", use_container_width=True)
    
    if ask_button and repo_name and question:
        with st.spinner(f"🤖 Agent is researching {repo_name}..."):
            # Progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("📥 Fetching repository info...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            status_text.text("🔎 Searching code and documentation...")
            progress_bar.progress(50)
            
            try:
                # Run query
                result = ask_about_repository(repo_name, question)
                
                progress_bar.progress(80)
                status_text.text("📝 Formulating answer...")
                time.sleep(0.3)
                
                progress_bar.progress(100)
                status_text.text("✅ Answer ready!")
                time.sleep(0.5)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Display results
                st.success("Query Completed Successfully!")
                
                # Extract response
                if result and "messages" in result:
                    for msg in reversed(result["messages"]):
                        if hasattr(msg, 'content'):
                            st.markdown("### 💡 Answer")
                            st.markdown(msg.content)
                            break
                
                # Show files created
                if "files" in result and result["files"]:
                    with st.expander(f"💾 Context Files Created ({len(result['files'])})"):
                        for filename in result["files"].keys():
                            st.code(filename, language="text")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure the repository name is correct and accessible")

# Tab 3: Examples
with tab3:
    st.markdown("### 📊 Example Use Cases")
    
    st.markdown("#### 1. Analyze an Issue")
    st.code("""
# Investigate a bug report
URL: https://github.com/langchain-ai/langchain/issues/1234

The agent will:
- Extract the error message and stack trace
- Find relevant code files
- Search for known solutions
- Provide fix recommendations
    """, language="text")
    
    st.markdown("#### 2. Understand a Repository")
    st.code("""
# Learn about a new codebase
Repository: fastapi/fastapi
Question: "Explain the project structure and main components"

The agent will:
- Analyze the repository structure
- Identify key files and modules
- Explain the architecture
- Provide code examples
    """, language="text")
    
    st.markdown("#### 3. Find Specific Code")
    st.code("""
# Locate functionality
Repository: openai/openai-python
Question: "Where is the ChatCompletion class defined?"

The agent will:
- Search for the class definition
- Show file location and line numbers
- Explain how it works
- Show usage examples
    """, language="text")
    
    st.markdown("---")
    
    st.markdown("### 🚀 Quick Test")
    st.markdown("Try these sample queries:")
    
    if st.button("📘 Analyze openai/openai-python structure"):
        st.info("Copy this to 'Ask Repository' tab:")
        st.code("Repository: openai/openai-python\nQuestion: What is this repository about?")
    
    if st.button("🔍 Find authentication code"):
        st.info("Copy this to 'Ask Repository' tab:")
        st.code("Repository: langchain-ai/langchain\nQuestion: Where is authentication handled?")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem 0;">
    <p style="margin: 0;">Built with ❤️ using LangGraph, LangChain, and Streamlit</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.875rem;">MAT496 - Introduction to LLM Course Project</p>
</div>
""", unsafe_allow_html=True)
