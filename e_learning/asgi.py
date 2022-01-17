import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_learning.settings')

django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack

import courses.routing as routing
import chat.routing as chat_routing



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    'websocket' : AuthMiddlewareStack(
        URLRouter(
            #routing.websocket_urlpatterns,
            chat_routing.websocket_urlpatterns
        )
    )
})