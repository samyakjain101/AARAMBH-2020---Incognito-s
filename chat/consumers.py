import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat
from django.contrib.auth.models import User
from profiles.models import Profile

# docker run -p 6379:6379 -d redis:5

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': '{} is online'.format(self.scope['user'].username),
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': '{} is offline'.format(self.scope['user'].username)
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'message' in text_data_json:
            message = text_data_json['message']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'author': self.scope['user'].username,
                }
            )


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        if 'author' in event:
            author = event['author']
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'author' : author,
            }))
        else:
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message
            }))

        