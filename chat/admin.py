from django.contrib import admin
from .models import Chat, Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "participants_list")
    search_fields = ("participants__username",)
    filter_horizontal = ("participants",)
    
    def participants_list(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    participants_list.short_description = "Participants"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_id", "sender_name", "short_content", "timestamp")
    list_filter = ("timestamp", "chat")
    search_fields = ("content", "sender__username")
    
    def chat_id(self, obj):
        return obj.chat.id
    chat_id.short_description = "Chat ID"
    
    def sender_name(self, obj):
        return obj.sender.username
    sender_name.short_description = "Sender"
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = "Content"