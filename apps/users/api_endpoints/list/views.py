from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.api_endpoints.list.serializer import UserSearchSerializer, UserListSerializer
from apps.users.models import User


class UserSearchAPIView(GenericAPIView):
	queryset = User.objects.all()
	serializer_class = UserSearchSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		username = serializer.validated_data.get("username")
		full_name = serializer.validated_data.get("full_name")
		phone_number = serializer.validated_data.get("phone_number")
		email = serializer.validated_data.get("email")

		queryset = self.queryset

		if username:
			queryset = queryset.filter(username__icontains=username)
		elif full_name:
			queryset = queryset.filter(full_name__icontains=full_name)
		elif phone_number:
			queryset = queryset.filter(phone_number=phone_number)
		elif email:
			queryset = queryset.filter(email__iexact=email)
		else:
			queryset = queryset.none()

		users = queryset.filter(is_active=True)

		return Response(UserListSerializer(users, many=True).data)
