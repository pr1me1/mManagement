from rest_framework import serializers

from apps.projects.models import Tasks, AuditLog
from apps.users.api_endpoints.list.serializer import UserListSerializer


class TaskModelSerializer(serializers.ModelSerializer):
	developers = serializers.SerializerMethodField()
	owner = serializers.SerializerMethodField()
	logs = serializers.SerializerMethodField()

	class Meta:
		model = Tasks
		fields = ("uuid", "name", "description", "status", "priority", "developers", "owner", "logs")
		read_only_fields = ("uuid", "status", "developers", "owner")

	def get_developers(self, obj):
		developers = obj.devs_res.all()
		return UserListSerializer(developers, many=True).data

	def get_owner(self, obj):
		return UserListSerializer(obj.created_by, many=False).data

	def get_logs(self, obj):
		logs = AuditLog.objects.filter(task=obj)
		return AuditLogModelSerializer(logs, many=True).data


class AuditLogModelSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()

	class Meta:
		model = AuditLog
		fields = ("uuid", "action", "reason", "user", "created_at")
		read_only_fields = ("uuid", "action", "reason", "user")

	def get_user(self, obj):
		return UserListSerializer(obj.created_by).data
