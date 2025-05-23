from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
import json
import uuid
from .qdrant_helper import search_qdrant
from .groq import answer_with_groq_using_qdrant_context
# Make sure your `model` and `client` are imported or initialized here
# from yourmodule import model, client

class RagConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user_id = self.scope['user'].id
            self.room_group_name = f"tutorai_{self.user_id}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print(f"User {self.user_id} connected to {self.room_group_name}")
        except Exception as e:
            print("Connection error:", e)
            await self.close()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            msg_type = data.get("type")

            if msg_type == "text":
                message = data.get("message")
                print(f"Received text message: {message}")

                # Call Qdrant search function
                results = search_qdrant(collection_name="lecture_materials", query=message, top_k=5)
                print("Qdrant search results:")
                for result in results:
                    print(result)

                # Send response back to user
                await self.send(text_data=json.dumps({
                    "type": "text",
                    "response": f"Search completed. Found {len(results)} results."
                }))

            elif msg_type == "image":
                image_data_url = data.get("dataURL")
                print("Received image (base64 Data URL)")
                # Optionally decode and save image if needed
            

            else:
                await self.send(text_data=json.dumps({
                    "error": "Unsupported message type"
                }))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "error": "Invalid JSON"
            }))
        except Exception as e:
            print("Error processing message:", e)
            await self.send(text_data=json.dumps({
                "error": str(e)
            }))
