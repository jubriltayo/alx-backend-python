from rest_framework import serializers
from .models import User, Message, Conversation
from .auth import create_user


class UserSerializer(serializers.ModelSerializer):
    """
    A singular serializer that handles user registration
    (with password hashed) and user data
    """

    # accepts plain password for registration
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
            'password']
        read_only_fields = ['user_id', 'created_at']

    def create(self, validated_data):
        user = create_user(validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'conversation',
            'message_body',
            'sent_at']
        read_only_fields = ['message_id', 'sent_at']

    def create(self, validated_data):
        sender = self.context['request'].user
        message = Message.objects.create(sender=sender, **validated_data)
        return message

    def validate(self, data):
        # Ensure AnonymousUser doesnt by checks
        if self.context['request'].user.is_anonymous:
            raise serializers.ValidationError(
                "Authenticated required to send a message")
        return data


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        if not participants:
            raise serializers.ValidationError(
                "At least one participant is required to \
                create a conversation")

        # Prevent duplicate conversations
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation
