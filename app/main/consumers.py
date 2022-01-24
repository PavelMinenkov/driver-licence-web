import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from main.redis import RedisReadOnlyChannel


class QRNotifications(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__async_task = None
        self.__connection_key = None

    def __del__(self):
        if self.__async_task and not self.__async_task.done():
            self.__async_task.cancel()

    async def connect(self):
        self.__async_task = asyncio.ensure_future(self.__listener())
        self.__connection_key = self.scope.get('url_route', {}).get('kwargs', {}).get('connection_key')
        await self.accept()

    async def disconnect(self, *args, **kwargs):
        await super().disconnect(*args, **kwargs)
        if self.__async_task is not None:
            self.__async_task.cancel()

    async def __listener(self):
        # Listen for events from Cloud Agent routed to Redis pub/sub
        redis_channel = await RedisReadOnlyChannel.create(name=self.__connection_key)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(f'Read-only redis: start to read address [{redis_channel.address}]')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        while True:
            success, data = await redis_channel.read(timeout=None)
            if success:
                await self.send_json(data)
            else:
                await self.close()
                return
