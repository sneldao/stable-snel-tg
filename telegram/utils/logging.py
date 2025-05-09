import logging
import os
import sys
from datetime import datetime
from typing import Optional, List, Dict, Any, Union

# Default log format includes timestamp, level, and message
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Map string log levels to actual logging levels
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def setup_logging(
    level: str = "INFO",
    format_str: Optional[str] = None,
    log_to_file: bool = False,
    log_file: Optional[str] = None,
    module_levels: Optional[Dict[str, str]] = None
) -> None:
    """
    Configure logging for the SNEL Telegram Bot.
    
    Args:
        level: General logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_str: Custom log format string
        log_to_file: Whether to log to a file
        log_file: Path to log file (default: logs/snel_bot_YYYY-MM-DD.log)
        module_levels: Dict of module names to specific log levels
    """
    # Get root logger
    root_logger = logging.getLogger()
    
    # Clear existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Set root logger level
    root_level = LOG_LEVELS.get(level.upper(), logging.INFO)
    root_logger.setLevel(root_level)
    
    # Create formatter
    log_format = format_str or DEFAULT_FORMAT
    formatter = logging.Formatter(log_format)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_to_file:
        if not log_file:
            # Create logs directory if it doesn't exist
            os.makedirs("logs", exist_ok=True)
            # Default log file includes date
            today = datetime.now().strftime("%Y-%m-%d")
            log_file = f"logs/snel_bot_{today}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific levels for modules if provided
    if module_levels:
        for module, module_level in module_levels.items():
            level_value = LOG_LEVELS.get(module_level.upper(), logging.INFO)
            logging.getLogger(module).setLevel(level_value)
    
    # Log configuration details
    logging.info(f"Logging initialized: level={level}, log_file={'Yes' if log_to_file else 'No'}")
    if module_levels:
        for module, module_level in module_levels.items():
            logging.info(f"Module level set: {module}={module_level}")

def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get a logger with the specified name and optional level.
    
    Args:
        name: Logger name (typically the module name)
        level: Optional level to set for this logger
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if level:
        level_value = LOG_LEVELS.get(level.upper(), logging.INFO)
        logger.setLevel(level_value)
    
    return logger

def log_exception(
    logger: logging.Logger, 
    exception: Exception, 
    context: Optional[Dict[str, Any]] = None,
    level: str = "ERROR"
) -> None:
    """
    Log an exception with optional context information.
    
    Args:
        logger: Logger to use
        exception: The exception to log
        context: Optional dict with context information
        level: Log level to use
    """
    level_value = LOG_LEVELS.get(level.upper(), logging.ERROR)
    
    # Create message with error details
    message = f"Exception {type(exception).__name__}: {str(exception)}"
    
    # Add context if provided
    if context:
        context_str = ", ".join(f"{k}={v}" for k, v in context.items())
        message += f" [Context: {context_str}]"
    
    # Log with traceback
    logger.log(level_value, message, exc_info=True)

def log_api_call(
    logger: logging.Logger,
    service: str,
    method: str,
    params: Optional[Dict[str, Any]] = None,
    success: bool = True,
    error: Optional[str] = None,
    response_time: Optional[float] = None
) -> None:
    """
    Log API call details for monitoring and debugging.
    
    Args:
        logger: Logger to use
        service: Service name (e.g., 'coingecko', 'venice')
        method: Method name
        params: Optional parameters used
        success: Whether the call succeeded
        error: Error message if failed
        response_time: Response time in seconds if available
    """
    # Format parameters for logging, omitting sensitive data
    params_str = ""
    if params:
        # Filter out any sensitive data before logging
        filtered_params = {}
        for key, value in params.items():
            if any(sensitive in key.lower() for sensitive in ["api_key", "token", "secret", "password"]):
                filtered_params[key] = "********"
            else:
                filtered_params[key] = value
        params_str = str(filtered_params)
    
    # Create detailed log message
    message_parts = [f"API Call: {service}.{method}"]
    
    if params_str:
        message_parts.append(f"Params: {params_str}")
    
    if response_time is not None:
        message_parts.append(f"Time: {response_time:.3f}s")
    
    message_parts.append(f"Status: {'SUCCESS' if success else 'FAILED'}")
    
    if error:
        message_parts.append(f"Error: {error}")
    
    # Join message parts
    message = " | ".join(message_parts)
    
    # Log at appropriate level
    if success:
        logger.debug(message)
    else:
        logger.error(message)

def enable_debug_mode() -> None:
    """Enable debug logging for all SNEL modules."""
    modules = [
        "snel",
        "snel.crypto",
        "snel.enhanced_crypto",
        "snel.news",
        "snel.info",
        "snel.ai",
        "snel.cache",
        "snel.retries"
    ]
    
    for module in modules:
        logging.getLogger(module).setLevel(logging.DEBUG)
    
    logging.info("Debug mode enabled for all SNEL modules")

def disable_debug_mode() -> None:
    """Disable debug logging for all SNEL modules."""
    modules = [
        "snel",
        "snel.crypto",
        "snel.enhanced_crypto",
        "snel.news",
        "snel.info",
        "snel.ai",
        "snel.cache",
        "snel.retries"
    ]
    
    for module in modules:
        logging.getLogger(module).setLevel(logging.INFO)
    
    logging.info("Debug mode disabled for all SNEL modules")