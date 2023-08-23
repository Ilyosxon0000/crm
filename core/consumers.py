# # consumers.py

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatRoomConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name=self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name=f'chat_{self.room_name}'
#         await self.channel_layer.group_add(self.room_group_name,self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.send(text_data=json.dumps({
#             'message': f"User has left the chat. (Code: {close_code})"
#         }))

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         # type1 = text_data_json['type']
#         message = text_data_json['message']
#         # name = text_data_json['name']
#         # agent = text_data_json.get('agent','')

#         # print('Receive',type1)

#         # if type1=='message':
#         #     await self.channel_layer.group_send(
#         #         self.room_group_name,{
#         #             'type':'chat_message',
#         #             'message':message,
#         #             'name':name,
#         #             'agent':agent,
#         #             'initials':message,
#         #         }
#         #     )
#         # await self.channel_layer.group_send(
#         #         self.room_group_name,json.dumps({
#         #             'message': message
#         #         }))
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Connect to the WebSocket
        await self.accept()
        
        # Get the room name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        
        # Add the user to the room's group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Remove the user from the room's group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        
        # Send the received message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username':username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username':username
        }))
