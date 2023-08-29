import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import chat_message
from users.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = text_data_json["user_id"]
        room_id = text_data_json["room_id"]
        msg = chat_message.objects.create(m_writer_id=user_id,
                                          m_room_id=room_id,
                                          m_content=message)
        nickname = User.objects.get(pk=user_id).u_nickname
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "nickname": nickname, "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        nickname = event["nickname"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, "nickname": nickname}))
