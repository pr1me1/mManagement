from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.api_endpoints.task.change_status.serializer import StatusChangerSerializer
from apps.projects.api_endpoints.task.manage.serializer import TaskModelSerializer


class StatusChangerAPIView(GenericAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = StatusChangerSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		task = serializer.save()
		return Response(
			TaskModelSerializer(task, context={'request': request}).data,
			status=status.HTTP_200_OK
		)
