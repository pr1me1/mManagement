from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .swagger import swagger_urlpatterns
from .task import test_email

urlpatterns = [
	path("admin/", admin.site.urls),
	path("api/v1/common/", include("apps.common.urls", namespace="common")),
	path("api/v1/", include("apps.users.urls", namespace="users")),
	path("api/v1/", include("apps.projects.urls", namespace="projects")),
	path("api/v1/", include("apps.socket_message.urls", namespace="socket_message")),
	path('api/v1/test-email/', test_email, name='test_email'),
]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
