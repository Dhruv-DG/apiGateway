from app.core.config import settings
import redis

try:
    redis_client = redis.Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True
    )
    redis_client.ping()
except Exception:
    redis_client = None
