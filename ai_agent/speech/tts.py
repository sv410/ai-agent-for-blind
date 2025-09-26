"""Text-to-Speech functionality."""

import asyncio
import logging
from typing import Optional
import pyttsx3

from ..core.config import Config


class TextToSpeech:
    """Text-to-Speech engine for converting text to audio."""
    
    def __init__(self, config: Config):
        """Initialize the TTS engine."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.engine = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the pyttsx3 engine."""
        try:
            self.engine = pyttsx3.init()
            
            # Configure voice settings
            self.engine.setProperty('rate', self.config.tts_rate)
            
            # Set voice if specified
            if self.config.tts_voice_id:
                voices = self.engine.getProperty('voices')
                for voice in voices:
                    if self.config.tts_voice_id in voice.id:
                        self.engine.setProperty('voice', voice.id)
                        break
            
            self.logger.info("TTS engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing TTS engine: {e}")
            self.engine = None
    
    async def speak(self, text: str) -> None:
        """Convert text to speech asynchronously."""
        if not self.engine:
            self.logger.error("TTS engine not available")
            return
        
        try:
            # Run TTS in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._speak_sync, text)
            
        except Exception as e:
            self.logger.error(f"Error in text-to-speech: {e}")
    
    def _speak_sync(self, text: str) -> None:
        """Synchronous speech method."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            self.logger.error(f"Error in synchronous speech: {e}")
    
    def get_available_voices(self) -> list:
        """Get list of available voices."""
        if not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [{"id": voice.id, "name": voice.name} for voice in voices]
        except Exception as e:
            self.logger.error(f"Error getting voices: {e}")
            return []
    
    def set_voice(self, voice_id: str) -> bool:
        """Set the voice for TTS."""
        if not self.engine:
            return False
        
        try:
            self.engine.setProperty('voice', voice_id)
            return True
        except Exception as e:
            self.logger.error(f"Error setting voice: {e}")
            return False
    
    def set_rate(self, rate: int) -> bool:
        """Set the speech rate."""
        if not self.engine:
            return False
        
        try:
            self.engine.setProperty('rate', rate)
            self.config.tts_rate = rate
            return True
        except Exception as e:
            self.logger.error(f"Error setting rate: {e}")
            return False