from core.celery import app
from core.task import send_email_task


@app.task(
	queue='sms',
)
def send_otp_task(phone_number: str, email: str, code: str) -> bool:
	"""
	Celery task to send a single SMS.
	"""

	if email:
		from apps.users.utils import send_otp_to_email
		return send_otp_to_email(email, code)
	else:
		from apps.users.utils import send_otp_to_phone
		return send_otp_to_phone(phone_number, code)
