import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        try:
            self.user_id = self.scope['user'].id
            print(self.user_id)
            self.room_group_name = f"user_notifications_{self.user_id}"
            print(self.room_group_name)
            print(self.channel_name)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            print(f"connected to {self.channel_layer} ")
            await self.accept()
            
        except Exception as e:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Received data: {text_data}")

    async def send_notification(self, event):
        print("NotificationConsumer.send_notification triggered!")
        notification = event['notification']
        await self.send(text_data=json.dumps({
        'notification': notification
    }))

