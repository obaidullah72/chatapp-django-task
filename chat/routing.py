# chat/routing.py
from django.urls import re_path
from . import consumers
from .middleware import JWTAuthMiddleware

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<chat_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
]