import time
from app.utils.redis_client import redis_client

ENDPOINT_LIMITS = {
    "/auth/login": 10,
    "/keys/create": 5,
    "/protected/data": 60
}

WINDOW_SIZE = 60

def is_allowed(identifier: str, path: str = "") -> bool:
    if redis_client is None:
        return True

    limit = ENDPOINT_LIMITS.get(path, 100)

    try:
        key = f"rate:{identifier}:{path}"
        now = int(time.time())

        redis_client.zremrangebyscore(key, 0, now - WINDOW_SIZE)
        count = redis_client.zcard(key)

        if count >= limit:
            return False

        redis_client.zadd(key, {now: now})
        redis_client.expire(key, WINDOW_SIZE)
        return True
    except Exception:
        return True

