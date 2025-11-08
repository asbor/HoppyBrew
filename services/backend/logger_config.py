import logging
import os
from logging.handlers import RotatingFileHandler

# Singleton logger instance

logger = None


def get_logger(name=None):
    global logger
    if logger is None:
        logger = configure_logger()
    if name:
        return logging.getLogger(name)
    return logger


def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Log format

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler (always works)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
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

    return logger
