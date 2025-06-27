from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.projects.api_endpoints.project.create.serializer import ProjectCreateSerializer


class ProjectCreateAPIView(CreateAPIView):
	serializer_class = ProjectCreateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		project = serializer.save(owner=self.request.user)
		return project


__all__ = ['ProjectCreateAPIView']
