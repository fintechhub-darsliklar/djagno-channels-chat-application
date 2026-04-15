from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Chat(models.Model):
    owner_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_chat")
    friend_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_chat")
    created_at = models.DateTimeField(auto_now_add=True)


class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chatting_messages")
    message = models.TextField()
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_messages")
    created_at = models.DateTimeField(auto_now_add=True)
    is_view = models.BooleanField(default=False)


