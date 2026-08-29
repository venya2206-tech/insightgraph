import redis.asyncio as aioredis
from app.core.config import get_settings

settings = get_settings()
_redis_client = None

async def get_redis():
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client

async def close_redis():
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None

async def test_redis_connection() -> bool:
    try:
        r = await get_redis()
        await r.ping()
        return True
    except Exception:
        return False
