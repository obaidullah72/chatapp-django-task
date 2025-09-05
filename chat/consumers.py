import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Chat, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract chat ID from route
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        self.user = self.scope.get('user', AnonymousUser())

        # 🔎 Debug info
        print("----- WEBSOCKET CONNECT -----")
        print(f"Chat ID: {self.chat_id}")
        print(f"User: {self.user}")
        print(f"User authenticated: {self.user.is_authenticated}")
        print(f"User ID: {getattr(self.user, 'id', None)}")

        if self.user.is_anonymous:
            print("❌ Rejecting connection (anonymous user)")
            await self.close()
            return

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()
        print("✅ WebSocket connection accepted")

    async def disconnect(self, close_code):
        print(f"----- WEBSOCKET DISCONNECT ----- Code: {close_code}")
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("----- WEBSOCKET RECEIVE -----")
        print(f"Raw data: {text_data}")

        try:
            data = json.loads(text_data)
            message_content = data.get("message", "").strip()

            if not message_content:
                print("⚠️ Empty message received, ignoring")
                return

            saved_message = await self.save_message(message_content)

            if saved_message:
                print(f"✅ Message saved with ID {saved_message.id}")
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    {
                        "type": "chat_message",
                        "message": saved_message.content,
                        "user": saved_message.sender.username,
                        "timestamp": saved_message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    },
                )
            else:
                print("❌ Message was not saved to DB")

        except Exception as e:
            print(f"❌ Error in receive(): {e}")

    @database_sync_to_async
    def save_message(self, message_content):
        try:
            print(f"Attempting to save message for chat {self.chat_id}")
            chat = Chat.objects.get(id=self.chat_id)

            # Check if user is a participant
            is_participant = chat.participants.filter(id=self.user.id).exists()
            print(f"User is participant: {is_participant}")

            if not is_participant:
                print("❌ User is not a participant, cannot save message")
                return None

            message = Message.objects.create(
                chat=chat,
                sender=self.user,
                content=message_content,
                timestamp=timezone.now()
            )
            print(f"✅ Message created in DB: {message.id}")
            return message

        except Chat.DoesNotExist:
            print(f"❌ Chat with ID {self.chat_id} does not exist")
            return None
        except Exception as e:
            print(f"❌ Error while saving message: {e}")
            return None

    async def chat_message(self, event):
        print("----- SENDING MESSAGE TO CLIENT -----")
        print(f"User: {event['user']} | Message: {event['message']}")
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "user": event["user"],
            "timestamp": event["timestamp"],
        }))
