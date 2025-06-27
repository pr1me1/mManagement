from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.models import Project, Tasks
from apps.socket_message.api_endpoints.list.serializer import ProjectMessageListSerializer, TaskMessageListSerializer
from apps.socket_message.models import ProjectMessage, TaskMessage


class ProjectMessageListRetrieve(ListAPIView):
	serializer_class = ProjectMessageListSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		try:
			project = Project.objects.get(uuid=self.kwargs.get('uuid'))
		except ObjectDoesNotExist:
			return Response("Invalid Project id", status=status.HTTP_404_NOT_FOUND, )

		return ProjectMessage.objects.filter(project=project)


class TaskMessageListRetrieve(ListAPIView):
	serializer_class = TaskMessageListSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		try:
			task = Tasks.objects.get(uuid=self.kwargs.get('uuid'))
		except ObjectDoesNotExist:
			return Response("Invalid Task id", status=status.HTTP_404_NOT_FOUND, )

		return TaskMessage.objects.filter(task=task)
