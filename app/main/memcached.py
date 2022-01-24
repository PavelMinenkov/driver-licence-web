import asyncio
import json
import logging
import aiomemcached
from typing import Optional, Any, Union, Dict

from django.conf import settings


class Memcached:

    __clients: Dict[int, aiomemcached.Client] = {}  # Map loop to client instance

    @classmethod
    async def get(cls, key: str, namespace: str = None) -> Any:
        cli = cls._get_client()
        if namespace:
            _key = f'{namespace}:{key}'
        else:
            _key = key
        try:
            value_b, _ = await cli.get(_key.encode())
        except Exception as e:
            return None
        value = value_b.decode() if value_b else None
        if value:
            descriptor = json.loads(value)
            typ = descriptor['type']
            value = descriptor['value']
            if typ == 'obj':
                value = json.loads(value)
            return value
        else:
            return None

    @classmethod
    async def set(cls, key: str, value: Union[dict, str, list], exp_time: int = None, namespace: str = None):
        cli = cls._get_client()
        if namespace:
            _key = f'{namespace}:{key}'
        else:
            _key = key
        _value = json.dumps({
            'type': 'obj' if type(value) is dict else 'str',
            'value': json.dumps(value) if type(value) is dict else value
        })
        try:
            await cli.set(_key.encode(), _value.encode(), exptime=exp_time or 0)
        except Exception:
            logging.exception('MemCached Set exception')

    @classmethod
    async def delete(cls, key: str, namespace: str = None):
        cli = cls._get_client()
        if namespace:
            _key = f'{namespace}:{key}'
        else:
            _key = key
        try:
            await cli.delete(_key.encode())
        except aiomemcached.ClientException:
            logging.exception('MemCached Delete exception')

    @classmethod
    async def touch(cls, key: str, exp_time: int, namespace: str = None):
        cli = cls._get_client()
        if namespace:
            _key = f'{namespace}:{key}'
        else:
            _key = key
        try:
            await cli.touch(_key.encode(), exp_time)
        except Exception:
            logging.exception('MemCached Touch exception')

    @classmethod
    def _get_client(cls) -> aiomemcached.Client:
        cur_loop = id(asyncio.get_event_loop())
        client = cls.__clients.get(cur_loop)
        if client is None:
            client = aiomemcached.Client(host=settings.MEMCACHED_HOST, pool_minsize=1)
            cls.__clients[cur_loop] = client
        return client

