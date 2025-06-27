from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.api_endpoints.profile.delete_profile.serializer import UserDestroySerializer
from apps.users.models import User


# class UserDestroyAPIView(DestroyAPIView):
# 	serializer_class = UserDestroySerializer
# 	queryset = User.objects.all()
# 	permission_classes = [IsAuthenticated]
#
# 	def get_object(self):
# 		try:
# 			serializer = self.get_serializer(data=self.request.data)
# 			serializer.is_valid(raise_exception=True)
# 			user = serializer.instance
#
# 			if user != self.request.user:
# 				raise PermissionDenied("You can only delete your own account")
#
# 			return user
# 		except User.DoesNotExist:
# 			raise Http404("User not found")
#
# 	def perform_destroy(self, instance):
# 		instance.is_active = False
# 		instance.save(update_fields=['is_active'])
#
# 	def destroy(self, request, *args, **kwargs):
# 		try:
# 			instance = self.get_object()
# 			self.perform_destroy(instance)
# 			return Response(
# 				{"detail": "Account deactivated successfully."},
# 				status=status.HTTP_204_NO_CONTENT
# 			)
# 		except PermissionDenied as e:
# 			return Response(
# 				{"detail": str(e)},
# 				status=status.HTTP_403_FORBIDDEN
# 			)
# 		except Http404:
# 			return Response(
# 				{"detail": "User not found."},
# 				status=status.HTTP_404_NOT_FOUND
# 			)


class UserDestroyAPIView(GenericAPIView):
	serializer_class = UserDestroySerializer
	permission_classes = [IsAuthenticated]

	def post(self, request, *args, **kwargs):

		try:
			serializer = self.serializer_class(data=request.data)
			serializer.is_valid(raise_exception=True)
			user = serializer.instance

			# if user != request.user:
			# 	raise PermissionDenied("You can only delete your own account")

			user.is_active = False
			user.save(update_fields=['is_active'])
			return Response(
				{"detail": "Account deactivated successfully."},
				status=status.HTTP_204_NO_CONTENT
			)
		except PermissionDenied as e:

			return Response(
				{"detail": str(e)},
				status=status.HTTP_403_FORBIDDEN
			)
		except User.DoesNotExist:

			return Response(
				{"detail": "User not found."},
				status=status.HTTP_404_NOT_FOUND
			)


__all__ = ['UserDestroyAPIView']
