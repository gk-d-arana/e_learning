from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('chat_room/<slug:chat_room_id>/', consumers.ChatRoomConsumer.as_asgi())
] 
