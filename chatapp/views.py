# chatapp/views.py
from django.shortcuts import render
from chat.models import Chat

def home(request):
    chats = Chat.objects.all()  # or filter by request.user
    return render(request, "home.html", {"chats": chats})
