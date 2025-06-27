from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.projects.models import Project
from apps.projects.utils import ProjectRoles
from apps.socket_message.signals import kicked_from_project
from apps.users.models import User


class KickStaffSerializer(serializers.Serializer):
	project_uuid = serializers.UUIDField()
	user_id = serializers.IntegerField()

	def _get_kicker(self):
		request = self.context.get("request")
		user = getattr(request, "user", None)
		if not user or not user.is_authenticated:
			raise serializers.ValidationError("User not authenticated or found.")

		return user

	def validate(self, attrs):
		project_uuid = attrs.get('project_uuid')
		user_id = attrs.get('user_id')

		kicker = self._get_kicker()

		try:
			project = Project.objects.get(uuid=project_uuid)
			self._project = project
		except ObjectDoesNotExist:
			raise serializers.ValidationError("Project not found")

		if kicker not in [project.manager, project.owner]:
			raise serializers.ValidationError("You have not got access to kick someone")

		try:
			staff = User.objects.get(pk=user_id)
			self._staff = staff
		except ObjectDoesNotExist:
			raise serializers.ValidationError("User not found")

		if project.tester.filter(id=staff.id).exists():
			self._staff_role = ProjectRoles.Tester
		elif project.developer.filter(id=staff.id).exists():
			self._staff_role = ProjectRoles.Developer
		elif project.manager.filter(id=staff.id).exists():
			if kicker != project.owner:
				raise serializers.ValidationError("You cannot kick other manager")
			self._staff_role = ProjectRoles.Manager
		else:
			raise serializers.ValidationError("You cannot kick owner")

		return attrs

	def save(self, **kwargs):
		project = self._project
		staff = self._staff
		role = ProjectRoles(self._staff_role)

		if role == ProjectRoles.Manager:
			project.manager.remove(staff)
		elif role == ProjectRoles.Developer:
			project.developer.remove(staff)
		else:
			project.tester.remove(staff)

		project.save()

		kicked_from_project.send(
			sender=self.__class__,
			user=staff,
			manager=self._get_kicker(),
			project=project,
		)

		return project
