"""Analysis and utility tools for code investigation."""
from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
import re

from src.state import GitHubAgentState


@tool
def extract_stack_trace(text: str) -> str:
    """Parse and extract stack trace information from text.
    
    Identifies:
    - Error types and messages
    - File paths and line numbers
    - Function names in the call stack
    - Exception chains
    
    Args:
        text: Text containing potential stack trace
    
    Returns:
        Structured analysis of the stack trace
    
    Examples:
        extract_stack_trace(issue_body)
    """
    findings = {
        'error_type': None,
        'error_message': None,
        'files': [],
        'line_numbers': [],
        'functions': [],
    }
    
    # Common patterns
    error_pattern = r'(\w+Error|\w+Exception):\s*(.+)'
    file_pattern = r'File\s+"([^"]+)",\s+line\s+(\d+)'
    function_pattern = r'in\s+(\w+)\s*\('
    traceback_pattern = r'Traceback\s*\(most recent call last\):'
    
    # Extract error type and message
    error_match = re.search(error_pattern, text)
    if error_match:
        findings['error_type'] = error_match.group(1)
        findings['error_message'] = error_match.group(2).strip()
    
    # Extract file paths and line numbers
    for match in re.finditer(file_pattern, text):
        file_path = match.group(1)
        line_num = match.group(2)
        findings['files'].append(file_path)
        findings['line_numbers'].append(int(line_num))
    
    # Extract function names
    for match in re.finditer(function_pattern, text):
        function_name = match.group(1)
        if function_name not in findings['functions']:
            findings['functions'].append(function_name)
    
    # Check if it's actually a stack trace
    has_traceback = re.search(traceback_pattern, text, re.IGNORECASE) is not None
    
    # Build output
    if not findings['error_type'] and not has_traceback:
        return "⚠️ No clear stack trace found in the text."
    
    output = ["# Stack Trace Analysis\n"]
    
    if findings['error_type']:
        output.append(f"**Error Type:** {findings['error_type']}")
    
    if findings['error_message']:
        output.append(f"**Error Message:** {findings['error_message']}\n")
    
    if findings['files']:
        output.append("## Files Mentioned")
        for file_path, line_num in zip(findings['files'], findings['line_numbers']):
            output.append(f"- `{file_path}` at line {line_num}")
        output.append("")
    
    if findings['functions']:
        output.append("## Functions in Call Stack")
        for func in findings['functions']:
            output.append(f"- `{func}()`")
        output.append("")
    
    output.append("💡 Next steps:")
    output.append("1. Search code for mentioned files")
    output.append("2. Read the specific file and line")
    output.append("3. Search online for the error message")
    
    return "\n".join(output)


@tool  
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection and planning.
    
    Use this to:
    - Analyze findings after each search or investigation
    - Assess if you have enough information
    - Plan next steps systematically
    - Decide whether to continue or conclude
    
    This creates a deliberate pause for quality decision-making.
    
    When to use:
    - After receiving search results
    - Before deciding next steps
    - When assessing research gaps
    - Before concluding investigation
    
    Reflection should address:
    1. What concrete information have I gathered?
    2. What crucial information is still missing?
    3. Do I have sufficient evidence for a good answer?
    4. Should I continue searching or provide my answer?
    
    Args:
        reflection: Your detailed reflection on progress and next steps
    
    Returns:
        Confirmation that reflection was recorded
    
    Examples:
        think_tool("I found the error in oauth.py line 45. The access_token key is missing validation...")
    """
    return f"💭 Reflection recorded: {reflection[:100]}..." if len(reflection) > 100 else f"💭 Reflection recorded: {reflection}"


@tool
def parse_error_from_issue(
    issue_content: str,
    state: Annotated[GitHubAgentState, InjectedState]
) -> str:
    """Parse error information from a GitHub issue.
    
    Extracts and structures:
    - Error messages
    - Stack traces
    - Environment info
    - Steps to reproduce
    
    Args:
        issue_content: The issue body/description text
    
    Returns:
        Structured summary of the error
    
    Examples:
        parse_error_from_issue(issue_body)
    """
    # Use extract_stack_trace for stack trace analysis
    stack_analysis = extract_stack_trace(issue_content)
    
    # Look for common sections
    sections = {}
    
    # Patterns for common issue sections
    section_patterns = {
        'environment': r'##?\s*environment',
        'steps': r'##?\s*(?:steps to reproduce|reproduction)',
        'expected': r'##?\s*expected (?:behavior|result)',
        'actual': r'##?\s*actual (?:behavior|result)',
        'version': r'version[:：]\s*([^\n]+)',
    }
    
    for section_name, pattern in section_patterns.items():
        match = re.search(pattern, issue_content, re.IGNORECASE)
        if match:
            sections[section_name] = "Found"
    
    # Build output
    output = ["# Issue Error Analysis\n"]
    
    output.append(stack_analysis)
    output.append("\n## Issue Structure")
    
    if sections:
        for section, status in sections.items():
            output.append(f"- {section.title()}: ✅ {status}")
    else:
        output.append("- ⚠️ No standard issue template sections found")
    
    output.append("\n💡 Recommendation:")
    output.append("1. Use read_file() to access the full issue details")
    output.append("2. Search for the specific file mentioned in stack trace")
    output.append("3. Research the error message online")
    
    return "\n".join(output)
