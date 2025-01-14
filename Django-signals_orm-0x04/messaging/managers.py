from django.db import models


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        # return unread messages for a user
        return self.filter(receiver=user, read=False).only('content', 'sender', 'timestamp')