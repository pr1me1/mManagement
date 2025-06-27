from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.api_endpoints.task.change_priority.serializer import ChangePrioritySerializer


class StatusChangerAPIView(GenericAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = ChangePrioritySerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		task = serializer.save()
		from apps.projects.api_endpoints.task.manage.serializer import TaskModelSerializer
		return Response(
			TaskModelSerializer(task, context={'request': request}).data,
			status=status.HTTP_200_OK
		)
