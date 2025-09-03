from django.shortcuts import redirect

def home(request):
    return redirect("chat-list-page")  # make sure "chat-list-page" exists in chat/urls.py