from django.urls import path

from apps.socket_message.consumers import ChatWebsocketConsumer, DirectWebSocketConsumer

websocket_urlpatterns = [
	path("projects/<uuid:project>/", ChatWebsocketConsumer.as_asgi()),
	path("direct/<str:username>/", DirectWebSocketConsumer.as_asgi())
]
