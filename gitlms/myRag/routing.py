# notifications/routing.py
from django.urls import path
from .consumers import RagConsumer

websocket_urlpatterns = [
    path("ws/tutorai/", RagConsumer.as_asgi()),
]