from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
	first_name = None
	last_name = None

	full_name = models.CharField(max_length=250, null=True, blank=True)
	avatar = models.ImageField(upload_to='users/avatars', blank=True, null=True, default=None)
	phone_number = PhoneNumberField(null=True, blank=True)
	email = models.EmailField(null=True, blank=True, default=None)
	last_login = models.DateTimeField(null=True, default=None, blank=True)
	password = models.CharField(max_length=128, blank=True)

	EMAIL_FIELD = "email"
	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ["email"]

	@property
	def token(self):
		refresh = RefreshToken.for_user(self)
		access = refresh.access_token
		return {
			"refresh": str(refresh),
			"access": str(access)
		}

	def clean(self):
		super().clean()

		if self.email:
			if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
				raise ValidationError({"email": "A user with this email already exists."})

		if self.phone_number:
			if User.objects.filter(phone_number=self.phone_number).exclude(pk=self.pk).exists():
				raise ValidationError({"phone_number": "A user with this phone number already exists."})

	def save(self, *args, **kwargs):
		self.full_clean()  # Run model validation, including clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.username}"
