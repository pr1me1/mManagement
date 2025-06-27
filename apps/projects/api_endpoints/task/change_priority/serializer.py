from rest_framework import serializers

from apps.projects.models import Tasks, AuditLog


class ChangePrioritySerializer(serializers.Serializer):
	new_priority = serializers.ChoiceField(choices=Tasks.TaskPriority.choices)
	task_uuid = serializers.UUIDField()

	def validate(self, attrs):
		request = self.context.get("request")
		if not request or not request.user.is_authenticated:
			raise serializers.ValidationError({"error": "User must be authenticated"})

		task_uuid = attrs['task_uuid']
		try:
			task = Tasks.objects.select_related('project', 'created_by').prefetch_related(
				'project__manager', 'devs_res', 'testers_res'
			).get(uuid=task_uuid)
		except Tasks.DoesNotExist:
			raise serializers.ValidationError({"task_uuid": "Task not found"})

		project = task.project
		if request.user not in (
				project.owner,
				*project.manager.all(),

		):
			raise serializers.ValidationError({"error": "User lacks permission to change the status of this task"})

		new_priority = attrs['new_priority']
		old_priority = Tasks.TaskStatus(task.priority)

		attrs['task'] = task
		attrs['new_priority'] = new_priority
		attrs['old_priority'] = old_priority
		attrs['requester'] = request.user

		return attrs

	def save(self, **kwargs):
		task = self.validated_data.get('task')
		new_priority = self.validated_data.get('new_priority')
		old_priority = self.validated_data.get('old_priority')
		requester = self.validated_data.get('requester')

		task.priority = new_priority
		task.save()

		from apps.socket_message.signals import task_priority_changed
		task_priority_changed.send(
			sender=self.__class__,
			task=task,
			project=task.project
		)

		AuditLog.objects.create(
			created_by=requester,
			action=f"Priority: {old_priority} -> {new_priority}",
			reason="",
			task=task
		)

		return task
