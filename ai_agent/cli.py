"""Command-line interface for the AI Agent."""

import asyncio
import click
import logging

from ai_agent import AIAgent, Config


@click.group()
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.pass_context
def cli(ctx, debug):
    """AI Agent for Blind Users - Command Line Interface"""
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    
    # Setup logging
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level)


@cli.command()
@click.option('--text', '-t', help='Text to process')
@click.pass_context
def text(ctx, text):
    """Process text input."""
    async def process_text():
        config = Config.from_env()
        if ctx.obj['debug']:
            config.debug_mode = True
        
        agent = AIAgent(config)
        
        if text:
            response = await agent.process_text_command(text)
            print(f"Response: {response}")
        else:
            print("Interactive text mode. Type 'quit' to exit.")
            while True:
                user_input = input("You: ")
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    break
                
                response = await agent.process_text_command(user_input)
                print(f"Agent: {response}")
    
    asyncio.run(process_text())


@cli.command()
@click.pass_context  
def voice(ctx):
    """Start voice interaction mode."""
    async def voice_mode():
        config = Config.from_env()
        if ctx.obj['debug']:
            config.debug_mode = True
        
        agent = AIAgent(config)
        
        print("Voice mode started. Press Ctrl+C to exit.")
        print("The agent will listen for voice commands and respond with speech.")
        
        try:
            while True:
                print("\nListening... (speak now)")
                response = await agent.process_voice_command()
                if response:
                    print(f"Agent response: {response}")
                else:
                    print("No command detected.")
                
                # Small delay between commands
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\nVoice mode ended.")
    
    asyncio.run(voice_mode())


@cli.command()
@click.argument('image_path')
@click.pass_context
def image(ctx, image_path):
    """Analyze an image file."""
    async def analyze_image():
        config = Config.from_env()
        if ctx.obj['debug']:
            config.debug_mode = True
        
        agent = AIAgent(config)
        
        print(f"Analyzing image: {image_path}")
        description = await agent.analyze_image(image_path)
        print(f"Description: {description}")
        
        # Also speak the description
        await agent.speak(description)
    
    asyncio.run(analyze_image())


@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=8000, help='Port to bind to')
@click.pass_context
def web(ctx, host, port):
    """Start the web interface."""
    config = Config.from_env()
    config.web_host = host
    config.web_port = port
    
    if ctx.obj['debug']:
        config.debug_mode = True
    
    agent = AIAgent(config)
    
    # Import here to avoid dependency issues
    from ai_agent.web.interface import WebInterface
    
    web_interface = WebInterface(agent, config)
    web_interface.run()


@cli.command()
def config():
    """Show current configuration."""
    config = Config.from_env()
    
    print("Current Configuration:")
    print(f"  TTS Rate: {config.tts_rate}")
    print(f"  Web Host: {config.web_host}")
    print(f"  Web Port: {config.web_port}")
    print(f"  Debug Mode: {config.debug_mode}")
    print(f"  Audio Timeout: {config.audio_timeout}")
    print(f"  Log File: {config.log_file}")
    print(f"  Temp Directory: {config.temp_dir}")
    
    if config.openai_api_key:
        print("  OpenAI API Key: Set")
    else:
        print("  OpenAI API Key: Not set")


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()