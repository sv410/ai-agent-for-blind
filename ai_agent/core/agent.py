"""Core AI Agent implementation."""

import logging
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime

from .config import Config
from ..speech.tts import TextToSpeech
from ..speech.stt import SpeechToText
from ..vision.image_analyzer import ImageAnalyzer
from ..utils.logger import setup_logger


class AIAgent:
    """Main AI Agent class that coordinates all functionality."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the AI Agent with configuration."""
        self.config = config or Config.from_env()
        self.logger = setup_logger(self.config.log_file)
        
        # Initialize components
        self.tts = TextToSpeech(self.config)
        self.stt = SpeechToText(self.config)
        self.image_analyzer = ImageAnalyzer(self.config)
        
        # Session state
        self.session_history: List[Dict[str, Any]] = []
        self.is_listening = False
        
        self.logger.info("AI Agent initialized successfully")
    
    async def process_voice_command(self) -> Optional[str]:
        """Listen for and process a voice command."""
        try:
            self.logger.info("Starting voice command processing")
            self.is_listening = True
            
            # Listen for audio input
            audio_text = await self.stt.listen_and_transcribe()
            
            if audio_text:
                self.logger.info(f"Received voice command: {audio_text}")
                response = await self.process_text_command(audio_text)
                
                # Speak the response
                if response:
                    await self.speak(response)
                
                return response
            
        except Exception as e:
            self.logger.error(f"Error processing voice command: {e}")
            error_msg = "Sorry, I had trouble understanding your command. Please try again."
            await self.speak(error_msg)
            return error_msg
        
        finally:
            self.is_listening = False
    
    async def process_text_command(self, text: str) -> str:
        """Process a text command and return a response."""
        try:
            command = text.lower().strip()
            
            # Add to session history
            self.session_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "user_input",
                "content": text
            })
            
            # Handle specific commands
            if any(word in command for word in ["describe", "image", "picture", "photo"]):
                return await self._handle_image_description_request()
            
            elif any(word in command for word in ["time", "clock"]):
                return self._handle_time_request()
            
            elif any(word in command for word in ["help", "commands", "what can you do"]):
                return self._handle_help_request()
            
            elif any(word in command for word in ["hello", "hi", "hey"]):
                return "Hello! I'm your AI assistant. I can help you with image descriptions, telling time, reading text, and many other tasks. Just ask me what you need!"
            
            else:
                # General AI response (placeholder for now)
                return f"I heard you say: '{text}'. This is a general response. In a full implementation, this would be processed by an AI model to provide intelligent responses."
        
        except Exception as e:
            self.logger.error(f"Error processing text command: {e}")
            return "I'm sorry, I encountered an error while processing your request."
    
    async def _handle_image_description_request(self) -> str:
        """Handle requests to describe images."""
        return "To describe an image, please use the web interface to upload a photo, or specify the path to an image file if using the command line interface."
    
    def _handle_time_request(self) -> str:
        """Handle requests for current time."""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%A, %B %d, %Y")
        return f"The current time is {time_str} on {date_str}."
    
    def _handle_help_request(self) -> str:
        """Handle help requests."""
        return """I can help you with several tasks:
        
        - Describe images: Say 'describe this image' or 'what's in this picture'
        - Tell time: Ask 'what time is it?' 
        - General conversation: Just talk to me naturally
        - Web interface: Use the web interface for file uploads and more features
        
        I'm designed to be accessible for blind and visually impaired users. All responses are provided through text-to-speech."""
    
    async def speak(self, text: str) -> None:
        """Convert text to speech and play it."""
        try:
            await self.tts.speak(text)
            
            # Add to session history
            self.session_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "agent_response",
                "content": text
            })
            
        except Exception as e:
            self.logger.error(f"Error in text-to-speech: {e}")
    
    async def analyze_image(self, image_path: str) -> str:
        """Analyze an image and return a description."""
        try:
            description = await self.image_analyzer.describe_image(image_path)
            return description
        except Exception as e:
            self.logger.error(f"Error analyzing image: {e}")
            return "I'm sorry, I couldn't analyze the image. Please make sure the file is a valid image format."
    
    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get the current session history."""
        return self.session_history.copy()
    
    def clear_session_history(self) -> None:
        """Clear the session history."""
        self.session_history.clear()
        self.logger.info("Session history cleared")