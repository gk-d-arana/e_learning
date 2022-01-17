from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('meeting/<slug:meeting_id>/', consumers.MeetingConsumer.as_asgi())
] 