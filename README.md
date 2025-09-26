# AI Agent for Blind Users

A comprehensive AI-powered assistant specifically designed to help blind and visually impaired users interact with technology through voice commands, text-to-speech, image description, and other accessibility features.

## 🌟 Features

### Core Accessibility Features
- **Text-to-Speech (TTS)** - Natural voice responses for all interactions
- **Speech-to-Text (STT)** - Voice command recognition and processing
- **Image Description** - AI-powered analysis and description of images
- **WCAG 2.1 AA Compliant** - Web interface designed for accessibility
- **High Contrast Mode** - Enhanced visual accessibility
- **Adjustable Font Sizes** - Customizable text sizing
- **Keyboard Navigation** - Full keyboard accessibility support

### Interface Options
- **Web Interface** - Accessible browser-based interface
- **Command Line Tool** - Terminal-based interaction
- **Voice Commands** - Hands-free operation
- **RESTful API** - Integration with other applications

### AI Capabilities
- Natural language conversation
- Context-aware responses
- Session history management
- Multi-modal interaction (text, voice, images)

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sv410/ai-agent-for-blind.git
cd ai-agent-for-blind
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install in development mode:
```bash
pip install -e .
```

### Basic Usage

#### Web Interface
Start the web server:
```bash
python -m ai_agent.cli web
# or
ai-agent web
```

Then open your browser to `http://localhost:8000`

#### Command Line Interface
```bash
# Interactive text mode
ai-agent text

# Voice command mode
ai-agent voice

# Analyze an image
ai-agent image path/to/image.jpg

# Show configuration
ai-agent config
```

#### Python API
```python
from ai_agent import AIAgent, Config

# Create agent with default configuration
agent = AIAgent()

# Process text command
response = await agent.process_text_command("What time is it?")
print(response)

# Analyze an image
description = await agent.analyze_image("photo.jpg")
print(description)
```

## ⚙️ Configuration

Configure the agent using environment variables or the `Config` class:

### Environment Variables
```bash
# API Keys (optional, for advanced AI features)
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"

# Speech Settings
export TTS_RATE="180"                    # Words per minute
export AUDIO_TIMEOUT="5"                 # Seconds to wait for audio
export AUDIO_PHRASE_TIMEOUT="1.0"       # Seconds between phrases

# Web Interface
export WEB_HOST="0.0.0.0"               # Host to bind to
export WEB_PORT="8000"                   # Port to bind to
export DEBUG="false"                     # Enable debug mode

# File Paths
export LOG_FILE="ai_agent.log"           # Log file location
export TEMP_DIR="temp"                   # Temporary files directory
```

### Configuration in Code
```python
from ai_agent import Config

config = Config(
    tts_rate=200,
    web_port=9000,
    debug_mode=True
)

agent = AIAgent(config)
```

## 🎯 Accessibility Features

### Web Interface Accessibility
- **Screen Reader Compatible** - Works with NVDA, JAWS, VoiceOver
- **Keyboard Navigation** - Tab-accessible controls
- **ARIA Labels** - Proper semantic markup
- **High Contrast Mode** - Alt+C to toggle
- **Adjustable Font Size** - Alt+Plus/Minus
- **Live Regions** - Screen reader announcements

### Keyboard Shortcuts
- `Alt+1` - Focus text input
- `Alt+2` - Start voice command
- `Alt+3` - Focus image upload
- `Alt+C` - Toggle high contrast
- `Alt+Plus` - Increase font size
- `Alt+Minus` - Decrease font size

### Voice Commands
- "What time is it?" - Get current time
- "Describe this image" - Request image description
- "Help" or "What can you do?" - Get help information
- "Hello" - Start conversation

## 🛠️ Development

### Project Structure
```
ai-agent-for-blind/
├── ai_agent/              # Main package
│   ├── core/             # Core agent logic
│   ├── speech/           # TTS and STT modules
│   ├── vision/           # Image analysis
│   ├── web/              # Web interface
│   └── utils/            # Utility functions
├── tests/                # Test files
├── templates/            # HTML templates
├── static/               # Static web assets
├── requirements.txt      # Dependencies
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

### Running Tests
```bash
pytest tests/
```

### Development Installation
```bash
pip install -e .[dev]
```

### Code Formatting
```bash
black ai_agent/
flake8 ai_agent/
```

## 🔧 Advanced Configuration

### Text-to-Speech Setup
The agent uses `pyttsx3` by default. For better quality:

1. **Windows**: Uses SAPI
2. **macOS**: Uses NSSpeechSynthesizer
3. **Linux**: Install espeak: `sudo apt-get install espeak`

### Speech Recognition Setup
For better accuracy, you may need:

1. **Microphone access** - Grant permissions when prompted
2. **Internet connection** - For Google Speech Recognition
3. **Offline recognition** - Install `pocketsphinx` for offline mode

### Audio Requirements
```bash
# Linux users may need:
sudo apt-get install portaudio19-dev python3-dev
sudo apt-get install espeak espeak-data

# macOS users may need:
brew install portaudio
```

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines
- Follow accessibility best practices
- Maintain WCAG 2.1 AA compliance
- Test with screen readers when possible
- Document accessibility features
- Write tests for new functionality

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with accessibility-first principles
- Designed for the blind and visually impaired community
- Powered by open-source speech and AI technologies

## 📞 Support

- Create an issue for bug reports
- Check the documentation for usage questions
- Join our community discussions

---

**Made with ❤️ for accessibility and independence**