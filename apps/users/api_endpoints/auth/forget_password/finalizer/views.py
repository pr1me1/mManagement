from django.contrib.auth import get_user_model as gmu
from django.core.cache import cache
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.api_endpoints.auth.forget_password.finalizer.serializer import ForgotPasswordFinalizerSerializer
from utils.generator import generator_cache_key, CacheType


class ForgotPasswordFinalizerAPIView(GenericAPIView):
	serializer_class = ForgotPasswordFinalizerSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		session = serializer.validated_data.get('session')
		phone_number = serializer.validated_data.get('phone_number')
		email = serializer.validated_data.get('email')
		password = serializer.validated_data.get('password')

		main_field = email if email else phone_number

		cache_key = generator_cache_key(CacheType.FORGOT_PASSWORD_CONFIRMED_OTP, main_field, session)

		if not cache_key:
			return Response({"detail": "Invalid session or OTP confirmation."}, status=400)

		try:
			user = gmu().objects.get(username=main_field)
		except gmu().DoesNotExist:
			raise gmu().DoesNotExist("User does not exist.")

		cache.delete(cache_key)

		user.set_password(password)
		user.save(update_fields=['password'])

		return Response({'login': main_field}, status=200)


__all__ = [
	'ForgotPasswordFinalizerAPIView'
]
