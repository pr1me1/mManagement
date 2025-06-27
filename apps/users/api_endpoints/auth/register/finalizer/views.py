from django.contrib.auth import get_user_model as gmu
from django.core.cache import cache
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.users.api_endpoints.auth.register.finalizer.serializer import RegistrationFinalizerSerializer
from utils.generator import generator_cache_key, CacheType


class RegistrationFinalizerAPIView(CreateAPIView):
	serializer_class = RegistrationFinalizerSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)

		session = serializer.validated_data.get('session')
		email = serializer.validated_data.get('email')
		password = serializer.validated_data.get('password')

		main_field = email

		cache_key = generator_cache_key(CacheType.REGISTRATION_CONFIRMED_OTP, main_field, session)

		if not cache_key:
			return Response({"detail": "Invalid session or OTP confirmation."}, status=400)

		clean_username = main_field.replace("+", "_")

		cache.delete(cache_key)

		user, _ = gmu().objects.get_or_create(
			username=clean_username,
			defaults={
				'email': email,
			},
		)

		user.set_password(password)
		user.save(update_fields=['password'])

		return Response({'login': main_field}, status=200)


__all__ = [
	'RegistrationFinalizerAPIView'
]
