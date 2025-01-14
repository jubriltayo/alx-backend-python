from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from messaging.models import User, Message, Notification, MessageHistory, UnreadMessagesManager


class MessagingSignalTest(TestCase):
    def setUp(self):
        # create users
        self.user1 = User.objects.create(email="user1@example.com", username="user1")
        self.user2 = User.objects.create(email="user2@example.com", username="user2")

    def test_message_notification(self):
        # send message
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello, user2!")

        # check notifications
        notifications = Notification.objects.filter(user=self.user2)
        self.assertEqual(notifications.count(), 1)
        self.assertEqual(notifications.first().message, message)
        self.assertFalse(notifications.first().is_read)


class UserDeletionSignalTest(TestCase):
    def setUp(self):
        self.client = APIClient() # to bypass the complexities of authentication via its force_authenticate method since its view (delete endpoint) has authentication required

        # create users
        self.user = User.objects.create_user(email="user1@example.com", username="user1", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.user_id = self.user.user_id # reaffirming custom user_id not default id

        self.message = Message.objects.create(sender=self.user, receiver=self.user, content="Test message")
        Notification.objects.create(user=self.user, message=self.message)
        MessageHistory.objects.create(message=self.message, old_content="Original message content")

    def test_message_edit_logging(self):
        self.message.content = "Edited Message"
        self.message.save()

        self.assertEqual(MessageHistory.objects.count(), 1)
        history = MessageHistory.objects.first()
        self.assertEqual(history.old_content, "Original message content")
        self.assertTrue(self.message.edited)

    def test_delete_user_and_cleanup_related_data(self):
        # delete user
        url = reverse("user-delete-account") # dynamic rendering of url also equal to api/users/delete-account/
        response = self.client.delete(url)
        
        # Verify response
        self.assertEqual(response.status_code, 204)

        # check related data cleanup
        self.assertFalse(Message.objects.filter(sender=self.user_id).exists())
        self.assertFalse(Notification.objects.filter(user=self.user_id).exists())
        self.assertFalse(MessageHistory.objects.filter(message__sender=self.user_id).exists())


class UnreadMessagesManagerTest(TestCase):
    def setUp(self):
        # create users
        self.user1 = User.objects.create(email="user1@example.com", username="user1")
        self.user2 = User.objects.create(email="user2@example.com", username="user2")

        # create messages
        self.message1 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Unread message")
        self.message2 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Read message", read=True)

    def test_for_user_returns_unread_messages(self):
        unread_messages = Message.unread_messages.for_user(self.user2)
        self.assertEqual(unread_messages.count(), 1) # user2 has 1 unread message
        self.assertEqual(unread_messages.first().content, "Unread message")
