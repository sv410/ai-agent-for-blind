"""
AI Agent for Blind Users

A comprehensive AI-powered assistant designed to help blind and visually 
impaired users interact with technology through voice commands, text-to-speech,
image description, and other accessibility features.
"""

__version__ = "1.0.0"
__author__ = "AI Agent Development Team"
__email__ = "support@ai-agent-blind.com"

from .core.agent import AIAgent
from .core.config import Config

__all__ = ["AIAgent", "Config"]