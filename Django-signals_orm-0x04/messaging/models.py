from django.db import models
from django.contrib.auth import get_user_model
import uuid
from .managers import UnreadMessagesManager


User = get_user_model() # This will use the custom user model of the main project (messaging_app)





class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    edited = models.BooleanField(default=False) # track if message has been edited
    edited_at = models.DateTimeField(null=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edited_messages', null=True)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE) # self-referential relationship for threaded replies (like WhatsApp replies)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager() # default manager
    unread_messages = UnreadMessagesManager() # custom manager

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email} to {self.receiver.email}"


class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} | Read: {self.is_read}"


class MessageHistory(models.Model):
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history for message {self.message.message_id}"

