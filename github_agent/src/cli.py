"""Command-line interface for GitHub Repository Analyzer Agent.

Provides easy access to agent functionality via CLI commands.
"""
import click
from rich.console import Console
from rich.markdown import Markdown
from langchain_core.messages import AIMessage

from src.main import analyze_issue, ask_about_repository, interactive_session
from src.config import Config

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """GitHub Repository Analyzer Agent
    
    An AI agent that analyzes GitHub repositories, investigates issues,
    and answers questions about code.
    """
    # Validate configuration on startup
    if not Config.validate():
        console.print("\n[red]❌ Configuration Error![/red]")
        console.print("Please update your .env file with required API keys.")
        console.print("\nRequired:")
        console.print("  - GITHUB_TOKEN")
        console.print("  - TAVILY_API_KEY")
        console.print("  - Either OPENAI_API_KEY or ANTHROPIC_API_KEY")
        raise click.Abort()


@cli.command()
@click.argument('issue_url')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def issue(issue_url, verbose):
    """Analyze a GitHub issue and provide investigation report.
    
    ISSUE_URL: Full GitHub issue URL
    
    Example:
        github-agent issue https://github.com/owner/repo/issues/123
    """
    console.print(f"\n[bold cyan]🔍 Analyzing Issue:[/bold cyan] {issue_url}\n")
    
    try:
        result = analyze_issue(issue_url)
        
        # Extract final AI response
        response = None
        for msg in reversed(result.get("messages", [])):
            if isinstance(msg, AIMessage):
                response = msg.content
                break
        
        if response:
            console.print("\n[bold green]📋 Investigation Report:[/bold green]\n")
            md = Markdown(response)
            console.print(md)
        else:
            console.print("[yellow]⚠️  No response from agent[/yellow]")
        
        # Show files created if verbose
        if verbose:
            files = result.get("files", {})
            console.print(f"\n[dim]💾 Files created: {len(files)}[/dim]")
            for filename in files.keys():
                console.print(f"[dim]  - {filename}[/dim]")
        
        console.print("\n[bold green]✅ Analysis complete![/bold green]\n")
        
    except Exception as e:
        console.print(f"\n[red]❌ Error:[/red] {str(e)}\n")
        if verbose:
            import traceback
            console.print("[dim]" + traceback.format_exc() + "[/dim]")
        raise click.Abort()


@cli.command()
@click.argument('repo_name')
@click.argument('question', nargs=-1, required=True)
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def ask(repo_name, question, verbose):
    """Ask a question about a GitHub repository.
    
    REPO_NAME: Repository in owner/repo format
    QUESTION: Your question about the repository
    
    Example:
        github-agent ask langchain-ai/langchain "How does ChatOpenAI work?"
    """
    question_text = " ".join(question)
    
    console.print(f"\n[bold cyan]🔍 Repository:[/bold cyan] {repo_name}")
    console.print(f"[bold cyan]❓ Question:[/bold cyan] {question_text}\n")
    
    try:
        result = ask_about_repository(repo_name, question_text)
        
        # Extract final AI response
        response = None
        for msg in reversed(result.get("messages", [])):
            if isinstance(msg, AIMessage):
                response = msg.content
                break
        
        if response:
            console.print("\n[bold green]💡 Answer:[/bold green]\n")
            md = Markdown(response)
            console.print(md)
        else:
            console.print("[yellow]⚠️  No response from agent[/yellow]")
        
        # Show files created if verbose
        if verbose:
            files = result.get("files", {})
            console.print(f"\n[dim]💾 Files created: {len(files)}[/dim]")
        
        console.print("\n[bold green]✅ Complete![/bold green]\n")
        
    except Exception as e:
        console.print(f"\n[red]❌ Error:[/red] {str(e)}\n")
        if verbose:
            import traceback
            console.print("[dim]" + traceback.format_exc() + "[/dim]")
        raise click.Abort()


@cli.command()
def interactive():
    """Start an interactive Q&A session with the agent.
    
    Type your questions and the agent will respond.
    Type 'exit' or 'quit' to end the session.
    
    Example:
        github-agent interactive
    """
    try:
        interactive_session()
    except Exception as e:
        console.print(f"\n[red]❌ Error:[/red] {str(e)}\n")
        raise click.Abort()


@cli.command()
def config():
    """Show current configuration and validate setup."""
    console.print("\n[bold cyan]🔧 Configuration Status:[/bold cyan]\n")
    
    Config.print_config()
    
    if Config.validate():
        console.print("\n[bold green]✅ Configuration is valid![/bold green]")
        console.print("\nYou're ready to use the GitHub Repository Analyzer.\n")
    else:
        console.print("\n[bold red]❌ Configuration is incomplete.[/bold red]")
        console.print("\nPlease update your .env file.\n")


@cli.command()
def info():
    """Show information about the agent and its capabilities."""
    info_text = """
# GitHub Repository Analyzer Agent

An intelligent AI agent that helps you analyze GitHub repositories,
investigate issues, and answer questions about code.

## Features

- 🔍 **Issue Analysis**: Deep investigation of GitHub issues with stack trace analysis
- 💡 **Repository Q&A**: Ask natural language questions about any repo
- 🌐 **Error Research**: Search for solutions and documentation online
- 📊 **Code Investigation**: Navigate repo structure and trace dependencies
- 🤖 **Sub-Agents**: Specialized agents for focused research

## Sub-Agents

1. **repo-investigator**: Analyzes code structure and locates files
2. **error-researcher**: Researches errors and finds solutions

## Available Tools (16)

**GitHub Tools:**
- search_code_in_repo, read_file_from_repo, list_repository_structure
- get_issue_details, get_repository_info

**Search Tools:**
- search_error_solution, search_documentation

**File & Analysis:**
- ls, read_file, write_file
- extract_stack_trace, parse_error_from_issue, think_tool

**Management:**
- write_todos, read_todos, mark_todo_done

## Usage Examples

```bash
# Analyze a GitHub issue
github-agent issue https://github.com/owner/repo/issues/123

# Ask about a repository
github-agent ask langchain-ai/langchain "How does ChatOpenAI work?"

# Interactive mode
github-agent interactive

# Check configuration
github-agent config
```

## Architecture

Built with:
- LangChain & LangGraph for agent orchestration
- PyGithub for GitHub API access
- Tavily for AI-powered web search
- OpenAI GPT-4o-mini or Anthropic Claude
"""
    
    md = Markdown(info_text)
    console.print(md)


if __name__ == "__main__":
    cli()
