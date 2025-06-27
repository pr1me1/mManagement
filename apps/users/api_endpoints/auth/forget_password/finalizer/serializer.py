from rest_framework import serializers


class ForgotPasswordFinalizerSerializer(serializers.Serializer):
	phone_number = serializers.CharField(max_length=15, required=False)
	email = serializers.EmailField(required=False)
	session = serializers.CharField(max_length=16)
	password = serializers.CharField(write_only=True, min_length=8, max_length=128)

	def validate_password(self, value):
		if len(value) < 8:
			raise serializers.ValidationError("Password must be at least 8 characters long.")
		if not any(char.isdigit() for char in value):
			raise serializers.ValidationError("Password must contain at least one digit.")
		if not any(char.isalpha() for char in value):
			raise serializers.ValidationError("Password must contain at least one letter.")
		return value

	def validate(self, attrs):
		phone_number = attrs.get('phone_number')
		email = attrs.get('email')
		session = attrs.get('session')

		if not (email or phone_number):
			raise serializers.ValidationError("Either email or phone number must be provided.")

		if email and phone_number:
			raise serializers.ValidationError("Only one of email or phone number should be provided.")

		if len(session) != 16:
			raise serializers.ValidationError("Session must be a 16-character string.")

		return attrs
