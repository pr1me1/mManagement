from rest_framework import serializers

from apps.socket_message.models import ProjectMessage, TaskMessage
from apps.users.api_endpoints.list.serializer import UserListSerializer


class ProjectMessageListSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()

	class Meta:
		model = ProjectMessage
		fields = ("id", "message", "type", "user")

	def get_user(self, obj):
		return UserListSerializer(obj.sender).data


class TaskMessageListSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()

	class Meta:
		model = TaskMessage
		fields = ("id", "message", "type", "user")

	def get_user(self, obj):
		return UserListSerializer(obj.sender).data
