from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.projects.models import Project
from apps.projects.utils import ProjectRoles
from apps.socket_message.signals import added_to_project
from apps.users.models import User


class PromoteToProjectSerializer(serializers.Serializer):
	project_uuid = serializers.UUIDField()
	user_id = serializers.IntegerField()
	role = serializers.ChoiceField(choices=ProjectRoles.choices)

	def validate(self, attrs):
		project_uuid = attrs.get('project_uuid')
		user_id = attrs.get('user_id')
		role = attrs.get('role')

		promoter = self._get_promoter()

		try:
			project = Project.objects.get(uuid=project_uuid)
		except ObjectDoesNotExist:
			raise serializers.ValidationError("Project not found")

		if project.owner == promoter:
			self._promoter_role = ProjectRoles.Owner
		elif promoter in [project.manager]:
			self._promoter_role = ProjectRoles.Manager
		elif promoter in [project.developer, project.tester]:
			raise serializers.ValidationError("you have not got to promote")

		try:
			promoted = User.objects.get(pk=user_id)
		except ObjectDoesNotExist:
			raise serializers.ValidationError("User not found")

		tester_count = project.tester.filter(id=promoted.id).exists()
		developer_count = project.developer.filter(id=promoted.id).exists()
		manager_count = project.manager.filter(id=promoted.id).exists()

		role_count = sum([tester_count, developer_count, manager_count])

		if role_count > 1:
			raise serializers.ValidationError("Single user cannot be in multiple roles at same time")

		if role == ProjectRoles.Owner:
			raise serializers.ValidationError("There will be only one owner in project")

		if role == ProjectRoles.Manager and self._promoter_role != ProjectRoles.Owner:
			raise serializers.ValidationError(f"Only owner can promote user to {role}")

		self._project = project
		self._promoted = promoted
		self._role = role

		return attrs

	def _get_promoter(self):
		request = self.context.get("request")
		user = getattr(request, "user", None)
		if not user or not user.is_authenticated:
			raise serializers.ValidationError("User not authenticated or found.")

		return user

	def save(self, **kwargs):
		project = self._project
		promoted = self._promoted
		role = ProjectRoles(self._role)

		if role == ProjectRoles.Manager:
			project.manager.add(promoted)
		elif role == ProjectRoles.Developer:
			project.developer.add(promoted)
		else:
			project.tester.add(promoted)

		project.save()

		added_to_project.send(
			sender=self.__class__,
			user=promoted,
			promoter=self._get_promoter(),
			project=project,
			role=role
		)

		return project
