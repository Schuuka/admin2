import os
import redis
from functools import wraps

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)


def cache_result(ttl=60):
    """Decorateur de cache (pattern cache-aside, repris du TP8)."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            key = f"{f.__name__}:{str(args)}:{str(kwargs)}"
            try:
                cached_value = redis_client.get(key)
            except redis.RedisError as e:
                print(f"[cache] indisponible, appel direct : {e}", flush=True)
                return f(*args, **kwargs)

            if cached_value:
                print(f"[cache] hit {key}", flush=True)
                return cached_value.decode("utf-8")

            print(f"[cache] miss {key}", flush=True)
            result = f(*args, **kwargs)
            try:
                redis_client.setex(key, ttl, result)
            except redis.RedisError:
                pass
            return result
        return decorated_function
    return decorator
