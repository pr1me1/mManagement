from rest_framework import serializers

from apps.projects.models import Tasks, AuditLog


class StatusChangerSerializer(serializers.Serializer):
	new_status = serializers.ChoiceField(choices=Tasks.TaskStatus.choices)
	reason = serializers.CharField(allow_blank=True, required=True)
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
				*task.devs_res.all(),
				*task.testers_res.all()
		):
			raise serializers.ValidationError({"error": "User lacks permission to change the status of this task"})

		new_status = attrs['new_status']
		old_status = Tasks.TaskStatus(task.status)

		allowed_transitions = {
			Tasks.TaskStatus.Backlog: [Tasks.TaskStatus.ToDo],
			Tasks.TaskStatus.ToDo: [Tasks.TaskStatus.Progress],
			Tasks.TaskStatus.Progress: [Tasks.TaskStatus.Ready],
			Tasks.TaskStatus.Ready: [Tasks.TaskStatus.Done, Tasks.TaskStatus.Rejected]
		}

		if old_status not in allowed_transitions or new_status not in allowed_transitions.get(old_status, []):
			raise serializers.ValidationError({
				"new_status": f"Cannot change status from '{old_status}' to '{new_status}'. "
							  f"Allowed transitions from '{old_status}': {allowed_transitions.get(old_status, [])}"
			})

		if old_status == Tasks.TaskStatus.Backlog:
			if request.user not in (project.owner, *project.manager.all()):
				raise serializers.ValidationError({
					"error": "Only project owner or managers can change status from Backlog to To Do"
				})
		elif old_status == Tasks.TaskStatus.Progress:
			if request.user not in task.devs_res.all():
				raise serializers.ValidationError({
					"error": "Only developers can change status from In Progress to Ready for Testing"
				})
		elif old_status == Tasks.TaskStatus.Ready:
			if request.user not in task.testers_res.all():
				raise serializers.ValidationError({
					"error": "Only testers can change status from Ready for Testing to Done or Rejected"
				})

		attrs['task'] = task
		attrs['new_status'] = new_status
		attrs['old_status'] = old_status
		attrs['requester'] = request.user

		return attrs

	def save(self, **kwargs):
		task = self.validated_data['task']
		task.status = self.validated_data['new_status']
		task.save()

		log = AuditLog.objects.create(
			created_by=self.validated_data['requester'],
			action=f"Status: {self.validated_data['old_status']} -> {self.validated_data['new_status']}",
			reason=self.validated_data["reason"] if self.validated_data["reason"] else "",
			task=task
		)

		return task
