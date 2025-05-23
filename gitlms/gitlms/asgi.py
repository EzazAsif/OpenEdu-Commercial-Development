import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notifications.routing import websocket_urlpatterns as notifications_urlpatterns  # Import WebSocket routing for notifications
from commChat.routing import websocket_urlpatterns as commchat_urlpatterns  # Import WebSocket routing for commChat
from myRag.routing import websocket_urlpatterns as myRag_urlpatterns
from commChat.consumers import *
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gitlms.settings')



application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # For HTTP requests
    "websocket": AuthMiddlewareStack(  # For WebSocket requests
        URLRouter(
            commchat_urlpatterns + notifications_urlpatterns +myRag_urlpatterns # Combine both WebSocket URL patterns
        )
    ),
})
