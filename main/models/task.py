from django.db import models

from main.models.status import Status

from . import User


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"
        CRITICAL = "critical"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    date_done_before = models.DateTimeField(null=True)
    priority = models.CharField(
        max_length=255, choices=Priority.choices, default=Priority.MEDIUM
    )
    status = models.ForeignKey(
        Status, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    author_task = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="author_tasks"
    )
    performer_task = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="performer_tasks", null=True
    )
    tags = models.ManyToManyField("Tag", related_name="tasks")

    def __str__(self):
        return self.title
