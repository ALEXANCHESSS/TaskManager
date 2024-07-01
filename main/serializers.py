from rest_framework import serializers

from main.models.status import Status

from .models.tag import Tag
from .models.task import Task
from .models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "date_joined",
        )


class TaskSerializer(serializers.ModelSerializer):
    author_task = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "date_create",
            "date_update",
            "date_done_before",
            "status",
            "priority",
            "author_task",
            "performer_task",
            "tags",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "title",
        )


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = (
            "id",
            "status",
        )
