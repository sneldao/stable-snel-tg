# SNEL Telegram Bot Utilities

This document provides an overview of the utility modules included in the SNEL Telegram Bot to enhance reliability, performance, and maintainability.

## Table of Contents

- [Cache System](#cache-system)
- [Error Handling & Retries](#error-handling--retries)
- [Rate Limiting](#rate-limiting)
- [Metrics & Monitoring](#metrics--monitoring)
- [Logging](#logging)
- [Startup Utilities](#startup-utilities)

## Cache System

Located in `telegram/utils/cache.py`, the caching system provides:

### Features

- In-memory caching with configurable TTL (Time To Live)
- Disk persistence for cache survival between restarts
- Automatic cleanup of expired entries
- Memory usage control with entry limits
- Cache invalidation by function name or prefix
- Cache statistics for monitoring

### How to Use

```python
from telegram.utils.cache import cached

# Basic usage with default 5-minute TTL
@cached()
async def get_data(param1, param2):
    # Expensive operation
    return result

# Custom TTL (1 hour) and prefix
@cached(ttl_seconds=3600, prefix="crypto")
async def get_coin_info(coin_id):
    # API call or database query
    return result

# Manually invalidate cache
from telegram.utils.cache import invalidate_cache

# Invalidate for a specific function
invalidate_cache(func_name="get_coin_info")

# Invalidate everything with a prefix
invalidate_cache(prefix="crypto")

# Get cache statistics
from telegram.utils.cache import get_cache_stats
stats = get_cache_stats()
```

## Error Handling & Retries

Located in `telegram/utils/retries.py`, the retry system provides:

### Features

- Retry decorator with configurable attempts
- Exponential backoff with jitter
- Circuit breaker pattern to prevent cascading failures
- Retry timeout functionality
- Specific exception handling
- Rate limit detection and appropriate backoff

### How to Use

```python
from telegram.utils.retries import retry, retry_with_timeout

# Basic retry with default settings (3 retries)
@retry()
async def fetch_data(url):
    # API call that might fail
    return result

# Advanced retry with circuit breaker
@retry(
    max_retries=5,
    initial_delay=1.0,
    backoff_factor=2.0,
    jitter=True,
    circuit_breaker="api_name",
    failure_threshold=5,
    recovery_time=60
)
async def get_external_data(endpoint):
    # Unreliable API call
    return result

# Retry with timeout
@retry_with_timeout(
    max_retries=3,
    timeout=10.0
)
async def fetch_with_timeout(url):
    # API call that might hang
    return result

# Check circuit breaker status
from telegram.utils.retries import get_circuit_breaker_status
status = get_circuit_breaker_status()

# Reset circuit breakers
from telegram.utils.retries import reset_circuit_breaker
reset_circuit_breaker("api_name")  # Reset specific service
reset_circuit_breaker()  # Reset all
```

## Rate Limiting

Located in `telegram/utils/limits/token_bucket.py`, the rate limiting system provides:

### Features

- Token bucket algorithm for precise rate control
- Fair sharing of tokens between competing requests
- Configurable token rates and bucket sizes
- Service-specific rate limiters
- Automatic waiting for tokens to be available
- Rate limit statistics

### How to Use

```python
from telegram.utils.limits.token_bucket import get_limiter, register_limiter

# Register a new rate limiter (typically done at startup)
register_limiter(
    name="coingecko",
    tokens_per_second=0.5,  # 30 per minute
    max_tokens=30           # Burst capacity
)

# Use in async functions
async def fetch_price(coin_id):
    limiter = get_limiter("coingecko")
    if limiter:
        await limiter.acquire()  # Will wait if necessary
    
    # Make API call
    return result

# Alternative approach with wrapper
from telegram.utils.limits.token_bucket import with_rate_limit

async def get_data():
    result = await with_rate_limit(
        "coingecko",
        api_client.fetch,
        "endpoint"
    )
    return result
```

## Metrics & Monitoring

Located in `telegram/utils/metrics.py`, the metrics system provides:

### Features

- API call performance tracking
- Cache efficiency monitoring
- Circuit breaker status tracking
- Rate limit utilization metrics
- Human-readable reports
- Metrics persistence
- Background metric collection

### How to Use

```python
from telegram.utils.metrics import record_api_call, get_dashboard

# Record API metrics manually
import time
start_time = time.time()
success = True
try:
    result = await api_call()
except Exception:
    success = False
    raise
finally:
    record_api_call(
        "service_name",
        "method_name",
        start_time,
        success,
        status_code=200,
        cache_hit=False
    )

# Use the decorator pattern
from telegram.utils.metrics import api_metrics_decorator

@api_metrics_decorator("coingecko")
async def get_price(coin_id):
    # API call
    return result

# Generate a report
dashboard = get_dashboard()
report = dashboard.generate_report()
print(report)

# Save metrics snapshot
filepath = dashboard.save_metrics_snapshot()
```

## Logging

Located in `telegram/utils/logging.py`, the logging system provides:

### Features

- Configurable log levels
- File and console logging
- Module-specific log levels
- Structured API call logging
- Exception logging with context
- Debug mode toggle

### How to Use

```python
from telegram.utils.logging import setup_logging, get_logger

# Configure logging
setup_logging(
    level="INFO",
    log_to_file=True,
    log_file="logs/bot.log",
    module_levels={
        "snel.crypto": "DEBUG",
        "snel.ai": "WARNING"
    }
)

# Get a logger for a specific module
logger = get_logger("snel.service")
logger.info("Service initialized")
logger.debug("Detailed information")

# Log API calls
from telegram.utils.logging import log_api_call

log_api_call(
    logger,
    service="coingecko",
    method="get_price",
    params={"coin_id": "bitcoin"},
    success=True,
    response_time=0.345
)

# Log exceptions with context
from telegram.utils.logging import log_exception

try:
    # Some code that might fail
    result = calculate_value()
except ValueError as e:
    log_exception(
        logger,
        e,
        context={"input": user_input, "step": "calculation"},
        level="ERROR"
    )

# Toggle debug mode
from telegram.utils.logging import enable_debug_mode, disable_debug_mode
enable_debug_mode()  # Set all modules to DEBUG
# ... do debugging ...
disable_debug_mode()  # Return to normal logging
```

## Startup Utilities

Located in `telegram/utils/startup.py`, the startup utilities provide:

### Features

- Environment variable loading
- Background task management
- API key checking
- Rate limiter initialization
- Cache cleanup scheduling

### How to Use

```python
from telegram.utils.startup import load_environment, initialize_background_tasks

# Load environment variables
load_environment(".env.prod")

# Initialize all background tasks
initialize_background_tasks()

# Check required API keys
from telegram.utils.startup import check_api_keys
if not check_api_keys():
    print("Missing required API keys!")
    exit(1)

# Shutdown background tasks on exit
from telegram.utils.startup import shutdown_background_tasks
try:
    # Main application code
    run_bot()
finally:
    shutdown_background_tasks()
```

## Integration Example

Here's an example of how to integrate all utilities together:

```python
import asyncio
from telegram.utils.startup import load_environment, initialize_background_tasks, shutdown_background_tasks
from telegram.utils.logging import setup_logging, get_logger
from telegram.services.enhanced_crypto_service import EnhancedCryptoService

async def main():
    # Setup logging
    setup_logging(level="INFO", log_to_file=True)
    logger = get_logger("snel.main")
    
    try:
        # Load environment and initialize background tasks
        load_environment()
        initialize_background_tasks()
        
        # Initialize services
        crypto_service = EnhancedCryptoService()
        
        # Use the service with all utilities integrated
        btc_price = await crypto_service.get_price("bitcoin")
        logger.info(f"Bitcoin price: ${btc_price['usd']}")
        
        # Generate and save metrics
        metrics_report = crypto_service.generate_metrics_report()
        logger.info(f"Metrics report generated:\n{metrics_report}")
        
        # Keep the application running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    finally:
        # Clean up
        shutdown_background_tasks()

if __name__ == "__main__":
    asyncio.run(main())
```

## Best Practices

1. **Cache Wisely**: Use shorter TTLs for volatile data, longer for stable data
2. **Circuit Breaker Naming**: Use consistent service names for circuit breakers
3. **Rate Limits**: Set rate limits according to API documentation
4. **Metrics Collection**: Enable metrics in production but be mindful of storage
5. **Logging Levels**: Use appropriate log levels to avoid log spam

---

For more information, refer to the docstrings in each utility module or contact the project maintainers.