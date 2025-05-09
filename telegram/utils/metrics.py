import asyncio
import logging
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
import time

# Import utility functions
from .cache import get_cache_stats
from .retries import get_circuit_breaker_status

# Configure logger
logger = logging.getLogger("snel.metrics")

class MetricsDashboard:
    """
    Dashboard for monitoring system metrics and performance.
    
    This class collects and reports on:
    - Cache usage and hit rates
    - API call performance
    - Rate limiting status
    - Circuit breaker status
    """
    
    def __init__(self):
        """Initialize the metrics dashboard."""
        self.api_metrics: Dict[str, Dict[str, Any]] = {}
        self.start_time = datetime.now()
        self.collection_enabled = True
        
        # Define metrics storage directory
        self.metrics_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.metrics")
        os.makedirs(self.metrics_dir, exist_ok=True)
        
        logger.info("Metrics dashboard initialized")
    
    def record_api_call(
        self, 
        service: str, 
        method: str, 
        response_time: float, 
        success: bool = True,
        status_code: Optional[int] = None,
        cache_hit: bool = False
    ):
        """
        Record metrics for an API call.
        
        Args:
            service: Service name (e.g., 'coingecko', 'venice')
            method: Method name or endpoint
            response_time: Response time in seconds
            success: Whether the call was successful
            status_code: HTTP status code if applicable
            cache_hit: Whether the result came from cache
        """
        if not self.collection_enabled:
            return
            
        # Initialize service metrics if needed
        if service not in self.api_metrics:
            self.api_metrics[service] = {
                'total_calls': 0,
                'success_calls': 0,
                'error_calls': 0,
                'cache_hits': 0,
                'total_time': 0.0,
                'min_time': float('inf'),
                'max_time': 0.0,
                'methods': {},
                'status_codes': {},
                'last_call_time': datetime.now().isoformat()
            }
        
        # Update service-level metrics
        metrics = self.api_metrics[service]
        metrics['total_calls'] += 1
        metrics['last_call_time'] = datetime.now().isoformat()
        
        if success:
            metrics['success_calls'] += 1
        else:
            metrics['error_calls'] += 1
            
        if cache_hit:
            metrics['cache_hits'] += 1
            
        # Only count response time for non-cache hits
        if not cache_hit:
            metrics['total_time'] += response_time
            metrics['min_time'] = min(metrics['min_time'], response_time)
            metrics['max_time'] = max(metrics['max_time'], response_time)
        
        # Update method-specific metrics
        if method not in metrics['methods']:
            metrics['methods'][method] = {
                'total_calls': 0,
                'success_calls': 0,
                'error_calls': 0,
                'cache_hits': 0,
                'total_time': 0.0,
                'min_time': float('inf'),
                'max_time': 0.0
            }
        
        method_metrics = metrics['methods'][method]
        method_metrics['total_calls'] += 1
        
        if success:
            method_metrics['success_calls'] += 1
        else:
            method_metrics['error_calls'] += 1
            
        if cache_hit:
            method_metrics['cache_hits'] += 1
            
        # Only count response time for non-cache hits
        if not cache_hit:
            method_metrics['total_time'] += response_time
            method_metrics['min_time'] = min(method_metrics['min_time'], response_time)
            method_metrics['max_time'] = max(method_metrics['max_time'], response_time)
        
        # Update status code metrics
        if status_code is not None:
            status_str = str(status_code)
            if status_str not in metrics['status_codes']:
                metrics['status_codes'][status_str] = 0
            metrics['status_codes'][status_str] += 1
    
    def get_api_metrics(self, service: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current API metrics.
        
        Args:
            service: Service name to get metrics for, or None for all
            
        Returns:
            Dict with metrics data
        """
        # Calculate derived metrics
        for svc_name, metrics in self.api_metrics.items():
            # Add average response time
            if metrics['total_calls'] - metrics['cache_hits'] > 0:
                metrics['avg_time'] = metrics['total_time'] / (metrics['total_calls'] - metrics['cache_hits'])
            else:
                metrics['avg_time'] = 0.0
                
            # Fix min_time if no calls recorded
            if metrics['min_time'] == float('inf'):
                metrics['min_time'] = 0.0
                
            # Calculate cache hit rate
            if metrics['total_calls'] > 0:
                metrics['cache_hit_rate'] = metrics['cache_hits'] / metrics['total_calls']
            else:
                metrics['cache_hit_rate'] = 0.0
                
            # Calculate success rate
            if metrics['total_calls'] > 0:
                metrics['success_rate'] = metrics['success_calls'] / metrics['total_calls']
            else:
                metrics['success_rate'] = 0.0
                
            # Calculate method-specific derived metrics
            for method_name, method_metrics in metrics['methods'].items():
                if method_metrics['total_calls'] - method_metrics['cache_hits'] > 0:
                    method_metrics['avg_time'] = method_metrics['total_time'] / (method_metrics['total_calls'] - method_metrics['cache_hits'])
                else:
                    method_metrics['avg_time'] = 0.0
                    
                if method_metrics['min_time'] == float('inf'):
                    method_metrics['min_time'] = 0.0
                    
                if method_metrics['total_calls'] > 0:
                    method_metrics['cache_hit_rate'] = method_metrics['cache_hits'] / method_metrics['total_calls']
                    method_metrics['success_rate'] = method_metrics['success_calls'] / method_metrics['total_calls']
                else:
                    method_metrics['cache_hit_rate'] = 0.0
                    method_metrics['success_rate'] = 0.0
        
        # Return metrics for requested service or all metrics
        if service:
            return self.api_metrics.get(service, {})
        else:
            return self.api_metrics
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get a complete dashboard with all metrics data.
        
        Returns:
            Dict with all metrics data for the dashboard
        """
        # Get cache statistics
        cache_stats = get_cache_stats()
        
        # Get circuit breaker status
        circuit_breaker_stats = get_circuit_breaker_status()
        
        # Get API metrics
        api_metrics = self.get_api_metrics()
        
        # Calculate uptime
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        # Check if any limiters module is available
        rate_limit_stats = {}
        try:
            from .limits.token_bucket import get_all_limiters
            limiters = get_all_limiters()
            rate_limit_stats = {name: limiter.get_status() for name, limiter in limiters.items()}
        except ImportError:
            pass
        
        # Assemble the dashboard data
        dashboard = {
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': uptime,
            'cache': cache_stats,
            'circuit_breakers': circuit_breaker_stats,
            'api_metrics': api_metrics,
            'rate_limits': rate_limit_stats
        }
        
        return dashboard
    
    def save_metrics_snapshot(self, filename: Optional[str] = None) -> str:
        """
        Save current metrics to a JSON file.
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to the saved metrics file
        """
        dashboard = self.get_dashboard_data()
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_{timestamp}.json"
            
        filepath = os.path.join(self.metrics_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(dashboard, f, indent=2)
            
        logger.info(f"Saved metrics snapshot to {filepath}")
        return filepath
    
    def reset_api_metrics(self, service: Optional[str] = None):
        """
        Reset API metrics.
        
        Args:
            service: Service to reset metrics for, or None for all
        """
        if service:
            if service in self.api_metrics:
                del self.api_metrics[service]
                logger.info(f"Reset metrics for {service}")
        else:
            self.api_metrics = {}
            logger.info("Reset all API metrics")
    
    def enable_collection(self):
        """Enable metrics collection."""
        self.collection_enabled = True
        logger.info("Metrics collection enabled")
    
    def disable_collection(self):
        """Disable metrics collection."""
        self.collection_enabled = False
        logger.info("Metrics collection disabled")
    
    def generate_report(self) -> str:
        """
        Generate a human-readable text report of current metrics.
        
        Returns:
            String containing the report
        """
        dashboard = self.get_dashboard_data()
        
        # Format the report
        lines = []
        lines.append("======= SNEL TELEGRAM BOT METRICS REPORT =======")
        lines.append(f"Generated: {dashboard['timestamp']}")
        lines.append(f"Uptime: {dashboard['uptime_seconds'] / 3600:.1f} hours")
        lines.append("")
        
        # Cache stats
        cache = dashboard['cache']
        lines.append("=== CACHE STATISTICS ===")
        lines.append(f"Total entries: {cache['total_entries']} / {cache['max_size']}")
        lines.append(f"Average age: {cache['average_age_seconds'] / 60:.1f} minutes")
        lines.append(f"Max age: {cache['max_age_seconds'] / 60:.1f} minutes")
        
        if 'entries_by_prefix' in cache:
            lines.append("Entries by prefix:")
            for prefix, count in cache['entries_by_prefix'].items():
                lines.append(f"  - {prefix}: {count}")
        lines.append("")
        
        # Circuit breakers
        if dashboard['circuit_breakers']:
            lines.append("=== CIRCUIT BREAKERS ===")
            for service, breaker in dashboard['circuit_breakers'].items():
                status = "OPEN" if breaker['state'] == 'open' else "CLOSED"
                lines.append(f"{service}: {status}")
                if breaker['state'] == 'open':
                    lines.append(f"  Time remaining: {breaker['time_remaining_seconds']:.1f}s")
                lines.append(f"  Failures: {breaker['failures']}")
                lines.append(f"  Last failure: {breaker['last_failure']}")
            lines.append("")
        
        # API metrics
        if dashboard['api_metrics']:
            lines.append("=== API METRICS ===")
            for service, metrics in dashboard['api_metrics'].items():
                lines.append(f"{service}:")
                lines.append(f"  Total calls: {metrics['total_calls']}")
                lines.append(f"  Success rate: {metrics['success_rate']*100:.1f}%")
                lines.append(f"  Cache hit rate: {metrics['cache_hit_rate']*100:.1f}%")
                if 'avg_time' in metrics:
                    lines.append(f"  Avg response time: {metrics['avg_time']*1000:.1f}ms")
                
                # Add method details for services with high call volumes
                if metrics['total_calls'] > 10:
                    lines.append("  Methods:")
                    for method, method_metrics in metrics['methods'].items():
                        if method_metrics['total_calls'] > 5:
                            lines.append(f"    {method}:")
                            lines.append(f"      Calls: {method_metrics['total_calls']}")
                            lines.append(f"      Success rate: {method_metrics['success_rate']*100:.1f}%")
                            lines.append(f"      Cache hit rate: {method_metrics['cache_hit_rate']*100:.1f}%")
                            if 'avg_time' in method_metrics:
                                lines.append(f"      Avg response time: {method_metrics['avg_time']*1000:.1f}ms")
            lines.append("")
        
        # Rate limits
        if dashboard['rate_limits']:
            lines.append("=== RATE LIMITS ===")
            for name, limiter in dashboard['rate_limits'].items():
                lines.append(f"{name}:")
                lines.append(f"  Tokens: {limiter['tokens']:.1f} / {limiter['max_tokens']}")
                lines.append(f"  Rate: {limiter['tokens_per_second']}/s")
                lines.append(f"  Utilization: {limiter['utilization']*100:.1f}%")
                if limiter['waiters'] > 0:
                    lines.append(f"  Waiters: {limiter['waiters']}")
            lines.append("")
        
        return "\n".join(lines)


# Create a singleton instance
_dashboard = MetricsDashboard()

def get_dashboard() -> MetricsDashboard:
    """Get the metrics dashboard singleton instance."""
    return _dashboard

async def start_metrics_collection_task(interval_seconds: int = 3600):
    """
    Start a background task to periodically save metrics snapshots.
    
    Args:
        interval_seconds: How often to save snapshots (default: 1 hour)
    """
    dashboard = get_dashboard()
    
    while True:
        try:
            # Wait for the interval
            await asyncio.sleep(interval_seconds)
            
            # Save a snapshot
            dashboard.save_metrics_snapshot()
            
        except asyncio.CancelledError:
            logger.info("Metrics collection task cancelled")
            break
        except Exception as e:
            logger.error(f"Error in metrics collection: {e}")
            # Continue running despite errors
            await asyncio.sleep(10)

def record_api_call(
    service: str, 
    method: str, 
    start_time: float, 
    success: bool = True,
    status_code: Optional[int] = None,
    cache_hit: bool = False
):
    """
    Record metrics for an API call from its start time.
    
    Args:
        service: Service name
        method: Method name or endpoint
        start_time: Call start time (from time.time())
        success: Whether the call was successful
        status_code: HTTP status code if applicable
        cache_hit: Whether the result came from cache
    """
    response_time = time.time() - start_time
    _dashboard.record_api_call(service, method, response_time, success, status_code, cache_hit)

def api_metrics_decorator(service: str, method: Optional[str] = None):
    """
    Decorator to record API call metrics.
    
    Args:
        service: Service name
        method: Method name (defaults to function name)
        
    Example:
        @api_metrics_decorator('coingecko')
        async def get_price(coin_id: str) -> Dict:
            # Function logic here...
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Get method name from parameter or function name
            method_name = method or func.__name__
            
            # Record start time
            start = time.time()
            cache_hit = False
            success = True
            status_code = None
            
            try:
                # Check if this is from cache (if function has a __cached__ attribute)
                if hasattr(func, '__cached__'):
                    # Check if result is in cache
                    pass  # Would need to check cache, but this requires modifying the cache decorator
                
                # Call the function
                result = await func(*args, **kwargs)
                
                # Extract status code if result has it
                if isinstance(result, dict) and 'status_code' in result:
                    status_code = result['status_code']
                
                return result
            except Exception as e:
                success = False
                # Try to extract status code from exception
                if hasattr(e, 'status_code'):
                    status_code = e.status_code
                elif hasattr(e, 'code'):
                    status_code = e.code
                raise
            finally:
                # Record the metrics
                response_time = time.time() - start
                _dashboard.record_api_call(
                    service, method_name, response_time, 
                    success, status_code, cache_hit
                )
        
        return wrapper
    return decorator