import asyncio
import logging
import time
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger("snel.limits")

class TokenBucketLimiter:
    """
    Token bucket rate limiter for API requests.
    
    This implements a token bucket algorithm for rate limiting:
    - Each bucket has a maximum capacity of tokens
    - Tokens are added at a fixed refill rate
    - Each operation consumes one or more tokens
    - If the bucket doesn't have enough tokens, the operation blocks until tokens are available
    """
    
    def __init__(
        self, 
        name: str,
        tokens_per_second: float, 
        max_tokens: int,
        fair_share: bool = True
    ):
        """
        Initialize a new token bucket rate limiter.
        
        Args:
            name: Name of this limiter for logging
            tokens_per_second: Rate at which tokens are added to the bucket
            max_tokens: Maximum capacity of the bucket
            fair_share: Whether to distribute tokens fairly among waiters
        """
        self.name = name
        self.tokens_per_second = tokens_per_second
        self.max_tokens = max_tokens
        self.fair_share = fair_share
        
        # Internal state
        self.tokens = max_tokens
        self.last_refill = time.monotonic()
        self.waiters: List[asyncio.Future] = []
        
        logger.debug(f"Rate limiter '{name}' initialized: {tokens_per_second}/s, max {max_tokens}")
    
    def _refill_tokens(self):
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.last_refill = now
        
        # Calculate new tokens and add them (up to max_tokens)
        new_tokens = elapsed * self.tokens_per_second
        self.tokens = min(self.max_tokens, self.tokens + new_tokens)
    
    def _notify_waiters(self):
        """Notify waiting coroutines that tokens are available."""
        if not self.waiters:
            return
            
        # If fair_share is enabled, we distribute tokens evenly
        if self.fair_share and len(self.waiters) > 1:
            # Calculate available tokens per waiter
            tokens_per_waiter = self.tokens / len(self.waiters)
            resolved_waiters = []
            
            for waiter in self.waiters:
                tokens_needed = waiter.get_loop().get_task_factory().tokens_needed
                if tokens_needed <= tokens_per_waiter:
                    waiter.set_result(None)
                    resolved_waiters.append(waiter)
                    self.tokens -= tokens_needed
            
            # Remove resolved waiters
            for waiter in resolved_waiters:
                self.waiters.remove(waiter)
        else:
            # Simple case: resolve waiters in order until we run out of tokens
            resolved_waiters = []
            
            for waiter in self.waiters:
                tokens_needed = waiter.get_loop().get_task_factory().tokens_needed
                if tokens_needed <= self.tokens:
                    waiter.set_result(None)
                    resolved_waiters.append(waiter)
                    self.tokens -= tokens_needed
                else:
                    break
            
            # Remove resolved waiters
            for waiter in resolved_waiters:
                self.waiters.remove(waiter)
    
    async def acquire(self, tokens: int = 1) -> float:
        """
        Acquire tokens from the bucket, waiting if necessary.
        
        Args:
            tokens: Number of tokens to acquire
            
        Returns:
            Time waited in seconds
        """
        start_time = time.monotonic()
        
        # Refill tokens
        self._refill_tokens()
        
        # If we have enough tokens, consume them immediately
        if tokens <= self.tokens:
            self.tokens -= tokens
            return 0.0
        
        # We need to wait for tokens
        loop = asyncio.get_running_loop()
        waiter = loop.create_future()
        waiter.get_loop().get_task_factory().tokens_needed = tokens
        self.waiters.append(waiter)
        
        # Log waiting
        logger.debug(
            f"Rate limit hit for '{self.name}': waiting for {tokens} tokens "
            f"(have {self.tokens:.2f}, rate {self.tokens_per_second}/s)"
        )
        
        try:
            await waiter
        except asyncio.CancelledError:
            # Remove waiter on cancellation
            if waiter in self.waiters:
                self.waiters.remove(waiter)
            raise
        
        wait_time = time.monotonic() - start_time
        if wait_time > 1.0:  # Only log significant waits
            logger.info(f"Rate limit delay for '{self.name}': waited {wait_time:.2f}s for {tokens} tokens")
        
        return wait_time
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of this rate limiter."""
        self._refill_tokens()  # Ensure tokens are up to date
        
        return {
            "name": self.name,
            "tokens": self.tokens,
            "max_tokens": self.max_tokens,
            "tokens_per_second": self.tokens_per_second,
            "waiters": len(self.waiters),
            "utilization": (self.max_tokens - self.tokens) / self.max_tokens
        }


# Global registry of rate limiters
_limiters: Dict[str, TokenBucketLimiter] = {}

def get_limiter(name: str) -> Optional[TokenBucketLimiter]:
    """Get a rate limiter by name."""
    return _limiters.get(name)

def register_limiter(
    name: str, 
    tokens_per_second: float, 
    max_tokens: int,
    fair_share: bool = True
) -> TokenBucketLimiter:
    """Register a new rate limiter with the given parameters."""
    if name in _limiters:
        logger.warning(f"Overwriting existing rate limiter '{name}'")
    
    limiter = TokenBucketLimiter(name, tokens_per_second, max_tokens, fair_share)
    _limiters[name] = limiter
    return limiter

def get_all_limiters() -> Dict[str, TokenBucketLimiter]:
    """Get all registered rate limiters."""
    return _limiters.copy()

async def with_rate_limit(name: str, func, *args, **kwargs):
    """
    Execute a function with rate limiting.
    
    Args:
        name: Name of the rate limiter to use
        func: Function to execute
        *args, **kwargs: Arguments to pass to the function
        
    Returns:
        Result of the function
    """
    limiter = get_limiter(name)
    if limiter is None:
        logger.warning(f"Rate limiter '{name}' not found, executing without limiting")
        return await func(*args, **kwargs)
    
    await limiter.acquire()
    return await func(*args, **kwargs)