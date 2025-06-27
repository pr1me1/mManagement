from django.core.cache import cache
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.api_endpoints.auth.forget_password.confirm_otp.serilaizer import ForgotPasswordConfirmOTPSerializer
from utils.generator import CacheType, generator_cache_key, generator, GeneratorType


class ForgotPasswordConfirmOTPAPIView(GenericAPIView):
	serializer_class = ForgotPasswordConfirmOTPSerializer
	CACHE_TIMEOUT = 300

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		otp = serializer.validated_data.get('otp')
		session = serializer.validated_data.get('session')
		email = serializer.validated_data.get('email')
		phone_number = serializer.validated_data.get('phone_number')

		main_field = email if email else phone_number
		cache_type = CacheType.FORGOT_PASSWORD_EMAIL if email else CacheType.FORGOT_PASSWORD_PHONE

		cache_key = generator_cache_key(cache_type, main_field, session)
		code = cache.get(cache_key)

		if code != otp:
			return Response({"detail": "Invalid OTP or session."}, status=400)

		cache.delete(cache_key)

		session = generator(generator_type=GeneratorType.ALPHA_NUMBER, length=16)
		cache_key = generator_cache_key(CacheType.FORGOT_PASSWORD_CONFIRMED_OTP, main_field, session)
		cache.set(cache_key, True, self.CACHE_TIMEOUT)

		return Response({'session': session, 'login': main_field}, status=200)


__all__ = [
	'ForgotPasswordConfirmOTPAPIView'
]
