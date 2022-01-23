import json
import asyncio

import sirius_sdk
from django.conf import settings
from django.core.management.base import BaseCommand

from main.redis import RedisWriteOnlyChannel


class Command(BaseCommand):

    help = 'Run actors SSI logic'

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

    def handle(self, *args, **options):
        asyncio.get_event_loop().run_until_complete(self.run_ssi())

    async def run_ssi(self):
        async with sirius_sdk.context(**settings.GOV['SDK']):
            endpoints = await sirius_sdk.endpoints()
            my_endpoint = [e for e in endpoints if e.routing_keys == []][0]
            listener = await sirius_sdk.subscribe()
            async for event in listener:
                if isinstance(event.message, sirius_sdk.aries_rfc.ConnRequest):
                    asyncio.ensure_future(self.establish_connection(

                    ))

    @staticmethod
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
            logger=Command.Logger(connection_key)
        )
        success, p2p = await sm.create_connection(request)
        if success:
            await sirius_sdk.PairwiseList.ensure_exists(p2p)
