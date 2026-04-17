from django.db import models
from users.models import CustomUser as User

# Create your models here.


class Chat(models.Model):
    owner_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_chat")
    friend_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_chat")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_opponent(self, user):
        return self.friend_user if self.owner_user == user else self.owner_user


class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chatting_messages")
    message = models.TextField()
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_messages")
    created_at = models.DateTimeField(auto_now_add=True)
    is_view = models.BooleanField(default=False)


