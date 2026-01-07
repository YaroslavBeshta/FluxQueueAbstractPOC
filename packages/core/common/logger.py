"""
Centralized logging configuration for the application.

This module provides a consistent logging setup across all services.
Logging can be configured via environment variables:
- LOG_LEVEL: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)
- LOG_FORMAT: json, text (default: text)
"""
import logging
import os
import sys
from typing import Optional


# Global flag to track if logging has been configured
_logging_configured = False


def setup_logging(
    level: Optional[str] = None,
    format_type: Optional[str] = None,
    service_name: Optional[str] = None
) -> None:
    """
    Configure logging for the application.
    
    This should be called once at application startup.
    Subsequent calls are ignored (idempotent).
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
               If None, reads from LOG_LEVEL env var or defaults to INFO
        format_type: 'json' or 'text' format
                     If None, reads from LOG_FORMAT env var or defaults to 'text'
        service_name: Name of the service (e.g., 'telegram_bot', 'notifications')
                      If None, attempts to infer from environment
    """
    global _logging_configured
    
    if _logging_configured:
        return  # Already configured, don't reconfigure
    
    # Determine log level
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    log_level = getattr(logging, level, logging.INFO)
    
    # Determine format
    if format_type is None:
        format_type = os.getenv("LOG_FORMAT", "text").lower()
    
    # Determine service name
    if service_name is None:
        # Try to infer from environment or use default
        service_name = os.getenv("SERVICE_NAME", "app")
    
    # Choose format
    if format_type == "json":
        # JSON format for structured logging (useful for log aggregation)
        log_format = (
            '{"timestamp": "%(asctime)s", '
            '"level": "%(levelname)s", '
            '"service": "%(name)s", '
            '"message": "%(message)s", '
            '"module": "%(module)s", '
            '"function": "%(funcName)s", '
            '"line": %(lineno)d}'
        )
    else:
        # Human-readable text format
        log_format = (
            f'%(asctime)s | %(levelname)-8s | {service_name} | '
            '%(name)s:%(funcName)s:%(lineno)d | %(message)s'
        )
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True  # Override any existing configuration
    )
    
    # Set levels for noisy third-party libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("telebot").setLevel(logging.INFO)
    logging.getLogger("schedule").setLevel(logging.WARNING)
    
    _logging_configured = True
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured: level={level}, format={format_type}, service={service_name}")


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    This is a convenience function that ensures logging is configured
    before returning a logger. Use this instead of logging.getLogger()
    directly.
    
    Args:
        name: Logger name (usually __name__ of the calling module)
              If None, uses 'root'
    
    Returns:
        Logger instance
    """
    if not _logging_configured:
        # Auto-configure if not already done
        setup_logging()
    
    if name is None:
        name = 'root'
    
    return logging.getLogger(name)

