import uuid

from django.db import models

from apps.common.models import BaseModel
from apps.users.models import User


class Project(BaseModel):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
	name = models.CharField(max_length=128)
	description = models.TextField()
	owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="projects_owned")
	manager = models.ManyToManyField(to=User, related_name="projects_managed")
	developer = models.ManyToManyField(to=User, related_name="projects_developed")
	tester = models.ManyToManyField(to=User, related_name="projects_tested")

	def __str__(self):
		return self.name


class Tasks(BaseModel):
	class TaskStatus(models.TextChoices):
		Backlog = "Backlog"
		ToDo = "To Do"
		Progress = "In Progress"
		Ready = "Ready for Testing"
		Done = "Done"
		Rejected = "Rejected"

	class TaskPriority(models.TextChoices):
		Low = "Low"
		Medium = "Medium"
		High = "High"

	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
	name = models.CharField(max_length=128)
	description = models.TextField()
	status = models.CharField(choices=TaskStatus.choices, default=TaskStatus.Backlog)
	priority = models.CharField(choices=TaskPriority.choices, default=TaskPriority.Low)
	project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="project_tasks")
	devs_res = models.ManyToManyField(to=User, related_name="task_responsible")
	created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="tasks_created")


class AuditLog(BaseModel):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
	action = models.TextField()
	reason = models.TextField(blank=True, default="")
	task = models.ForeignKey(to=Tasks, on_delete=models.CASCADE)
	created_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="log_created")
