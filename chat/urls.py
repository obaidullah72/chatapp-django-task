from django.urls import path
from .views import (
    ChatListView, 
    chat_list_page, 
    chat_page, 
    get_or_create_chat,
    chat_messages
)

urlpatterns = [
    # API (REST)
    path("chats/", ChatListView.as_view(), name="chat-list"),

    # Frontend pages
    path("chat-list-page/", chat_list_page, name="chat-list-page"),
    path("", chat_page, name="chat-lobby"),              # /chat/ → chat lobby
    path("<int:chat_id>/", chat_page, name="chat-detail"),  # /chat/10/ → specific chat

    # AJAX / API endpoints
    path("get_or_create_chat/<int:user_id>/", get_or_create_chat, name="get_or_create_chat"),
    path("<int:chat_id>/messages/", chat_messages, name="chat_messages"),
]
