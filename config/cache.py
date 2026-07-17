import redis
import json
import pickle
import logging
from typing import Any, Optional
from config.settings import get_settings
from functools import wraps

logger = logging.getLogger(__name__)
settings = get_settings()

class RedisCache:
    """Redis cache manager for application-wide caching."""
    
    def __init__(self):
        try:
            self.client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=False,
                socket_connect_timeout=5,
                socket_keepalive=True,
            )
            self.client.ping()
            logger.info("Connected to Redis cache")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            self.client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.client:
            return None
        try:
            value = self.client.get(key)
            if value:
                return pickle.loads(value)
        except Exception as e:
            logger.error(f"Cache get error for {key}: {e}")
        return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache."""
        if not self.client:
            return False
        try:
            ttl = ttl or settings.REDIS_CACHE_TTL
            self.client.setex(key, ttl, pickle.dumps(value))
            return True
        except Exception as e:
            logger.error(f"Cache set error for {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.client:
            return False
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete error for {key}: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache."""
        if not self.client:
            return False
        try:
            self.client.flushdb()
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    def cache_decorator(self, ttl: int = None):
        """Decorator for caching function results."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key from function name and arguments
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                
                # Try to get from cache
                cached = self.get(cache_key)
                if cached is not None:
                    logger.debug(f"Cache hit for {cache_key}")
                    return cached
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            return wrapper
        return decorator

# Global cache instance
cache = RedisCache()
