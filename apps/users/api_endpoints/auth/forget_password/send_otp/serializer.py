from rest_framework import serializers


class ForgotPasswordSendOTPSerializer(serializers.Serializer):
	email = serializers.EmailField(required=False)
	phone_number = serializers.CharField(required=False)

	def validate(self, attrs):
		email = attrs.get('email')
		phone_number = attrs.get('phone_number')

		if not (email or phone_number):
			raise serializers.ValidationError("Either email or phone number must be provided.")

		if email and phone_number:
			raise serializers.ValidationError("Only one of email or phone number should be provided.")

		return attrs
