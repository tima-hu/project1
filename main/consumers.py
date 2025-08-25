from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Присоединяем пользователя к группе чата
        self.room_group_name = "chat_room"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Удаляем пользователя из группы при отключении
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Парсим JSON, пришедший от фронтенда
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Отправляем сообщение всем в группе
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        # Получаем данные из события
        message = event['message']
        username = event['username']

        # Отправляем нормальный JSON на фронтенд
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
