from django.apps import AppConfig


class ProjectsConfig(AppConfig):
	default_auto_field = "django.db.models.BigAutoField"
	name = "apps.projects"

	def ready(self):
		import apps.socket_message.signals  # noqa
