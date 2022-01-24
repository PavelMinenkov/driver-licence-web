import base64
import asyncio
from typing import Any
from abc import ABC, abstractmethod

import aioredis
from django.conf import settings


class ChannelIsClosedError(Exception):
    pass


class ReadWriteTimeoutError(Exception):
    pass


class CustomRedisChannel(ABC):

    MANGLING_PREFIX = 'driver-licence-'

    def __init__(self):
        self._name = None
        self._address = None
        self._is_closed = True
        self._redis = None
        self._channel = None

    def __del__(self):
        if not self._is_closed and self._redis:
            self._redis.close()

    @classmethod
    async def create(cls, name: str, live_timeout: int = None):
        inst = cls()
        name = cls.MANGLING_PREFIX + name
        inst._name = 'channel://' + name
        inst._is_closed = False
        redis_server = settings.REDIS_HOST
        if settings.REDIS_PORT:
            redis_server = f'{redis_server}:{settings.REDIS_PORT}'
        address = 'redis://%s/%s' % (redis_server, name)
        await inst.create_from_address(address, live_timeout)
        return inst

    async def close(self):
        if not self.is_closed:
            self._redis.close()
            self._is_closed = True

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def is_closed(self):
        return self._is_closed

    @abstractmethod
    async def create_from_address(self, address: str, live_timeout: int = None):
        raise NotImplemented

    @abstractmethod
    async def _setup(self):
        raise NotImplemented


class CustomReadOnlyChannel(CustomRedisChannel):

    @abstractmethod
    async def read(self, timeout) -> (bool, Any):
        raise NotImplemented


class CustomWriteOnlyChannel(CustomRedisChannel):

    @abstractmethod
    async def write(self, data) -> bool:
        raise NotImplemented


class RedisReadOnlyChannel(CustomReadOnlyChannel):

    def __init__(self):
        super().__init__()
        self.__queue = list()

    async def create_from_address(self, address: str, live_timeout: int = None):
        if not address.startswith('redis://'):
            raise RuntimeError('Unexpected address protocol')
        address = address[8:]
        redis_address, name = address.split('/')
        live_timeout = live_timeout or 5
        self._redis = await aioredis.create_redis('redis://%s' % redis_address, timeout=live_timeout)
        self._address = 'redis://%s/%s' % (redis_address, name)
        await self._setup()
        return self

    async def read(self, timeout) -> (bool, Any):
        if self._is_closed:
            raise ChannelIsClosedError
        try:
            while True:
                await asyncio.wait_for(self.__async_reader(), timeout=timeout)
                packet = self.__queue.pop(0)
                if packet['kind'] == 'data':
                    break
                elif packet['kind'] == 'close':
                    await self.close()
                    return False, None
        except asyncio.TimeoutError:
            raise ReadWriteTimeoutError
        if packet['is_bytes']:
            data = base64.b64decode(packet['body'])
        else:
            data = packet['body']
        return True, data

    async def close(self):
        await super().close()

    async def _setup(self):
        res = await self._redis.subscribe(self.name)
        self._channel = res[0]

    async def __async_reader(self):
        await self._channel.wait_message()
        msg = await self._channel.get_json()
        self.__queue.append(msg)


class RedisWriteOnlyChannel(CustomWriteOnlyChannel):

    async def create_from_address(self, address: str, live_timeout: int = None):
        if not address.startswith('redis://'):
            raise RuntimeError('Unexpected address protocol')
        address = address[8:]
        redis_address, name = address.split('/')
        live_timeout = live_timeout or 5
        self._redis = await aioredis.create_redis('redis://%s' % redis_address, timeout=live_timeout)
        self._address = 'redis://%s/%s' % (redis_address, name)
        await self._setup()
        return self

    async def write(self, data) -> bool:
        """Send data to recipients
        Return: True if almost one recipient received packet
        """
        if self._is_closed:
            raise ChannelIsClosedError
        is_bytes = isinstance(data, bytes)
        if is_bytes:
            data = base64.b64encode(data).decode("ascii")
        packet = dict(kind='data', body=data, is_bytes=is_bytes)
        counter = await self._redis.publish_json(self.name, packet)
        return counter > 0

    async def close(self, quietly: bool = False):
        if not self.is_closed:
            if not quietly:
                packet = dict(kind='close', body=None)
                await self._redis.publish_json(self.name, packet)
            await super().close()

    async def _setup(self):
        pass
