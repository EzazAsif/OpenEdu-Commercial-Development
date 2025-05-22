from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
import json
import uuid

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        sender = text_data_json.get('sender', '')
        timestamp = text_data_json.get('timestamp', '')

        # ✅ Cache each message with its own expiry
        unique_id = uuid.uuid4().hex
        message_key = f"{self.group_name}:{unique_id}"  # e.g., chat_123:abc123

        cache.set(message_key, text_data, timeout=3600)  # 1 hour expiry

        # ✅ Maintain an index of all message keys for the group
        index_key = f"{self.group_name}:index"
        existing_keys = cache.get(index_key, [])
        existing_keys.append(message_key)
        cache.set(index_key, existing_keys, timeout=3600)

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

    async def chat_message(self, event):
        print("Group message event:", event)
        await self.send(text_data=json.dumps({
            'id':event['id'],
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))
