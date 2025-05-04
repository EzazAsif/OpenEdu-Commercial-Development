# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CommChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ins_id = self.scope['url_route']['kwargs']['ins_id']
        self.group_name = f"chat_{self.ins_id}"

        # Join the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
