"""
Simple example of using the AI Agent for Blind Users.

This example demonstrates basic usage patterns.
"""

import asyncio
from ai_agent import AIAgent, Config


async def main():
    """Main example function."""
    print("AI Agent for Blind Users - Example")
    print("=" * 40)
    
    # Create configuration
    config = Config.from_env()
    config.debug_mode = True  # Enable debug logging for example
    
    # Create AI agent
    agent = AIAgent(config)
    
    print("Agent initialized successfully!")
    print()
    
    # Example 1: Process text commands
    print("Example 1: Text Commands")
    print("-" * 25)
    
    commands = [
        "Hello",
        "What time is it?",
        "Help",
        "What can you do?"
    ]
    
    for command in commands:
        print(f"User: {command}")
        response = await agent.process_text_command(command)
        print(f"Agent: {response}")
        print()
    
    # Example 2: Session history
    print("Example 2: Session History")
    print("-" * 26)
    
    history = agent.get_session_history()
    print(f"Session has {len(history)} interactions:")
    
    for i, entry in enumerate(history, 1):
        entry_type = "User" if entry["type"] == "user_input" else "Agent"
        timestamp = entry["timestamp"]
        content = entry["content"][:50] + "..." if len(entry["content"]) > 50 else entry["content"]
        print(f"{i}. [{entry_type}] {timestamp}: {content}")
    
    print()
    
    # Example 3: Configuration display
    print("Example 3: Current Configuration")
    print("-" * 34)
    
    print(f"TTS Rate: {config.tts_rate} words/minute")
    print(f"Web Interface: {config.web_host}:{config.web_port}")
    print(f"Debug Mode: {config.debug_mode}")
    print(f"Audio Timeout: {config.audio_timeout} seconds")
    print(f"Log File: {config.log_file}")
    
    print()
    print("Example completed!")
    print("To run the web interface: python -m ai_agent.cli web")
    print("To run voice mode: python -m ai_agent.cli voice")


if __name__ == "__main__":
    asyncio.run(main())