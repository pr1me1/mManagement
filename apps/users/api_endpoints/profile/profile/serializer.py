from rest_framework import serializers

from apps.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'full_name', 'username', 'phone_number', 'email', 'date_joined', 'avatar',)
		read_only_fields = ('username', 'phone_number', 'email', 'date_joined')
