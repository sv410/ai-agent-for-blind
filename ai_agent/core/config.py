"""Configuration management for the AI Agent."""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration settings for the AI Agent."""
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Speech settings
    tts_engine: str = "pyttsx3"
    tts_rate: int = 180
    tts_voice_id: Optional[str] = None
    
    # Web interface
    web_host: str = "0.0.0.0"
    web_port: int = 8000
    debug_mode: bool = False
    
    # Audio settings
    audio_timeout: int = 5
    audio_phrase_timeout: float = 1.0
    
    # File paths
    log_file: str = "ai_agent.log"
    temp_dir: str = "temp"
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            tts_rate=int(os.getenv("TTS_RATE", "180")),
            web_host=os.getenv("WEB_HOST", "0.0.0.0"),
            web_port=int(os.getenv("WEB_PORT", "8000")),
            debug_mode=os.getenv("DEBUG", "false").lower() == "true",
            audio_timeout=int(os.getenv("AUDIO_TIMEOUT", "5")),
            audio_phrase_timeout=float(os.getenv("AUDIO_PHRASE_TIMEOUT", "1.0")),
            log_file=os.getenv("LOG_FILE", "ai_agent.log"),
            temp_dir=os.getenv("TEMP_DIR", "temp"),
        )