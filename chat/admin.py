from django.contrib import admin
from .models import Chat, Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    search_fields = ("participants__username",)
    filter_horizontal = ("participants",)  # nice widget for ManyToMany

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "sender", "content", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("content", "sender__username")
