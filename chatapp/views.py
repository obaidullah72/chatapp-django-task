from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from chat.models import Chat 
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

@login_required
def home(request):
    chats = Chat.objects.filter(participants=request.user)

    chats_with_status = [{"chat": chat} for chat in chats]

    return render(request, "home.html", {"chats": chats_with_status})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()          # creates the user
            login(request, user)        # log the user in immediately
            return redirect('home')     # redirect to home or chat page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})