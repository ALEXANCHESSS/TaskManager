from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import DeleteAdminOnly

from .filters import TaskFilter, UserFilter
from .models.tag import Tag
from .models.task import Task
from .models.user import User
from .models.status import Status
from .serializers import StatusSerializer, TagSerializer, TaskSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated, DeleteAdminOnly]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("author_task", "performer_task").all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter
    permission_classes = [IsAuthenticated, DeleteAdminOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.prefetch_related("tasks").all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, DeleteAdminOnly]


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated, DeleteAdminOnly]
