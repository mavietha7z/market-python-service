from app.core.cache import cache


def cacheGet(key: str):
    """Get value from cache"""
    return cache.get(key)


def cacheSet(key: str, value, ttl: int = 300):
    """Set value to cache with TTL"""
    cache[key] = value
