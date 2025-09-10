from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from chat.models import Chat 
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib import messages

@login_required
def home(request):
    chats = Chat.objects.filter(participants=request.user)

    chats_with_status = [{"chat": chat} for chat in chats]

    return render(request, "home.html", {"chats": chats_with_status})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()          
            messages.success(request, "Your account has been created! Please log in.")       
            return redirect('login')     
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})