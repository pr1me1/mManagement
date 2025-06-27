from django.db.models import Case, When, Value, IntegerField
from rest_framework import serializers

from apps.projects.api_endpoints.task.manage.serializer import TaskModelSerializer
from apps.projects.models import Project, Tasks
from apps.users.api_endpoints.list.serializer import UserListSerializer


class ProjectModelSerializer(serializers.ModelSerializer):
	project_owner = serializers.SerializerMethodField()
	project_manager = serializers.SerializerMethodField()
	project_developer = serializers.SerializerMethodField()
	project_tester = serializers.SerializerMethodField()
	tasks = serializers.SerializerMethodField()

	class Meta:
		model = Project
		fields = ("uuid", "name", "description", "project_owner", "project_manager", "project_developer",
				  "project_tester", 'tasks')
		read_only_fields = ["uuid", 'created_at']

	def get_project_owner(self, obj):
		return UserListSerializer(obj.owner, many=False).data

	def get_project_tester(self, obj):
		testers = obj.tester.all()
		return UserListSerializer(testers, many=True).data

	def get_project_developer(self, obj):
		developers = obj.developer.all()
		return UserListSerializer(developers, many=True).data

	def get_project_manager(self, obj):
		managers = obj.manager.all()
		return UserListSerializer(managers, many=True).data

	def get_tasks(self, obj):
		tasks = Tasks.objects.filter(project=obj).annotate(
			priority_order=Case(
				When(priority=Tasks.TaskPriority.High, then=Value(1)),
				When(priority=Tasks.TaskPriority.Medium, then=Value(2)),
				When(priority=Tasks.TaskPriority.Low, then=Value(3)),
				output_field=IntegerField()
			)
		).order_by('priority_order')

		return TaskModelSerializer(tasks, many=True, context=self.context).data
