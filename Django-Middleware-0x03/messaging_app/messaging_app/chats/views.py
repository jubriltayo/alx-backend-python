from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import MethodNotAllowed, AuthenticationFailed
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from .auth import create_user, generate_tokens_for_user, authenticate_user
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter


# Authentication views
class UserRegistrationView(APIView):
    """
    API endpoint to register users.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = create_user(serializer.validated_data)
            user_serializer = UserSerializer(user) # re-serialize the user to include the user_id
            return Response({
                "status": "success",
                "message": "User registered successfully",
                "data": {
                    "user": user_serializer.data,
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint to login users.
    """
    permission_classes = [permissions.AllowAny]

    def post (self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                "status": "error",
                "message": "Email and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = authenticate_user(email.lower(), password)
            tokens = generate_tokens_for_user(user)

            serializer = UserSerializer(user)
            
            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                    **tokens,
                    "user": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)



# API views
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Prevent creating users via this API
        return Response({
            "status": "error",
            "message": "User creation is not allowed via this endpoint. Please use the registration endpoint instead."
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({
                "status": "error",
                "message": "You do not have permission to view all users. Only admins can access this resource."
            }, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['delete'], url_path='delete-account')
    def delete_account(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({
            "status": "success",
            "message": "Your account has been deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Restrict conversations to those involving the authenticated user
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        # Customize the create response and include the creator as participant
        data = request.data.copy()
        participants = data.get('participants', [])

        # Ensure the creator is included in the participants list
        if str(request.user.user_id) not in participants:
            participants.append(str(request.user.user_id))
            data['participants'] = participants

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            conversation = serializer.save()
            return Response({
                "status": "success",
                "message": "Conversation created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Failed to create conversation",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        """
        Restrict messages to conversations involving the authenticated user.
        """
        user = self.request.user

        if not user.is_authenticated or isinstance(user, AnonymousUser):
            return Message.objects.none()
    
        # Filter messages by conversations the user is a participant of
        return Message.objects.filter(conversation__participants=user)

    # List all messages for a specific conversation
    def list(self, request, *args, **kwargs):
        """
        List all messages for a specific conversation.
        Supports filtering and pagination.
        """
        conversation_id = self.kwargs.get('conversation')
        
        # Filter messages by the specified conversation, if provided
        if conversation_id:
            queryset = self.get_queryset().filter(conversation__conversation_id=conversation_id)
        else:
            queryset = self.get_queryset()

        # Applying filtering and pagination
        filtered_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filtered_queryset)

        if paginated_queryset is not None:
            return self.get_paginated_response(paginated_queryset)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)

    # Create a new message
    @action(detail=False, methods=['post'])
    def send_message(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation or create a new one based on participants.
        """
        # conversation_id = request.data.get('conversation_id')
        participants = request.data.get('participants', [])
        message_data = request.data.get('message_body')

        if not participants:
                return Response({
                    "status": "error",
                    "message": "Participants are required"
                }, status=status.HTTP_400_BAD_REQUEST)

        if not message_data:
            return Response({
                "status": "error",
                "message": "Message body is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Ensure sender (request.user) is included in the participants list
        if request.user.user_id not in participants:
            participants.append(request.user.user_id)

        # Check for an existing conversation with the same participants
        conversation = (
            Conversation.objects
            .filter(participants__user_id__in=participants)
            .annotate(num_participants=Count('participants'))
            .filter(num_participants=len(participants))
            .distinct()
            .first()
        )

        # If no conversation exists, create a new one
        if not conversation:
            conversation_data = {'participants': participants}
            conversation_serializer = ConversationSerializer(data=conversation_data)
            if conversation_serializer.is_valid():
                conversation = conversation_serializer.save()
            else:
                return Response({
                    "status": "error",
                    "message": "Failed to create conversation",
                    "errors": conversation_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # create and save the message
        message_serializer = self.get_serializer(data={
            "message_body": message_data,
            "conversation": conversation.conversation_id,
            "sender": request.user.user_id
        })
        if message_serializer.is_valid():
            message_serializer.save()
            return Response(message_serializer.data, status=status.HTTP_201_CREATED)
        return Response(message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @method_decorator(cache_page(60))
    def unread_messages_view(self, request, *args, **kwargs):
        """
        API endpoint to get unread messages for the authenticated user.
        Cache for 60 seconds.
        """
        user = request.user

        if not user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=401)
        
        unread_messages = Message.unread_messages.for_user(user)
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
