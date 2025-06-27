from rest_framework import serializers


class RegistrationConfirmOTPSerializer(serializers.Serializer):
	email = serializers.EmailField(required=False)
	otp = serializers.CharField(max_length=6, min_length=6, required=True)
	session = serializers.CharField(max_length=16, required=True)

	def validate(self, attrs):
		otp = attrs.get('otp')
		session = attrs.get('session')
		email = attrs.get('email')

		if not otp.isdigit():
			raise serializers.ValidationError("OTP must be a 6-digit number.")

		if len(session) != 16:
			raise serializers.ValidationError("Session must be a 16-character string.")

		if not email:
			raise serializers.ValidationError("Email must be provided.")

		return attrs
