from django.urls import path
from .views import ChatListView, chat_list_page, chat_page 
from . import views

urlpatterns = [
    # API
    path("chats/", ChatListView.as_view(), name="chat-list"),

    # Frontend pages
    path("chat-list-page/", chat_list_page, name="chat-list-page"),
    path("chat/<int:chat_id>/", chat_page, name="chat-page"),
     path('profile/', views.profile_page, name='profile-page'),
]
