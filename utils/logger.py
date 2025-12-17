# utils/logger.py
"""
Logging system for GST Processing Tool v5.0

This module provides:
1. Logging to a text file (gst_tool.log) - appends all runs
2. Logging to the UI (via signals) - shown in the Log tab
3. Different log levels: INFO, WARNING, ERROR, DEBUG

Usage:
    from utils.logger import get_logger
    
    logger = get_logger()
    logger.info("Processing started")
    logger.warning("File not found")
    logger.error("Processing failed")
"""

import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable

from utils.constants import LOG_FILE_NAME


class GSTLogger:
    """
    Custom logger that writes to both file and UI.
    
    The file logging happens automatically.
    For UI logging, you need to connect a callback function.
    """
    
    _instance = None  # Singleton instance
    
    def __new__(cls):
        """Ensure only one logger instance exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the logger (only once)."""
        if self._initialized:
            return
        
        self._initialized = True
        self._ui_callback: Optional[Callable] = None
        self._setup_file_logger()
    
    def _setup_file_logger(self):
        """Set up the file logger."""
        # Find the logs directory (relative to this file's location)
        # Go up from utils/ to project root, then into logs/
        current_dir = Path(__file__).parent.parent
        log_dir = current_dir / "logs"
        
        # Create logs directory if it doesn't exist
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / LOG_FILE_NAME
        
        # Create logger
        self._logger = logging.getLogger("GST_Tool")
        self._logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        self._logger.handlers = []
        
        # File handler - appends to existing log
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Format: 2025-06-14 10:30:45 | INFO  | Message here
        file_format = logging.Formatter(
            '%(asctime)s | %(levelname)-5s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        
        self._logger.addHandler(file_handler)
        
        # Log session start
        self._logger.info("=" * 60)
        self._logger.info(f"GST Tool Session Started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._logger.info("=" * 60)
    
    def set_ui_callback(self, callback: Callable[[str, str, str], None]):
        """
        Set the callback function for UI logging.
        
        The callback receives: (timestamp, level, message)
        
        Args:
            callback: Function that takes (timestamp, level, message)
        """
        self._ui_callback = callback
    
    def _log(self, level: str, message: str):
        """
        Internal method to log to both file and UI.
        
        Args:
            level: Log level (INFO, WARNING, ERROR, DEBUG)
            message: Log message
        """
        # Get timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Log to file
        if level == "INFO":
            self._logger.info(message)
        elif level == "WARNING":
            self._logger.warning(message)
        elif level == "ERROR":
            self._logger.error(message)
        elif level == "DEBUG":
            self._logger.debug(message)
        
        # Log to UI if callback is set
        if self._ui_callback:
            try:
                self._ui_callback(timestamp, level, message)
            except Exception as e:
                self._logger.error(f"UI logging failed: {e}")
    
    def info(self, message: str):
        """Log an informational message."""
        self._log("INFO", message)
    
    def warning(self, message: str):
        """Log a warning message."""
        self._log("WARNING", message)
    
    def error(self, message: str):
        """Log an error message."""
        self._log("ERROR", message)
    
    def debug(self, message: str):
        """Log a debug message."""
        self._log("DEBUG", message)
    
    def success(self, message: str):
        """Log a success message (logged as INFO with ✓ prefix)."""
        self._log("INFO", f"✓ {message}")
    
    def processing(self, client_name: str):
        """Log that processing has started for a client."""
        self._log("INFO", f"Processing: {client_name}")
    
    def merged(self, client_name: str):
        """Log successful merge."""
        self._log("INFO", f"✓ Merged: {client_name}")
    
    def created(self, client_name: str):
        """Log file creation."""
        self._log("INFO", f"✓ Created GSTR-2B: {client_name}")
    
    def copied(self, client_name: str):
        """Log file copy (no IMS)."""
        self._log("WARNING", f"⚠ Copied without IMS: {client_name}")
    
    def failed(self, client_name: str, reason: str):
        """Log processing failure."""
        self._log("ERROR", f"✗ Failed: {client_name} - {reason}")
    
    def separator(self):
        """Log a separator line."""
        self._log("INFO", "-" * 50)
    
    def session_end(self):
        """Log session end."""
        self._logger.info("=" * 60)
        self._logger.info(f"Session Ended - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._logger.info("=" * 60)
        self._logger.info("")  # Blank line between sessions


# Global logger instance
_logger_instance: Optional[GSTLogger] = None


def setup_logger() -> GSTLogger:
    """
    Set up and return the logger instance.
    
    Call this once at application startup.
    
    Returns:
        GSTLogger instance
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = GSTLogger()
    return _logger_instance


def get_logger() -> GSTLogger:
    """
    Get the logger instance.
    
    If not set up, creates a new instance.
    
    Returns:
        GSTLogger instance
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = setup_logger()
    return _logger_instance
