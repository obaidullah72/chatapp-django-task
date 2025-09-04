from django.urls import path
from .views import ChatListView, chat_list_page, chat_page, chat_messages_api

urlpatterns = [
    # API (REST)
    path("chats/", ChatListView.as_view(), name="chat-list"),

    # Frontend pages
    path("chat-list-page/", chat_list_page, name="chat-list-page"),
    path("chat/<int:chat_id>/", chat_page, name="chat-page"),

    # API (for AJAX loading messages inside chat-list-page)
    path("chat/<int:chat_id>/messages/", chat_messages_api, name="chat-messages-api"),
]
