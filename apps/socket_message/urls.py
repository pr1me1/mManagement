from django.urls import path

from apps.socket_message.api_endpoints.list.views import TaskMessageListRetrieve, ProjectMessageListRetrieve

app_name = "apps.socket_message"


urlpatterns = [
	# path('task/<uuid:uuid>/messages', TaskMessageListRetrieve.as_view(), name='task_messages'),
	# path("project/<uuid:uuid>/messages", ProjectMessageListRetrieve.as_view())
]
