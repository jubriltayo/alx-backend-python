from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer



class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    # List all messages for a specific conversation
    def list(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_id')
        if not conversation_id:
            return Response({'error': 'Conversation ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.queryset.filter(conversation__conversation_id=conversation_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Create a new message for an existing conversation
    @action(detail=True, methods=['post'])
    def send_message(self, request, *args, **kwargs):
        # get the conversation by ID
        conversation_id = self.kwargs.get('conversation_id')
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # validate and create message
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(conversation=conversation, sender=request.user) # link message to conversation
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

