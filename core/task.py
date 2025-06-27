from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(subject, message, from_email, recipient_list):
	send_mail(
		subject=subject,
		message=message,
		from_email=from_email,
		recipient_list=recipient_list,
		fail_silently=False,
	)


from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def test_email(request):
	subject = "Test Email from Celery"
	message = "This is a test email sent via Celery."
	from_email = "primel040304@gmail.com"
	recipient_list = ["jumayevjavohir585@gmail.com", "noktamov4@gmail.com"]
	send_email_task.delay(subject, message, from_email, recipient_list)
	return Response({"status": "email task queued"})
