# consumers.py

import asyncio
import time

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


class ChartWebSocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope['user'].is_authenticated:
            await self.accept()
        else:
            await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        if self.scope['client']:
            # Send data when the client connects
            try:
                # Keep sending data until the client disconnects
                while True:
                    # Check if the client is still connected
                    if not self.scope['client']:
                        break

                    # Send your desired data to the client
                    data = "Hello, client!"
                    print(self.scope['client'])
                    await self.send(data)

                    # Wait for a while before sending the next data
                    time.sleep(1)
            except asyncio.CancelledError:
                # Handle the client disconnection
                print("Client disconnected")

    async def disconnect(self, code):
        if self.scope['user'].is_authenticated:
            self.scope['user'].update_uuid()
        self.scope['client'] = None
        await self.close()
