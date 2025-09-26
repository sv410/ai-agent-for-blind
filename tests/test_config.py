"""Test the configuration management."""

import os
import pytest
from ai_agent.core.config import Config


class TestConfig:
    """Test cases for the Config class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        
        assert config.tts_engine == "pyttsx3"
        assert config.tts_rate == 180
        assert config.web_host == "0.0.0.0"
        assert config.web_port == 8000
        assert config.debug_mode is False
        assert config.audio_timeout == 5
        assert config.audio_phrase_timeout == 1.0
        assert config.log_file == "ai_agent.log"
        assert config.temp_dir == "temp"
    
    def test_from_env_with_defaults(self):
        """Test loading configuration from environment with defaults."""
        # Clear any existing env vars
        env_vars = [
            "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "TTS_RATE", 
            "WEB_HOST", "WEB_PORT", "DEBUG", "AUDIO_TIMEOUT",
            "AUDIO_PHRASE_TIMEOUT", "LOG_FILE", "TEMP_DIR"
        ]
        
        for var in env_vars:
            if var in os.environ:
                del os.environ[var]
        
        config = Config.from_env()
        
        # Should use defaults
        assert config.tts_rate == 180
        assert config.web_host == "0.0.0.0"
        assert config.web_port == 8000
        assert config.debug_mode is False
    
    def test_from_env_with_custom_values(self):
        """Test loading configuration from environment with custom values."""
        # Set custom environment variables
        os.environ.update({
            "TTS_RATE": "200",
            "WEB_HOST": "127.0.0.1",
            "WEB_PORT": "9000",
            "DEBUG": "true",
            "AUDIO_TIMEOUT": "10",
            "LOG_FILE": "custom.log"
        })
        
        try:
            config = Config.from_env()
            
            assert config.tts_rate == 200
            assert config.web_host == "127.0.0.1"
            assert config.web_port == 9000
            assert config.debug_mode is True
            assert config.audio_timeout == 10
            assert config.log_file == "custom.log"
        
        finally:
            # Clean up environment variables
            for var in ["TTS_RATE", "WEB_HOST", "WEB_PORT", "DEBUG", "AUDIO_TIMEOUT", "LOG_FILE"]:
                if var in os.environ:
                    del os.environ[var]