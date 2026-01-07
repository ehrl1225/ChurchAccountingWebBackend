from typing import Optional
from fastapi import HTTPException, status
from redis.asyncio import Redis, ConnectionPool

from common.env import settings


class RedisClient:
    _pool: Optional[ConnectionPool] = None
    _client: Optional[Redis] = None

    @classmethod
    async def init(cls):
        cls._pool = ConnectionPool.from_url(url=settings.profile_config.REDIS_URL, encoding="utf-8", decode_responses=True)
        cls._client = Redis(connection_pool=cls._pool)

    @classmethod
    def get_client(cls) -> Redis:
        if not cls._client:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()
        if cls._pool:
            await cls._pool.disconnect(inuse_connections=True)

async def get_redis() -> Redis:
    return RedisClient.get_client()