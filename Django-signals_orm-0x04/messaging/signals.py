from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, MessageHistory, Notification


User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created: # ensure signal only runs when a new message is created
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log message edits and save the old message content in MessageHistory
    """
    if not instance.pk: # if the message is new (never saved), no need to log edit
        return
    
    try:
        # fetch the old message content before it is updated
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.message_body != instance.message_body:
            # if the message content has changed, save the old content in MessageHistory
            MessageHistory.objects.create(message=old_message, old_content=old_message.message_body)
            # mark the message as edited
            instance.edited = True
            instance.edited_by = instance.sender
            instance.edited_at = instance.timestamp
    except Message.DoesNotExist:
        pass


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    Signal to cleanup user related data when a user is deleted
    """
    # delete all messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    # delete all notifications for the user
    Notification.objects.filter(user=instance).delete()
    # delete all message histories related to the user's sent messages
    MessageHistory.objects.filter(message__sender=instance).delete()
