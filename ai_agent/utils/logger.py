"""Logging utilities."""

import logging
import sys
from typing import Optional


def setup_logger(log_file: Optional[str] = None, log_level: int = logging.INFO) -> logging.Logger:
    """Set up logging configuration."""
    
    # Create logger
    logger = logging.getLogger("ai_agent")
    logger.setLevel(log_level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if log file is specified
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Could not create file handler: {e}")
    
    return logger