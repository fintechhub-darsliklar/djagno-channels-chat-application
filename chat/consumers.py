import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Messages
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = text_data_json["user_id"]
        chat_id = text_data_json["chat_id"]
        
        # Bazaga saqlash
        chat = Chat.objects.get(id=chat_id)
        sender = User.objects.get(id=user_id)
        Messages.objects.create(
            chat=chat,
            sender_user=sender,
            message=message
        )
        
        # Xabarni guruhga yuborish (user_id ni ham qo'shamiz!)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat.message", 
                "message": message,
                "user_id": user_id  # BU JUDA MUHIM!
            }
        )

    def chat_message(self, event):
        message = event["message"]
        user_id = event["user_id"] # Guruhdan kelgan ID ni olamiz

        # WebSocket orqali front-endga yuborish
        self.send(text_data=json.dumps({
            "message": message,
            "user_id": user_id # Front-end endi kimligini biladi
        }))