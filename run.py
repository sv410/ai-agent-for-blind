#!/usr/bin/env python3
"""
Quick start script for the AI Agent for Blind Users.

This script helps users get started quickly with the agent.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import pyttsx3
        import speech_recognition
        import fastapi
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def main():
    """Main function."""
    print("AI Agent for Blind Users - Quick Start")
    print("=" * 40)
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("\nWould you like to install the required dependencies? (y/n)")
        response = input().lower()
        
        if response == 'y':
            if not install_dependencies():
                print("Please install dependencies manually: pip install -r requirements.txt")
                sys.exit(1)
        else:
            print("Please install dependencies manually: pip install -r requirements.txt")
            sys.exit(1)
    
    print("\nAvailable commands:")
    print("1. Start web interface: python -m ai_agent.cli web")
    print("2. Voice interaction: python -m ai_agent.cli voice")
    print("3. Text interaction: python -m ai_agent.cli text")
    print("4. Analyze image: python -m ai_agent.cli image <path>")
    print("5. Show config: python -m ai_agent.cli config")
    print("6. Run example: python example.py")
    
    print("\nFor full documentation, see: README.md")
    
    print("\nWhat would you like to do?")
    print("1. Start web interface")
    print("2. Run example")
    print("3. Exit")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        print("Starting web interface...")
        os.system(f"{sys.executable} -m ai_agent.cli web")
    elif choice == "2":
        print("Running example...")
        os.system(f"{sys.executable} example.py")
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()