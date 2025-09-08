from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from chat.models import Chat

@login_required
def home(request):
    chats = Chat.objects.filter(participants=request.user)

    chats_with_status = [{"chat": chat} for chat in chats]

    return render(request, "home.html", {"chats": chats_with_status})