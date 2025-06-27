from django.contrib.auth import get_user_model as gmu, authenticate
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers


class UserDestroySerializer(serializers.Serializer):
	username = serializers.CharField(max_length=256, required=True)
	password = serializers.CharField(min_length=8, max_length=64, required=True)

	def validate(self, attrs):
		username = attrs.get('username')
		password = attrs.get('password')

		try:
			gmu().objects.get(username=username)
		except ObjectDoesNotExist:
			raise serializers.ValidationError({"username": "A user with this username does not exist."})

		authenticated_user = authenticate(username=username, password=password)
		if not authenticated_user:
			raise serializers.ValidationError({"password": "Invalid password."})

		self.instance = authenticated_user
		return attrs
