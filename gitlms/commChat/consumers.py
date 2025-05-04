from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CommChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ins_id = self.scope['url_route']['kwargs']['ins_id']
        self.group_name = f"chat_{self.ins_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        sender = text_data_json.get('sender', '')
        timestamp = text_data_json.get('timestamp', '')

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'timestamp': timestamp,
            }
        )

    # Receive message from group
    async def chat_message(self, event):
        # Send full data to WebSocket
        print( event)
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))
