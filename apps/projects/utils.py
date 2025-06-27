from django.db import models


class ProjectRoles(models.TextChoices):
	Owner = "project_owner"
	Manager = "project_manager"
	Developer = "project_developer"
	Tester = "project_tester"

