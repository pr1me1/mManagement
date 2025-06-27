from django.contrib.auth import get_user_model as gmu
from django.core.cache import cache
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.api_endpoints.auth.forget_password.send_otp.serializer import ForgotPasswordSendOTPSerializer
from apps.users.tasks import send_otp_task
from utils.generator import CacheType, generator_cache_key, generator, GeneratorType


class ForgotPasswordSendOTPAPIView(GenericAPIView):
	CACHE_TIMEOUT = 300

	serializer_class = ForgotPasswordSendOTPSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		email = serializer.validated_data.get('email')
		phone_number = serializer.validated_data.get('phone_number')

		username = email if email else phone_number

		try:
			gmu().objects.get(username=username)
		except gmu().DoesNotExist:
			return Response({"detail": "User does not exist."}, status=404)

		cache_type = CacheType.FORGOT_PASSWORD_EMAIL if email else CacheType.FORGOT_PASSWORD_PHONE

		cache_key = generator_cache_key(cache_type, username)

		if cache.keys(f'{cache_key}*'):
			return Response({"detail": "OTP already sent. Please wait before requesting a new one."}, status=429)

		code = generator(generator_type=GeneratorType.NUMBER, length=6)
		session = generator(generator_type=GeneratorType.ALPHA_NUMBER, length=16)
		cache_key = generator_cache_key(cache_type, username, session)

		cache.set(cache_key, code, self.CACHE_TIMEOUT)

		send_otp_task.delay(phone_number, email, code)

		return Response({"session": session, "login": username, 'code': code}, status=200)


__all__ = [
	'ForgotPasswordSendOTPAPIView'
]
