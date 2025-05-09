import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
import os
import time

from ..utils.cache import cached
from ..utils.retries import retry, is_recoverable_error
from ..utils.limits.token_bucket import get_limiter
from ..utils.metrics import record_api_call
from ..utils.coin_mapper import get_coin_id
from .crypto_service import CryptoService

# Configure logger
logger = logging.getLogger("snel.enhanced_crypto")

class EnhancedCryptoService(CryptoService):
    """
    Enhanced version of CryptoService with caching and retry capabilities.
    
    This class extends the base CryptoService to provide:
    - Response caching with configurable TTL
    - Automatic retries with exponential backoff
    - Rate limit handling
    - Better error reporting
    """
    
    def __init__(self):
        """Initialize the enhanced crypto service."""
        super().__init__()
        
        # Cache TTLs in seconds for different data types
        self.cache_ttls = {
            'price': 60,           # 1 minute for current price
            'detailed_price': 300, # 5 minutes for detailed price
            'coin_info': 3600,     # 1 hour for coin info (changes rarely)
            'top_coins': 300,      # 5 minutes for top coins
            'historical': 3600,    # 1 hour for historical data
            'market_data': 300     # 5 minutes for market data
        }
        
        logger.info("EnhancedCryptoService initialized with caching and retries")
    
    @cached(ttl_seconds=60)  # 1 minute cache
    @retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0, circuit_breaker="coingecko")
    async def get_price(self, coin_id: str) -> Dict:
        """Get current price for a coin with caching and retries."""
        # Map symbol to coin ID if needed
        coin_id = get_coin_id(coin_id)
        logger.debug(f"Fetching price for {coin_id}")
        
        # Apply rate limiting
        limiter = get_limiter("coingecko")
        if limiter:
            await limiter.acquire()
            
        # Record API metrics
        start_time = time.time()
        cache_hit = False  # Will be set by cache decorator
        success = True
        result = None
        
        try:
            result = await super().get_price(coin_id)
            return result
        except Exception as e:
            success = False
            raise
        finally:
            record_api_call("coingecko", "get_price", start_time, success, None, cache_hit)
    
    @cached(ttl_seconds=300)  # 5 minute cache
    @retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0, circuit_breaker="coingecko")
    async def get_detailed_price(self, coin_id: str) -> Dict:
        """Get detailed price information with caching and retries."""
        # Map symbol to coin ID if needed
        coin_id = get_coin_id(coin_id)
        logger.debug(f"Fetching detailed price for {coin_id}")
        
        # Apply rate limiting
        limiter = get_limiter("coingecko")
        if limiter:
            await limiter.acquire()
            
        # Record API metrics
        start_time = time.time()
        cache_hit = False
        success = True
        
        try:
            result = await super().get_detailed_price(coin_id)
            return result
        except Exception as e:
            success = False
            raise
        finally:
            record_api_call("coingecko", "get_detailed_price", start_time, success, None, cache_hit)
    
    @cached(ttl_seconds=3600)  # 1 hour cache
    @retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0, circuit_breaker="coingecko")
    async def get_coin_info(self, coin_id: str) -> Dict:
        """Get detailed information about a coin with caching and retries."""
        # Map symbol to coin ID if needed
        coin_id = get_coin_id(coin_id)
        logger.debug(f"Fetching coin info for {coin_id}")
        
        # Apply rate limiting
        limiter = get_limiter("coingecko")
        if limiter:
            await limiter.acquire()
            
        # Record API metrics
        start_time = time.time()
        cache_hit = False
        success = True
        
        try:
            result = await super().get_coin_info(coin_id)
            return result
        except Exception as e:
            success = False
            raise
        finally:
            record_api_call("coingecko", "get_coin_info", start_time, success, None, cache_hit)
    
    @cached(ttl_seconds=300)  # 5 minute cache
    @retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0, circuit_breaker="coingecko")
    async def get_top_coins(self, limit: int = 30) -> List[Dict]:
        """Get top coins by market cap with caching and retries."""
        logger.debug(f"Fetching top {limit} coins")
        
        # Apply rate limiting
        limiter = get_limiter("coingecko")
        if limiter:
            await limiter.acquire()
            
        # Record API metrics
        start_time = time.time()
        cache_hit = False
        success = True
        
        try:
            result = await super().get_top_coins(limit)
            return result
        except Exception as e:
            success = False
            raise
        finally:
            record_api_call("coingecko", "get_top_coins", start_time, success, None, cache_hit)
    
    @cached(ttl_seconds=300)  # 5 minute cache
    @retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0, circuit_breaker="coingecko")
    async def get_movers(self, timeframe: str = '24h', direction: str = 'gainers') -> List[Dict]:
        """Get best/worst performing coins with caching and retries."""
        logger.debug(f"Fetching {direction} for {timeframe}")
        return await super().get_movers(timeframe, direction)
    
    @cached(ttl_seconds=3600)  # 1 hour cache for chart data
    @retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0, circuit_breaker="coingecko")
    async def generate_price_chart(self, coin_id: str, days: int = 7) -> Optional[bytes]:
        """Generate a price chart with caching and retries."""
        # Map symbol to coin ID if needed
        coin_id = get_coin_id(coin_id)
        logger.debug(f"Generating price chart for {coin_id} over {days} days")
        return await super().generate_price_chart(coin_id, days)
    
    @cached(ttl_seconds=3600)  # 1 hour cache for chart data
    @retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0, circuit_breaker="coingecko")
    async def generate_candlestick_chart(self, coin_id: str, days: int = 7) -> Optional[bytes]:
        """Generate a candlestick chart with caching and retries."""
        # Map symbol to coin ID if needed
        coin_id = get_coin_id(coin_id)
        logger.debug(f"Generating candlestick chart for {coin_id} over {days} days")
        return await super().generate_candlestick_chart(coin_id, days)
    
    @cached(ttl_seconds=300)  # 5 minute cache
    @retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0, circuit_breaker="coingecko")
    async def get_price_change(self, coin_id: str, period: str = '7d') -> Dict:
        """Get price change analysis with caching and retries."""
        # Map symbol to coin ID if needed
        coin_id = get_coin_id(coin_id)
        logger.debug(f"Getting price change for {coin_id} over {period}")
        return await super().get_price_change(coin_id, period)
    
    @cached(ttl_seconds=300)  # 5 minute cache
    @retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0, circuit_breaker="coingecko")
    async def get_roi(self, coin_id: str) -> Dict:
        """Calculate Return on Investment with caching and retries."""
        # Map symbol to coin ID if needed
        coin_id = get_coin_id(coin_id)
        logger.debug(f"Calculating ROI for {coin_id}")
        return await super().get_roi(coin_id)
    
    @cached(ttl_seconds=300)  # 5 minute cache
    @retry(max_retries=3, initial_delay=1.0, backoff_factor=2.0, circuit_breaker="coingecko")
    async def get_ath_analysis(self, coin_id: str) -> Dict:
        """Get All Time High analysis with caching and retries."""
        # Map symbol to coin ID if needed
        coin_id = get_coin_id(coin_id)
        logger.debug(f"Getting ATH analysis for {coin_id}")
        return await super().get_ath_analysis(coin_id)
    
    # Utility methods
    
    def clear_cache(self, coin_id: Optional[str] = None):
        """
        Clear specific or all cached data.
        
        Args:
            coin_id: If provided, clear only cache for this coin, otherwise all cache
        """
        from ..utils.cache import invalidate_cache
        
        if coin_id:
            logger.info(f"Clearing cache for {coin_id}")
            # Invalidate specific coin cache by prefix
            invalidate_cache(prefix=f"get_price_{coin_id}")
            invalidate_cache(prefix=f"get_detailed_price_{coin_id}")
            invalidate_cache(prefix=f"get_coin_info_{coin_id}")
        else:
            logger.info("Clearing all crypto data cache")
            # Invalidate all methods
            invalidate_cache(func_name="get_price")
            invalidate_cache(func_name="get_detailed_price")
            invalidate_cache(func_name="get_coin_info")
            invalidate_cache(func_name="get_top_coins")
            invalidate_cache(func_name="get_movers")
            invalidate_cache(func_name="generate_price_chart")
            invalidate_cache(func_name="generate_candlestick_chart")
            invalidate_cache(func_name="get_price_change")
            invalidate_cache(func_name="get_roi")
            invalidate_cache(func_name="get_ath_analysis")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the cache usage."""
        from ..utils.cache import get_cache_stats
        return get_cache_stats()
        
    def get_circuit_breaker_stats(self) -> Dict[str, Any]:
        """Get statistics about the circuit breaker status."""
        from ..utils.retries import get_circuit_breaker_status
        return get_circuit_breaker_status()
        
    def reset_circuit_breaker(self, service: Optional[str] = None):
        """
        Reset circuit breaker for a specific service or all services.
        
        Args:
            service: Service name to reset (None for all)
        """
        from ..utils.retries import reset_circuit_breaker
        reset_circuit_breaker(service)
        logger.info(f"Reset circuit breaker: {service or 'all'}")
        
    def get_metrics_dashboard(self) -> Dict[str, Any]:
        """Get complete metrics dashboard data."""
        from ..utils.metrics import get_dashboard
        dashboard = get_dashboard()
        return dashboard.get_dashboard_data()
        
    def generate_metrics_report(self) -> str:
        """Generate a human-readable metrics report."""
        from ..utils.metrics import get_dashboard
        dashboard = get_dashboard()
        return dashboard.generate_report()
        
    def save_metrics_snapshot(self) -> str:
        """Save current metrics to a JSON file."""
        from ..utils.metrics import get_dashboard
        dashboard = get_dashboard()
        return dashboard.save_metrics_snapshot()
        
    def reset_metrics(self, service: Optional[str] = None):
        """
        Reset metrics for a specific service or all services.
        
        Args:
            service: Service name to reset (None for all)
        """
        from ..utils.metrics import get_dashboard
        dashboard = get_dashboard()
        dashboard.reset_api_metrics(service)
        logger.info(f"Reset metrics: {service or 'all'}")