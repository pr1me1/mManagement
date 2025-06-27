import redis
from celery import Celery
from django.conf import settings
from rest_framework.decorators import api_view

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")

redis_client = redis.StrictRedis(
	host=settings.REDIS_HOST,
	port=settings.REDIS_PORT,
	db=settings.REDIS_DB,
)


@api_view(["GET"])
def health_check_redis(request):
	try:
		redis_client.ping()
		return Response({"status": "success"}, status=status.HTTP_200_OK)
	except redis.ConnectionError:
		return Response(
			{"status": "error", "message": "Redis server is not working."},
			status=status.HTTP_400_BAD_REQUEST,
		)


from celery.exceptions import OperationalError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def health_check_celery(request):
	try:
		response = app.control.ping()
		if response:

			return Response(
				{"status": "success", "workers": response}, status=status.HTTP_200_OK
			)
		else:

			return Response(
				{"status": "error", "message": "No Celery workers responded."},
				status=status.HTTP_400_BAD_REQUEST,
			)
	except OperationalError as e:

		return Response(
			{"status": "error", "message": f"Celery OperationalError occurred: {str(e)}"},
			status=status.HTTP_500_INTERNAL_SERVER_ERROR,
		)
