"""Simplified AI Agent for deployment without speech dependencies."""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import json


class Config:
    """Configuration for the AI Agent."""
    
    def __init__(self):
        self.tts_rate = 180
        self.web_host = "0.0.0.0"
        self.web_port = 8000
        self.debug_mode = False
        self.audio_timeout = 5
        self.log_file = "ai_agent.log"
        self.temp_dir = "temp"
        self.openai_api_key = None
        
    @classmethod
    def from_env(cls):
        """Create configuration from environment variables."""
        import os
        
        config = cls()
        config.tts_rate = int(os.environ.get("TTS_RATE", "180"))
        config.web_host = os.environ.get("WEB_HOST", "0.0.0.0")
        config.web_port = int(os.environ.get("WEB_PORT", "8000"))
        config.debug_mode = os.environ.get("DEBUG", "false").lower() == "true"
        config.audio_timeout = int(os.environ.get("AUDIO_TIMEOUT", "5"))
        config.log_file = os.environ.get("LOG_FILE", "ai_agent.log")
        config.temp_dir = os.environ.get("TEMP_DIR", "temp")
        config.openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        return config


class AIAgent:
    """Simplified AI Agent for deployment."""
    
    def __init__(self, config: Config = None):
        """Initialize the AI agent."""
        self.config = config or Config.from_env()
        self.logger = logging.getLogger(__name__)
        self.session_history: List[Dict[str, Any]] = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.DEBUG if self.config.debug_mode else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        self.logger.info("AI Agent initialized successfully (deployment mode)")
    
    async def process_text_command(self, text: str) -> str:
        """Process a text command and return a response."""
        self.logger.info(f"Processing text command: {text}")
        
        # Add to session history
        self.session_history.append({
            "type": "user_input",
            "content": text,
            "timestamp": datetime.now().isoformat()
        })
        
        # Simple response logic
        text_lower = text.lower().strip()
        
        if any(greeting in text_lower for greeting in ["hello", "hi", "hey"]):
            response = "Hello! I'm your AI assistant. I can help you with image descriptions, telling time, reading text, and many other tasks. Just ask me what you need!"
        
        elif "time" in text_lower:
            current_time = datetime.now()
            response = f"The current time is {current_time.strftime('%I:%M %p')} on {current_time.strftime('%A, %B %d, %Y')}."
        
        elif any(help_word in text_lower for help_word in ["help", "what can you do", "commands"]):
            response = """I can help you with several tasks:

        - Describe images: Say 'describe this image' or 'what's in this picture'
        - Tell time: Ask 'what time is it?'
        - General conversation: Just talk to me naturally
        - Web interface: Use the web interface for file uploads and more features

        I'm designed to be accessible for blind and visually impaired users. All responses are provided through text-to-speech."""
        
        elif "image" in text_lower or "picture" in text_lower:
            response = "To analyze an image, please upload it using the web interface. I can describe what I see in the image to help you understand its contents."
        
        elif any(bye in text_lower for bye in ["bye", "goodbye", "exit", "quit"]):
            response = "Goodbye! Feel free to come back anytime you need assistance."
        
        else:
            response = f"I understand you said: '{text}'. I'm a simple AI assistant in deployment mode. I can tell time, provide help information, and assist with basic tasks. How can I help you today?"
        
        # Add response to session history
        self.session_history.append({
            "type": "agent_response",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    async def process_voice_command(self) -> Optional[str]:
        """Process voice command (disabled in deployment mode)."""
        return "Voice commands are not available in deployment mode. Please use text input instead."
    
    async def analyze_image(self, image_path: str) -> str:
        """Analyze an image (simplified for deployment)."""
        self.logger.info(f"Image analysis requested for: {image_path}")
        return "Image analysis is temporarily unavailable in deployment mode. This feature requires additional AI services to be configured."
    
    async def speak(self, text: str) -> None:
        """Speak text (disabled in deployment mode)."""
        self.logger.info(f"TTS requested: {text[:50]}...")
        # In deployment mode, this would return the text for client-side TTS
        pass
    
    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get the session history."""
        return self.session_history.copy()
    
    def clear_session_history(self) -> None:
        """Clear the session history."""
        self.session_history.clear()
        self.logger.info("Session history cleared")