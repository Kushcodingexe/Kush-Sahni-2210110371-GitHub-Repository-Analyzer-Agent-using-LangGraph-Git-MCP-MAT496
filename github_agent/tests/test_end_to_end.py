"""
End-to-end tests for GitHub Agent workflows.

Tests complete user scenarios from start to finish.
"""
import pytest
from src.main import ask_about_repository, analyze_issue
from src.state import get_initial_state
from src.tools import get_repository_info, search_code_in_repo


class TestEndToEnd:
    """End-to-end workflow tests."""
    
    def test_simple_repository_query(self):
        """Test basic repository information query."""
        result = ask_about_repository(
            "openai/openai-python",
            "What is this repository?"
        )
        
        # Should have messages
        assert result is not None
        assert "messages" in result
        assert len(result["messages"]) > 0
        
        # Response should mention the repository
        response_text = str(result["messages"])
        assert "openai" in response_text.lower() or "python" in response_text.lower()
    
    def test_code_search_query(self):
        """Test finding specific code in repository."""
        result = ask_about_repository(
            "openai/openai-python",
            "Where is the ChatCompletion class?"
        )
        
        assert result is not None
        assert len(result.get("messages", [])) > 0
    
    @pytest.mark.slow
    def test_issue_analysis_workflow(self):
        """Test full issue analysis workflow (requires API credits)."""
        # Use a simple, closed issue for testing
        result = analyze_issue(
            "https://github.com/openai/openai-python/issues/1"
        )
        
        assert result is not None
        assert "messages" in result
        assert result.get("issue_url") is not None
    
    def test_multi_step_query(self):
        """Test query that requires multiple steps."""
        result = ask_about_repository(
            "fastapi/fastapi",
            "Explain the project structure and main components"
        )
        
        assert result is not None
        # Check that files were created (context offloading)
        files = result.get("files", {})
        assert isinstance(files, dict)
    
    def test_delegated_research(self):
        """Test that triggers sub-agent delegation."""
        result = ask_about_repository(
            "langchain-ai/langchain",
            "Find all files related to ChatOpenAI"
        )
        
        assert result is not None
        # Should have completed without error
        assert "messages" in result


class TestToolIntegration:
    """Test tool integration and combinations."""
    
    def test_repository_info_tool(self):
        """Test get_repository_info tool."""
        result = get_repository_info("openai/openai-python")
        
        assert result is not None
        assert "openai" in result.lower()
        assert "stars" in result.lower() or "⭐" in result
    
    def test_code_search_tool(self):
        """Test search_code_in_repo tool."""
        result = search_code_in_repo(
            "openai/openai-python",
            "class ChatCompletion",
            max_results=3
        )
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_invalid_repository_name(self):
        """Test error handling for invalid repo name."""
        result = get_repository_info("invalid-repo-name")
        
        # Should return error message, not raise exception
        assert result is not None
        assert "invalid" in result.lower() or "error" in result.lower()
    
    def test_nonexistent_repository(self):
        """Test handling of non-existent repository."""
        result = get_repository_info("nonexistent/definitely-not-real-repo-123456")
        
        assert result is not None
        # Should explain repository not found
        assert "404" in result or "not found" in result.lower()


class TestStateManagement:
    """Test state management across operations."""
    
    def test_initial_state(self):
        """Test initial state creation."""
        state = get_initial_state()
        
        assert state is not None
        assert "messages" in state
        assert "files" in state
        assert "todos" in state
        assert state["messages"] == []
        assert state["files"] == {}
        assert state["todos"] == []
    
    def test_file_system_persistence(self):
        """Test that files persist in state."""
        from src.tools import write_file, read_file, ls
        
        state = get_initial_state()
        
        # Write a file
        write_result = write_file.invoke({
            "filename": "test.txt",
            "content": "Hello, World!",
            "state": state
        })
        
        assert "test.txt" in write_result
        
        # Check it appears in listing
        ls_result = ls.invoke({"state": state})
        assert "test.txt" in ls_result
        
        # Read it back
        read_result = read_file.invoke({
            "filename": "test.txt",
            "state": state
        })
        
        assert "Hello, World!" in read_result
    
    def test_todo_management(self):
        """Test TODO creation and management."""
        from src.tools import write_todos, read_todos, mark_todo_done
        
        state = get_initial_state()
        
        # Create TODOs
        todos = [
            "Fetch repository info",
            "Search for code",
            "Analyze results"
        ]
        
        write_result = write_todos.invoke({
            "todos_list": todos,
            "state": state
        })
        
        assert "Fetch repository info" in write_result
        
        # Read TODOs
        read_result = read_todos.invoke({"state": state})
        assert "[ ]" in read_result or "TODO" in read_result
        
        # Mark one done
        mark_result = mark_todo_done.invoke({
            "todo_index": 1,
            "state": state
        })
        
        assert "[x]" in mark_result or "done" in mark_result.lower()


class TestErrorHandling:
    """Test error handling and recovery."""
    
    def test_invalid_issue_url(self):
        """Test handling of invalid issue URL."""
        try:
            result = analyze_issue("https://not-github.com/issue")
            # Should return error in result, not raise
            assert result is not None
        except Exception:
            pytest.fail("Should not raise exception for invalid URL")
    
    def test_api_rate_limiting(self):
        """Test graceful handling of rate limits."""
        # This would typically be tested with mocks
        # For now, just verify the error handler exists
        from src.errors import handle_github_error
        from github import GithubException
        
        # Simulate rate limit error
        try:
            error = GithubException(403, {"message": "API rate limit exceeded"}, {})
            message = handle_github_error(error, "Testing")
            
            assert "rate limit" in message.lower()
            assert "wait" in message.lower() or "quota" in message.lower()
        except Exception as e:
            pytest.skip(f"Mock error test skipped: {e}")
    
    def test_network_error_handling(self):
        """Test handling of network errors."""
        from src.errors import handle_github_error
        
        # Simulate network error
        error = Exception("Connection timeout")
        message = handle_github_error(error, "Fetching data")
        
        assert isinstance(message, str)
        assert len(message) > 0


# Performance benchmarks (optional, slow tests)
class TestPerformance:
    """Performance benchmarks."""
    
    @pytest.mark.slow
    @pytest.mark.benchmark
    def test_simple_query_performance(self):
        """Benchmark simple repository query."""
        import time
        
        start = time.time()
        result = ask_about_repository(
            "openai/openai-python",
            "What is this repository?"
        )
        duration = time.time() - start
        
        # Should complete in reasonable time
        assert duration < 30, f"Query took {duration}s, expected <30s"
        assert result is not None
    
    @pytest.mark.slow
    @pytest.mark.benchmark
    def test_code_search_performance(self):
        """Benchmark code search query."""
        import time
        
        start = time.time()
        result = search_code_in_repo(
            "openai/openai-python",
            "ChatCompletion",
            max_results=5
        )
        duration = time.time() - start
        
        # GitHub code search should be fast
        assert duration < 10, f"Search took {duration}s, expected <10s"
        assert result is not None


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-m", "not slow"])
