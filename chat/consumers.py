from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from chat.serializers import MessageSerializer
from rest_framework.authtoken.models import Token
from users.models import Instructor
from .models import ChatRoom, Message


class ChatRoomConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def add_message_to_chat_room(self, message, message_from, message_to):
        message_from_user = Instructor.objects.get(id=message_from)
        message_to_user = Instructor.objects.get(id=message_to)
        message = Message.objects.create(
            message=message, message_from=message_from_user, 
            message_to=message_to_user
        )
        message.save()
        chat_room, created = ChatRoom.objects.get_or_create(id=self.room_group_name)
        chat_room.messages.add(message)
        chat_room.save()

    @database_sync_to_async
    def add_participants(self, instructor_id):
        chat_room, created = ChatRoom.objects.get_or_create(id=self.room_group_name)
        chat_room.chat_room_participants.add(Instructor.objects.get(id=instructor_id))

    
    @database_sync_to_async
    def get_chat_room(self):
        chat_room, created = ChatRoom.objects.get_or_create(id=self.room_group_name)
        return chat_room


    @database_sync_to_async
    def get_chat_room_data(self):
        chat_room, created = ChatRoom.objects.get_or_create(id=self.room_group_name)
        data = MessageSerializer(chat_room.messages, many=True).data
        return data


    async def connect(self):
        print(self.scope['url_route']['kwargs']['chat_room_id'])
        self.room_group_name = self.scope['url_route']['kwargs']['chat_room_id']
        self.chat_room = await self.get_chat_room()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        chat_room_data = await self.get_chat_room_data()
        
        await self.send_chat_room_data({
            'type' : 'send.chat.room.data',
            'data' : chat_room_data
        })
   
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('Disconnected')


    async def receive(self, text_data):  
        revieve_dict = json.loads(text_data)
        
        token = Token.objects.get(key=revieve_dict['token'])
        
        if token is not None:
            pass       
        print('yes', token)
        
        message = revieve_dict['message']
        message_from = revieve_dict['message_from_id']
        message_to = revieve_dict['message_to_id']
        
        await self.add_message_to_chat_room(message, message_from, message_to)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'send.message', 
                'message' : message,
                'message_from': message_from
            }
        ) 


    async def send_message(self, event):
        message = event['message']
        #message_from = event['message_from']
        await self.send(text_data=json.dumps({
            'message' : message,
            #'message_from': message_from
        }))

    async def send_chat_room_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({
            'data' : data
        }))