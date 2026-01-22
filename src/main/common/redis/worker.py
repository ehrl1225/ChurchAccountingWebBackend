from redis import Redis
from rq import Queue, SpawnWorker

from common.env import settings

if __name__ == '__main__':
    connection = Redis.from_url(settings.get_redis_url())
    listen = ['default']
    queues = [Queue(name, connection=connection) for name in listen]
    worker = SpawnWorker(queues, connection=connection)
    worker.work()
