import json

from django.core.cache import cache
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.api_endpoints.auth.register.send_otp.serializer import RegistrationSendOTPSerializer
from apps.users.utils import send_otp_to_email
from utils.generator import CacheType, generator_cache_key, generator, GeneratorType


class RegistrationSendOTPAPIView(GenericAPIView):
	CACHE_TIMEOUT = 60
	serializer_class = RegistrationSendOTPSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		email = serializer.validated_data.get('email')
		full_name = serializer.validated_data.get('full_name')

		main_field = email
		cache_type = CacheType.REGISTRATION_EMAIL_VERIFICATION

		cache_key = generator_cache_key(cache_type, main_field)

		if cache.keys(f'{cache_key}*'):
			return Response({"detail": "OTP already sent. Please wait before requesting a new one."}, status=429)

		code = generator(generator_type=GeneratorType.NUMBER, length=6)
		session = generator(generator_type=GeneratorType.ALPHA_NUMBER, length=16)
		cache_key = generator_cache_key(cache_type, main_field, session)

		cache.set(cache_key, json.dumps([code, full_name]), self.CACHE_TIMEOUT)

		send_otp_to_email(email, code)

		return Response({"session": session, "login": main_field, "code": code}, status=200)


__all__ = [
	'RegistrationSendOTPAPIView'
]
