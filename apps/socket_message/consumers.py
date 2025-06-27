from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatWebsocketConsumer(AsyncJsonWebsocketConsumer):
	routers = {
		"send_message": "send_message",
		"send_notification": "send_notification",
		"send_status_change": "send_status_change",
	}

	async def connect(self):
		self.room_name = self.scope["url_route"]["kwargs"]["project"]
		self.room_group_name = f"project_{self.room_name}"

		await self.channel_layer.group_add(self.room_group_name, self.channel_name)
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name, self.channel_name
		)

	async def receive_json(self, content, **kwargs):
		message_type = content.get('type')
		router = self.routers.get(message_type)
		data = content['data']

		await self.channel_layer.group_send(
			self.room_group_name, {"type": router, "data": data}
		)

	async def send_message_from_django(self, event):
		data = event["data"]

		await self.send_json(content={"type": "message", "data": data})


class DirectWebSocketConsumer(AsyncJsonWebsocketConsumer):
	routers = {
		"send_message": "send_message",
		"send_notification": "send_notification",
		"send_status_change": "send_status_change",
	}

	async def connect(self):
		self.direct_room = self.scope["url_route"]["kwargs"]["username"]

		self.room_name = f"direct_{self.direct_room}"

		await self.channel_layer.group_add(self.room_name, self.channel_name)
		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_name, self.channel_name
		)

	async def receive_json(self, content, **kwargs):
		message_type = content.get('type')
		router = self.routers.get(message_type)
		data = content['data']

		await self.channel_layer.group_send(
			self.room_name, {"type": router, "data": data}
		)

	async def send_message_from_django(self, event):
		data = event["data"]

		await self.send_json(content={"type": "notification", "data": data})
