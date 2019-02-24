from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
import json
import hashlib
from slackclient import SlackClient

#For when you don't have redis; You can only see your own chat.
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
        
#     async def disconnect(self, close_code):
#         print(close_code)
#         pass
        
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         user = text_data_json['user']
#         message = text_data_json['message']
#         print(user, message)
#         await self.send(text_data=json.dumps({'user': user, 'message': message}))

   
#For when you do have redis; You can see everyone's chat.
class ChatConsumer(AsyncWebsocketConsumer):
    def send_to_slack(self, user, message):
        print("+++++++++++++++++++++++ room grouup name++++++++++++++++"  + self.room_group_name)
        room = ScrumChatRoom.objects.get(hash=self.room_group_name)
        print("+++++++++++++++++++++++room send to slack++++++++++++++++")
        print(room)        
        try:
            slack = room.scrumslack_set.filter(room=room).first()  
            if slack is not None and self.slack_username != "empty":
                user = self.slack_username 
            elif slack is None:
                print("=======================No slack installed yet========================")
                return
        except ScrumSlack.DoesNotExist:
            return
        print("+++++++++++++++++++++++ACCESS TOKEN++++++++++++++++")
        print(slack)
        print(self.slack_username)
        print(slack.channel_id)
        sc = SlackClient(slack.bot_access_token )
        print("=====================USERNAME====================" + self.slack_username)
        if user == 'SERVER INFO':
            as_user = True
        else:
            as_user = False
        sc.api_call(
          "chat.postMessage",
          channel=slack.channel_id,
          text=message,
          username=user,
          as_user = as_user
        )
        print("After call")
        return

    def getRecentMessages(self):
        messages = []
        for message in self.room_object.scrumchatmessage_set.filter(room_id=self.room_object.id).order_by('-pk')[:30]:
            messages.insert(0, {'user': message.user, 'message': message.message})
        # del messages[-1]
        return messages

    def getOrCreateRoom(self):
        room = ScrumChatRoom.objects.filter(hash=self.room_group_name)
        print(room)
        room_count = self.getCount(room)
        if room_count == 0:
            new_room = self.generate_room(self.identity, self.room_group_name)
            self.generate_message(new_room, 'SERVER INFO', '=== This is the beginning of the chatroom history. ===')
            self.room_object = new_room
        else:
            self.room_object = self.firstObject(room)        
        return

    def getCount(self, object):
        return object.count()

    def firstObject(self, object):
        return object[0]

    def generate_room(self, this_name, this_hash):
        new_room = ScrumChatRoom(name=this_name, hash=this_hash)
        new_room.save()
        return new_room

    def generate_message(self, this_room, this_user, this_message):
        new_message = ScrumChatMessage(room=this_room, user=this_user, message=this_message)
        new_message.save()

    async def connect(self):
        self.room_group_name = hashlib.sha256(b'._global_chat_.').hexdigest()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'user': 'SERVER INFO', 'message': self.user + ' has left.'})
        await database_sync_to_async(self.generate_message)(self.room_object, 'SERVER INFO', str(self.user + ' has left.'))
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.user = text_data_json['user']
        self.slack_username = text_data_json['slack_username']
        message = text_data_json['message']
        print("Received Goal ID " + text_data_json['goal_id'])
        
        self.identity = text_data_json['goal_id']
        
        if message[:6] == '!join ':
            print("IDENTITY =============================" + self.identity)
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            self.room_group_name = hashlib.sha256(self.identity.encode('UTF-8')).hexdigest() 
            print("========ROOM GROUP NAME=========" + self.room_group_name)
            self.getOrCreateRoom()
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'user': 'SERVER INFO', 'message': self.user + ' has joined.'})
            # await database_sync_to_async(self.generate_message)(self.room_object, 'SERVER INFO', str(self.user + ' has joined.'))
            messages = await database_sync_to_async(self.getRecentMessages)()

                
            await self.send(text_data=json.dumps({'messages': messages}))
           

        elif self.identity[:9] == 'main_chat' and self.room_group_name != hashlib.sha256(self.identity.encode('UTF-8')).hexdigest():
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            self.room_group_name = hashlib.sha256(self.identity.encode('UTF-8')).hexdigest() 
            self.getOrCreateRoom()
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'user': 'SERVER INFO', 'message': self.user + ' has joined.'})
            # await database_sync_to_async(self.generate_message)(self.room_object, 'SERVER INFO', str(self.user + ' has joined.'))
            messages = await database_sync_to_async(self.getRecentMessages)()                    
            await self.send(text_data=json.dumps({'messages': messages}))
                

        elif message[:5] == '!goal' and self.room_group_name != 'chat_%s' % self.identity:    
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)            
            self.room_group_name = hashlib.sha256(self.identity.encode('UTF-8')).hexdigest()
            self.getOrCreateRoom()
            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'user': 'SERVER INFO', 'message': self.user + ' has joined.'})
            # await database_sync_to_async(self.generate_message)(self.room_object, 'SERVER INFO', str(self.user + ' has joined.'))
            messages = await database_sync_to_async(self.getRecentMessages)()
            await self.send(text_data=json.dumps({'messages': messages}))

        else:
            if self.identity[:9] == 'main_chat':
                self.send_to_slack(self.user,message)
            await self.channel_layer.group_send(self.room_group_name, {'type': 'chat_message', 'user': self.user, 'message': message})
            await database_sync_to_async(self.generate_message)(self.room_object, self.user, message)

    async def chat_message(self, event):
        user = event['user']
        message = event['message']
        await self.send(text_data=json.dumps({'user': user, 'message': message}))  
























