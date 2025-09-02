from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
from django.shortcuts import render

# Create your views here.
