from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MeetingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['meeting_id']
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('Disconnected')


    async def receive(self, text_data):  
        print(text_data)
        revieve_dict = json.loads(text_data)
        message = revieve_dict['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'send.message', 
                'message' : message
            }
        ) 


    async def send_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message' : message
        }))