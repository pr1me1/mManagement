from rest_framework import serializers

from apps.projects.models import Project


class ProjectCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = ['name', 'description']

	name = serializers.CharField(max_length=128, required=True)
	description = serializers.CharField(required=True, allow_blank=True)
