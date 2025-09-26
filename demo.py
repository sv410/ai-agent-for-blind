"""
Demo mode for the AI Agent - works without external dependencies.

This provides a demonstration of the core functionality without requiring
speech recognition, TTS, or AI model dependencies.
"""

import asyncio
from datetime import datetime
from typing import Optional


class DemoAgent:
    """Demo version of the AI Agent with minimal dependencies."""
    
    def __init__(self):
        """Initialize the demo agent."""
        self.session_history = []
        print("🤖 AI Agent for Blind Users - Demo Mode")
        print("=" * 45)
        print("This demo shows the core functionality without requiring")
        print("speech recognition or text-to-speech dependencies.")
        print()
    
    async def process_text_command(self, text: str) -> str:
        """Process a text command and return a response."""
        command = text.lower().strip()
        
        # Add to session history
        self.session_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "user_input",
            "content": text
        })
        
        # Handle specific commands
        if any(word in command for word in ["hello", "hi", "hey"]):
            response = ("Hello! I'm your AI assistant. I can help you with "
                       "image descriptions, telling time, reading text, and many "
                       "other tasks. Just ask me what you need!")
        
        elif any(word in command for word in ["time", "clock"]):
            now = datetime.now()
            time_str = now.strftime("%I:%M %p")
            date_str = now.strftime("%A, %B %d, %Y")
            response = f"The current time is {time_str} on {date_str}."
        
        elif any(word in command for word in ["help", "commands", "what can you do"]):
            response = """I can help you with several tasks:
            
- Describe images: Say 'describe this image' or 'what's in this picture'
- Tell time: Ask 'what time is it?' 
- General conversation: Just talk to me naturally
- Web interface: Use the web interface for file uploads and more features

I'm designed to be accessible for blind and visually impaired users. 
All responses are provided through text-to-speech in the full version."""
        
        elif any(word in command for word in ["describe", "image", "picture", "photo"]):
            response = ("To describe an image, please use the web interface to "
                       "upload a photo, or specify the path to an image file "
                       "when using the command line interface. In this demo mode, "
                       "image analysis is not available, but the full version "
                       "includes AI-powered image description.")
        
        elif any(word in command for word in ["quit", "exit", "bye", "goodbye"]):
            response = ("Goodbye! Thank you for trying the AI Agent for Blind Users. "
                       "To use the full version with voice commands and TTS, "
                       "install the dependencies: pip install -r requirements.txt")
        
        else:
            response = (f"I heard you say: '{text}'. This is the demo version "
                       f"showing basic text processing. In the full implementation, "
                       f"this would be processed by AI models to provide intelligent, "
                       f"context-aware responses with speech synthesis.")
        
        # Add response to history
        self.session_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": "agent_response", 
            "content": response
        })
        
        return response
    
    def get_session_history(self):
        """Get the session history."""
        return self.session_history.copy()
    
    def display_features(self):
        """Display the main features of the full version."""
        print("🎯 Full Version Features:")
        print("-" * 25)
        features = [
            "🗣️  Text-to-Speech (TTS) - Natural voice responses",
            "🎤 Speech-to-Text (STT) - Voice command recognition", 
            "📷 Image Analysis - AI-powered image description",
            "🌐 Web Interface - Accessible browser interface",
            "⌨️  CLI Tool - Command-line interaction",
            "🎨 High Contrast Mode - Enhanced visual accessibility",
            "📝 Session History - Conversation tracking",
            "🔊 Voice Commands - Hands-free operation",
            "♿ WCAG 2.1 AA Compliant - Full accessibility support",
            "🔧 Configurable - Customizable settings"
        ]
        
        for feature in features:
            print(f"  {feature}")
        print()


async def demo_interactive_mode():
    """Run an interactive demo."""
    agent = DemoAgent()
    agent.display_features()
    
    print("💬 Interactive Demo Mode")
    print("-" * 22)
    print("Type your messages below. Type 'quit' to exit.")
    print("Try: 'hello', 'what time is it?', 'help', 'describe image'")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            response = await agent.process_text_command(user_input)
            print(f"Agent: {response}")
            print()
            
            if any(word in user_input.lower() for word in ["quit", "exit", "bye"]):
                break
                
        except KeyboardInterrupt:
            print("\n\nDemo ended. Thanks for trying the AI Agent!")
            break
        except EOFError:
            print("\n\nDemo ended. Thanks for trying the AI Agent!")
            break
    
    # Show session summary
    history = agent.get_session_history()
    print(f"\n📊 Session Summary: {len(history)} total interactions")
    user_messages = len([h for h in history if h["type"] == "user_input"])
    agent_responses = len([h for h in history if h["type"] == "agent_response"])
    print(f"   👤 User messages: {user_messages}")
    print(f"   🤖 Agent responses: {agent_responses}")


def main():
    """Main demo function."""
    print("Starting AI Agent Demo...")
    print()
    asyncio.run(demo_interactive_mode())


if __name__ == "__main__":
    main()