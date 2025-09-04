from rest_framework import generics, permissions
from .models import Chat
from .serializers import ChatSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model 
from django.http import JsonResponse
from .models import Chat, Message  

User = get_user_model()  # ✅ Get CustomUser safely


class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)

@login_required
def chat_list_page(request):
    chats = Chat.objects.all()
    return render(request, "chat_list.html", {"chats": chats})


@login_required
def chat_messages_api(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    messages = chat.messages.all().values(
        "id", "sender__username", "content", "timestamp"
    )
    return JsonResponse(list(messages), safe=False)

@login_required
def chat_page(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # ✅ get all messages for this chat
    messages = chat.messages.all()  # because of related_name="messages"

    users = User.objects.exclude(id=request.user.id)
    return render(request, "chat_page.html", {
        "chat": chat,
        "user": request.user,
        "users": users,
        "messages": messages,  # ✅ pass messages to template
    })