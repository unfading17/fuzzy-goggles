import time
import functools
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def measure_execution_time(func: Callable) -> Callable:
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            if execution_time > 1.0:
                logger.warning(
                    f"Slow function: {func.__name__} took {execution_time:.2f}s"
                )
            logger.debug(
                f"{func.__name__} executed in {execution_time:.4f}s"
            )
    return wrapper

class PerformanceMonitor:
    """Monitor application performance metrics."""
    
    def __init__(self):
        self.metrics = {}
    
    def record(self, metric_name: str, value: float):
        """Record performance metric."""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(value)
    
    def get_average(self, metric_name: str) -> float:
        """Get average metric value."""
        if metric_name not in self.metrics or not self.metrics[metric_name]:
            return 0.0
        values = self.metrics[metric_name]
        return sum(values) / len(values)
    
    def get_max(self, metric_name: str) -> float:
        """Get max metric value."""
        if metric_name not in self.metrics or not self.metrics[metric_name]:
            return 0.0
        return max(self.metrics[metric_name])
    
    def clear(self):
        """Clear all metrics."""
        self.metrics.clear()

performance_monitor = PerformanceMonitor()
