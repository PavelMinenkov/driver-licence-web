import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class QRNotifications(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__async_task = None

    async def connect(self):
        self.__async_task = asyncio.ensure_future(self.__listener())
        await self.accept()

    async def disconnect(self, *args, **kwargs):
        await super().disconnect(*args, **kwargs)
        if self.__async_task is not None:
            self.__async_task.cancel()

    async def __listener(self):
        # Listen for events from Cloud Agent
        counter = 1
        while True:
            await asyncio.sleep(1)
            await self.send_json(
                {
                    'counter': counter
                }
            )
            counter += 1
