import time
from app.utils.redis_client import redis_client

ROLE_LIMITS = {
    "free": (60, 60),
    "pro": (300, 60),
    "admin": (1000, 60)
}

def get_limit(path: str):
    for prefix, rule in LIMITS.items():
        if path.startswith(prefix):
            return rule
    return (60, 60)


def is_allowed(identifier: str, path: str,  role: str = "free") -> bool:
    if redis_client is None:
        return True  # fail-open

    try:
        limit, window = ROLE_LIMITS.get(role, ROLE_LIMITS["free"])

        key = f"rate:{identifier}:{path}"
        now = int(time.time())

        with redis_client.pipeline(transaction=True) as pipe:
            pipe.zremrangebyscore(key, 0, now - window)
            pipe.zcard(key)
            results = pipe.execute()

            count = results[1]
            if count >= limit:
                return False

            pipe.zadd(key, {now: now})
            pipe.expire(key, window)
            pipe.execute()

        return True

    except Exception:
        return True
