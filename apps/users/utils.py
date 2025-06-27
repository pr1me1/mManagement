from django.conf import settings

from core.task import send_email_task


def send_otp_to_email(email: str, code: str):
	send_email_task.delay(
		subject='Verification Code',
		message=f'Your verification code is: {code}',
		from_email=settings.DEFAULT_FROM_EMAIL,
		recipient_list=[email],
	)


def send_notification_to_email(project_name, email, message: str):
	send_email_task.delay(
		subject=f'Urgent from {project_name}',
		message=message,
		from_email=settings.DEFAULT_FROM_EMAIL,
		recipient_list=email,
	)
