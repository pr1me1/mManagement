from rest_framework import serializers

from apps.projects.models import Tasks, AuditLog
from apps.users.models import User
from apps.users.utils import send_notification_to_email


class SetStaffSerializer(serializers.Serializer):
	staff_ids = serializers.ListField(child=serializers.IntegerField(), required=True)
	role = serializers.ChoiceField(choices=["developer", "tester"])
	task_uuid = serializers.UUIDField(write_only=True)

	def validate(self, attrs):
		request = self.context.get("request")
		if not request or not request.user.is_authenticated:
			raise serializers.ValidationError({"error": "User must be authenticated"})

		task_uuid = attrs.get('task_uuid')
		try:
			task = Tasks.objects.select_related('project').get(uuid=task_uuid)
		except Tasks.DoesNotExist:
			raise serializers.ValidationError({"task_uuid": "Task not found"})

		if request.user not in (task.project.owner, task.project.manager):
			raise serializers.ValidationError({"error": "User lacks permission to assign staff to this task"})

		staff_ids = attrs['staff_ids']
		if not staff_ids:
			raise serializers.ValidationError({"staff_ids": "At least one user ID is required"})

		staffs = User.objects.filter(id__in=staff_ids)
		if len(staffs) != len(set(staff_ids)):
			raise serializers.ValidationError({"staff_ids": "One or more user IDs are invalid"})

		existing_devs = set(task.devs_res.values_list('id', flat=True))
		existing_testers = set(task.testers_res.values_list('id', flat=True))
		new_staff_ids = set(staff_ids)
		if new_staff_ids & (existing_devs | existing_testers):
			raise serializers.ValidationError(
				{"staff_ids": "One or more users are already assigned as developers or testers"})

		attrs['task'] = task
		attrs['staffs'] = staffs
		attrs['requester'] = request.user
		return attrs

	def save(self):
		task = self.validated_data['task']
		staffs = self.validated_data['staffs']
		role = self.validated_data['role']

		if role == 'developer':
			task.devs_res.add(*staffs)
		else:
			task.testers_res.add(*staffs)

		task.status = Tasks.TaskStatus.Progress
		task.save()

		if task.priority == Tasks.TaskPriority.High:
			email = []

			for staff in staffs:
				email.append(staff.email)

			send_notification_to_email(task.project.name, email,
									   f"From now you are responsible for the high-priority task named {task.name}")

		AuditLog.objects.create(
			created_by=self.validated_data['requester'],
			action=f"Status: Backlog -> ToDo by adding staff(s)",
			reason="",
			task=task
		)

		return task
