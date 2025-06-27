from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.api_endpoints.profile.profile.serializer import UserModelSerializer
from apps.users.models import User


class UserModelAPIView(GenericAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = UserModelSerializer
	queryset = User.objects.all()

	def get_object(self):
		try:
			user = User.objects.get(pk=self.request.user.pk)
			return user
		except User.DoesNotExist:
			raise NotFound("User not found.")

	def get(self, request, *args, **kwargs):
		user = self.get_object()
		serializer = self.get_serializer(user)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def patch(self, request, *args, **kwargs):
		user = self.get_object()
		serializer = self.get_serializer(user, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
