from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@login_required
def profile_page(request):
    return render(request, "users/profile.html", {"user": request.user})


# ✅ Custom Login
class CustomLoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})


# ✅ Custom Logout
class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("home")
