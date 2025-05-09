import asyncio
import logging
from typing import Optional, Dict, Any
import os
from pathlib import Path

# Configure logger
logger = logging.getLogger("snel.startup")

# Global task reference
_cleanup_task = None
_metrics_task = None
_background_tasks = []

async def start_cache_cleanup(interval_seconds: int = 300):
    """Start the cache cleanup background task."""
    from .cache import cleanup_expired_cache
    
    logger.info(f"Starting cache cleanup task (runs every {interval_seconds}s)")
    
    while True:
        try:
            # Wait first to prevent immediate cleanup on startup
            await asyncio.sleep(interval_seconds)
            
            # Perform cleanup
            removed_count = cleanup_expired_cache()
            if removed_count > 0:
                logger.info(f"Cleaned up {removed_count} expired cache entries")
        except asyncio.CancelledError:
            logger.info("Cache cleanup task cancelled")
            break
        except Exception as e:
            logger.error(f"Error in cache cleanup: {e}")
            # Continue running despite errors
            await asyncio.sleep(10)

def initialize_background_tasks():
    """Initialize all background tasks for the application."""
    global _cleanup_task, _metrics_task, _background_tasks
    
    # Cancel any existing tasks
    if _cleanup_task and not _cleanup_task.done():
        _cleanup_task.cancel()
        
    if _metrics_task and not _metrics_task.done():
        _metrics_task.cancel()
    
    for task in _background_tasks:
        if not task.done():
            task.cancel()
    
    _background_tasks = []
    
    try:
        # Get the current event loop
        loop = asyncio.get_event_loop()
        
        # Start cache cleanup task
        _cleanup_task = loop.create_task(start_cache_cleanup())
        _background_tasks.append(_cleanup_task)
        
        # Start metrics collection task (hourly)
        try:
            from .metrics import start_metrics_collection_task
            _metrics_task = loop.create_task(start_metrics_collection_task(3600))
            _background_tasks.append(_metrics_task)
        except ImportError:
            logger.info("Metrics module not available, skipping metrics task")
        
        # Initialize rate limiters
        initialize_rate_limiters()
        
        logger.info(f"Initialized {len(_background_tasks)} background tasks")
    except Exception as e:
        logger.error(f"Failed to initialize background tasks: {e}")

def load_environment(env_file: Optional[str] = None):
    """Load environment variables from .env file."""
    from dotenv import load_dotenv
    
    # Default to .env if not specified
    if not env_file:
        env_file = ".env"
    
    # Check if the file exists
    env_path = Path(env_file)
    if env_path.exists():
        load_dotenv(env_file)
        logger.info(f"Loaded environment from {env_file}")
    else:
        logger.warning(f"Environment file {env_file} not found")
    
    # Log important environment variables (without values)
    env_vars = [
        "TELEGRAM_BOT_TOKEN",
        "GEMINI_API_KEY",
        "COINGECKO_API_KEY",
        "CRYPTOPANIC_API_KEY",
        "VENICE_API_KEY",
        "LOG_LEVEL"
    ]
    
    present_vars = [var for var in env_vars if os.getenv(var)]
    missing_vars = [var for var in env_vars if not os.getenv(var)]
    
    if present_vars:
        logger.info(f"Environment variables found: {', '.join(present_vars)}")
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")

def check_api_keys():
    """Check that required API keys are available."""
    required_keys = {
        "TELEGRAM_BOT_TOKEN": "Bot will not function without Telegram token",
    }
    
    recommended_keys = {
        "GEMINI_API_KEY": "AI features will be limited",
        "COINGECKO_API_KEY": "May experience rate limits with free tier",
        "CRYPTOPANIC_API_KEY": "News functionality will use fallbacks",
        "VENICE_API_KEY": "Stablecoin-specific data will be limited"
    }
    
    missing_required = []
    missing_recommended = []
    
    # Check required keys
    for key, message in required_keys.items():
        if not os.getenv(key):
            missing_required.append(f"{key}: {message}")
    
    # Check recommended keys
    for key, message in recommended_keys.items():
        if not os.getenv(key):
            missing_recommended.append(f"{key}: {message}")
    
    # Log results
    if not missing_required:
        logger.info("All required API keys are present")
    else:
        logger.error(f"Missing required API keys: {', '.join(missing_required)}")
    
    if missing_recommended:
        logger.warning(f"Missing recommended API keys: {', '.join(missing_recommended)}")
    
    return len(missing_required) == 0

def initialize_rate_limiters():
    """Initialize rate limiters for external APIs."""
    try:
        from .limits.token_bucket import register_limiter
        
        # Default rate limits for external APIs
        rate_limits = {
            # CoinGecko free tier: 10-30 calls/minute
            "coingecko": {
                "tokens_per_second": 0.5,  # 30 per minute
                "max_tokens": 30,          # Burst capacity
            },
            # CryptoPanic free tier: 30 calls/hour
            "cryptopanic": {
                "tokens_per_second": 0.01,  # 36 per hour
                "max_tokens": 10,           # Burst capacity
            },
            # Venice API: 1000 calls/day
            "venice": {
                "tokens_per_second": 0.012,  # 1000 per day
                "max_tokens": 50,            # Burst capacity
            },
            # AI API (Gemini): 60 calls/minute
            "gemini": {
                "tokens_per_second": 1.0,    # 60 per minute
                "max_tokens": 10,            # Burst capacity
            }
        }
        
        # Register all rate limiters
        for name, config in rate_limits.items():
            register_limiter(
                name,
                tokens_per_second=config["tokens_per_second"],
                max_tokens=config["max_tokens"]
            )
            logger.info(
                f"Registered rate limiter for {name}: "
                f"{config['tokens_per_second']}/s, max {config['max_tokens']}"
            )
    except ImportError:
        logger.info("Rate limiting module not available, skipping rate limiter initialization")

def shutdown_background_tasks():
    """Cancel all background tasks."""
    global _background_tasks
    
    for task in _background_tasks:
        if not task.done():
            task.cancel()
    
    _background_tasks = []
    logger.info("All background tasks have been cancelled")