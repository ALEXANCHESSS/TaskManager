from django.db import models

from . import User


class Task(models.Model):
    class Status(models.TextChoices):
        NEW = "new_task"
        DEVELOPMENT = "in_development"
        QA = "in_qa"
        CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    class Priority(models.TextChoices):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        CRITICAL = "critical"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    date_done_before = models.DateTimeField()
    status = models.CharField(
        max_length=255, choices=Status.choices, default=Status.NEW
    )
    priority = models.CharField(
        max_length=255, choices=Priority.choices, default=Priority.MEDIUM
    )
    author_task = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="authored_tasks"
    )
    performer_task = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="performer_tasks", null=True
    )

    def __str__(self):
        return self.title
