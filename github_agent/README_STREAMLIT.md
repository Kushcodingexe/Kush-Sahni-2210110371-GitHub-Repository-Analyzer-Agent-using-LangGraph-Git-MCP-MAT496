# Streamlit UI Guide

## Quick Start

### 1. Install Streamlit

```bash
pip install streamlit
```

### 2. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## Features ✨

### 🔍 Analyze Issue Tab
- Input any GitHub issue URL
- Get comprehensive investigation report
- See stack trace analysis
- View suggested fixes
- Progress indicators show agent thinking

### 💬 Ask Repository Tab
- Query any public GitHub repository
- Ask natural language questions
- Get detailed answers with code references
- Understand project structure
- Find specific functionality

### 📊 Examples Tab
- Sample use cases
- Quick test buttons
- Copy-paste templates

---

## UI Features

### Modern Design
- ✅ Gradient headers
- ✅ Smooth animations
- ✅ Hover effects
- ✅ Professional color scheme
- ✅ Responsive layout

### User Experience
- ✅ Progress indicators
- ✅ Real-time status updates
- ✅ Clear error messages
- ✅ Expandable context files
- ✅ Configuration dashboard

### Sidebar Info
- API key status checks
- Current model configuration
- Quick links to documentation
- Agent capabilities overview

---

## Screenshots

### Main Interface
The app features a clean, modern interface with:
- Gradient purple header
- Tabbed navigation
- Sidebar with configuration
- Professional styling

### Analyze Issue
1. Enter GitHub issue URL
2. Click "Analyze"
3. Watch progress bar
4. See detailed report

### Ask Repository
1. Enter repository name (owner/repo)
2. Type your question
3. Get AI-powered answer
4. View context files created

---

## Configuration

The UI automatically detects your `.env` configuration and shows:
- ✅ GitHub Token status
- ✅ Tavily API status
- ✅ LLM API status
- Current model being used
- Max concurrent sub-agents

---

## Tips for Best Experience

### 1. Good Questions to Ask
```
"What is this repository about?"
"How does authentication work?"
"Where is the main API defined?"
"Explain the project structure"
"Find error handling code"
```

### 2. Issue Analysis
- Works with any public GitHub issue
- Better results with detailed issues
- Stack traces are automatically extracted
- Related code is automatically found

### 3. Performance
- First query may take 10-30 seconds
- Subsequent queries are faster
- Progress bar shows agent activity
- Context files show research depth

---

## Docker Deployment

Run the Streamlit app in Docker:

```bash
# Add to Dockerfile
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0"]

# Run container
docker run -p 8501:8501 --env-file .env github-agent
```

Access at `http://localhost:8501`

---

## Cloud Deployment

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add secrets (API keys)
5. Deploy!

### Other Platforms
- **Heroku**: Use Procfile with streamlit
- **AWS**: Deploy on EC2 or ECS
- **GCP**: Use Cloud Run
- **Azure**: Container Instances

---

## Customization

### Change Colors
Edit the CSS in `streamlit_app.py`:
```python
--primary-color: #6366f1;    # Purple gradient
--secondary-color: #8b5cf6;  # Darker purple
--success-color: #10b981;    # Green
```

### Add More Tabs
```python
tab4 = st.tabs(["New Feature"])
with tab4:
    st.markdown("### Your Feature")
    # Add your code
```

### Modify Layout
```python
st.set_page_config(
    layout="wide",  # or "centered"
    initial_sidebar_state="expanded"  # or "collapsed"
)
```

---

## Troubleshooting

### App won't start
```bash
# Check if streamlit is installed
pip show streamlit

# Reinstall if needed
pip install streamlit --upgrade
```

### API errors
- Check `.env` file exists
- Verify API keys are correct
- Ensure no quotes around values

### Port already in use
```bash
# Use different port
streamlit run streamlit_app.py --server.port 8502
```

---

## Development

### Run in Development Mode
```bash
streamlit run streamlit_app.py --server.runOnSave true
```

Auto-reloads on file changes!

### Debug Mode
```bash
streamlit run streamlit_app.py --logger.level=debug
```

---

## Next Steps

1. **Try it out**: Run `streamlit run streamlit_app.py`
2. **Customize**: Change colors, add features
3. **Deploy**: Share with others on Streamlit Cloud
4. **Extend**: Add more tabs, visualizations

Enjoy your beautiful AI agent UI! 🚀
