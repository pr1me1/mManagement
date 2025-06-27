from rest_framework import serializers


class RegistrationFinalizerSerializer(serializers.Serializer):
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
		email = attrs.get('email')
		session = attrs.get('session')

		if not email:
			raise serializers.ValidationError("Email ormust be provided.")

		if len(session) != 16:
			raise serializers.ValidationError("Session must be a 16-character string.")

		return attrs
