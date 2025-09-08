from rest_framework import generics, permissions
from .models import Chat, Message
from .serializers import ChatSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .utils import is_user_online   # 👈 import your helper function

User = get_user_model()


# ✅ DRF API for listing chats
class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)


@login_required
def chat_list_page(request):
    chats = Chat.objects.filter(participants=request.user)

    for chat in chats:
        other_user = chat.participants.exclude(id=request.user.id).first()
        chat.other_user = other_user
        chat.is_online = is_user_online(other_user.id) if other_user else False

    return render(request, "chat_list.html", {"chats": chats})

# ✅ API for fetching messages
@login_required
def chat_messages_api(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    messages = chat.messages.all().values(
        "id", "sender__username", "content", "timestamp"
    )
    return JsonResponse(list(messages), safe=False)


@login_required
def chat_page(request, chat_id=None):
    chat = None
    messages = []
    if chat_id:
        chat = Chat.objects.filter(id=chat_id).first()
        if chat and request.user in chat.participants.all():
            messages = chat.messages.all()
        else:
            # Instead of 404, just show empty chat
            chat = None
            messages = []
    
    users = User.objects.exclude(id=request.user.id)

    # add online status here too
    users_with_status = [
        {"id": u.id, "username": u.username, "is_online": is_user_online(u.id)}
        for u in users
    ]

    return render(request, "chat_page.html", {
        "chat": chat,
        "users": users_with_status,
        "messages": messages,
    })


# ✅ Start chat with specific user
@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    chat_qs = Chat.objects.filter(participants=request.user).filter(participants=other_user)

    if chat_qs.exists():
        chat = chat_qs.first()
    else:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)

    users = User.objects.exclude(id=request.user.id)

    # add online status for dropdown users
    users_with_status = [
        {"id": u.id, "username": u.username, "is_online": is_user_online(u.id)}
        for u in users
    ]

    messages = chat.messages.all()

    return render(request, "chat_page.html", {
        "chat": chat,
        "user": request.user,
        "users": users_with_status,
        "messages": messages,
    })


# ✅ API: get or create chat with a user
@login_required
def get_or_create_chat(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)
        chat = Chat.objects.filter(participants=request.user).filter(participants=target_user).first()

        if not chat:
            chat = Chat.objects.create()
            chat.participants.add(request.user, target_user)

        return JsonResponse({'chat_id': chat.id})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ✅ API: get all messages for chat
@login_required
def chat_messages(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
        if not chat.participants.filter(id=request.user.id).exists():
            return JsonResponse({'error': 'Access denied'}, status=403)

        messages = Message.objects.filter(chat=chat).select_related('sender').order_by('timestamp')
        messages_data = [
            {
                'id': msg.id,
                'content': msg.content,
                'sender__username': msg.sender.username,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for msg in messages
        ]
        return JsonResponse(messages_data, safe=False)
    except Chat.DoesNotExist:
        return JsonResponse({'error': 'Chat not found'}, status=404)
