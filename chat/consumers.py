import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Messages
from django.contrib.auth import get_user_model
from .seralizers import queryset_to_dict
from django.db.models import Q

User = get_user_model()

def chatting(self, text_data_json):
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


def searching(self, data):
    query = data["query"]
    user_id = data["user_id"]
    print("izlandi", query)
    print("kim ", user_id)
    # Bazaga saqlash
    users = User.objects.filter(Q(first_name__icontains=query ) | Q(last_name__icontains=query) | Q(username__icontains=query))
    async_to_sync(self.channel_layer.group_send)(
        self.room_group_name, {
            "type": "chat.message", 
            "action_type": "search", 
            "message": queryset_to_dict(users),
            "user_id": user_id 
        }
    )


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        
        user_chat = self.room_group_name
        if "gr_" not in self.room_group_name:
            if user_chat.startswith("chat_"):
                try:
                    user = User.objects.get(id=self.room_name)
                    user.is_online = True
                    user.save()
                except:
                    pass
        
        self.room_group_name.replace("gr_", "")
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        user_chat = self.room_group_name
        if user_chat.startswith("chat_"):
            user_id = user_chat.split("chat_")[-1]
            try:
                user = User.objects.get(id=user_id)
                print(user, "online emas")
                user.is_online = False
                user.save()
            except:
                pass
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action_type = text_data_json["action_type"]
        if action_type == "chat":
            chatting(self, text_data_json)
        elif action_type == "search":
            searching(self, text_data_json)

    def chat_message(self, event):
        message = event["message"]
        user_id = event["user_id"] # Guruhdan kelgan ID ni olamiz

        # WebSocket orqali front-endga yuborish
        self.send(text_data=json.dumps({
            "message": message,
            "user_id": user_id # Front-end endi kimligini biladi
        }))