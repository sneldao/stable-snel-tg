import asyncio
import functools
import logging
import random
import time
from typing import Callable, Dict, List, Optional, Type, TypeVar, Any, Union, Awaitable
from datetime import datetime, timedelta

# Configure logger
logger = logging.getLogger("snel.retries")

# Type variables for better type hints
T = TypeVar('T')
RetryableFunction = Callable[..., Awaitable[T]]

class RetryError(Exception):
    """Exception raised when max retries is exceeded."""
    def __init__(self, message: str, original_exception: Exception, attempts: int):
        super().__init__(message)
        self.original_exception = original_exception
        self.attempts = attempts

class CircuitBreakerError(Exception):
    """Exception raised when a circuit breaker is open."""
    def __init__(self, service: str, until: datetime):
        message = f"Circuit breaker for service '{service}' is open until {until.isoformat()}"
        super().__init__(message)
        self.service = service
        self.until = until
        
# Circuit breaker state
_circuit_breakers: Dict[str, Dict[str, Any]] = {}

def _check_circuit_breaker(service: str) -> Optional[CircuitBreakerError]:
    """Check if circuit breaker is open for a service."""
    if service in _circuit_breakers:
        breaker = _circuit_breakers[service]
        if datetime.now() < breaker["until"]:
            return CircuitBreakerError(service, breaker["until"])
        else:
            # Reset circuit breaker state if recovery time has passed
            _circuit_breakers[service]["failures"] = 0
            _circuit_breakers[service]["state"] = "closed"
    return None

def _update_circuit_breaker(service: str, success: bool, threshold: int = 5, recovery_time: int = 60):
    """Update circuit breaker state based on success/failure."""
    now = datetime.now()
    
    # Initialize circuit breaker if it doesn't exist
    if service not in _circuit_breakers:
        _circuit_breakers[service] = {
            "failures": 0,
            "state": "closed",
            "last_failure": now,
            "until": now
        }
    
    breaker = _circuit_breakers[service]
    
    if success:
        # Reset failure count on success if circuit breaker is not open
        if breaker["state"] != "open":
            breaker["failures"] = max(0, breaker["failures"] - 1)
    else:
        # Increment failure count
        breaker["failures"] += 1
        breaker["last_failure"] = now
        
        # Check if we need to open the circuit breaker
        if breaker["failures"] >= threshold and breaker["state"] != "open":
            breaker["state"] = "open"
            breaker["until"] = now + timedelta(seconds=recovery_time)
            logger.warning(
                f"Circuit breaker for {service} opened until "
                f"{breaker['until'].isoformat()} after {breaker['failures']} failures"
            )

def retry(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0, 
    backoff_factor: float = 2.0,
    jitter: bool = True,
    retry_exceptions: Optional[List[Type[Exception]]] = None,
    ignore_exceptions: Optional[List[Type[Exception]]] = None,
    circuit_breaker: Optional[str] = None,
    failure_threshold: int = 5,
    recovery_time: int = 60
):
    """
    Retry decorator for async functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        backoff_factor: Multiplier for the delay on each retry
        jitter: Add randomness to delay to prevent thundering herd
        retry_exceptions: Exceptions that should trigger a retry (defaults to all)
        ignore_exceptions: Exceptions that should not trigger a retry
        circuit_breaker: Optional service name for circuit breaker pattern
        failure_threshold: Number of failures before opening circuit breaker
        recovery_time: Seconds to keep circuit breaker open after threshold reached
        
    Example:
        @retry(max_retries=5, initial_delay=2, circuit_breaker="coingecko")
        async def fetch_data(url: str) -> Dict:
            # Function logic here...
    """
    def decorator(func: RetryableFunction) -> RetryableFunction:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check circuit breaker if enabled
            if circuit_breaker:
                breaker_error = _check_circuit_breaker(circuit_breaker)
                if breaker_error:
                    raise breaker_error
                    
            last_exception = None
            attempt = 0
            delay = initial_delay
            
            while attempt <= max_retries:
                try:
                    result = await func(*args, **kwargs)
                    
                    # Update circuit breaker on success
                    if circuit_breaker:
                        _update_circuit_breaker(circuit_breaker, True, failure_threshold, recovery_time)
                        
                    return result
                except Exception as e:
                    last_exception = e
                    
                    # Check if this exception should be ignored
                    if ignore_exceptions and any(isinstance(e, exc) for exc in ignore_exceptions):
                        logger.debug(f"Exception {type(e).__name__} ignored, not retrying")
                        raise
                    
                    # Check if this exception should trigger a retry
                    if retry_exceptions and not any(isinstance(e, exc) for exc in retry_exceptions):
                        logger.debug(f"Exception {type(e).__name__} not in retry_exceptions, not retrying")
                        raise
                    
                    attempt += 1
                    
                    # Update circuit breaker on failure
                    if circuit_breaker:
                        _update_circuit_breaker(circuit_breaker, False, failure_threshold, recovery_time)
                        
                        # Re-check circuit breaker as it might have just opened
                        breaker_error = _check_circuit_breaker(circuit_breaker)
                        if breaker_error:
                            raise breaker_error
                    
                    # If we've hit max retries, raise the RetryError
                    if attempt > max_retries:
                        logger.warning(
                            f"Max retries ({max_retries}) exceeded for {func.__name__}: {str(e)}"
                        )
                        raise RetryError(
                            f"Function {func.__name__} failed after {attempt} attempts",
                            last_exception,
                            attempt
                        ) from last_exception
                    
                    # Handle rate limit errors differently based on headers or error message
                    is_rate_limit = (
                        "rate limit" in str(e).lower() or 
                        "429" in str(e) or 
                        "too many requests" in str(e).lower() or
                        "quota exceeded" in str(e).lower()
                    )
                    
                    # Calculate delay with exponential backoff
                    if is_rate_limit:
                        # Use a more aggressive backoff for rate limits
                        delay = min(max_delay, delay * backoff_factor * 1.5)
                    else:
                        delay = min(max_delay, delay * backoff_factor)
                    
                    # Add jitter to prevent thundering herd
                    if jitter:
                        delay = delay * (0.5 + random.random())
                    
                    logger.info(
                        f"Retry {attempt}/{max_retries} for {func.__name__} "
                        f"after {delay:.2f}s: {type(e).__name__}: {str(e)}"
                    )
                    
                    # Wait before next attempt
                    await asyncio.sleep(delay)
            
            # This should never be reached, but just in case
            assert last_exception is not None
            raise last_exception
        
        return wrapper
    return decorator

def retry_with_timeout(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    timeout: float = 30.0,
    retry_exceptions: Optional[List[Type[Exception]]] = None,
    circuit_breaker: Optional[str] = None,
    failure_threshold: int = 5,
    recovery_time: int = 60
):
    """
    Retry decorator with timeout for async functions.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for the delay on each retry
        timeout: Maximum time to wait for function execution in seconds
        retry_exceptions: Exceptions that should trigger a retry (defaults to all)
        circuit_breaker: Optional service name for circuit breaker pattern
        failure_threshold: Number of failures before opening circuit breaker
        recovery_time: Seconds to keep circuit breaker open after threshold reached
        
    Example:
        @retry_with_timeout(timeout=10.0, circuit_breaker="news_api")
        async def fetch_external_api(endpoint: str) -> Dict:
            # Function logic here...
    """
    def decorator(func: RetryableFunction) -> RetryableFunction:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check circuit breaker if enabled
            if circuit_breaker:
                breaker_error = _check_circuit_breaker(circuit_breaker)
                if breaker_error:
                    raise breaker_error
                    
            last_exception = None
            attempt = 0
            delay = initial_delay
            
            async def execute_with_timeout():
                # Create a timeout task
                try:
                    return await asyncio.wait_for(func(*args, **kwargs), timeout)
                except asyncio.TimeoutError:
                    logger.warning(f"Function {func.__name__} timed out after {timeout} seconds")
                    raise
            
            while attempt <= max_retries:
                try:
                    result = await execute_with_timeout()
                    
                    # Update circuit breaker on success
                    if circuit_breaker:
                        _update_circuit_breaker(circuit_breaker, True, failure_threshold, recovery_time)
                        
                    return result
                except Exception as e:
                    last_exception = e
                    
                    # Check if this exception should trigger a retry
                    if retry_exceptions and not any(isinstance(e, exc) for exc in retry_exceptions):
                        raise
                    
                    attempt += 1
                    
                    # Update circuit breaker on failure
                    if circuit_breaker:
                        _update_circuit_breaker(circuit_breaker, False, failure_threshold, recovery_time)
                        
                        # Re-check circuit breaker as it might have just opened
                        breaker_error = _check_circuit_breaker(circuit_breaker)
                        if breaker_error:
                            raise breaker_error
                    
                    # If we've hit max retries or got a timeout, raise the exception
                    if attempt > max_retries or isinstance(e, asyncio.TimeoutError):
                        if isinstance(e, asyncio.TimeoutError):
                            logger.warning(
                                f"Function {func.__name__} timed out after {timeout} seconds"
                            )
                        else:
                            logger.warning(
                                f"Max retries ({max_retries}) exceeded for {func.__name__}: {str(e)}"
                            )
                        raise RetryError(
                            f"Function {func.__name__} failed after {attempt} attempts",
                            last_exception,
                            attempt
                        ) from last_exception
                    
                    # Calculate delay with exponential backoff
                    delay = min(timeout/2, delay * backoff_factor)
                    
                    logger.info(
                        f"Retry {attempt}/{max_retries} for {func.__name__} "
                        f"after {delay:.2f}s: {type(e).__name__}: {str(e)}"
                    )
                    
                    # Wait before next attempt
                    await asyncio.sleep(delay)
            
            # This should never be reached, but just in case
            assert last_exception is not None
            raise last_exception
        
        return wrapper
    return decorator

def is_recoverable_error(error: Exception) -> bool:
    """
    Check if an error is potentially recoverable with a retry.
    
    Args:
        error: The exception to check
        
    Returns:
        True if the error might be resolved by retrying
    """
    # Don't retry if circuit breaker is open
    if isinstance(error, CircuitBreakerError):
        return False
        
    # Network-related errors are often temporary
    network_errors = [
        "ConnectionError", "TimeoutError", "ConnectionRefusedError", 
        "ConnectionResetError", "ReadTimeout", "ConnectTimeout"
    ]
    
    # Rate limit or server errors that might resolve with time
    service_errors = [
        "429", "TooManyRequests", "RateLimitError", "500", 
        "503", "ServiceUnavailable", "ServerError", "InternalServerError"
    ]
    
    error_str = str(error)
    error_type = type(error).__name__
    
    # Check for network errors
    if any(err_type in error_type for err_type in network_errors):
        return True
    
    # Check for rate limits and server errors
    if (
        any(err_text in error_str for err_text in service_errors) or
        "rate limit" in error_str.lower() or
        "quota exceeded" in error_str.lower() or
        "try again later" in error_str.lower()
    ):
        return True
    
    return False

def get_circuit_breaker_status() -> Dict[str, Dict[str, Any]]:
    """
    Get the current status of all circuit breakers.
    
    Returns:
        Dict mapping service names to their circuit breaker status
    """
    now = datetime.now()
    result = {}
    
    for service, breaker in _circuit_breakers.items():
        is_open = breaker["state"] == "open" and now < breaker["until"]
        time_remaining = (breaker["until"] - now).total_seconds() if is_open else 0
        
        result[service] = {
            "state": "open" if is_open else "closed",
            "failures": breaker["failures"],
            "last_failure": breaker["last_failure"].isoformat(),
            "time_remaining_seconds": max(0, time_remaining)
        }
    
    return result

def reset_circuit_breaker(service: Optional[str] = None) -> None:
    """
    Reset one or all circuit breakers.
    
    Args:
        service: Service to reset, or None for all services
    """
    global _circuit_breakers
    
    if service:
        if service in _circuit_breakers:
            _circuit_breakers[service] = {
                "failures": 0,
                "state": "closed",
                "last_failure": datetime.now(),
                "until": datetime.now()
            }
            logger.info(f"Reset circuit breaker for {service}")
    else:
        _circuit_breakers = {}
        logger.info("Reset all circuit breakers")