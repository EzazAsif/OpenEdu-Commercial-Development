from django.urls import re_path
from .consumers import CommChatConsumer

websocket_urlpatterns = [
    re_path(r"^ws/commChat/(?P<ins_id>\d+)$", CommChatConsumer.as_asgi()),  # Correct regex for capturing ins_id
]
