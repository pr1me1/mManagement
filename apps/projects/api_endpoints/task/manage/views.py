from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.api_endpoints.task.manage.serializer import TaskModelSerializer
from apps.projects.models import Tasks


class TaskDetailView(generics.GenericAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = TaskModelSerializer

	def get_object(self):
		uuid = self.kwargs.get('uuid')
		if not uuid:
			return Response(
				{"error": "Task UUID is required in query parameters"},
				status=status.HTTP_400_BAD_REQUEST
			)
		try:
			task = Tasks.objects.get(uuid=uuid)
			project = task.project
			if self.request.user not in (project.owner, project.manager, task.created_by):
				return Response(
					{"error": "You do not have permission to access this task"},
					status=status.HTTP_403_FORBIDDEN
				)
			return task
		except ObjectDoesNotExist:
			return Response(
				{"error": "Task not found"},
				status=status.HTTP_404_NOT_FOUND
			)

	def get(self, request, *args, **kwargs):
		task = self.get_object()
		if isinstance(task, Response):
			return task
		serializer = self.get_serializer(task)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def patch(self, request, *args, **kwargs):
		task = self.get_object()
		if isinstance(task, Response):
			return task
		serializer = self.get_serializer(task, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, *args, **kwargs):
		task = self.get_object()
		if isinstance(task, Response):
			return task
		task.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
