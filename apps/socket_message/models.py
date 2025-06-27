from django.contrib.auth import get_user_model as gmu
from django.db import models

from apps.common.models import BaseModel
from apps.projects.models import Project, Tasks


class SocketMessage(BaseModel):
	class MessageType(models.TextChoices):
		private = "private"
		group = "group"

	message = models.TextField()
	sender = models.ForeignKey(to=gmu(), on_delete=models.SET_NULL, null=True)
	type = models.CharField(max_length=16, choices=MessageType.choices)

	class Meta:
		abstract = True


class ProjectMessage(SocketMessage):
	project = models.ForeignKey(to=Project, on_delete=models.CASCADE)

	def __str__(self):
		return self.message


class TaskMessage(SocketMessage):
	task = models.ForeignKey(to=Tasks, on_delete=models.CASCADE)

	def __str__(self):
		return self.message
