import json
import logging
from json import JSONDecodeError
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Улучшенный WebSocket-чат.
    Поддерживает несколько комнат, обработку ошибок
    и базовую проверку аутентификации.
    """

    async def connect(self):
        # Получаем имя комнаты из URL: path("ws/chat/<room_name>/", ChatConsumer.as_asgi())
        self.room_name = self.scope["url_route"]["kwargs"].get("room_name", "default")
        self.room_group_name = f"chat_{self.room_name}"

        # Проверка аутентификации (опционально)
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            # Можно разрешить анонимов: просто закомментируйте блок ниже
            await self.close(code=4001)  # 4001 – кастомный код «Not authenticated»
            return

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        logger.info("User %s joined room %s", user, self.room_name)

    async def disconnect(self, close_code):
        # Отписка от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info("User disconnected from room %s", self.room_name)
        raise StopConsumer()  # корректно завершает consumer

    async def receive(self, text_data: str):
        """
        Получаем сообщение от клиента, валидируем и рассылаем в комнату.
        """
        try:
            data = json.loads(text_data)
        except JSONDecodeError:
            logger.warning("Invalid JSON from %s: %s", self.channel_name, text_data)
            return

        message = data.get("message")
        username = data.get("username")

        if not message or not username:
            logger.warning("Missing fields in message: %s", data)
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username
            }
        )

    async def chat_message(self, event: dict):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"]
        }))
