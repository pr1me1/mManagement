from django.contrib import admin

from apps.projects.models import Project, Tasks, AuditLog

# Register your models here.

admin.site.register(Project)
admin.site.register(Tasks)
admin.site.register(AuditLog)
