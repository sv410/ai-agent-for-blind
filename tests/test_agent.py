"""Test the core AI Agent functionality."""

import pytest
import asyncio
from unittest.mock import Mock, patch

from ai_agent.core.agent import AIAgent
from ai_agent.core.config import Config


class TestAIAgent:
    """Test cases for the AIAgent class."""
    
    @pytest.fixture
    def config(self):
        """Create a test configuration."""
        return Config(
            openai_api_key=None,
            tts_rate=150,
            debug_mode=True,
            log_file=None  # Don't create log files in tests
        )
    
    @pytest.fixture
    def agent(self, config):
        """Create an AI agent for testing."""
        with patch('ai_agent.core.agent.setup_logger'), \
             patch('ai_agent.speech.tts.TextToSpeech'), \
             patch('ai_agent.speech.stt.SpeechToText'), \
             patch('ai_agent.vision.image_analyzer.ImageAnalyzer'):
            return AIAgent(config)
    
    def test_agent_initialization(self, agent):
        """Test that the agent initializes properly."""
        assert agent is not None
        assert agent.config is not None
        assert agent.session_history == []
        assert agent.is_listening is False
    
    @pytest.mark.asyncio
    async def test_process_text_command_hello(self, agent):
        """Test processing a greeting command."""
        response = await agent.process_text_command("Hello")
        
        assert "Hello!" in response
        assert "AI assistant" in response
        assert len(agent.session_history) == 1
        assert agent.session_history[0]["type"] == "user_input"
        assert agent.session_history[0]["content"] == "Hello"
    
    @pytest.mark.asyncio
    async def test_process_text_command_time(self, agent):
        """Test processing a time request."""
        response = await agent.process_text_command("What time is it?")
        
        assert "current time is" in response
        assert len(agent.session_history) == 1
    
    @pytest.mark.asyncio
    async def test_process_text_command_help(self, agent):
        """Test processing a help request."""
        response = await agent.process_text_command("help")
        
        assert "I can help you with" in response
        assert "Describe images" in response
        assert "Tell time" in response
    
    @pytest.mark.asyncio
    async def test_process_text_command_image_description(self, agent):
        """Test processing an image description request."""
        response = await agent.process_text_command("describe this image")
        
        assert "image" in response.lower()
        assert "web interface" in response.lower()
    
    def test_session_history_management(self, agent):
        """Test session history functionality."""
        # Initially empty
        assert agent.get_session_history() == []
        
        # Add some history
        agent.session_history.append({
            "timestamp": "2024-01-01T00:00:00",
            "type": "user_input",
            "content": "test"
        })
        
        # Check history
        history = agent.get_session_history()
        assert len(history) == 1
        assert history[0]["content"] == "test"
        
        # Clear history
        agent.clear_session_history()
        assert agent.get_session_history() == []