from rest_framework import serializers


class RegistrationSendOTPSerializer(serializers.Serializer):
	email = serializers.EmailField(required=False)

	def validate(self, attrs):
		email = attrs.get('email')

		if not email:
			raise serializers.ValidationError("Email must be provided.")

		return attrs
