from django.contrib import admin

from main.models.status import Status

from .models.tag import Tag
from .models.task import Task
from .models.user import User


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(User, site=task_manager_admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "role"]
    pass


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ["title"]
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "priority", "author_task"]
    pass


@admin.register(Status, site=task_manager_admin_site)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["status"]
    pass
