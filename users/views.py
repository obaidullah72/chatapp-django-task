from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# 👇 frontend profile page (HTML)
@login_required
def profile_page(request):
    return render(request, "users/profile.html", {"user": request.user})
