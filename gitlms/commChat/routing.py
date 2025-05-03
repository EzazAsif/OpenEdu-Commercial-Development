# commChat/routing.py
from django.urls import re_path
from .consumers import CommChatConsumer

websocket_urlpatterns = [
    re_path(r"^ws/commChat/$", CommChatConsumer.as_asgi()),  # Include trailing slash
]
