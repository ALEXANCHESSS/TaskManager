from django.shortcuts import render

from rest_framework import viewsets

from .filters import TaskFilter, UserFilter
from models.tag import Tag
from models.task import Task
from models.user import User
from serializers import TaskSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("author_task", "performer_task").all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.prefetch_related("task").all()
    serializer_class = TaskSerializer
