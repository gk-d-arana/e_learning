from django.urls import path
from .views import *


urlpatterns = [
    path('manage_course_message/', ManageCourseMessage.as_view()),
    path('create_chat_room/', CreateChatRoom.as_view()),
    path('notifications_manager/', NotificationManager.as_view()),
]
