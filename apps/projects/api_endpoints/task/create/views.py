from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.projects.api_endpoints.task.create.serializer import TaskCreateSerializer


class TaskCreateAPIView(CreateAPIView):
	serializer_class = TaskCreateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		task = serializer.save(owner=self.request.user)
		return task


__all__ = ['TaskCreateAPIView']
