"""Analysis tools for code investigation and error extraction.

Provides utilities for parsing stack traces, analyzing dependencies,
and extracting structured information from code and errors.
"""
import re
from typing import Annotated
from langchain_core.tools import tool
from github import Github

from src.config import Config


# Initialize GitHub client
github_client = Github(Config.GITHUB_TOKEN)


@tool
def extract_stack_trace(text: str) -> str:
    """Parse and extract stack trace information from text.
    
    Analyzes text (like issue descriptions or error logs) to find stack traces,
    error messages, file paths, line numbers, and function names.
    
    Args:
        text: Text containing potential stack trace or error information
    
    Returns:
        Structured breakdown of the error information found
    
    Example:
        extract_stack_trace(issue_body)
    """
    result = []
    result.append("🔍 Stack Trace Analysis\n")
    
    # Detect error type and message
    error_patterns = [
        r'(\w+Error): (.+)',
        r'(\w+Exception): (.+)',
        r'(\w+Warning): (.+)',
        r'Error: (.+)',
        r'ERROR: (.+)'
    ]
    
    errors_found = []
    for pattern in error_patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        errors_found.extend(matches)
    
    if errors_found:
        result.append("## Errors/Exceptions Found\n")
        for i, error in enumerate(errors_found[:5], 1):  # First 5
            if isinstance(error, tuple):
                result.append(f"{i}. **{error[0]}**: {error[1]}")
            else:
                result.append(f"{i}. {error}")
    
    # Extract file paths
    file_patterns = [
        r'File "([^"]+)", line (\d+)',  # Python style
        r'at ([/\w.-]+):(\d+):(\d+)',  # JavaScript style
        r'([/\w.-]+\.py):(\d+)',  # Simple Python
        r'([/\w.-]+\.js):(\d+)',  # Simple JavaScript
    ]
    
    files_found = []
    for pattern in file_patterns:
        matches = re.findall(pattern, text)
        files_found.extend(matches)
    
    if files_found:
        result.append("\n## Files and Line Numbers\n")
        for i, file_info in enumerate(list(set(files_found))[:10], 1):  # First 10 unique
            if isinstance(file_info, tuple) and len(file_info) >= 2:
                result.append(f"{i}. `{file_info[0]}` - Line {file_info[1]}")
            else:
                result.append(f"{i}. `{file_info}`")
    
    # Extract function names
    function_patterns = [
        r'in (\w+)\(',  # Python style
        r'function (\w+)',  # JavaScript
        r'def (\w+)\(',  # Python definition
    ]
    
    functions_found = []
    for pattern in function_patterns:
        matches = re.findall(pattern, text)
        functions_found.extend(matches)
    
    if functions_found:
        result.append("\n## Functions Mentioned\n")
        unique_funcs = list(set(functions_found))[:10]
        for i, func in enumerate(unique_funcs, 1):
            result.append(f"{i}. `{func}()`")
    
    # Extract library/package names
    import_patterns = [
        r'import (\w+)',
        r'from ([\w.]+)',
        r'require\([\'"]([^\'"]+)[\'"]\)',
    ]
    
    libraries_found = []
    for pattern in import_patterns:
        matches = re.findall(pattern, text)
        libraries_found.extend(matches)
    
    if libraries_found:
        result.append("\n## Libraries/Packages Referenced\n")
        unique_libs = list(set(libraries_found))[:10]
        for i, lib in enumerate(unique_libs, 1):
            result.append(f"{i}. `{lib}`")
    
    # Summary
    result.append("\n## Summary\n")
    result.append(f"- Errors found: {len(errors_found)}")
    result.append(f"- Files referenced: {len(set(files_found))}")
    result.append(f"- Functions mentioned: {len(set(functions_found))}")
    result.append(f"- Libraries detected: {len(set(libraries_found))}")
    
    if not any([errors_found, files_found, functions_found, libraries_found]):
        result.append("\n⚠️ No clear stack trace or error pattern detected in the text.")
        result.append("The text may not contain a standard stack trace format.")
    
    return '\n'.join(result)


@tool
def find_code_dependencies(
    repo_name: str,
    file_path: str
) -> str:
    """Analyze imports and dependencies in a code file.
    
    Examines a code file to identify imports, external dependencies,
    and internal module references.
    
    Args:
        repo_name: Full repository name (owner/repo)
        file_path: Path to the file in the repository
    
    Returns:
        List of dependencies found in the file
    
    Example:
        find_code_dependencies("langchain-ai/langchain", "src/chat_models/openai.py")
    """
    try:
        repo = github_client.get_repo(repo_name)
        file_content = repo.get_contents(file_path)
        code = file_content.decoded_content.decode('utf-8')
        
        result = []
        result.append(f"📦 Dependency Analysis: {file_path}\n")
        
        # Python imports
        import_pattern = r'^(?:from ([\w.]+) import|import ([\w.,\s]+))'
        imports = re.findall(import_pattern, code, re.MULTILINE)
        
        if imports:
            result.append("## Python Imports\n")
            external = []
            internal = []
            
            for imp in imports:
                module = imp[0] if imp[0] else imp[1]
                # Guess if external (no dot) or internal (has dot or relative)
                if '.' in module or module.startswith('.'):
                    internal.append(module)
                else:
                    external.append(module)
            
            if external:
                result.append("### External Libraries")
                for lib in sorted(set(external)):
                    result.append(f"- `{lib}`")
            
            if internal:
                result.append("\n### Internal Modules")
                for mod in sorted(set(internal)):
                    result.append(f"- `{mod}`")
        
        # JavaScript/TypeScript imports
        js_import_pattern = r'(?:import .+ from [\'"]([^\'"]+)[\'"]|require\([\'"]([^\'"]+)[\'"]\))'
        js_imports = re.findall(js_import_pattern, code)
        
        if js_imports:
            result.append("\n## JavaScript/TypeScript Imports\n")
            for imp in js_imports:
                module = imp[0] if imp[0] else imp[1]
                result.append(f"- `{module}`")
        
        result.append(f"\n**Total imports found:** {len(imports) + len(js_imports)}")
        
        return '\n'.join(result)
        
    except Exception as e:
        return f"❌ Error analyzing dependencies: {str(e)}"


# Export all tools
__all__ = ['extract_stack_trace', 'find_code_dependencies']
