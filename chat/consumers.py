import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Chat, Message

User = get_user_model()

# 🔹 Global in-memory store for online users (not shared across processes)
ONLINE_USERS = set()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        self.user = self.scope.get('user', AnonymousUser())

        if self.user.is_anonymous:
            await self.close()
            return

        # ✅ Mark user online
        ONLINE_USERS.add(self.user.id)
        print(f"✅ {self.user.username} is now ONLINE. Online users: {ONLINE_USERS}")

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if self.user and not isinstance(self.user, AnonymousUser):
            # ✅ Mark user offline
            if self.user.id in ONLINE_USERS:
                ONLINE_USERS.remove(self.user.id)
                print(f"❌ {self.user.username} went OFFLINE. Online users: {ONLINE_USERS}")

        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_content = data.get("message", "").strip()

            if not message_content:
                return

            saved_message = await self.save_message(message_content)

            if saved_message:
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        "type": "chat_message",
                        "message": saved_message.content,
                        "user": saved_message.sender.username,
                        "timestamp": saved_message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    },
                )
        except Exception as e:
            print(f"❌ Error in receive(): {e}")

    @database_sync_to_async
    def save_message(self, message_content):
        try:
            chat = Chat.objects.get(id=self.chat_id)

            if not chat.participants.filter(id=self.user.id).exists():
                return None

            message = Message.objects.create(
                chat=chat,
                sender=self.user,
                content=message_content,
                timestamp=timezone.now()
            )
            return message
        except Chat.DoesNotExist:
            return None
        except Exception as e:
            print(f"❌ Error while saving message: {e}")
            return None

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "user": event["user"],
            "timestamp": event["timestamp"],
        }))
