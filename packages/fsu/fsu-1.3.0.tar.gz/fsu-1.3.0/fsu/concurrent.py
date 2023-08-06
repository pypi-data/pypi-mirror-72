from collections import namedtuple
from contextlib import asynccontextmanager
from asyncio import sleep
from os import urandom

RedisLock = namedtuple("RedisLock", ["lock"])

def make_redis_lock(get_redis):
    redis = None

    async def get_redis_():
        nonlocal redis

        if redis is None:
            redis = await get_redis()

        return redis

    @asynccontextmanager
    async def lock(key, timeout = 60):
        r = await get_redis_()
        v = urandom(20)

        accuired = False

        while not accuired:
            accuired = await r.set(key, v, expire=timeout, exist="SET_IF_NOT_EXIST")

            if not accuired:
                await sleep(1)

        try:
            yield
        finally:
            await r.eval("""
                if redis.call("get", KEYS[1]) == ARGV[1]
                then
                    return redis.call("del", KEYS[1])
                else
                    return 0
                end
            """, [key], [v])

    redis_lock = RedisLock(
        lock = lock,
    )

    return redis_lock
