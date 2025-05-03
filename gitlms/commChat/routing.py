# commChat/routing.py
from django.urls import path
from .consumers import CommChatConsumer

websocket_urlpatterns = [
   path("ws/commChat/<int:ins_id>", CommChatConsumer.as_asgi()),  # Include trailing slash
]
