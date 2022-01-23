import json
import asyncio

import sirius_sdk

from main.redis import RedisWriteOnlyChannel


class Logger:

    def __init__(self, redis_pub_name: str):
        self.__redis_pub_name = redis_pub_name
        self.__redis = None

    async def __call__(self, *args, **kwargs):
        if self.__redis is not None:
            self.__redis = await RedisWriteOnlyChannel.create(self.__redis_pub_name)
        data = kwargs
        print(json.dumps(data, indent=2, sort_keys=True))
        await self.__redis.write(
            {
                'type': 'logger',
                'data': kwargs
            }
        )


async def run(me: sirius_sdk.Pairwise.Me):
    endpoints = await sirius_sdk.endpoints()
    my_endpoint = [e for e in endpoints if e.routing_keys == []][0]
    # Load balance input event stream among multiple listeners
    listener = await sirius_sdk.subscribe(group_id='MAIN')
    async for event in listener:
        if isinstance(event.message, sirius_sdk.aries_rfc.ConnRequest):
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
    sm = sirius_sdk.aries_rfc.Inviter(
        me=me,
        connection_key=connection_key,
        my_endpoint=my_endpoint,
        logger=Logger(connection_key)
    )
    success, p2p = await sm.create_connection(request)
    if success:
        await sirius_sdk.PairwiseList.ensure_exists(p2p)
