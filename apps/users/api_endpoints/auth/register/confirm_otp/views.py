import json

from django.core.cache import cache
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.api_endpoints.auth.register.confirm_otp.serializer import RegistrationConfirmOTPSerializer
from utils.generator import CacheType, generator_cache_key, generator, GeneratorType


class RegistrationConfirmOTPAPIView(GenericAPIView):
	serializer_class = RegistrationConfirmOTPSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		otp = serializer.validated_data.get('otp')
		session = serializer.validated_data.get('session')
		email = serializer.validated_data.get('email')

		main_field = email
		cache_type = CacheType.REGISTRATION_EMAIL_VERIFICATION

		cache_key = generator_cache_key(cache_type, main_field, session)
		cached_data = cache.get(cache_key)
		code, full_name = json.loads(cached_data) if cached_data else (None, None)

		if not cached_data or code != otp:
			return Response({"detail": "Invalid OTP or session."}, status=400)

		cache.delete(cache_key)
		session = generator(generator_type=GeneratorType.ALPHA_NUMBER, length=16)
		cache_key = generator_cache_key(CacheType.REGISTRATION_CONFIRMED_OTP, main_field, session)
		cache.set(cache_key, json.dumps([full_name]), 300)

		return Response({'session': session, 'login': main_field}, status=200)  # Adjust response as needed


__all__ = [
	'RegistrationConfirmOTPAPIView'
]
