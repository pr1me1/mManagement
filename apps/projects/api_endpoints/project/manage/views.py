from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.api_endpoints.project.manage.serializer import ProjectModelSerializer
from apps.projects.models import Project


class ProjectModelAPIView(GenericAPIView):
	serializer_class = ProjectModelSerializer
	permission_classes = [IsAuthenticated]
	queryset = Project.objects.all()

	def get_object(self):
		uuid = self.kwargs.get('uuid')
		return Project.objects.get(uuid=uuid)

	def patch(self, request, *args, **kwargs):
		project = self.get_object()
		serializer = self.get_serializer(project, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)

	def delete(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

	def get(self, request, *args, **kwargs):
		project = self.get_object()
		serializer = self.get_serializer(project)
		return Response(serializer.data, status=status.HTTP_200_OK)


__all__ = ['ProjectModelAPIView']
