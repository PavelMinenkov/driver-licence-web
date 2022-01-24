import json
import asyncio
import logging

import sirius_sdk
from django.conf import settings

from main.redis import RedisWriteOnlyChannel
from main.authorization import login
from main.helpers import BrowserSession


class RedisLogger:

    def __init__(self, redis_pub_name: str):
        self.__redis_pub_name = redis_pub_name
        self.__redis = None

    async def __call__(self, *args, **kwargs):
        redis_channel = await self._get_redis_channel()
        data = kwargs
        print(json.dumps(data, indent=2, sort_keys=True))
        success = await redis_channel.write(
            {
                'type': 'logger',
                'data': kwargs
            }
        )
        if not success:
            logging.warning(f'Redis write-only channel [{redis_channel.address}] returned False, no recipients on read side')

    async def _get_redis_channel(self) -> RedisWriteOnlyChannel:
        if self.__redis is None:
            self.__redis = await RedisWriteOnlyChannel.create(self.__redis_pub_name)
        return self.__redis

    async def done(self, success: bool, comment: str = None):
        redis_channel = await self._get_redis_channel()
        await redis_channel.write(
            {
                'type': 'done',
                'data': {
                    'success': success,
                    'comment': comment
                }
            }
        )
        await redis_channel.close()


async def run(me: sirius_sdk.Pairwise.Me):
    endpoints = await sirius_sdk.endpoints()
    my_endpoint = [e for e in endpoints if e.routing_keys == []][0]
    # Load balance input event stream among multiple listeners
    if settings.PRODUCTION:
        group_id = 'PRODUCTION'
    else:
        group_id = 'DEBUG'
    listener = await sirius_sdk.subscribe(group_id)
    async for event in listener:
        if isinstance(event.message, sirius_sdk.aries_rfc.ConnRequest):
            is_exists = await BrowserSession.is_session_exists(event.recipient_verkey)
            if is_exists:
                asyncio.ensure_future(
                    establish_connection(
                        me=me,
                        my_endpoint=my_endpoint,
                        connection_key=event.recipient_verkey,
                        request=event.message
                    )
                )


async def establish_connection(
        me: sirius_sdk.Pairwise.Me,
        my_endpoint: sirius_sdk.Endpoint,
        connection_key: str,
        request: sirius_sdk.aries_rfc.ConnRequest
):
    logger = RedisLogger(connection_key)
    sm = sirius_sdk.aries_rfc.Inviter(
        me=me,
        connection_key=connection_key,
        my_endpoint=my_endpoint,
        logger=logger
    )
    success, p2p = await sm.create_connection(request)
    if success:
        await sirius_sdk.PairwiseList.ensure_exists(p2p)
        await login(connection_key, p2p)
        await logger.done(success=True, comment='Connection established')
    else:
        await logger.done(success=False, comment=sm.problem_report.explain if sm.problem_report else '')
