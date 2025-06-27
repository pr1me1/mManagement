from rest_framework import serializers


class ForgotPasswordConfirmOTPSerializer(serializers.Serializer):
	phone_number = serializers.CharField(max_length=15, required=False)
	email = serializers.EmailField(required=False)
	otp = serializers.CharField(max_length=6, min_length=6, required=True)
	session = serializers.CharField(max_length=16, required=True)

	def validate(self, attrs):
		otp = attrs.get('otp')
		session = attrs.get('session')
		email = attrs.get('email')
		phone_number = attrs.get('phone_number')

		if not otp.isdigit():
			raise serializers.ValidationError("OTP must be a 6-digit number.")

		if len(session) != 16:
			raise serializers.ValidationError("Session must be a 16-character string.")

		if not (email or phone_number):
			raise serializers.ValidationError("Either email or phone number must be provided.")

		if email and phone_number:
			raise serializers.ValidationError("Only one of email or phone number should be provided.")

		return attrs
