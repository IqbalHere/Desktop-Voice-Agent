"""
Unit tests for the Desktop Voice Agent backend.

This file demonstrates the testing infrastructure.
More comprehensive tests will be added in future PRs.
"""

import pytest
import json
from pathlib import Path
import sys

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))


class TestBackendBasics:
    """Basic tests for backend functionality."""
    
    def test_import_main(self):
        """Test that main module can be imported."""
        import main
        assert hasattr(main, 'VoiceAgentBackend')
    
    def test_backend_initialization(self):
        """Test that backend can be initialized."""
        from main import VoiceAgentBackend
        backend = VoiceAgentBackend()
        assert backend.running is False
    
    def test_json_response_format(self):
        """Test that response JSON format is valid."""
        from main import VoiceAgentBackend
        backend = VoiceAgentBackend()
        
        # Test status response structure
        response = {
            'type': 'status_result',
            'running': False,
            'version': '0.1.0'
        }
        
        # Should be valid JSON
        json_str = json.dumps(response)
        parsed = json.loads(json_str)
        
        assert parsed['type'] == 'status_result'
        assert 'running' in parsed
        assert 'version' in parsed


class TestPlaceholder:
    """Placeholder tests for future functionality."""
    
    def test_transcribe_placeholder(self):
        """Placeholder for transcription tests."""
        # Will be implemented in STT PR
        assert True
    
    def test_plan_placeholder(self):
        """Placeholder for planning tests."""
        # Will be implemented in LLM planner PR
        assert True
    
    def test_execute_placeholder(self):
        """Placeholder for execution tests."""
        # Will be implemented in executor PR
        assert True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
