from rest_framework import generics, permissions
from .models import Chat
from .serializers import ChatSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User

class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)

@login_required
def chat_list_page(request):
    chats = Chat.objects.all()   # show all chats, not just user’s
    return render(request, "chat_list.html", {"chats": chats})


@login_required
def profile_page(request):
    return render(request, "profile.html", {"user": request.user}) 

# chat/views.py - UPDATE your chat_page function
@login_required
def chat_page(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    return render(request, "chat_page.html", {
        "chat": chat,
        "user": request.user,
    })