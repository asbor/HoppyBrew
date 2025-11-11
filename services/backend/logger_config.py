"""
Logger configuration module with proper Singleton pattern.

This module provides a centralized logging configuration for the HoppyBrew application.
Uses a thread-safe Singleton pattern to ensure logger is configured only once.
"""
import logging
import os
import threading
from logging.handlers import RotatingFileHandler
from typing import Optional


class LoggerManager:
    """
    Singleton logger manager that ensures logging is configured only once.
    Thread-safe implementation using double-checked locking pattern.
    """

    _instance: Optional['LoggerManager'] = None
    _lock: threading.Lock = threading.Lock()
    _configured: bool = False

    def __new__(cls):
        """Ensure only one instance of LoggerManager exists."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def configure_logger(self) -> logging.Logger:
        """
        Configure the root logger with console and file handlers.
        This method is called only once, even if invoked multiple times.

        Returns:
            logging.Logger: The configured root logger
        """
        if self._configured:
            return logging.getLogger()

        with self._lock:
            if self._configured:
                return logging.getLogger()

            logger = logging.getLogger()

            # Only configure if not already configured
            if not logger.handlers:
                logger.setLevel(logging.INFO)  # Changed to INFO to reduce noise

                # Log format
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )

                # Console handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.INFO)
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

                # File handler (only if writable)
                try:
                    log_file = os.environ.get("LOG_FILE", "/tmp/hoppybrew.log")
                    file_handler = RotatingFileHandler(
                        log_file, maxBytes=1024 * 1024, backupCount=10
                    )
                    file_handler.setLevel(logging.DEBUG)
                    file_handler.setFormatter(formatter)
                    logger.addHandler(file_handler)
                except (PermissionError, OSError) as e:
                    # If file logging fails, continue with console only
                    logger.warning(f"Could not create file handler: {e}. Using console only.")

            self._configured = True
            return logger

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """
        Get a logger instance, configuring the root logger if needed.

        Args:
            name: Optional name for the logger. If None, returns root logger.

        Returns:
            logging.Logger: A logger instance
        """
        # Ensure logger is configured
        if not self._configured:
            self.configure_logger()

        if name:
            return logging.getLogger(name)
        return logging.getLogger()


# Global instance for convenient access
_manager = LoggerManager()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance. Configures logging on first call.

    Args:
        name: Optional name for the logger. If None, returns root logger.

    Returns:
        logging.Logger: A logger instance
    """
    return _manager.get_logger(name)
