from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.api_endpoints.task.manage.serializer import TaskModelSerializer
from apps.projects.api_endpoints.task.set_staff.serializer import SetStaffSerializer
from apps.projects.models import Tasks


class SetStaffAPIView(GenericAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = SetStaffSerializer
	queryset = Tasks.objects.all()

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		task = serializer.save()
		return Response(
			TaskModelSerializer(task, context={'request': request}).data,
			status=status.HTTP_200_OK
		)
