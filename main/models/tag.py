from django.db import models

from . import Task


class Tag(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
