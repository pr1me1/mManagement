from rest_framework import serializers

from apps.users.models import User


class UserListSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ("id", "username", "full_name", "last_login",)


class UserSearchSerializer(serializers.Serializer):
	username = serializers.CharField(required=False)
	full_name = serializers.CharField(required=False)
	phone_number = serializers.CharField(required=False)
	email = serializers.EmailField(required=False)

	def validate(self, attrs):
		username = attrs.get("username")
		full_name = attrs.get("full_name")
		phone_number = attrs.get("phone_number")
		email = attrs.get("email")

		# Ensure exactly one field is provided
		provided_fields = [f for f in [username, full_name, phone_number, email] if f]
		if not provided_fields:
			raise serializers.ValidationError("One of email, phone number, username, or full name must be provided.")
		if len(provided_fields) > 1:
			raise serializers.ValidationError(
				"Only one of email, phone number, username, or full name should be provided.")

		return attrs
# class Meta:
# 	model = User
# 	fields = ("id", "username", "full_name", "last_login", "phone_number", "email")
