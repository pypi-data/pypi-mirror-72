import redis
from os import getenv
from time import sleep


class RedisDB:
    __slots__ = ['redis']

    __redis_host = getenv('REDIS_HOST') or '0.0.0.0'
    __redis_password = getenv('REDIS_PASSWORD') or 'redispass'
    __redis_port = getenv('REDIS_PORT') or 6379

    def __init__(self):
        self.__connect()

    def __connect(self):
        try:
            self.redis = redis.Redis(host=self.__redis_host, password=self.__redis_password, port=self.__redis_port)

        except Exception as ex:
            print(ex, flush=True)
            self.__reconect()

    def __reconect(self):
        try:
            if not self.redis:
                self.__connect()

        except Exception:
            sleep(3)
            self.__reconect()
