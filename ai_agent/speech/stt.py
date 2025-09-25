"""Speech-to-Text functionality."""

import asyncio
import logging
from typing import Optional
import speech_recognition as sr

from ..core.config import Config


class SpeechToText:
    """Speech-to-Text engine for converting audio to text."""
    
    def __init__(self, config: Config):
        """Initialize the STT engine."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self._initialize_microphone()
    
    def _initialize_microphone(self):
        """Initialize the microphone."""
        try:
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.logger.info("Microphone initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing microphone: {e}")
            self.microphone = None
    
    async def listen_and_transcribe(self) -> Optional[str]:
        """Listen for audio and transcribe to text."""
        if not self.microphone:
            self.logger.error("Microphone not available")
            return None
        
        try:
            # Run speech recognition in a separate thread
            loop = asyncio.get_event_loop()
            audio_data = await loop.run_in_executor(None, self._listen_sync)
            
            if audio_data:
                text = await loop.run_in_executor(None, self._transcribe_sync, audio_data)
                return text
            
        except Exception as e:
            self.logger.error(f"Error in speech recognition: {e}")
        
        return None
    
    def _listen_sync(self) -> Optional[sr.AudioData]:
        """Listen for audio synchronously."""
        try:
            with self.microphone as source:
                self.logger.info("Listening for audio...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=self.config.audio_timeout,
                    phrase_time_limit=self.config.audio_phrase_timeout
                )
                return audio
                
        except sr.WaitTimeoutError:
            self.logger.info("Listening timeout - no speech detected")
            return None
        except Exception as e:
            self.logger.error(f"Error listening for audio: {e}")
            return None
    
    def _transcribe_sync(self, audio_data: sr.AudioData) -> Optional[str]:
        """Transcribe audio to text synchronously."""
        try:
            # Try Google Speech Recognition first
            text = self.recognizer.recognize_google(audio_data)
            self.logger.info(f"Transcribed text: {text}")
            return text
            
        except sr.UnknownValueError:
            self.logger.info("Could not understand audio")
            return None
        except sr.RequestError as e:
            self.logger.error(f"Could not request results from Google Speech Recognition: {e}")
            
            # Fallback to offline recognition if available
            try:
                text = self.recognizer.recognize_sphinx(audio_data)
                self.logger.info(f"Offline transcribed text: {text}")
                return text
            except Exception as offline_e:
                self.logger.error(f"Offline recognition also failed: {offline_e}")
                return None
    
    def get_microphone_names(self) -> list:
        """Get list of available microphones."""
        try:
            return sr.Microphone.list_microphone_names()
        except Exception as e:
            self.logger.error(f"Error getting microphone names: {e}")
            return []