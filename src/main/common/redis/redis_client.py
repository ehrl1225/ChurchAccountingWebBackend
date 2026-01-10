from typing import Optional
from fastapi import HTTPException, status
from redis.asyncio import Redis as AsyncRedis, ConnectionPool
from redis import Redis as SyncRedis
from rq import Queue

from common.env import settings


class RedisClient:
    _pool: Optional[ConnectionPool] = None
    _client: Optional[AsyncRedis] = None
    _queue: Optional[Queue] = None

    @classmethod
    async def init(cls):
        cls._pool = ConnectionPool.from_url(
            url=settings.profile_config.REDIS_URL,
            encoding="utf-8",
            decode_responses=True)
        cls._client = AsyncRedis(connection_pool=cls._pool)
        cls._sync_client = SyncRedis.from_url(url=settings.profile_config.REDIS_URL, encoding="utf-8", decode_responses=True)
        cls._queue = Queue(connection=cls._sync_client)

    @classmethod
    def get_client(cls) -> AsyncRedis:
        if not cls._client:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return cls._client

    @classmethod
    def get_queue(cls) -> Queue:
        if not cls._queue:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return cls._queue

    @classmethod
    async def close(cls):
        if cls._sync_client:
            cls._sync_client.close()
        if cls._client:
            await cls._client.close()
        if cls._pool:
            await cls._pool.disconnect(inuse_connections=True)

async def get_redis() -> AsyncRedis:
    return RedisClient.get_client()

async def get_queue() -> Queue:
    return RedisClient.get_queue()