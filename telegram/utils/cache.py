from functools import wraps
from datetime import datetime, timedelta
import asyncio
import json
import logging
import os
import pickle
from typing import Dict, Any, Callable, Optional, TypeVar, Awaitable, Union, List

# Configure logger
logger = logging.getLogger("snel.cache")

# Type variables for better type hints
T = TypeVar('T')
CacheableFunction = Callable[..., Awaitable[T]]

# In-memory cache store
_mem_cache: Dict[str, Dict[str, Any]] = {}

# Maximum cache size to prevent memory issues
_MAX_CACHE_ENTRIES = 1000

# Cache persistence settings
_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.cache/snel_cache.pkl")
_ENABLE_PERSISTENCE = True  # Can be controlled via environment variable

def _get_cache_key(func_name: str, args: tuple, kwargs: Dict[str, Any]) -> str:
    """Generate a unique cache key based on function name and arguments."""
    # Convert args and kwargs to strings for the key
    # Exclude self/cls arguments from class methods
    if args and (str(args[0]).startswith('<') or str(type(args[0])).startswith("<class '")):
        args = args[1:]
    
    # Handle complex objects and ensure consistent string representation
    args_str = str([str(arg) for arg in args])
    kwargs_str = str(sorted([(k, str(v)) for k, v in kwargs.items()]))
    
    return f"{func_name}:{args_str}:{kwargs_str}"

def _clean_cache_if_needed():
    """Remove oldest cache entries if cache is too large."""
    if len(_mem_cache) > _MAX_CACHE_ENTRIES:
        # Sort by expiry time and remove oldest entries
        sorted_entries = sorted(
            [(k, v["expiry"]) for k, v in _mem_cache.items()], 
            key=lambda x: x[1]
        )
        # Remove the oldest 20% of entries
        entries_to_remove = sorted_entries[:int(len(_mem_cache) * 0.2)]
        for key, _ in entries_to_remove:
            del _mem_cache[key]
        logger.info(f"Cache cleanup: removed {len(entries_to_remove)} old entries")
        
    # Persist cache if enabled
    if _ENABLE_PERSISTENCE:
        _save_cache_to_disk()
        
def _save_cache_to_disk():
    """Save the current cache to disk for persistence."""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(_CACHE_FILE), exist_ok=True)
        
        # Filter out expired entries before saving
        now = datetime.now()
        persistent_cache = {
            k: v for k, v in _mem_cache.items() 
            if v["expiry"] > now
        }
        
        # Save to disk
        with open(_CACHE_FILE, 'wb') as f:
            pickle.dump(persistent_cache, f)
        
        logger.debug(f"Cache saved to disk: {len(persistent_cache)} entries")
    except Exception as e:
        logger.warning(f"Failed to save cache to disk: {e}")

def _load_cache_from_disk():
    """Load cache from disk if available."""
    global _mem_cache
    
    try:
        if os.path.exists(_CACHE_FILE):
            with open(_CACHE_FILE, 'rb') as f:
                loaded_cache = pickle.load(f)
            
            # Filter out expired entries
            now = datetime.now()
            valid_entries = {
                k: v for k, v in loaded_cache.items() 
                if v["expiry"] > now
            }
            
            _mem_cache = valid_entries
            logger.info(f"Loaded {len(valid_entries)} cache entries from disk")
            
            # Clean up expired entries from disk cache
            if len(valid_entries) < len(loaded_cache):
                _save_cache_to_disk()
    except Exception as e:
        logger.warning(f"Failed to load cache from disk: {e}")

def cached(ttl_seconds: int = 300, cache_none: bool = False, prefix: str = ""):
    """
    Cache decorator with time-to-live for async functions.
    
    Args:
        ttl_seconds: How long to cache results in seconds (default: 5 minutes)
        cache_none: Whether to cache None results (default: False)
        prefix: Optional prefix for cache keys (useful for namespacing)
        
    Example:
        @cached(ttl_seconds=60)
        async def get_price(self, coin_id: str) -> Dict:
            # Function logic here...
    """
    def decorator(func: CacheableFunction) -> CacheableFunction:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate cache key
            func_name = prefix + func.__name__ if prefix else func.__name__
            key = _get_cache_key(func_name, args, kwargs)
            
            # Check if we have a cached value and it's still valid
            if key in _mem_cache:
                entry = _mem_cache[key]
                if datetime.now() < entry["expiry"]:
                    logger.debug(f"Cache hit: {func_name}")
                    return entry["value"]
                else:
                    # Expired entry
                    del _mem_cache[key]
                    logger.debug(f"Cache expired: {func_name}")
            
            # No cache hit, call the function
            result = await func(*args, **kwargs)
            
            # Don't cache None results unless explicitly requested
            if result is None and not cache_none:
                return result
                
            # Cache the result with expiry time
            _mem_cache[key] = {
                "value": result,
                "expiry": datetime.now() + timedelta(seconds=ttl_seconds),
                "created": datetime.now()
            }
            
            # Clean cache if needed
            _clean_cache_if_needed()
            
            logger.debug(f"Cache miss: {func_name}")
            return result
        return wrapper
    return decorator

def invalidate_cache(func_name: Optional[str] = None, prefix: str = ""):
    """
    Invalidate all cache entries for a specific function or with a prefix.
    
    Args:
        func_name: Function name to invalidate (None for all)
        prefix: Optional prefix to match (used with func_name)
    """
    global _mem_cache
    
    if func_name:
        full_name = prefix + func_name if prefix else func_name
        _mem_cache = {k: v for k, v in _mem_cache.items() if not k.startswith(f"{full_name}:")}
        logger.info(f"Invalidated cache for {full_name}")
    elif prefix:
        _mem_cache = {k: v for k, v in _mem_cache.items() if not k.startswith(f"{prefix}")}
        logger.info(f"Invalidated cache with prefix {prefix}")
    else:
        _mem_cache = {}
        logger.info("Invalidated all cache entries")
    
    # Update persisted cache
    if _ENABLE_PERSISTENCE:
        _save_cache_to_disk()

def get_cache_stats() -> Dict[str, Any]:
    """
    Get statistics about the current cache usage.
    
    Returns:
        Dict with cache statistics
    """
    # Count entries by prefix
    prefixes: Dict[str, int] = {}
    for key in _mem_cache.keys():
        prefix = key.split(':')[0]
        prefixes[prefix] = prefixes.get(prefix, 0) + 1
    
    # Calculate average and max age
    now = datetime.now()
    ages = [(now - v["created"]).total_seconds() for v in _mem_cache.values()]
    avg_age = sum(ages) / len(ages) if ages else 0
    max_age = max(ages) if ages else 0
    
    return {
        "total_entries": len(_mem_cache),
        "entries_by_prefix": prefixes,
        "average_age_seconds": avg_age,
        "max_age_seconds": max_age,
        "max_size": _MAX_CACHE_ENTRIES
    }

async def start_cache_cleanup_task(interval_seconds: int = 300):
    """
    Start a background task to periodically clean expired cache entries.
    
    Args:
        interval_seconds: How often to check for expired entries (default: 5 minutes)
    """
    while True:
        # Wait for the interval
        await asyncio.sleep(interval_seconds)
        
        # Find and remove expired entries
        now = datetime.now()
        expired_keys = [
            k for k, v in _mem_cache.items() 
            if v["expiry"] < now
        ]
        
        # Remove expired entries
        for key in expired_keys:
            del _mem_cache[key]
            
        if expired_keys:
            logger.info(f"Cache cleanup: removed {len(expired_keys)} expired entries")
            
        # Persist cache to disk periodically
        if _ENABLE_PERSISTENCE:
            _save_cache_to_disk()

def cleanup_expired_cache() -> int:
    """
    Clean up expired cache entries.
    
    Returns:
        Number of removed entries
    """
    now = datetime.now()
    expired_keys = [
        k for k, v in _mem_cache.items() 
        if v["expiry"] < now
    ]
    
    # Remove expired entries
    for key in expired_keys:
        del _mem_cache[key]
        
    # Persist changes if any entries were removed
    if expired_keys and _ENABLE_PERSISTENCE:
        _save_cache_to_disk()
        
    return len(expired_keys)

# Initialize cache from disk when module is loaded
if _ENABLE_PERSISTENCE:
    _load_cache_from_disk()