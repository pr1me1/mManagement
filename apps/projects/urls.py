from django.urls import path

from apps.projects.api_endpoints.project.create.view import ProjectCreateAPIView
from apps.projects.api_endpoints.project.kick.views import KickFromProjectAPIView
from apps.projects.api_endpoints.project.manage.views import ProjectModelAPIView
from apps.projects.api_endpoints.project.promote.views import PromoteToProjectAPIView
from apps.projects.api_endpoints.task.change_status.views import StatusChangerAPIView
from apps.projects.api_endpoints.task.create.views import TaskCreateAPIView
from apps.projects.api_endpoints.task.manage.views import TaskDetailView
from apps.projects.api_endpoints.task.set_staff.views import SetStaffAPIView

app_name = "apps.projects"

urlpatterns = [
	path('project/create/', ProjectCreateAPIView.as_view(), name='create_project'),
	path('project/<uuid:uuid>/', ProjectModelAPIView.as_view(), name='project_manage'),
	path('project/promote/', PromoteToProjectAPIView.as_view(), name='staff_promote'),
	path('project/kick/', KickFromProjectAPIView.as_view(), name='kick_staff'),
	path('task/create/', TaskCreateAPIView.as_view(), name='create_task'),
	path('task/<uuid:uuid>', TaskDetailView.as_view(), name='detail_task'),
	path('task/<uuid:uuid>', TaskDetailView.as_view(), name='detail_task'),
	path('task/set-staff/', SetStaffAPIView.as_view(), name='set_staff_to_task'),
	path('task/change-status/', StatusChangerAPIView.as_view(), name='set_staff_to_task'),
]
