from rest_framework.permissions import BasePermission
from .models import Conversation


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participant of a conversation to access it
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False  # Deny access for unauthenticated users
        if isinstance(obj, Conversation):
            # Check if user is a participant in the conversation
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation_id'):
            # For Message objects, check the conversation's participants
            return request.user in obj.conversation_id.participants.all()
        return False
