from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.projects.api_endpoints.project.kick.serilaizer import KickStaffSerializer
from apps.projects.api_endpoints.project.manage.serializer import ProjectModelSerializer


class KickFromProjectAPIView(GenericAPIView):
	serializer_class = KickStaffSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = self.serializer_class(data=request.data, context={"request": request})
		serializer.is_valid(raise_exception=True)
		project = serializer.save()
		return Response(
			ProjectModelSerializer(project).data,
			status=status.HTTP_200_OK
		)


__all__ = ['KickFromProjectAPIView']
