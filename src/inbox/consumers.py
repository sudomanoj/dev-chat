import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    This class is responsible for handling the chat websocket connections
    """
    async def connect(self):
        self.user = self.scope.get('user')
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.user_group_name = f'chat_{self.user.uuid}'
        
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        print(f'Added {self.channel_name} channel to {self.user_group_name} group')
        
        await self.accept()
        
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )
        
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        receiver = text_data_json.get('receiver')
        
        if not message or not receiver:
            return
        
        receiver_user = await self.get_user(receiver)
        if not receiver_user:
            return
        
        await self.save_message(message, receiver_user)
        
        await self.channel_layer.group_send(
            f'chat_{receiver}',
            {
                'type': 'chat.message',
                'message': message,
                'sender': str(self.user.uuid),
            }
        )
        print(f'Sent message to chat_{receiver}')
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))
        
    @database_sync_to_async
    def get_user(self, receiver):
        try:
            user = get_user_model().objects.get(uuid=receiver)
            return user
        except get_user_model().DoesNotExist:
            return None
        
    @database_sync_to_async
    @transaction.atomic
    def save_message(self, message, receiver_user):
        message_obj = Message(
            sender=self.user,
            receiver=receiver_user,
            message=message,
            created_at=timezone.now(),
        )
        message_obj.save()
        return message_obj
    
    
    
        
        
        
        