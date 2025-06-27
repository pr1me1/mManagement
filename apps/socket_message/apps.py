from django.apps import AppConfig


class SocketMessageConfig(AppConfig):
	default_auto_field = "django.db.models.BigAutoField"
	name = "apps.socket_message"

	def ready(self):
		import apps.socket_message.signals  # noqa
