import json
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView ,DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from chat.models import ChatRoom
from chat.serializers import *
from .models import *
from users.models import Instructor
from rest_framework.authtoken.models import Token
from django.http.response import JsonResponse
from django.core.exceptions import PermissionDenied


class NotificationManager(CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView):

    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        
    def destroy(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        inbox, created = Inbox.objects.get_or_create(inbox_owner=instructor)
        inbox.save()
        for message in inbox.messages.all():
            inbox.messages.remove(message)
        inbox.save()
        return Response({'message' : 'success'})
    
    def list(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        inbox, created = Inbox.objects.get_or_create(inbox_owner=instructor)
        inbox.save()
        return Response(InboxSerializer(inbox).data)




class ManageCourseMessage(CreateAPIView, UpdateAPIView, DestroyAPIView):
    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.POST))
        except Exception as e:
            pass
        
class CreateChatRoom(CreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            instructor = Instructor.objects.get(user=Token.objects.get(key=request.headers['Authorization']).user)
        except Exception as e:
            raise PermissionDenied
        data = json.loads(request.body)
        chat_participant_2 = Instructor.objects.get(id=data[['chat_participant_2']])
        chat_room = ChatRoom.objects.create()
        chat_room.save()
        chat_room.chat_room_participants.add(instructor)
        chat_room.chat_room_participants.add(chat_participant_2)
        return JsonResponse({'chat_room_id' : chat_room.id })