from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Message
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.cache import cache_page


@login_required
def delete_user(request):
    if request.method == 'DELETE':
        user = request.user
        user.delete()
        return redirect('home')
    return redirect('home')


def fetch_replies(message):
    replies = list(message.replies.select_related('sender').all())
    return [
        {
            "id": reply.id,
            "sender": reply.sender.username,
            "content": reply.content,
            "timestamp": reply.timestamp,
            "replies": fetch_replies(reply),
        }
        for reply in replies
    ]

@login_required
@cache_page(60)
def get_threaded_conversation(request, message_id):
    root_message = get_object_or_404(Message.objects.select_related('sender', 'receiver'), id=message_id)
    if root_message.recipient != request.user and root_message.sender != request.user:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    threaded_conversation = {
        "id": root_message.id,
        "sender": root_message.sender.username,
        "content": root_message.content,
        "timestamp": root_message.timestamp,
        "replies": fetch_replies(root_message),
    }
    return JsonResponse(threaded_conversation, safe=False)

@csrf_exempt
@login_required
def create_message(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        content = data.get("content")
        recipient_id = data.get("recipient_id")
        parent_message_id = data.get("parent_message_id")

        if not content or not recipient_id:
            return JsonResponse({"error": "Content and recipient are required"}, status=400)

        # Optional parent message for replies
        parent_message = None
        if parent_message_id:
            parent_message = get_object_or_404(Message, id=parent_message_id)

        message = Message.objects.create(
            sender=request.user,
            recipient_id=recipient_id,
            content=content,
            parent_message=parent_message,
        )
        return JsonResponse({"message": "Message created successfully", "id": message.id}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def get_user_conversations(request):
    messages = Message.objects.filter(
        recipient=request.user
    ).select_related('sender', 'parent_message')

    conversations = [
        {
            "id": message.id,
            "sender": message.sender.username,
            "content": message.content,
            "timestamp": message.timestamp,
            "parent_message_id": message.parent_message.id if message.parent_message else None,
        }
        for message in messages
    ]
    return JsonResponse(conversations, safe=False, status=200)

@login_required
def get_unread_messages(request):
    unread_messages = Message.unread.unread_for_user.filter(receiver=request.user).only('id', 'sender', 'receiver', 'content', 'timestamp')
    unread_messages = [
        {
            "id": message.id,
            "sender": message.sender.username,
            "content": message.content,
            "timestamp": message.timestamp,
        }
        for message in unread_messages
    ]
    return JsonResponse(unread_messages, safe=False, status=200)
