from django.urls import re_path
from . import consumers  # импортируем consumers из main

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]
