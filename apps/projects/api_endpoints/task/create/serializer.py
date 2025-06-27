from rest_framework import serializers

from apps.projects.models import Tasks, Project


# class TaskCreateSerializer(serializers.Serializer):
# 	name = serializers.CharField(min_length=4, required=True)
# 	description = serializers.CharField(allow_blank=True, required=False)
# 	priority = serializers.ChoiceField(choices=Tasks.TaskPriority.choices)
# 	project_uuid = serializers.UUIDField()
#
# 	def validate(self, attrs):
# 		request = self.context.get("request")
# 		if not request or not request.user.is_authenticated:
# 			raise serializers.ValidationError({"error": "User must be authenticated"})
#
# 		try:
# 			project = Project.objects.get(uuid=attrs['project_uuid'])
# 		except Project.DoesNotExist:
# 			raise serializers.ValidationError({"project_uuid": "Project not found"})
#
# 		if request.user not in (project.owner, project.manager):
# 			raise serializers.ValidationError({"error": "User lacks permission to create task for this project"})
#
# 		attrs['project'] = project
# 		attrs['creator'] = request.user
# 		return attrs
#
# 	def create(self, validated_data):
# 		project = validated_data['project']
# 		creator = validated_data['creator']
#
# 		task = Tasks.objects.create(
# 			name=validated_data['name'],
# 			description=validated_data['description'],
# 			priority=validated_data['priority'],
# 			project=project,
# 			created_by=creator,
# 			status=Tasks.TaskStatus.Backlog
# 		)
# 		return task


class TaskCreateSerializer(serializers.ModelSerializer):
	name = serializers.CharField(min_length=4, required=True)
	project_uuid = serializers.UUIDField(write_only=True)
	priority = serializers.ChoiceField(choices=Tasks.TaskPriority.choices, default=Tasks.TaskPriority.Low)
	project = serializers.PrimaryKeyRelatedField(read_only=True)

	class Meta:
		model = Tasks
		fields = ['uuid', 'name', 'description', 'status', 'priority', 'project', 'project_uuid', 'created_by']
		read_only_fields = ['uuid', 'status', 'created_by']

	def validate(self, attrs):
		request = self.context.get("request")
		if not request or not request.user.is_authenticated:
			raise serializers.ValidationError({"error": "User must be authenticated"})

		project_uuid = attrs.get('project_uuid')
		try:
			project = Project.objects.get(uuid=project_uuid)
		except Project.DoesNotExist:
			raise serializers.ValidationError({"project_uuid": "Project not found"})

		if request.user not in (project.owner, project.manager):
			raise serializers.ValidationError({"error": "User lacks permission to create task for this project"})

		attrs['project'] = project
		attrs['created_by'] = request.user
		return attrs

	def create(self, validated_data):

		validated_data.pop('project_uuid', None)

		task = Tasks.objects.create(
			name=validated_data['name'],
			description=validated_data.get('description', ''),
			priority=validated_data['priority'],
			project=validated_data['project'],
			created_by=validated_data['created_by']
		)

		from apps.socket_message.signals import new_task_created
		new_task_created.send(
			sender=self.__class__,
			task=task,
			project=validated_data.get("project")
		)

		return task
